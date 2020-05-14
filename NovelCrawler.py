import requests
import time
from bs4 import BeautifulSoup
from tqdm import tqdm

def get_content(target):
    try:
        r=requests.get(url=target)
        r.raise_for_status()
        r.encoding=r.apparent_encoding
        html=r.text
        bf=BeautifulSoup(html,'lxml')
        texts=bf.find('div',id='content')
        content=texts.text.strip().split('\xa0'*4)
        return content
    except:
        return []

if __name__=="__main__":
    try:
        target='https://www.xsbiquge.com/15_15338/'
        server='https://www.xsbiquge.com'
        book_name='诡异之主'
        r=requests.get(url=target)
        r.raise_for_status()
        r.encoding=r.apparent_encoding
        html=r.text
        bs=BeautifulSoup(html,'lxml')
        chapters=bs.find('div',id='list')
        chapters=chapters.find_all('a')
        for chapter in tqdm(chapters[:100]):
            chapter_name=chapter.string
            url=server+chapter.get('href')
            content=get_content(url)
            with open(book_name,'a',encoding='utf-8') as f:
                f.write(chapter_name)
                f.write('\n')
                f.write('\n'.join(content))
                f.write('\n')
            time.sleep(1.0)
    except:
        print("error")