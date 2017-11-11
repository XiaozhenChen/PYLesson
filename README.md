# PYLesson

## [糗事百科]()

	1.

## [百度贴吧]()


## 正则表达式
- re.search(pattern,strRsc)

- re.sub(pattern,replace,strRsc)

-------
## 正则表达式规则
- `.`		匹配任意字符
-  `*`		匹配0个或多个的表达式
-  `?`		匹配0个或1个由前面的正则表达式定义的片段，非贪婪方式
-  `\d`	等价于`[0-9]` 匹配任意数字

-----
## `python`中`str`换行方式

- 三个单引号 

	```
		print('''我是一个程序员
       我刚开始学习python''')
	```
- 三个双引号

	```
	print("""我是一个程序员
       我刚开始学习python""")
	```
		
- `\`结尾

	```
	print("我是一个程序员，\
       我刚开始学python")
	```
	
----

## `urllib`模块的使用
	
### 1. 基本方法
urllib.request.urlopen(url, data=None, [timeout, ]*, cafile=None, capath=None, cadefault=False, context=None)

- url:  需要打开的网址
- data: Post提交的数据
- timeout: 设置网站的访问超时时间

直接用`urllib.request`模块的`urlopen()`获取页面,`page`的数据数据格式为`bytes`类型,需要`decode()`解码,转换成`str`类型.

```
from urllib import request
response = request.urlopen(r'http://python.org/') # <http.client.HTTPResponse object at 0x00000000048BC908> HTTPResponse类型
page = response.read()
page = page.decode('utf-8')
```

### urlopen返回对象提供的方法

- read(),readline(),readlines(),fileno(),close():对HTTPResponse类型数据进行操作
- info():返回HTTPMessage对象,表示远程服务器返回的头信息
- getcode():返回Http状态码.
- geturl():返回请求的url

### 2. Request的使用
urllib.request.Request(url, data=None, headers={}, method=None)

使用request()来包装请求,在通过urlopen()获取页面

```
url = r'http://www.lagou.com/zhaopin/Python/?labelWords=label'
headers = {
    'User-Agent': r'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  r'Chrome/45.0.2454.85 Safari/537.36 115Browser/6.0.3',
    'Referer': r'http://www.lagou.com/zhaopin/Python/?labelWords=label',
    'Connection': 'keep-alive'
}
req = request.Request(url, headers=headers)
page = request.urlopen(req).read()
page = page.decode('utf-8')
```

用来包装头部的数据:

- User-Agent:这个头部可以携带如下几条信息: 浏览器名和版本号、操作系统名和版本号、默认语言
- Referer:可以用来防止盗链,有一些网站图片显示来源http://**.com,就是检查Referer来鉴定的
- Connection:表示连接状态,记录Session的状态

### Post数据
urllib.request.urlopen(url, data=None, [timeout, ]*, cafile=None, capath=None, cadefault=False, context=None)

urlopen()的data参数默认为None,当data参数不为空时,urlopen()提交方式为Post.

```
from urllib import request, parse
url = r'http://www.lagou.com/jobs/positionAjax.json?'
headers = {
    'User-Agent': r'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  r'Chrome/45.0.2454.85 Safari/537.36 115Browser/6.0.3',
    'Referer': r'http://www.lagou.com/zhaopin/Python/?labelWords=label',
    'Connection': 'keep-alive'
}
data = {
    'first': 'true',
    'pn': 1,
    'kd': 'Python'
}
data = parse.urlencode(data).encode('utf-8')
req = request.Request(url, headers=headers, data=data)
page = request.urlopen(req).read()
page = page.decode('utf-8')
```

urllib.parse.urlencode(query, doseq=False, safe='', encoding=None, errors=None)

urlencode()主要作用就是将url附上要提交的数据.

```
data = {
    'first': 'true',
    'pn': 1,
    'kd': 'Python'
}
data = parse.urlencode(data).encode('utf-8')
```
经过`urlencode()`转换后的`data`数据为`?first=true?pn=1?kd=python`,最后提交的url为`http://www.lagou.com/jobs/positionAjax.json?first=true?pn=1?kd=Python`

Post的数据必须是`bytes`,不能是`str`因此需要进行`encode()`编码.这里依然使用了`Request`进行包装.

当然也可以把`data`数据封装在`urlopen()`参数中.

### 异常处理

```
def get_page(url):
    headers = {
        'User-Agent': r'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                    r'Chrome/45.0.2454.85 Safari/537.36 115Browser/6.0.3',
        'Referer': r'http://www.lagou.com/zhaopin/Python/?labelWords=label',
        'Connection': 'keep-alive'
    }
    data = {
        'first': 'true',
        'pn': 1,
        'kd': 'Python'
    }
    data = parse.urlencode(data).encode('utf-8')
    req = request.Request(url, headers=headers)
    try:
        page = request.urlopen(req, data=data).read()
        page = page.decode('utf-8')
    except error.HTTPError as e:
        print(e.code())
        print(e.read().decode('utf-8'))
    return page
```

### 使用代理

urllib.request.ProxyHandler(proxies=None)
当需要抓取的网站设置了访问权限,这时就需要用到代理来抓取服务.

```
data = {
        'first': 'true',
        'pn': 1,
        'kd': 'Python'
    }
proxy = request.ProxyHandler({'http': '5.22.195.215:80'})  # 设置proxy
opener = request.build_opener(proxy)  # 挂载opener
request.install_opener(opener)  # 安装opener
data = parse.urlencode(data).encode('utf-8')
page = opener.open(url, data).read()
page = page.decode('utf-8')
return page
```
