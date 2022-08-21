(function(w){
    let key = "1234";
    let cul = function (d){
        return d+"a";
    }
    w["huachen"] = {
        md5: function(s){
            s = cul(s);
            return "计算过的" + s;
        }
    }

    // var jiami = function(data){
    //     console.log("aes加密"+ data);
    // };
    // w.jiami = jiami;
    // return jiami
})(window)