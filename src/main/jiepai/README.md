# 分析ajax抓取今日头条街拍美图

1. 分析ajax
2. requests请求返回text和content的区别
3. `yield`的使用
4. 保存数据到`mysql`
5. `md5`判断相同文件
6. 多线程

----
1. 浏览器`F12`模式下调试 ,<del>用多了就有经验了😄😄😄</del>
2. 对于`requests`请求的返回的`response`如果是`content`就是二进制内容,如果是`text`就是网页的正常结果
3. 
	
	> 带有`yield`的函数就不是一个普通的函数了,此时的函数是一个`generator`，是可以直接作用于`for`循环的.
	
	>简要理解：`yield`就是 `return` 返回一个值，并且记住这个返回的位置，下次迭代就从这个位置后(下一行)开始
	
	> 参考如下[迭代器](https://www.liaoxuefeng.com/wiki/0014316089557264a6b348958f449949df42a6d3a2e542c000/00143178254193589df9c612d2449618ea460e7a672a366000) , [yield 使用浅析](https://www.liaoxuefeng.com/article/001373892916170b88313a39f294309970ad53fc6851243000) , [简单理解yield](http://www.jianshu.com/p/d09778f4e055)

4. `pymysql`的使用
5. > - 一个字符的`md5`

		a=md5('a')
		result=a.hexdigest()
6. 