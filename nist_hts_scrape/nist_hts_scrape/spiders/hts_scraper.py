#By: Jamil Ahmad 
#Time: July 2018
#Purpose: Spider for scraping data from a NIST database -- Science Fair

import scrapy
from nist_hts_scrape.items import htsItem
import re
import numpy as np
from scrapy.selector import Selector 
from scrapy.http import HtmlResponse
from scrapy.selector import HtmlXPathSelector



class nist_hts_scrape(scrapy.Spider):
	name = "nist_hts_scraper"

	#main start url
	start_urls = ["https://srdata.nist.gov/CeramicDataPortal/Hts/DoSearch?AuthorLastName=&PublVolume=&PublSource=&PublYear=&ChemicalFamily=&StructureType=&InformalName=&Properties=18"]

	def parse(self, response):
		hrefs = response.xpath("//a[contains(@href, '/CeramicDataPortal/Hts/')]/@href").extract()
		for href in hrefs:

			url = "https://srdata.nist.gov" + href

			yield scrapy.Request(url, callback=self.parse_dir_contents)

	def parse_dir_contents(self, response):
		item = htsItem()

		#getting chemical family 
		item['chemicalFamily'] = response.xpath("//div[contains(@id, 'M1P1')]/y-1/text()[6]").extract()

		#etc...
		item['extraHTML'] = response.xpath("//div[contains(@id, 'M1P1')]").extract()
		item['link'] = response.url
		# item['chemicalFormula'] = 
		item['chemicalClass'] = response.xpath("//div[contains(@id, 'M1P1')]/y-1/text()[8]").extract()
		item['informalFormula'] = response.xpath("//div[contains(@id, 'M1P1')]/y-1/text()[4]").extract()
		item['criticalTemps'] = response.xpath("//table[contains(@class, 'table table-striped table-bordered table-condensed')]/tr/td[2]/text()").extract()
		
		#we process this from criticalTemps array
		temps = np.array(response.xpath("//table[contains(@class, 'table table-striped table-bordered table-condensed')]/tr/td[2]/text()").extract()).astype(np.float)
		item['avgCriticalTemp'] = np.mean(temps)
		item['stdCriticalTemp'] = np.std(temps)
		
		item['method'] = response.xpath("//div[contains(@id, 'M1P1')]/text()[3]").extract()
		item['measurementMethod'] = response.xpath("//div[contains(@id, 'M1P2')]/text()[4]").extract()



		yield item 

