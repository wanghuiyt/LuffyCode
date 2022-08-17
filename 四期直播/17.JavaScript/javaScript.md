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



