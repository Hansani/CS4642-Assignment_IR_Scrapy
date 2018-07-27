# -*- coding: utf-8 -*-
import scrapy


class DatacampSpider(scrapy.Spider):
    name = 'datacamp'
    allowed_domains = ['www.datacamp.com/']
    api_ulr = 'https://www.datacamp.com/community/tutorials?page={}'
    start_urls = [api_ulr.format(1)]

    def parse(self, response):
        self.log('I just visited: ' + response.url)

        for info in response.css('div.list>div.TutorialCard>div.info'):
            item = {
                'title':info.css('div.infoHead>div.TagLine>div.Tag>span.title::text').extract(),
                'topic':info.css('div.infoHead>h2.blue>a::text').extract_first(),
                'topic_url' : info.css('div.infoHead>h2.blue>a::attr(href)').extract_first(),
                'description': info.css('div.infoHead>span.description::text').extract_first(),
                'author_name': info.css('div.authorWrapper>div.Author>a.jsx-566588255>div.info>div.name::text').extract_first(),
                'author_profile': info.css('div.authorWrapper>div.Author>a.jsx-566588255::attr(href)').extract_first(),
            }
            yield item
        # follow pagination link
        current_page_index = int(response.css('ul > li.selected > a::text').extract_first())
        next_page_index = current_page_index + 1
        if(next_page_index<12):
            next_page_url = self.api_ulr.format(next_page_index)
            self.log(next_page_url)
            yield scrapy.Request(url=next_page_url, callback=self.parse, dont_filter=True)
