# `requests`设置代理请求


对于需要使用代理时，可以通过为任意请求方法提供`proxies`参数来配置单个请求：

```
import requests

proxies = {
  "http": "http://10.10.1.10:3128",
  "https": "http://10.10.1.10:1080",
}

requests.get("http://example.org", proxies=proxies)
```

[`requests`高级使用](http://docs.python-requests.org/zh_CN/latest/user/advanced.html)