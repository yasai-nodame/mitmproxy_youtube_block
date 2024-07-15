from mitmproxy import http, ctx
from mitmproxy.http import cookies 
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
            target_cookies = ['VISITOR_INF', 'HSID', 'SSID', 'YSC', 'PREF', 'SID']
            
            cookies = flow.request.headers.get('cookie', '').split('=')  # 文字列でcookiesの情報取得
            ctx.log.info(f'cookies: {cookies}')
            
            new_cookies = []
            # cookieタグを抽出。 =の後の値は取得しない。
                
            for cookie in cookies:
                new_cookies.extend(cookie.split(','))

            ctx.log.info(f'new_cookies: {new_cookies}') # new_cookiesにcookiesのheaderとその値が入っている。
            
            # ここからnew_cookiesを使って、cookiesのheadersを削除する処理を書く。
            
    

def responseheaders(flow: http.HTTPFlow):
    for block_url in block_list:
        if flow.response.url.startwith(block_url):
            flow.response.headers['content-length'] = 0
            flow.response.headers.update({
                'content-type': 'text/html',
                'cache-control': 'no-cache'
            })
