import json
import os
import re
import time
import requests


cookies = {
    'buvid3': '640508AE-B0FE-77B6-B7C4-6D13E076BBA930446infoc',
    'b_nut': '1708940330',
    'CURRENT_FNVAL': '4048',
    'bsource': 'search_bing',
    '_uuid': '932BF10F2-419D-3FD5-F122-410418A24A64548200infoc',
    'rpdid': "|(u))ulY~)|J0J'u~|)mR|JRm",
    'bmg_af_switch': '1',
    'enable_web_push': 'DISABLE',
    'header_theme_version': 'CLOSE',
    'bmg_src_def_domain': 'i0.hdslb.com',
    'FEED_LIVE_VERSION': 'V8',
    'bp_video_offset_358283711': '743507552657997859',
    'DedeUserID': '332891302',
    'DedeUserID__ckMd5': 'e2f1947d9df9161a',
    'buvid4': '4A8DBD8F-EE9D-78B1-31D6-0D73FA456AC439266-023090914-CChLgk3XNLX0JHCHFtDUrw%3D%3D',
    'fingerprint': '9cacc3147c497058abd89562f664b29a',
    'buvid_fp_plain': 'undefined',
    'CURRENT_QUALITY': '80',
    'SESSDATA': '18d110f5%2C1725776347%2Cac24e%2A31CjAPpSbRyD0l2FjXgi319WlFfqIDxfTYGREzLE7s4gtmDR_wpKocIdu4MrFLv683AjISVk1ud1QxZXZDWmxjLVB4SGFwQlprNzI1TjZ5cktlZk5jZGcxaEppdGdVODlhajBOMjFYWTFtTzJCcVhwcXV6WHktV3l5NXBtM0k3enZDd2p6MzVseG1RIIEC',
    'bili_jct': '41c4254ca07148c048677af09dc60d80',
    'sid': '741x3leo',
    'is-2022-channel': '1',
    'home_feed_column': '5',
    'browser_resolution': '1699-812',
    'buvid_fp': '86e40f35c50b1d288ca0c2b806681fe4',
    'bili_ticket': 'eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MTA1ODI0OTcsImlhdCI6MTcxMDMyMzIzNywicGx0IjotMX0.-3PyVo_JRnEwR2TxXLRlfWwxjqNXsPWWsQfiGwY-dCs',
    'bili_ticket_expires': '1710582437',
    'PVID': '2',
    'bp_video_offset_332891302': '908313590889447458',
    'b_lsid': '1071093710B_18E37E0B95B',
}


url = 'https://www.bilibili.com/video/BV1Ym411S78m/'
headers = {
    'authority': 'www.bilibili.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'cache-control': 'max-age=0',
    'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Microsoft Edge";v="116"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.69',
    'referer': 'https://www.bilibili.com/video/BV1Ym411S78m/?spm_id_from=333.1007.tianma.1-1-1.click&vd_source=97af887489618fcad92d535a7ba14669'
}

params = {
    'spm_id_from': '333.337.search-card.all.click',
    'vd_source': '97af887489618fcad92d535a7ba14669',
}


def request(url, headers, cookies, params):
    # 防止请求过快，导致ip被封禁
    time.sleep(1)
    # 发送请求
    response = requests.get(url, params=params, cookies=cookies,
                            headers=headers)
    if response.status_code == 200:
        return response.status_code, response.text
    else:
        return response.status_code, "请求失败"


def solution_txt(txt: str):
    info = re.search('window.__playinfo__=(.*?)</script>', txt, re.S).group(1)
    if info == None:
        return '', ''
    else:
        title = re.search('<title data-vue-meta="true">(.*?)_哔哩哔哩_bilibili</title>', txt, re.S).group(1)
        json_data = json.loads(info)
        video_url = json_data['data']['dash']['video'][0]['baseUrl']
        audio_url = json_data['data']['dash']['audio'][0]['baseUrl']
    return title, video_url, audio_url


def downloads(url1, url2):
    txt1 = requests.get(url1, headers=headers, cookies=cookies).content
    txt2 = requests.get(url2, headers=headers, cookies=cookies).content
    # 创建结果目录
    os.mkdir('result') if not os.path.exists('./result') else print('存在result文件夹')
    with open('./result/video.m4s', 'wb', ) as f:
        f.write(txt1)
    with open('./result/audio.m4s', 'wb') as f:
        f.write(txt2)


def m4stomp4ORmp3():
    for i in os.listdir('result'):
        newfile_name = i[:6]
        if newfile_name == 'video.':
            newfile_name = newfile_name + 'mp4'
        else:
            newfile_name = newfile_name + 'mp3'
        with open(f"./result/{i}", 'rb') as f:
            with open(f"./result/{newfile_name}", 'wb') as file:
                file.write(f.read())
    print('格式转换完毕')


def hebing(title):
    from moviepy.editor import VideoFileClip, AudioFileClip
    common_path = 'result/'
    # 加载视频文件
    video = VideoFileClip("result/video.mp4")
    
    # 加载音频文件
    audio = AudioFileClip("result/audio.mp3")
    
    # 将音频添加到视频中
    final_video = video.set_audio(audio)
    
    # 输出结果
    final_video.write_videofile(common_path + f"{title}.mp4")
    
    # 删除多余文件
    for item in os.listdir('result'):
        if item[:5] in ['audio', 'video']:
            os.remove('result/' + item)
    print('合并完成')


def main():
    status_code, info = request(url, headers, cookies, params)
    if status_code == 200:
        print('请求成功')
        title, video, audio = solution_txt(info)
        print('地址提取完毕')
        if not video and not audio:
            print('没有匹配到数据')
            return
        else:
            print('正在下载，请耐心等待……')
            downloads(video, audio)
            print('下载完成')
            m4stomp4ORmp3()
            print('开始合并音视频')
            hebing(title)
    else:
        print(f'请求失败，状态码为{status_code}')


if __name__ == '__main__':
    main()
    print('下载完成')
