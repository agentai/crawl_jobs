# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

import random
from scrapy import signals
import json
import requests


class UserAgentDownloaderMiddleware(object):

    USER_AGENT = ["Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.163 Safari/535.1",
                  "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36",
                  "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0",
                  "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
                  "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11",
                  "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",
                  'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6',
                  'Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5',
                  'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
                  'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)',
                  'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11',
                  'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; 360SE)',
                  'Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)',
                  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20',
                  'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6',
                  'Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10',
                  'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER',
                  'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1',
                  'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)',
                  'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12',
                  'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)',
                  'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1',
                  # 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.3 Mobile/14E277 Safari/603.1.30',
                  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
                  ]

    def process_request(self, request, spider):
        user_agent = random.choice(self.USER_AGENT)
        request.headers['User-Agent'] = user_agent


from fake_useragent import UserAgent # pip install fake_useragent


class RandomUserAgentMiddlware(object):
    """
    随机跟换user-agent
    """
    def __init__(self,crawler):
        super(RandomUserAgentMiddlware,self).__init__()
        self.ua = UserAgent()
        self.ua_type = crawler.settings.get('RANDOM_UA_TYPE', 'random') #从setting文件中读取RANDOM_UA_TYPE值

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def process_request(self, request, spider):  ###系统电泳函数
        def get_ua():
            return getattr(self.ua, self.ua_type)
        # user_agent_random=get_ua()
        request.headers.setdefault('User_Agent', get_ua())
        pass


class ProxyMiddleware(object):
    def __init__(self, proxy_url):
        self.proxy_url = proxy_url

    def get_random_proxy(self):
        try:
            response = requests.get(self.proxy_url)
            if response.status_code == 200:
                p = json.loads(response.text)
                proxy = p.get("proxy", "")

                # print('get proxy ...')
                ip = {"http": "http://" + proxy, "https": "https://" + proxy}
                r = requests.get("http://www.baidu.com", proxies=ip, timeout=4)
                if r.status_code == 200:
                    return proxy
        except:
            print('get proxy again ...')
            return self.get_random_proxy()

    def process_request(self, request, spider):
            proxy = self.get_random_proxy()
            if proxy:
                print('======' + '使用代理 ' + str(proxy) + "======")
                request.meta['proxy'] = 'https://{proxy}'.format(proxy=proxy)

    def process_response(self, request, response, spider):
        if response.status != 200:
            print("again response ip:")
            request.meta['proxy'] = 'https://{proxy}'.format(proxy=self.get_random_proxy())
            return request
        return response

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        return cls(
            proxy_url=settings.get('PROXY_URL')
        )



# 创建一个中间件     ip代理池
from collections import defaultdict
from scrapy.exceptions import NotConfigured

class RandomProxyMiddleware(object):

    def __init__(self, settings):
        # 第三步 初始化配置和变量
        # 在settings中写一个 PROXIES 列表配置
        # 从settings中把代理读进来（把环境变量读进来）
        # self.proxies = settings.getlist("PROXIES")
        self.proxy_url = settings.get('PROXY_URL')
        self.proxies = self.get_proxies()
        self.stats = defaultdict(int)  # 默认值是0    统计次数
        self.max_failed = 3  # 请求最多不超过3次

    def get_proxies(self):
        response = requests.get(self.proxy_url)
        return list(filter(lambda y: len(y) > 0, [x.get("proxy", "") for x in json.loads(response.text)]))

    @classmethod
    def from_cralwer(cls, crawler):
        # 第一步 创建中间件对象
        # 首先获取配置 HTTPPROXY_ENABLED 看看是否启用代理，
        if not crawler.settings.getbool("HTTPPROXY_ENABLED"):  # 如果没有启用代理
            raise NotConfigured
        # auth_encoding = crawler.settings.get("HTTPPROXY_AUTH_ENCODING")  # 读取配置，这里暂时不用
        # 第二步
        return cls(settings=crawler.settings)  # cls（）实际调用的是 init()函数，如果init接受参数，cls就需要参数

    def process_request(self, request, spider):
        # 第四步 为每个request对象随机分配一个ip代理
        # 让这个请求使用代理                       初始url不使用代理ip
        if self.proxies and not request.meta.get("proxy") and request.url not in spider.start_urls:
            request.meta["proxy"] = random.choice(self.proxies)

    def process_response(self, request, response, spider):
        self.proxies = self.get_proxies()
        # 第五步： 请求成功
        cur_proxy = request.meta.get('proxy')
        # 判断是否被对方禁封
        if response.status > 400:
            # 给相应的ip失败次数 +1
            self.stats[cur_proxy] += 1
            print("当前ip{}，第{}次出现错误状态码".format(cur_proxy, self.stats[cur_proxy]))
        # 当某个ip的失败次数累计到一定数量
        if self.stats[cur_proxy] >= self.max_failed:  # 当前ip失败超过3次
            print("当前状态码是{}，代理{}可能被封了".format(response.status, cur_proxy))
            # 可以认为该ip被对方封了，从代理池中删除这个ip
            self.remove_proxy(cur_proxy)
            del request.meta['proxy']
            # 将这个请求重新给调度器，重新下载
            return request

        # 状态码正常的时候，正常返回
        return response

    def process_exception(self, request, exception, spider):
        self.proxies = self.get_proxies()
        # 第五步：请求失败
        cur_proxy = request.meta.get('proxy')   # 取出当前代理
        from twisted.internet.error import ConnectionRefusedError, TimeoutError
        # 如果本次请求使用了代理，并且网络请求报错，认为这个ip出了问题
        if cur_proxy and isinstance(exception, (ConnectionRefusedError, TimeoutError)):
            print("当前的{}和当前的{}".format(exception, cur_proxy))
            self.remove_proxy(cur_proxy)
            del request.meta['proxy']
            # 重新下载这个请求
            return request

    def remove_proxy(self, proxy):
        if proxy in self.proxies:
            self.proxies.remove(proxy)
            print("从代理列表中删除{}".format(proxy))
