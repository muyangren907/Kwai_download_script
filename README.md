快手批量下载脚本
===========

![](https://raw.githubusercontent.com/muyangren907/Kwai_download_script/master/screenshots/1.png)


## 使用

- ①将json文件获取到该项目同一文件夹下
- ②运行run.bat
- ③当然你也可以自己在cmd下运行
```
.\venv\Scripts\python.exe kuaishou.py
```

## 说明
-	若该主播正在直播，则获取到的第一个json文件第一项为直播信息（即feeds数组中的第一项），需要删去，否则程序运行会报错
- 获取到的json项目分类有：视频(包含视频和图片电影)，图集(即长图)，图片
- 下载的文件命名规则下面有说明，对于过长的标题，只截取前30字，并清除不能出现在文件夹或文件名中的字符
- 程序编写平台为Windows 10，使用JetBrains PyCharm作为ide，python版本为3.6，文本文件均采用UTF-8编码
- 默认线程数为30，源代码中有详细注释，可根据实际情况进行更改

#### 下载的文件命名规则
- 首先会在该文件夹下生成以主播快手昵称为名的文件夹(假设为user_name)
-	视频保存为mp4文件，命名为"作品编号_标题.mp4"，保存在user_name中
- 图集会在user_name下生成一个文件夹，文件夹命名为"作品编号_标题"，文件夹下图片为webp格式，命名为"序号.webp"，序号从0开始编号
- 图片保存为jpg文件，命名为"作品编号_标题.jpg"，保存在user_name中
- user_name下还会生成一个user_name.txt的文件，记录了下载时间，每种类型文件的个数
