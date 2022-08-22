var webDES = function() {
    var func = function(a, b, c) {
        if (0 === b)
            return a['substr'](c);
        var r;
        r = '' + a['substr'](0, b);
        r += a['substr'](b+c);
        return r;
    };
    this['shell'] = function(data) {
        // 拿到最后一个字符并转化成十进制数+9
        var a = parseInt(data[data['length']-1], 16)+ 9
        // 拿到data[a]位置的数据，转化成十进制
        var b = parseInt(data[a], 16);
        // 把数据进行处理，返回了新数据
        data = func(data, a, 1);
        // 从数据中从b位置开始截取，截取8个字符
        a = data['substr'](b, 8);
        // 再次对数据进行处理，得到新数据
        data = func(data, b, 8);
        // 把a处理成utf-8的字节
        b = _grsa_JS['enc']['Utf8']['parse'](a);
        // 把a处理成utf-8的字节
        a = _grsa_JS['enc']['Utf8']['parse'](a);
        // 执行到这里 a和b的值是一样的
        a = _grsa_JS['DES']['decrypt'](  // DES 解密
            {'ciphertext': _grsa_JS['enc']['Hex']['parse'](data)},  // 把数据进行了Hex16进制的处理->处理成字节
            b,  // 这里是密钥
            {
                'iv': a,  // 偏移量
                'mode': _grsa_JS['mode']['ECB'],  // 模式： MODE_ECB
                'padding': _grsa_JS['pad']['Pkcs7']  // pad：填充逻辑(Pkcs7)
            })['toString'](_grsa_JS['enc']['Utf8']);  // 字节转成字符串（utf-8）,到这里已经得到解密后的数据
        // 切割，保留开头到最后一个大括号位置的内容，返回
        return a['substring'](0, a['lastIndexOf']('}')+ 1);
    };
}

// 前端加密和解密逻辑
// xxx.AES|DES.encrypt({数据},密钥，{加密参数})
// xxx.AES|DES.decrypt({数据},密钥，{解密参数})
