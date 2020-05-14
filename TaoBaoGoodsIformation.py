import requests
import re

def getHTMLText(url):
    try:
        kv={'cookie':'thw=cn; cna=2gy3FvvGFFcCARvJw7QB/Gtz; v=0; cookie2=195f098a1d219d57604d400f76bd1af2; t=58b2699cebaa203e0ee3be050e68bf41; _tb_token_=8e1be86361e7; _samesite_flag_=true; sgcookie=EfuoJUokwoUFbZjLfF4v9; uc3=vt3=F8dBxGXKxwSapgTO%2BvA%3D&lg2=URm48syIIVrSKA%3D%3D&id2=VyyZGEbSCcFQZQ%3D%3D&nk2=F5RBx%2BJ5OA5%2BwHQ%3D; csg=9efa6ad5; lgc=tb422957420; dnk=tb422957420; skt=efd5b4edaacde9c6; existShop=MTU4OTAxNjYzNA%3D%3D; uc4=id4=0%40VXtWBr1j5Y2srEUU2IpQQVl%2FewmQ&nk4=0%40FY4KoqIh5ALCCszJTn3Mj7gAnV6VGQ%3D%3D; tracknick=tb422957420; _cc_=U%2BGCWk%2F7og%3D%3D; enc=JwSyb%2FURHjj64AePDjrKmIkTwDuTZres95h3QVMO5dnL07Hd6U2luZo2JxhfEBulgrYOwoi9%2F7gCscqCCHm9XQ%3D%3D; tfstk=cS_CBwmdnTQNt6bE7TNwYquDb9Tda9gB_W9GOGdK1hjoqy1BBscsuKTGs_DtWnd1.; mt=ci=11_1; hng=CN%7Czh-CN%7CCNY%7C156; uc1=cookie16=V32FPkk%2FxXMk5UvIbNtImtMfJQ%3D%3D&cookie21=U%2BGCWk%2F7pY%2FF&cookie15=U%2BGCWk%2F75gdr5Q%3D%3D&existShop=false&pas=0&cookie14=UoTUM2DyG7jx9A%3D%3D; JSESSIONID=2115CE6461D780D27153C8002D7E0519; isg=BFZW_XNwFJeKCiC09LUfjUsZpwpY95oxp1KwMsC_QjnUg_YdKIfqQbxxGx9vMJJJ; l=eBjBUQnqQSz9QR99BOfaFurza77OSIRYYuPzaNbMiT5P995B55oAWZbrDDL6C3GVh6fJR3uzKtO9BeYBcQAonxv92j-la_kmn',\
            'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'}
        r=requests.get(url,timeout=30,headers=kv)
        r.raise_for_status()
        r.encoding=r.apparent_encoding
        return r.text
    except:
        return ''

def parsePage(html,ilist):
    try:
        plt=re.findall(r'\"view_price\"\:\"[\d\.]*\"',html)
        tlt=re.findall(r'\"raw_title\"\:\".*?\"',html)
        for i in range(len(plt)):
            price=eval(plt[i].split(':')[1])
            title=eval(tlt[i].split(':')[1])
            ilist.append([price,title])
    except:
        print('')

def printGoodsList(ilist):
    tplt="{:4}\t{:8}\t{:16}"
    print(tplt.format('序号','价格','商品名称'))
    cnt=0
    for g in ilist:
        cnt+=1
        print(tplt.format(cnt,g[0],g[1]))

if __name__=='__main__':
    goods='书包'
    depth=2
    start_url='https://s.taobao.com/search?q='+goods
    inforlist=[]
    for i in range(depth):
        try:
            url=start_url+'&s='+str(44*i)
            html=getHTMLText(url)
            parsePage(html,inforlist)
        except:
            continue
    printGoodsList(inforlist)
