# 目的
> 为了还原正常的请求参数或者返回的内容的解密  
> 切记不要钻牛角尖  
> 看着别人的加密或解密逻辑，用我们的程序(python/java/c/nodejs/javascript)把这个过程还原出来
## Charles
破解网站：https://www.zzzmode.com/mytools/charles/  
先安装证书  
win+R 运行certlm.msc  
找到charles的证书，将其拖拽到受信任的证书颁发机构中
## 安装 pyexecjs
把pyexecjs的运行时环境更换为更加强大的nodejs  
nodejs -> chrome的V8引擎  
