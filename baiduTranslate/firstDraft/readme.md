# baiduTranslate【逆向】

1. 寻找翻译接口

   1. 按下f12调出开发人员工具

   2. 在输入框内随便打一些字符

   3. 开始抓包

   4. 点击network模块【点击全部右面的Fetch/XHR】过滤请求

      ![请求过滤结果](https://github.com/happy-join-github/pythonSpider/blob/main/baiduTranslate/firstDraft/images/%E8%AF%B7%E6%B1%82%E8%BF%87%E6%BB%A4.jpeg)

   5. 从上往下开始点击看响应内容，看有没有翻译后的结果。

   6. 当我在看倒数第二个请求的时候，请求响应了一个json数据。里面有翻译内容。

      ![请求json数据](https://github.com/happy-join-github/pythonSpider/blob/main/baiduTranslate/firstDraft/images/json%E6%95%B0%E6%8D%AE.jpeg)

   7. 我可以清晰的看到翻译数据。响应回来的不是狗而是一段unicode编码。

   8. 先请求打印结果看看。

      在请求上右键-->复制-->复制为cURL   

      打开网站[Convert curl commands to code (curlconverter.com)](https://curlconverter.com/)

      粘贴下面会显示转换为python代码的结果

      > 复制到pycham
      >
      > 在后面添加这行代码
      >
      > ```python
      > # 上面代码省略
      > print(response.txt)
      > ```
      >
      > ![响应数据](https://github.com/happy-join-github/pythonSpider/blob/main/baiduTranslate/firstDraft/images/%E5%93%8D%E5%BA%94%E6%95%B0%E6%8D%AE.jpeg)
      >
      > 结果响应的是' \ u72d7'搜索以下结果发现是unicode编码方式。

   9. 解决编码问题

      导入json库，将返回的json字符串转换为json格式提取文件

      ```python
      import json
      json_data = json.loads(response.text)
      # 打印看看
      print(json_data)
      ```

      ![解决编码问题](https://github.com/happy-join-github/pythonSpider/blob/main/baiduTranslate/firstDraft/images/%E8%BD%AC%E7%BC%96%E7%A0%81.jpeg)

   10. 提取数据

       ```python
       trans_result = json_data['trans_result']['data'][0]['dst']
       print(trans_result)   # 狗
       ```

2. 解决请求参数的问题

   1. 输入不同的字符看请求参数的变化。

      我输入了dog和cat后结果

      ![参数比较](https://github.com/happy-join-github/pythonSpider/blob/main/baiduTranslate/firstDraft/images/compare.jpeg)

      我发现只有两个参数不同,sign和ts，还发现ts是13为的数字，而且两次请求的ts值相差不多。根据经验猜测应该是时间戳。但是只是猜测，具体是什么还需要根据具体的js代码为准。

   2. 开始寻找sign的生成逻辑。怎么找呢？

   3. 打开查找开始搜索全部文件中包含关键词的文件。

      > 点击控制面板的❌**左面**的三个点。点击搜索在输入框中输入要搜索的关键字，一般我们搜索关键字赋值的地方，所以输入sign:回车

      ![关键字搜索](https://github.com/happy-join-github/pythonSpider/blob/main/baiduTranslate/firstDraft/images/%E5%85%B3%E9%94%AE%E5%AD%97%E6%90%9C%E7%B4%A0.jpeg)

      > 依次点击每个文件，在文件中搜索关键字的位置。上面的那个搜索是搜索那个文件包含关键字，接下来的搜索是定位关键字具体位置。我们可以在文件中按ctrl+f搜索sign:

   4. 第一个文件有7个匹配项。以及看这7个匹配的位置。打上断点，因为我们也不知道是不是这个地方。

      这七个位置只有六个符合有一个匹配的位置是   getAcsSign: function() 很显然不是。

      刷新页面重新进行请求，验证那个是生成sign的函数。

      一刷新页面结果前两个没有没有断住，所以不是生成的sign的函数。我们前两个断点移除就行。

      > 看断点返回的是什么，方法是用就像复制一样把b(e)选中，把鼠标放在上面就会出现的函数的返回结果。放上结果显示871501.634748回过去看sign发现我们请求的sign值和这个值一样。所以我们这个b函数就是我们要找的函数。找到生成函数就好办了。接下就简单了。
      
   5. 扣取生成sign的函数，我们需要重新刷新以下网页停顿到我们打断点的位置，之后我们直接把鼠标放到b函数上面就会出现函数的地址点击一下进入函数，把函数体全部扣下来。

      ![函数体](https://github.com/happy-join-github/pythonSpider/blob/main/baiduTranslate/firstDraft/images/%E8%A7%A3%E5%AF%86%E4%BD%8D%E7%BD%AE.png)

      ![函数体](https://github.com/happy-join-github/pythonSpider/blob/main/baiduTranslate/firstDraft/images/%E5%87%BD%E6%95%B0%E4%BD%93.png)

      直接在爬虫的动议目录下建一个js文件。里面放我们扣下来的函数体。点击运行。只有看函数体缺什么参数我们补什么参数。

      在代码的最后一行加上打印语句并调用函数，并把函数赋值给变量或给函数起了一个名字。

      为什么呢？

      > 学过js的我们一定知道函数的定义
      >
      > ```javascript
      > /*函数定义 */
      > funciton name(param){
      >     /*函数体*/
      > }
      > name = function(param){
      > 	/*函数体*/
      > }
      > ```
      >
      > 刚才我们扣下来的函数是一个匿名函数，就想python中的labda函数。需要赋值给变量才能使用。上面的两种函数定义是差不多一样的。都可以通过name()来调用。

      运行之后我们发现报错了，把了一个r is not defined的错误，看报错的是哪一行代码，再刷新网页进行请求，并把r的值补上。

      ![r的值](https://github.com/happy-join-github/pythonSpider/blob/main/baiduTranslate/firstDraft/images/r%E5%80%BC.png)

      直接定义一个全局变量r

      ```javascript
      /* 定义位置一定要在函数调用的前面，要不然会报错 r is not defined*/
      var r='320305.131321201'
      ```

      然后再次运行有报错了 n is not defined刷新网页在找n的位置

      ![n的位置](https://github.com/happy-join-github/pythonSpider/blob/main/baiduTranslate/firstDraft/images/n%E7%9A%84%E4%BD%8D%E7%BD%AE.png)

   点击跳转，复制粘贴到js代码中。再次运行。结果输出结果了表示参数我们已经找全了。

   我们进行调试，我们的代码看看是不是和请求的一样，测试用例

   分别在调用函数请求cat和dog的sign值。

   看函数输出的值和发送请求的值是否一样。

   ```javascript
   /*测试用例*/
   console.log(getsign('cat'))   /*661701.982004*/
   console.log(getsign('dog'))   /*871501.634748*/
   ```

   我们看我们请求过的cat和dog的sign值

   ![](https://github.com/happy-join-github/pythonSpider/blob/main/baiduTranslate/firstDraft/images/compare.jpeg)

   发现一模一样，我们还需要解决ts的问题。在我们找到b(e)的地方有好几个参数。我们看到ts: +new Date确定就是时间戳我们就不需要扣代码了，直接写在文件的最后。

   ```javascript
   /* 最后我们对js文件做最后的处理*/
   function getSignAndTs(query){
       sign=getsign(query)
       ts=+new Date
       return [sign,ts]
   }
   ```

3. 在python如何调用js代码 

   我们需要安装execjs库来帮助我们进行解析js文件

   ```
   pip install PyExecJS
   ```

   execjs库包的简单操作

   > 函数的return会被result变量直接接收。
   >
   > result = execjs.compile(需要编译的js文件).call(调用的函数名,函数参数)
   >
   > **重点**
   >
   > 我们需要把js文件先读取再去调用上面的代码
   >
   > query=input('请输入要查询的单词')
   >
   > with open('js path','r',encoding='utf-8') as f:
   >
   > ​	js_data=f.read()
   >
   > result = execjs.compile(js_data).call(getSignAndTs,query)

这样我们就把问题全解决了。

![allcode](https://github.com/happy-join-github/pythonSpider/blob/main/baiduTranslate/firstDraft/images/allcode.jpeg)

