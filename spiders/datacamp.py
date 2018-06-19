# -*- coding: utf-8 -*-
import scrapy


class DatacampSpider(scrapy.Spider):
    name = 'datacamp'
    allowed_domains = ['www.datacamp.com/']
    start_urls = ['https://www.datacamp.com/community/tutorials']

    def parse(self, response):
        self.log('I just visited: ' + response.url)
	page_index = response.css('ul > li > a::text').extract_first()
    	page_urls = response.css('ul > li > a::attr(href)').extract()
    	
	for info in response.css('div.info'):
	   item = {
	      'topic':info.css('a.jsx-379356511::text').extract_first(),
	      'topic_url' : info.css('a.jsx-379356511::attr(href)').extract_first(),
	      'author_name': info.css('div.name::text').extract_first(),
              'author_profile': info.css('a.jsx-566588255::attr(href)').extract_first(),
              'description': info.css('span.description::text').extract_first(),
	   }
	   yield item

	# follow pagination link
	current_page = int(response.css('li.selected > a::text').extract_first())

	for index in page_index:
	   index = int(index)	
	   if (current_page == int(index)):
	       next_page_url = page_urls[index]
	       if next_page_url:
	      	  next_page_url = response.urljoin(next_page_url)
	          self.log(next_page_url)
	          yield scrapy.Request(url=next_page_url, callback= self.parse)


