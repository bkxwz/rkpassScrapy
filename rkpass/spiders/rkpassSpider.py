# -*- coding: utf-8 -*-
import scrapy
import re


class RkpassspiderSpider(scrapy.Spider):
    name = 'rkpassSpider'
    allowed_domains = ['www.rkpass.cn']
    start_urls = []

    for i in range(23, 24):
        start_urls.append('http://www.rkpass.cn/tk_timu/6_553_' + str(i) + '_xuanze.html')

    def parse(self, response):
        dataimg = response.xpath(".//span[@class='shisi_text']/img[last()]/@src").extract()  # 爬取题目及选项中图片
        product_id = re.findall('\((.*?)\)', response.xpath(".//script//text()").extract()[0])[0].split(',')[0].strip(
            "'")  # 该题目id 用于整理答案
        question = "".join(response.xpath(".//table/tr[2]/td/span[@class='shisi_text']//text()").extract())  # 题目
        A = "".join("".join(response.xpath(".//table/tr[5]/td/span[@class='shisi_text']//text()").extract()).split()) # D选项
        B = "".join("".join(response.xpath(".//table/tr[7]/td/span[@class='shisi_text']//text()").extract()).split()) # D选项
        C = "".join("".join(response.xpath(".//table/tr[9]/td/span[@class='shisi_text']//text()").extract()).split()) # D选项
        D = "".join("".join(response.xpath(".//table/tr[11]/td/span[@class='shisi_text']//text()").extract()).split()) # D选项

        questionImg = ''  # 初始化 防止插库失败
        if len(dataimg) > 0:  # 判断题目及选项中是否有图片
            if len(dataimg) == 1:
                questionImg = dataimg[0]  # 第一张为题目图片
            elif len(dataimg) == 4:  # 图片总数等于4张 即为选项中图片
                A = A + dataimg[0]
                B = B + dataimg[1]
                C = C + dataimg[2]
                D = D + dataimg[3]
            elif len(dataimg) == 5:  # 图片总数等于5张 则分别是A、B、C、D中的图片
                questionImg = dataimg[0]  # 第一张为题目图片
                A = A + dataimg[1]
                B = B + dataimg[2]
                C = C + dataimg[3]
                D = D + dataimg[4]
        print(C)
        print(question)

        url = 'http://www.rkpass.cn/tk_jiexi.jsp?product_id=' + product_id + '&tixing=xuanze&answer=&paper_id=&tihao=&cache='
        yield scrapy.Request(url, callback=self.parse_detail, dont_filter=True)

    def parse_detail(self, response):
        answer = response.xpath(".//td/span[@class='shisi_text']//text()").extract()[2].strip()  # 答案
        answerAnalysis = response.xpath(".//table/tr[3]/td//text()").extract()  # 答案解析
        answerAnalysis = "".join(answerAnalysis[3:len(answerAnalysis)])
        print(answerAnalysis)
