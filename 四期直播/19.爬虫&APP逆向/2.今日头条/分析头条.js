function I(e, t) {
    var n, r, a = "".concat(location.protocol, "//").concat(location.host);
    (function(e) {
        return !A.some((function(t) {
            return e.indexOf(t) > -1
        }
        ))
    }
    )(e) && (a += "/toutiao");
    // var o = {
    //     url: a + e
    // };
    var o = {
        url: "https://www.toutiao.com/api/pc/list/feed?channel_id=3189398972&max_behot_time=1661647455&category=pc_profile_channel&client_extra_params=%7B%22short_video_item%22:%22filter%22%7D&aid=24&app_name=toutiao_web"
    }
    return t.data && (o.body = t.data),
    (null === (n = window.byted_acrawler) || void 0 === n || null === (r = n.sign) || void 0 === r ? void 0 : r.call(n, o)) || ""
}