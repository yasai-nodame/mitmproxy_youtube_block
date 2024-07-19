import re
from mitmproxy import http, ctx

def requestheaders(flow: http.HTTPFlow):
    """
    リクエスト URL を広告ブロックリストと照合し、広告をブロックします。
    """

    try:
        # フィルタリストを読み込み、正規表現オブジェクトに変換
        filter_sets = load_filter_sets()

        # URL を抽出
        request_url = flow.request.url

        # URL フィルタリング
        for filter_set in filter_sets.values():
            if any(match for match in filter_set.match(request_url)):
                # 広告ブロック判定
                flow.abort()
                ctx.log.info(f'広告をブロック: {request_url}')
                break  # 一致したらループを抜ける

    except Exception as e:  # エラー処理
        ctx.log.error(f'広告ブロック処理でエラー発生: {e}')

def load_filter_sets():
    """
    フィルタリストを読み込み、正規表現オブジェクトの辞書を返す
    """

    filter_sets = {}
    for filename, filter_type in [('adguard.txt', 'easylist'), ('adguard.txt', 'adguard'),
                                ('fanboy.txt', 'fanboy'), ('ublock.txt', 'ublock')]:
        filter_set = set()
        with open(filename, 'rb') as f:
            for line in f:
                filter_rule = line.decode().strip()
                filter_set.add(re.compile(filter_rule))
        filter_sets[filter_type] = filter_set
    return filter_sets


    
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

# def responseheaders(flow: http.HTTPFlow):
#     for block_url in block_list:
#         if flow.response.url.startwith(block_url):
#             flow.response.headers['content-length'] = 0
#             flow.response.headers.update({
#                 'content-type': 'text/html',
#                 'cache-control': 'no-cache'
#             })
