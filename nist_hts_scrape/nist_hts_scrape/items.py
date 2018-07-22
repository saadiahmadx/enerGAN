import scrapy

class htsItem(scrapy.Item):
	extraHTML = scrapy.Field()
	chemicalFamily = scrapy.Field()
	chemicalFormula = scrapy.Field()
	chemicalClass = scrapy.Field()
	informalFormula = scrapy.Field()
	criticalTemps = scrapy.Field()
	avgCriticalTemp = scrapy.Field()
	stdCriticalTemp = scrapy.Field()
	method = scrapy.Field()
	measurementMethod = scrapy.Field()
	link = scrapy.Field()

