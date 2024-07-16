from mitmproxy import http, ctx

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
            
            cookies = flow.request.headers.get('cookie', '').split('=')  # 文字列でcookiesの情報取得
            ctx.log.info(f'cookies: {cookies}')
            
            divide_cookies = [] # cookieのname=valueを、　'name', 'value'と分けていくリスト 
            new_cookies_new = []
            
            # cookieタグを抽出。 =の後の値は取得しない。
                
            for cookie in cookies:
                divide_cookies.extend(cookie.split(','))

            ctx.log.info(f'new_cookies: {divide_cookies}') # new_cookiesにcookiesのheaderとその値が入っている。

            for divide_cookie in divide_cookies:
                for target_cookie in target_cookies:
                    if divide_cookie.strip() == target_cookie:
                        ctx.log.info(f'divide_cookie:{divide_cookie} = target_cookie: {target_cookie} is True') #全て一致してた。
            
                
            
            
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
