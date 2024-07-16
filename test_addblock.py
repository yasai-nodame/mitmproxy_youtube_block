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
            flow.request.headers['user-agent'] =  '	Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0.3 Safari/605.1.15'
            flow.request.headers['accept'] = 'text/html'
            flow.request.headers['referer'] = 'https://www3.nhk.or.jp/news/'
            
            flow.request.headers.update({
                'X-Forwarded-For': '180.59.78.1',
                'X-Forwarded-Proto': 'HTTPS'
            })
            
            # 削除するcookieリスト
            target_cookies = ['VISITOR_INFO1_LIVE', 'HSID', 'SSID', 'YSC', 'PREF', 'SID']
            cookies = flow.request.headers.get('cookie', '').split(',') # 文字列でcookiesの情報取得
            
            divide_cookies = [] # cookieのname=valueを、　'name', 'value'と分けていくリスト 
            new_cookies_new = []
            
            # cookie headerの最初の=の時だけ、分割。
            # (例 PREF=tz=Asia.Tokyo&f5=30000&f7=100&f4=4000000 の時、 'PREF', 'tz=Asia.Tokyo&f5=30000&f7=100&f4=4000000' で分割する。
            for cookie in cookies:
                name, value = cookie.split('=', maxsplit=1)
                divide_cookies.extend([name, value])

            ctx.log.info(f'new_cookies: {divide_cookies}') # new_cookiesにcookiesのheaderとその値が入っている。
                        
            for i in range(len(divide_cookies) - 1, -1, -1):
                for target_cookie in target_cookies:
                    if divide_cookies[i].strip() == target_cookie:
                        del divide_cookies[i]
                        if i < len(divide_cookies):
                            del divide_cookies[i]
            
            # 前の要素と次の要素をcookie header形式に変換　つまり、 name=valueの形式にする。
            
            
            
            
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
    """

# def responseheaders(flow: http.HTTPFlow):
#     for block_url in block_list:
#         if flow.response.url.startwith(block_url):
#             flow.response.headers['content-length'] = 0
#             flow.response.headers.update({
#                 'content-type': 'text/html',
#                 'cache-control': 'no-cache'
#             })
