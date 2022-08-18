## javascript 关于++
```javascript
var a = 10;
a ++;  // 表示自己增加1 => a = a + 1
console.log(a)  // 11
++ a;  // 也表示自己增加1 => a = a + 1
console.log(a);  // 12
/**
 * 注意：++不论变量在前面还是在后面，它自己一定是增加1的，a = a + 1
 * a ++ 这个表达式的值是a
 * ++ a 这个表达式的值是a + 1
 * = 永远最后运行
 */
var a = 1;
// var b = a++;  // 原来a的值赋值给b，a自增1
// console.log(b);  // 1
// console.log(a);  // 2
// var c = ++a;
// console.log(c);  // 2
// console.log(a);  // 2
a = a++;  // a++的结局是1，a在这个过程中会自增1
console.log(a);  // a = 1
a = ++a;  // ++a的结局是2
console.log(a);  // 2
```
## 循环
```javascript
var arr = [11, 22, 33, 44]
// 循环遍历数组中的东西
for(var i = 0; i<arr.length;i++){
    console.log(arr[i]);
}
// 出来的是索引
for(var i in arr){  // 出来的是索引
    console.log(i);
}
// 循环arr,拿到arr中的每一项，传递给function()让其运行
// 参数1：就是元素本身
// 参数2：元素的索引
// 参数3：数组本身
arr.forEach(function(a, b, c){
    console.log(a);
    console.log(b);
    console.log(c);
})
```
## 函数
> 函数的运行不是依赖于函数名，而是依赖于内存地址
## 定时器
```javascript
setTimeout(任务,时间)  // 过多长时间执行任务
let s = setInterval(任务,时间)  // 每隔多长时间自动运行任务
clearInterval(s)  // 停止一个定时器
```
## 时间
```javascript
let t = new Date();
// 前端格式化时间
let year = t.getFullYear();
let month = t.getMonth() + 1;  // 月份从0开始
let week = t.getDay();  // 拿到的是星期几
let day = t.getDate();  // 日期
let hour = t.getHours();
let minute = t.getMinutes();
let second = t.getSeconds();
let fmt_time = year + "-" + month + "-" + day + " " + hour + ":" + minute + ":" + second
```
## 时间戳
```javascript
let d = new Date();
console.log(d.getTime());  // 获取时间戳(毫秒)
```


