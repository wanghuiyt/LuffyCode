import json

data = "callback=jsonp1&guid=l7d1stvh_ql78atkhbfq&platform=4330701&vid=i000075mu8r&defn=auto&charge=0&defaultfmt=auto&otype=json&defnpayver=1&appVer=1.2.10&sphttps=1&sphls=1&spwm=4&dtype=3&defsrc=1&encryptVer=8.1&sdtfrom=4330701&cKey=--0122F46409D16419761E7CF64C400CF7C7C22BE9AA1EEDA5B516691325920A823DB2AFC68FE3D18F3F1F9517D4CE7C46AC7902D56BCC4BF41CAF62561A7EAD648E7516AB3B7645793F13EC8BC7E85728DB8EB808A667E6774AD4826543D30CC36A51DB29D3689630566A66422FB12382A67EA8B143D916EB0F1065F3A381F4F0F04DA0380025C9475E1FD4F563A5EDB380C7F124B384EFA827A982D1C7B647F172&panoramic=false&flowid=l7d1tzgd_g0khd335w2"

data_dict = {item.split("=")[0]: item.split("=")[1] for item in data.split("&")}
print(json.dumps(data_dict, indent=2))

