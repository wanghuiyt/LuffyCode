import json
import scrapy
from scrapy.http.response.html import HtmlResponse


class KsSpider(scrapy.Spider):
    name = 'ks'
    allowed_domains = ['wangxiao.cn']
    start_urls = ['http://ks.wangxiao.cn/']

    def parse(self, resp: HtmlResponse, **kwargs):
        # 解析页面结构
        # li_list = resp.xpath('//ul[@class="first-title"]/li')
        # for li in li_list:
        #     first_title = li.xpath('./p/span/text()').extract_first()
        #     a_list = li.xpath('./div/a')  # 所有二级类目
        #     for a in a_list:
        #         second_title = a.xpath('./text()').extract_first()
        #         second_href = a.xpath('./@href').extract_first()
        #         second_href = resp.urljoin(second_href).replace("TestPaper", "exampoint")
        #         print(first_title, second_title, second_href)
        #         # 访问二级类目中的考点练习
        #         yield scrapy.Request(
        #             url=second_href,
        #             callback=self.parse_second,
        #             meta={"first_title": first_title, "second_title": second_title}
        #         )
        yield scrapy.Request(
            url="http://ks.wangxiao.cn/exampoint/list?sign=jz1",
            callback=self.parse_second,
            meta={
                "first_title": "工程类",
                "second_title": "一级建造师"
            }
        )

    def parse_second(self, resp: HtmlResponse, **kwargs):
        a_list = resp.xpath('//div[@class="filter-item"]/a')
        for a in a_list:
            third_title = a.xpath('./text()').extract_first()
            third_href = a.xpath('./@href').extract_first()
            third_href = resp.urljoin(third_href)
            yield scrapy.Request(
                url=third_href,
                callback=self.parse_third,
                meta={
                    "first_title": resp.meta.get("first_title"),
                    "second_title": resp.meta.get("second_title"),
                    "third_title": third_title,
                }
            )
            break  # return 这里都可以

    def parse_third(self, resp: HtmlResponse, **kwargs):
        first_title = resp.meta.get("first_title")
        second_title = resp.meta.get("second_title")
        third_title = resp.meta.get("third_title")
        chapter_items = resp.xpath('//div[@class="panel-content"]/ul[@class="chapter-item"]')
        for chapter in chapter_items:
            # 拿到了url，如果拿到，就是文件夹，拿不到就是一个文件
            section_point_items = chapter.xpath('.//ul[@class="section-point-item"]')
            if section_point_items:
                # section-point-item是最里层，拿到外层的外层->chapter-item
                for point_item in section_point_items:
                    # ancestor: 从内层向外层查找元素，不包括自身
                    # ancestor-or-self: 包括自身
                    points = point_item.xpath('./ancestor::ul[@class="chapter-item" or @class="section-item"]')
                    r = [first_title, second_title, third_title]
                    for point in points:
                        p_name = "".join(point.xpath("./li[1]/text()").extract()).strip().replace(" ", "")  # 文字信息
                        r.append(p_name)
                    dir_path = "/".join(r)
                    # 文件名字
                    file_name = "".join(point_item.xpath("./li[1]/text()").extract()).strip().replace(" ", "")
                    # print(dir_path, file_name)
                    top = point_item.xpath('./li[2]/text()').extract_first().split("/")[1]
                    sign = point_item.xpath('./li[3]/span/@data_sign').extract_first()
                    subSign = point_item.xpath('./li[3]/span/@data_subsign').extract_first()
                    data ={
                        "examPointType": "",
                        "practiceType": "2",
                        "questionType": "",
                        "sign": sign,
                        "subsign": subSign,
                        "top": top,
                    }
                    # 发送请求到listQuestions，获取到题目
                    url = "http://ks.wangxiao.cn/practice/listQuestions"
                    yield scrapy.Request(
                        url=url,
                        method="POST",
                        body=json.dumps(data),
                        headers={
                            "Content-Type": "application/json; charset=UTF-8"
                        },
                        callback=self.parse_questions,
                        meta={
                            "dir_path": dir_path,
                            "file_name": file_name
                        }
                    )
                    return  # 为了测试
            else:
                # 文件名字
                dir_path = "/".join([first_title, second_title, third_title])
                file_name = "".join(chapter.xpath("./li[1]/text()").extract()).strip().replace(" ", "")
                # print(dir_path, file_name)
                top = chapter.xpath('./li[2]/text()').extract_first().split("/")[1]
                sign = chapter.xpath('./li[3]/span/@data_sign').extract_first()
                subSign = chapter.xpath('./li[3]/span/@data_subsign').extract_first()
                data = {
                    "examPointType": "",
                    "practiceType": "2",
                    "questionType": "",
                    "sign": sign,
                    "subsign": subSign,
                    "top": top,
                }
                # 发送请求到listQuestions，获取到题目
                url = "http://ks.wangxiao.cn/practice/listQuestions"
                yield scrapy.Request(
                    url=url,
                    method="POST",
                    body=json.dumps(data),
                    headers={
                        "Content-Type": "application/json; charset=UTF-8"
                    },
                    callback=self.parse_questions,
                    meta={
                        "dir_path": dir_path,
                        "file_name": file_name
                    }
                )

    def parse_questions(self, resp: HtmlResponse, **kwargs):
        dir_path = resp.meta["dir_path"]
        file_name = resp.meta["file_name"]
        # json.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)
        # 本次请求拿到的东西不是json
        dic = resp.json()
        data_list = dic["Data"]
        for data in data_list:
            questions = data.get("questions")
            if questions:
                for question in questions:
                    question_info = self.process_question(question)
                    yield {
                        "dir_path": dir_path,
                        "file_name": file_name,
                        "question_info": question_info
                    }
            else:
                materials = data.get("materials")
                for mater in materials:
                    mater_content = mater["materials"]["content"]
                    questions = mater["questions"]
                    qs = []
                    for q in questions:
                        q_info = self.process_question(q)
                        qs.append(q_info)
                    question_info = mater_content + "\n\n" + "\n".join(qs)
                    yield {
                        "dir_path": dir_path,
                        "file_name": file_name,
                        "question_info": question_info
                    }

    def process_question(self, question):
        content = question["content"]
        options = question["options"]
        right_list = []
        opt_list = []
        for opt in options:
            opt_name = opt["name"]
            opt_content = opt["content"]
            opt_str = f"{opt_name}.{opt_content}"
            opt_list.append(opt_str)
            is_right = opt['isRight']
            if is_right == 1:
                if opt_name in "ABCDEFGH":
                    right_list.append(opt_name)
                else:
                    right_list.append(opt_content)
        analysis = question["textAnalysis"]
        if opt_list:
            question_info = content + "\n" + "\n".join(opt_list) + "\n\n" + "答案：" + ",".join(right_list) + "\n\n" + "解析：" + analysis
        else:
            question_info = content + "\n\n" + "解析：" + analysis
        return question_info

"""
requests
    get
        Query String Parameters -> url
        url上拼接?xx=xxx&xx=xxx
        params =》 也可也i把上述参数进行设置
    post
        Form Data
            把字段传递给data即可 requests.post(url, data=dict)
        Request Payload
            把字典处理成json传递给data
            同时需要给出请求头中的Content-Type: application/json
"""













