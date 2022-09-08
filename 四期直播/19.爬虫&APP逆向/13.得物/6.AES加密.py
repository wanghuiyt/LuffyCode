import base64
from hashlib import md5
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad


def aes_encrypt(data_string):
    key = "d245a0ba8d678a61"
    aes = AES.new(
        key=key.encode("utf-8"),
        mode=AES.MODE_ECB
    )
    raw = pad(data_string.encode("utf-8"), 16)
    res = aes.encrypt(raw)
    return base64.encodebytes(res)


def md5_encrypt(data_string):
    obj = md5()
    obj.update(data_string.encode("utf-8"))
    return obj.hexdigest()


data_string = "anchorReplyId0contentId86602895contentType0lastIdlimit20loginToken669caca5|1194166641|b7ff632bf4de36faplatformandroidsourcetimestamp1662553595921uuidb94151b948e026e9v4.84.0"
res = aes_encrypt(data_string)
result = res.replace(b'\n', b'')
result = result.decode("utf-8")
result = md5_encrypt(result)
print(result)

# Zcv/ythIy5MNpkdAJoj8VDF0wQ0mL9MrdM2gdmUnMGFQ+HVCcyDJQ3Yx5rRfCjIDqFS0B5DeaHQW44s59OTTZt1Lom3hMvRMfnGV+fsefptjDevk1jNZakucwbKoKk+ql6FgNSErnCEOWENhWRvbuFFSIRmZzxU0dJwGHj4H070e+0bDXOnjyxrlSg1laJsz1VZx+YfjBaxTY7tsOaSd8SNpUP4LOIexI1KZ4gFbtuA=
# Zcv/ythIy5MNpkdAJoj8VDF0wQ0mL9MrdM2gdmUnMGFQ+HVCcyDJQ3Yx5rRfCjIDqFS0B5DeaHQW44s59OTTZt1Lom3hMvRMfnGV+fsefptjDevk1jNZakucwbKoKk+ql6FgNSErnCEOWENhWRvbuFFSIRmZzxU0dJwGHj4H070e+0bDXOnjyxrlSg1laJsz1VZx+YfjBaxTY7tsOaSd8SNpUP4LOIexI1KZ4gFbtuA=
