import scrapy
import re
from video.items import VideoItem

ex_list = ['番剧', '电影', '国创', '电视剧', '综艺', '纪录片', '动画', '虚拟UP主', '公益', '单机游戏', '搞笑', 'VLOG']


class VideospiderSpider(scrapy.Spider):
    name = "videospider"
    allowed_domains = ["bilibili.com"]
    start_urls = ["https://www.bilibili.com/"]

    def parse(self, response):
        # -------test--------
        # yield scrapy.Request(
        #     url='https://www.bilibili.com/v/cinephile',
        #     callback=self.parse_second
        #
        # )
        # return None
        # -------test--------
        data_list = re.findall(
            r'--><a class="channel-link" href="//(.*?)" style="letter-spacing:.px;" target="_blank">(.*?)</a><!----><!--]--><!--',
            response.body.decode('utf-8'))
        for data in data_list:
            href = "https://" + data[0]
            tag = data[1]
            if tag not in ex_list:
                yield scrapy.Request(
                    url=href,
                    callback=self.parse_second,
                    meta={'tag': tag}
                )

    def parse_second(self, response):
        # -------test--------
        # tag = '鬼畜'
        # yield scrapy.Request(
        #     url='https://www.bilibili.com/v/cinephile/cinecism',
        #     callback=self.parse_third,
        #     meta={
        #         'tag': tag,
        #         'middleware': 'SeleniumMiddleware'
        #     }
        # )
        # return None
        # -------test--------
        tag = response.meta['tag']
        data_list = response.xpath('//*[@id="i_cecream"]/div/main/div/div/div/div[1]/div[2]/a/@href').extract()
        print(data_list)
        for data in data_list:
            href = "https:" + data
            yield scrapy.Request(
                url=href,
                callback=self.parse_third,
                meta={
                    'tag': tag,
                    # 判断是否使用下载中间件
                    'middleware': 'SeleniumMiddleware'
                }
            )

    def parse_third(self, response):
        item = VideoItem()
        tag = response.meta['tag']
        data_list = response.xpath('//*[@id="i_cecream"]/div/main/div/div[3]/div[2]/div/div[2]')
        res = []
        for data in data_list:
            img = 'https:' + data.xpath('./a/div/div[1]/picture/source[1]/@srcset').extract()[0]
            img_url = img.replace('.avif', '')
            item['title'] = data.xpath('./div/div/h3/a/text()').extract()[0]
            item['watch'] = data.xpath('./a/div/div[2]/div/div/span/span/text()').extract()[0]
            item['tag'] = tag
            item['href'] = 'https:' + data.xpath('./div/div/h3/a/@href').extract()[0]
            item['img'] = img_url
            yield item
