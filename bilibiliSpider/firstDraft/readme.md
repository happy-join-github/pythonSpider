# 爬取过程

1. 确定网址。打开bilibili网页随便点击一个视频

2. 按f12，点击面板的network选项，网页开始加载发送请求

3. 点击视频让**视频暂停**不影响我们对**网络请求**的定位

   1. 这一步我们需要明确我找请求的目的。
      1. 目的是：需要找出视频的地址。
      2. 对视频地址发送请求，获取视频数据。

   - 定位步骤
     - 复制视频的标题
     - 按ctrl+f，打开搜索面板，把复制的标题放在搜索框内。按enter。(快速检索是那个**请求**，缩小请求的查找范围)
     - 依次点击结果，查看响应，若无响应查看下一个请求，有响应，按ctrl+f搜索data查看数据位置(快速检索**数据**位置)

4. 分析数据

   视频数据有两种情况

   1. 音频和视频分离
   2. 视频分片段(视频流)

   - 搜索data这个关键字显示有331条，我们点击向下的箭头依次看是否为视频地址,(视频地址一般在js代码中)

   - 当搜索到第26个data匹配结果的时候，看到了字体为红色的数据且在js部分。

   - 再往下看到了在dash下video下面的url，是四个url不知道分别代表什么意思。复制前两个在浏览器中打开，发现下载了两个以**.m4s为**后缀的文件。开始编写代码转换为MP4看是哪种情况？

     ```python
     # 把下载的两个.m4s文件移动到testTools文件夹内
     # python代码如下
     import os
     import re
     
     reg = re.compile('.*?m4s', re.S)
     file = [re.match(reg, item).group() for item in os.listdir('./') if re.match(reg, item)]
     print(file)
     
     for i in range(len(file)):
         with open(file[i], 'rb') as oldfile:
             newPath = file[i][:-3] + 'mp4'
             with open(newPath, 'wb') as newfile:
                 newfile.write(oldfile.read())
         print(f'已完成{i + 1}个')
     print('全部完成，请查看')
     ```
     
- 编写完成代码，运行代码，打开看看mp4内容发现两个视频是一样的且都没有声音，确定了bilibili的属于第一种，并不是一成不变，也有可能会变成视频流的方式。
  
- 开始爬取视频并合并
  
- 为了保证是发送请求的是同一个浏览器的两个请求，而不是两个浏览器分别发送的请求，我们要保证session一样，发现给出的数据也有session。
  
5. 写代码

6. 展示结果

## 爬取遇到的问题

1. 怎么快速定位发送请求的方法

   解决办法：上文已给出

2. 怎么快速定位url地址

   解决办法：上文已给出

3. 怎么确定视频属于那种类型

   1. 采取视频流的方式
   2. 采取视频音频分离的方法

   解决办法：上文已给出

4. 怎么合并视频和音频。

   解决办法：使用第三方库moviepy
   
   > 下载  pip install moviepy
   >
   > 步骤
   >
   > 1. 引用库包     from moviepy.editor import VideoFileClip, AudioFileClip
   > 2. 加载音频文件    audio = AudioFileClip(音频地址)
   > 3. 加载视频文件  video = VideoFileClip(视频地址)
   > 4. 合并     result = video.set_audio(audio)
   > 5. 输出    result.write_videofile(合并后文件保存地址)
## 注意

此代码需要以来环境

> os库
>
> requests库
>
> re库
>
> time库
>
> json库
>
> moviepy库
>
> 需要pip install的库包有：
>
> requests、moviepy库
>
> moviepy库包依赖ffmpeg安装包。我已经放在tools文件夹下面了。直接放到电脑的任何一个位置，有个要求就是**路径不要包含中文**。
>
> 配置环境变量。此电脑右键-->属性-->高级系统设置-->环境变量--》在系统变量找到path-->新建-->输入文件夹的路径/bin就可以了。

> 注意每次下载完成视频，请将result文件**合成的完整视频剪切的其他位置**。防止代码执行的逻辑的错误。
>
> 注意本脚本不能下载vip视频。如需下载vip视频，请加qq2431242530了解。

## 使用方法

> 根据b站的放爬虫机制会做出实时的更新，具体更新说明请看update.md文档
>
> 需要改动代码位置
>
> - headers里referer，需要在里面填写浏览器地址栏的全部地址。
> - params里面的两个值。这两个值在地址栏有，照着填入就行。

## 完善项目

1. 给这个项目设计一款qt界面，方便爬取。
    ![初步设计图](https://github.com/happy-join-github/pythonSpider/blob/main/bilibiliSpider/firstDraft/images/qt.png)

2. 完善开发，添加更多的功能。

   ​																																2024-03-05 14：48
