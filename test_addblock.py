from mitmproxy import http, ctx
import re

block_list = [
    'https://www.youtube.com/api',
    'https://www.youtube.com/youtubei',
    'https://www.youtube.com/pagead'
    'https://googleads.g.doubleclick.net',
    
]

def requestheaders(flow: http.HTTPFlow):
    for block_url in block_list:
        if flow.request.url.startswith(block_url):
            flow.request.headers['user-agent'] =  'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36'
            flow.request.headers['accept'] = 'text/html'
            flow.request.headers['referer'] = 'https://news.yahoo.co.jp/'
            
            flow.request.headers.update({
                'X-Forwarded-For': '180.59.78.7',
                'X-Forwarded-Proto': 'HTTPS'
            })
            
            # 削除するcookieリスト
            target_cookies = ['VISITOR_INFO1_LIVE', 'HSID', 'SSID', 'YSC', 'PREF', 'SID']
            cookies = flow.request.headers.get('cookie', '').split(',') # 文字列でcookiesの情報取得
            
            divide_cookies = [] # cookieのname=valueを、　'name', 'value'と分けていくリスト 
            
            
            # cookie headerの最初の=の時だけ、分割。
            # (例 PREF=tz=Asia.Tokyo&f5=30000&f7=100&f4=4000000 の時、 'PREF', 'tz=Asia.Tokyo&f5=30000&f7=100&f4=4000000' で分割する。
            for cookie in cookies:
                name, value = cookie.split('=', maxsplit=1)
                divide_cookies.extend([name, value])

            ctx.log.info(f'new_cookies: {divide_cookies}') # new_cookiesにcookiesのheaderとその値が入っている。
                        
            for i in range(len(divide_cookies) - 1, -1, -1): # 逆順に要素を取得していく理由は、順方向だと、削除したときにインデックスがずれるのを防ぐため。
                for target_cookie in target_cookies:
                    if divide_cookies[i].strip() == target_cookie:
                        del divide_cookies[i]
                        if i < len(divide_cookies):
                            del divide_cookies[i]
            
            # 前の要素と次の要素をcookie header形式に変換　つまり、 name=valueの形式にする。
            cookies_str = ''
            for i in range(0, len(divide_cookies), 2): # 0~リストの長さlen(divide_cookies)を、2ずつ飛ばして回していく。step
                if i + 1 < len(divide_cookies): # list index out of range 防止で i + 1がリストの長さ以下だった場合 true:
                    cookies_str += f'{divide_cookies[i]}={divide_cookies[i + 1]}; ' # cookie headerのように ;をつける。

            # 最後のセミコロンとスペースを削除
            if cookies_str.endswith('; '): # cookies_str.endwith(';') つまり、cookies_strの最後が;の場合 true:
                cookies_str = cookies_str[:-2] # セミコロンと空白がついているため [:-2]のスライスで削除。 つまり、cookies_strの0から-2までの部分文字列を取得。
            
            flow.request.headers['cookie'] = cookies_str
            

def responseheaders(flow: http.HTTPFlow):
    for block_url in block_list:
        if flow.response.url.startwith(block_url):
            flow.response.headers['content-length'] = 0
            flow.response.headers.update({
                'content-type': 'text/html',
                'cache-control': 'no-cache'
            })


# まだ、広告が表示される。　とりあえず、ほかはブロックされてるかクロームの開発者モードで確認。











    """
    ['aaa=aaa', 'bbb=bbb', 'ccc=ccc']となったとき、 flow.request.headers.get('cookie', '').split('=')
    を実行すると、['aaa', 'aaa,bbb', 'bbb,ccc', 'ccc,ddd']と続いていく。
    あくまで、split('=')と=を明示的にしたため、カンマはスルーされる。
    なので、次に['aaa', 'aaa,bbb', 'bbb,ccc', 'ccc,ddd']を格納したcookiesを回し、
    for cookie in cookies:
        new_cookies.extend(cookie.split(','))とカンマを明示的にsplit()させると、
    ['aaa', 'aaa', 'bbb', 'bbb', 'ccc', 'ccc']と要素ごとに区切られる。
    listのappendと、extendの違いは、append()は単一の要素を追加。
    extend()は複数の要素を追加できる。
    
    書き方としては、 list = [1,2,3,4,5,6] とある時、 
    append()の場合は、単一なので、 list.append(10)で、 list = [1,2,3,4,5,6,10]となる。
    extend()の場合は、複数なので、 list.extend([10,11]) とすると、 list = [1,2,3,4,5,6,10,11]となる。
    
    
    次に、for i in range(len(divide_cookies) - 1, -1, -1): # 逆順に要素を取得していく理由は、順方向だと、削除したときにインデックスがずれるのを防ぐため。
                for target_cookie in target_cookies:
                    if divide_cookies[i].strip() == target_cookie:
                        del divide_cookies[i]
                        if i < len(divide_cookies):
                            del divide_cookies[i]のコードの説明をする。
        
        divide_cookies = ['PREF', 'tz=Asia.Tokyo&f5=30000&f7=100&f4=4000000', 'HSID', 'value1', 'SSID', 'value2'] とする。
        
        for i in range(len(divide_cookies) - 1, -1, -1): 
        これはdivide_cookiesの要素を逆順にする(len(divide_cookies) - 1)
        逆順にした状態の最後の要素のことを指す(-1), この場合だと、逆順にした状態の最後の要素は0を指す。つまり'PREF'
        stepで、1回ずつ逆順に回していく(-1)
        
        target_cookie in target_cookies:
        これでtarget_cookiesの要素を回していく。
        
        divide_cookies[5].strip() == target_cookie: これはFalseなので、また回す。
        divide_cookies[4].strip() == target_cookie: これはTrueなので、削除する。
        divide_cookies = ['PREF', 'tz=Asia.Tokyo&f5=30000&f7=100&f4=4000000', 'HSID', 'value1', 'SSID', 'value2']
        これから、
        divide_cookies = ['PREF', 'tz=Asia.Tokyo&f5=30000&f7=100&f4=4000000', 'HSID', 'value1', 'value2']
        'SSID'を消した状態。len(divide_cookies)は、5のまま。なぜならまだif文が続いていて、回していないから。
        
        if i < len(divide_cookies): 
        この len(divide_cookies)は、この処理が終われば更新されるように設計されている。
        今は if 4 < 5でTrue:になる。
        なので、del divide_cookies[4]になり、
        divide_cookies = ['PREF', 'tz=Asia.Tokyo&f5=30000&f7=100&f4=4000000', 'HSID', 'value1', 'value2']
        から、
        divide_cookies = ['PREF', 'tz=Asia.Tokyo&f5=30000&f7=100&f4=4000000', 'HSID', 'value1']
        になる。
    """
