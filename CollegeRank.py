import requests
from bs4 import BeautifulSoup
import bs4


def getHTMLtext(url):
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return ''


def fillUnivList(ulist, html):
    soup = BeautifulSoup(html, "html.parser")
    for tr in soup.find('tbody').children:
        if isinstance(tr, bs4.element.Tag):
            tds = tr('td')
            ulist.append([tds[0].string, tds[1].string, tds[2].string, tds[3].string])


def printUnivList(ulist, num):
    # print("{:^10}\t{:^10}\t{:^10}\t{:^10}".format('排名','学校名称','地址','总分'))
    tplist = "{0:^10}\t{1:{4}^10}\t{2:^10}\t{3:<6}"
    print(tplist.format('排名', '学校名称', '地址', '总分', chr(12288)))
    for i in range(num):
        u = ulist[i]
        # print("{:^10}\t{:^10}\t{:^10}\t{:^10}".format(u[0],u[1],u[2],u[3]))
        print(tplist.format(u[0], u[1], u[2], u[3], chr(12288)))


if __name__ == "__main__":
    uinfo = []
    url = "http://zuihaodaxue.com/Greater_China_Ranking2019_0.html"
    html = getHTMLtext(url)
    fillUnivList(uinfo, html)
    printUnivList(uinfo, 20)
