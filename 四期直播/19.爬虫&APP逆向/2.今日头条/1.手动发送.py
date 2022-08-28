import requests

resp = requests.get("https://www.toutiao.com/api/pc/list/feed?channel_id=3189398972&max_behot_time=1661646448&category=pc_profile_channel&client_extra_params=%7B%22short_video_item%22:%22filter%22%7D&aid=24&app_name=toutiao_web&_signature=_02B4Z6wo00901vC414gAAIDCcLotyumUr8LwnNMAAN8yLf514x0g5obKEwxTZozFXMZq9gt2k8KV9Q0dn481.-Ofct8q7JLfPltjdA7lCaOkEIZ5wedKeiCWkM7g60iXodCGpSE.Tr3aWPqk91")
print(resp.text)

