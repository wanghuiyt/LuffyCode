import base64
from Crypto.Cipher import DES3
from Crypto.Util.Padding import pad

# BS = 8
# pad = lambda s: s+(BS-len(s)%BS)*chr(BS-len(s)%BS)

# 3DES的MODE_CBC模式下只有前24位有意义
key = b'appapiche168comappapiche168comap'[0:24]
iv = b'appapich'

# plaintext = pad("5e505994-2b71-3a99-b5a9-6dd8c8286e06|3405276992893|322159").encode("utf-8")

plaintext = pad("5e505994-2b71-3a99-b5a9-6dd8c8286e06|3405276992893|322159".encode("utf-8"), 8)

# 使用MODE_CBC创建cipher
cipher = DES3.new(key=key, mode=DES3.MODE_CBC, IV=iv)
result = cipher.encrypt(plaintext)
res = base64.b64encode(result).decode("utf-8")
print(res)

# b1sdhA4UHOZ/vYuiOTszaNXb3cO7knDzTrzTgfwCMPQ3cM65ithqOhK2GeDA9WcIdYSgcROZrjnXqLF3L/ICwQ==
# b1sdhA4UHOZ/vYuiOTszaNXb3cO7knDzTrzTgfwCMPR44H5QqjSaloiRvUIi1Gtn8StU7cWWYSH0/VGXqC5G+A==
# b1sdhA4UHOZ/vYuiOTszaNXb3cO7knDzTrzTgfwCMPR44H5QqjSaloiRvUIi 1Gtn8StU7cWWYSH0/VGXqC5G+A==