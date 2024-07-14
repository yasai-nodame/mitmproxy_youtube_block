from mitmproxy import http 
from mitmproxy.http import cookies 

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
            
            # cookie情報だけ、削除されてない。 要因はおそらく、request.cookieには存在してなくて、 cookie()を別で作って削除する方法。document確認。
            del flow.request.cookies['VISITOR_INF01_LIVE']
            del flow.request.cookies['HSID']
            del flow.request.cookies['SSID']
            del flow.request.cookies['YSC']
            del flow.request.cookies['PREF']
            del flow.request.cookies['SID']
    

def responseheaders(flow: http.HTTPFlow):
    for block_url in block_list:
        if flow.response.url.startwith(block_url):
            flow.response.headers['content-length'] = 0
            flow.response.headers.update({
                'content-type': 'text/html',
                'cache-control': 'no-cache'
            })
