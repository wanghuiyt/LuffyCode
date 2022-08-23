function a(a) {
    a = 16
    var d, e, b = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", c = "";
    for (d = 0; d < 16; d++) {
        e = Math.random() * b.length;  // e是b的长度的随机值
        e = Math.floor(e);  // 取整
        c += b.charAt(e);  // 拿到b中对应位置的字符
    }
    return c  // 从b中随机抽出16个字符，拼接成字符串
}

function b(data, b) {
    var c = CryptoJS.enc.Utf8.parse(b)  // 密钥key
        , d = CryptoJS.enc.Utf8.parse("0102030405060708")  // IV
        , e = CryptoJS.enc.Utf8.parse(data)  // 数据
        , f = CryptoJS.AES.encrypt(e, c, {
        iv: d,
        mode: CryptoJS.mode.CBC
    });
    return f.toString()
}

function c(a, b, c) {
    var d, e;
    setMaxDigits(131);
    d = new RSAKeyPair(b, "", c);
    e = encryptedString(d, a);
    return e;
}


function d(data, e, f, g) {
    var h = {};
    // var i = a(16);  // 16位的随机字符串
    var i = "Y5oLbwFDuYI9MCws";
    h.encText = b(data, g);  // 对data进行加密，密钥是g，IV是0102030405060708
    h.encText = b(h.encText, i);  // 对h.encText进行加密，密钥是i,IV是0102030405060708
    // 调用c，把i,e,f传递进去，猜测是对i进行加密
    // h.encSecKey = c(i, e, f);  // rsa加密。被加密的是i,密钥是e和f
    h.encSecKey = 'd6cf71ac77cd9f94cc877657b5cee28488e4efc26ca5a22c2b8cc01b6ec9ad0fe8dc65e510ad40386551e2db64660de8c21ccd0bba08304f24bf5fd92336c2fe6492f0e7f043c23a9050c4caedef490ecf48491557bfe438947d939531ee91218b04ea1593424da35daccbf39667a62f65766ff9272f81d89d7bf684cf083643'
    // 两种方案
    // 1.固定i的数据，得到encSecKey可以固定
    // 2.

    return h;
}
