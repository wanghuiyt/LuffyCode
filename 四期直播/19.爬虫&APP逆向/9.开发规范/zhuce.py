import importlib

Card_dict = {
    "card1": "card.card1",
    "card2": "card.card2",
}


def run(card):
    card_path = Card_dict.get(card)
    obj = importlib.import_module(card_path)

    # 1.发送请求获取手机号
    # phone = obj.get_number()
    phone = getattr(obj, "get_number")()
    # 2.注册平台

    # 3.接收验证码
    code = getattr(obj, "get_code")(phone)
    # 4.写入文件
    print(phone, code)
    pass


if __name__ == '__main__':
    run("card1")
