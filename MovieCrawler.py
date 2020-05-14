import os
import ffmpy3
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
from multiprocessing.dummy import Pool as ThreadPool

def getHref(search_name):
    try:
        search_url = 'http://www.jisudhw.com'+'/index.php'
        search_params={
            'm':'vod-search'
        }
        search_headers={
            'Host': 'www.jisudhw.com',
            'Origin': 'http: // www.jisudhw.com',
            'Referer': 'http: // www.jisudhw.com / index.php?m = vod - search',
            'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'
            }
        search_data={
            'wd': search_name,
            'submit':'search'
        }
        r=requests.post(url=search_url,params=search_params,headers=search_headers,data=search_data)
        r.raise_for_status()
        print(r.status_code)
        r.encoding=r.apparent_encoding
        bs=BeautifulSoup(r.text,'lxml')
        target_tag=bs.find('span',class_='xing_vb4')    # 这种搜索方式可能不太稳定
        target_url=search_url+target_tag.a.get('href')    #注意使用get来获取键值
        return target_url
    except:
        return ''

def getEpisodeHref(episodes_url):
    try:
        r = requests.get(episodes_url)
        r.raise_for_status()
        r.encoding = 'utf-8'
        soup = BeautifulSoup(r.text,'lxml')
        # mids = soup.find('div', id="1")            #id不是Python的关键词
        infor={}
        num=1
        for each_url in soup.find_all('input'):
            if 'm3u8' in each_url.get('value'):
                url=each_url.get('value')           #'单'标签也可以用get
                if url not in infor.keys():         #keys
                    infor[num]=url
                    num+=1
        return infor
    except:
        return {}
def DownloadVideo(url):
    name = os.path.join(save_dir, '第{:03}集.mp4' .format(num))
    ffmpy3.FFmpeg(inputs={url:None},outputs={name:None}).run()


if __name__=="__main__":
    search_name='越狱第一季'
    search_url='http://www.jisudhw.com'
    episodes_url=getHref(search_name)
    print(episodes_url)
    all_infor=getEpisodeHref(episodes_url)
    root='/Users/yun/Desktop/Pyhello/'
    save_dir=root+search_name
    num=1
    try:
        if not os.path.exists(save_dir):
            os.mkdir(save_dir)
        print("File creation succeeded")
    except:
        print('File creation failed')
    for key,value in all_infor.items():         #字典遍历
        DownloadVideo(value)
        num+=1





