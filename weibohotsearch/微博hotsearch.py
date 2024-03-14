import requests

cookies = {
    'XSRF-TOKEN': 'koZ2wbL0G_xnbVBMamf0GTVZ',
    'SUB': '_2AkMSsl8wf8NxqwFRmfocz2LgZYx_zQ7EieKk7q7rJRMxHRl-yT9kqncLtRB6OTJx30Q2bHIGwOcLolP8pP5NAqsn1aNy',
    'SUBP': '0033WrSXqPxfM72-Ws9jqgMF55529P9D9WhCp0MOU82SgIym7YIMhwEB',
    'WBPSESS': 'V0zdZ7jH8_6F0CA8c_ussV9tptq0oz5c1E_36g-FJ1m9IU1zgLDyX9jP_ftSp3zl-_y0mCYzmNhJk4POS8PkhfL-bUIVmkGBuPs1czb-sHC0FQ5LpYa4vbAbLu80ikBFZYc7Ko0Ei5nIexMrAQGfEAdAi1pl4bqd2bmCoaOo2KA=',
}

headers = {
    'authority': 'weibo.com',
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'client-version': 'v2.44.75',
    # 'cookie': 'XSRF-TOKEN=koZ2wbL0G_xnbVBMamf0GTVZ; SUB=_2AkMSsl8wf8NxqwFRmfocz2LgZYx_zQ7EieKk7q7rJRMxHRl-yT9kqncLtRB6OTJx30Q2bHIGwOcLolP8pP5NAqsn1aNy; SUBP=0033WrSXqPxfM72-Ws9jqgMF55529P9D9WhCp0MOU82SgIym7YIMhwEB; WBPSESS=V0zdZ7jH8_6F0CA8c_ussV9tptq0oz5c1E_36g-FJ1m9IU1zgLDyX9jP_ftSp3zl-_y0mCYzmNhJk4POS8PkhfL-bUIVmkGBuPs1czb-sHC0FQ5LpYa4vbAbLu80ikBFZYc7Ko0Ei5nIexMrAQGfEAdAi1pl4bqd2bmCoaOo2KA=',
    'referer': 'https://weibo.com/newlogin?tabtype=search&gid=&openLoginLayer=0&url=',
    'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Microsoft Edge";v="116"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'server-version': 'v2024.03.06.1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.69',
    'x-requested-with': 'XMLHttpRequest',
    'x-xsrf-token': 'koZ2wbL0G_xnbVBMamf0GTVZ',
}

response = requests.get('https://weibo.com/ajax/side/hotSearch', cookies=cookies, headers=headers).json()
txt_lst = response['data']['realtime']
content_lst = []
for i in range(len(txt_lst)):
    content_lst.append(txt_lst[i]['note']+'\n')
print(content_lst)
with open('微博热搜.txt','w',encoding='utf-8') as f:
    f.writelines(content_lst)




from wordcloud import WordCloud
from matplotlib import pyplot as plt
import jieba

# 获取文本txt的路径（txt和代码在一个路径下面）
text = open('微博热搜.txt', encoding="utf-8").read()
ls = jieba.lcut(text)
text = " ".join(ls)
# 停用词
excludes = {
    '是','做','的','后','玩','了','三','来','你','喊','倍','已','无','被','开',
    '大','吧','为','拿','给','给','3','15','吞','喝','和','有','上','红色','一分','能','二',
}
# 生成词云
# mask=mask
wc = WordCloud(
    font_path='simhei.ttf',
    scale=2,
    max_font_size=90, #最大字号
    width=1800,height=400,
    background_color='white', #设置背景颜色
    stopwords = excludes
)
wc.generate(text) # 从文本生成wordcloud
# wc.generate\_from\_text(text) #用这种表达方式也可以
# 显示图像
plt.imshow(wc,interpolation='bilinear')
plt.axis('off')
plt.tight_layout()
wc.to_file('微博热搜.png') # 储存图像
#plt.savefig('标签云效果图.png',dpi=200) #用这个可以指定像素
plt.show()