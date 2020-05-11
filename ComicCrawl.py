import re
import os
import time
import requests
from tqdm import tqdm
from bs4 import BeautifulSoup
from contextlib import closing

def GetComicName_Href(target_url):
    try:
        r=requests.get(url=target_url)
        r.raise_for_status()
        r.encoding=r.apparent_encoding
        bs=BeautifulSoup(r.text,'lxml')
        list_con_li = bs.find('ul',class_='list_con_li autoHeight')   #注意用class_
        comic_list=list_con_li.find_all('a')
        chapters=[]
        for comic in comic_list:
            href=comic.get('href')
            name=comic.text
            chapters.insert(0,[name,href])
        return chapters
    except:
        return []

def Getpics(name,url,path):
    download_header = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
        'Referer': url
    }
    chapter_save_dir = os.path.join(path,name)  # os.path.join()
    if not os.path.exists(chapter_save_dir):
        os.mkdir(chapter_save_dir)
        r = requests.get(url)
        html = BeautifulSoup(r.text, 'lxml')
        script_info = html.script
        pics = re.findall('\d{13,14}', str(script_info))
        for pic in pics:
            if len(pic)==13:
                pic=pic+'0'
        pics=sorted(pics, key=lambda x:int(x))
        chapterpic_front = re.findall(r'\|(\d{4})\|', str(script_info))[0]  # r'\|(\d{4})\|'
        chapterpic_behind = re.findall(r'\|(\d{5})\|', str(script_info))[0]
        for idx, pic in enumerate(pics):
            if pic[-1]==0:
                url = 'https://images.dmzj.com/img/chapterpic/' + chapterpic_front + '/' + chapterpic_behind + '/' + pic[:-1] + '.jpg'
            else:
                url='https://images.dmzj.com/img/chapterpic/' + chapterpic_front + '/' + chapterpic_behind + '/' + pic + '.jpg'
            pic_name = '%03d.jpg' % (idx + 1)
            pic_save_path = os.path.join(chapter_save_dir, pic_name)
            with closing(requests.get(url, headers=download_header, stream=True)) as response:
                chunk_size = 1024
                content_size = int(response.headers['content-length'])
                if response.status_code == 200:
                    print('文件大小:%0.2f KB' % (content_size / chunk_size))
                    with open(pic_save_path, 'wb') as file:
                        for data in response.iter_content(chunk_size=chunk_size):
                            file.write(data)
                        else:
                            print('ConnectError')
                        file.close()
            time.sleep(5)


if __name__=="__main__":
    comicname = '妖神记'                     #漫画名称
    root = '/Users/yun/Desktop/Pyhello/'    #储存地址根目录
    path = root + comicname
    try:
        if not os.path.exists(root):
            os.mkdir(root)
        if not os.path.exists(path):
            os.mkdir(path)
        print('File creation succeeded')
    except:
        print('File creation failed ')
    target_url = 'https://www.dmzj.com/info/yaoshenji.html'  #漫画目录链接
    chapters = GetComicName_Href(target_url)
    for i in tqdm(chapters[:10]):
        if i[0]!=[] and i[1]!=0:
            Getpics(i[0],i[1],path)
        else:
            print('第%d章信息缺失'%i)

