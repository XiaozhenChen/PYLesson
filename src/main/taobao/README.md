# 淘宝MM照片
1. 获取淘宝MM 姓名 头像 年龄
2. 抓取每一个MM的资料简介以及写真
3. 把每一个MM的写真图片按照文件夹保存到本地
4. 熟悉文件保存的过程

---
## os 模块
1. os.path.exists(path)  判断路径是否存在
2. os.path.makedirs(path) 创建文件目录

## urllib 模块
1.保存图片
	
```
response=urlopen(imgUrl)
data=response.read()
f=open(imgName,'wb')
f.write(data)
f.close()
```

## 正则表达式

1.re.findall()

