# 抓取猫眼电眼TOP100
1. `requests`模块的使用
2. `json`模块的使用
3. 正则表达式的使用
4. 多线程的使用
5. 文件的保存

----

1. `requests`模块请求时添加一个`headers`
2. `json.dumps(content)`将字典转成字符串,需要注意的是汉字会被进行编码.如果不需要编码可以这么使用`json.dumps(content,ensure_ascii=False)`
3. `re.compile(r'',re.S)` 其中第二个参数`re.S`表示匹配任意的字符,如果不加`re.S`对于正则中的`.`是无法匹配换行符的
4. <del>就那么用吧😄😄</del>
5. 注意文件的写入模式以及编码格式