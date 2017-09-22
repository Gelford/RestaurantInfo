# coding=utf-8
# -*- coding : utf-8-*-

from scrapy.spiders import CrawlSpider
from scrapy.selector import Selector
from scrapy.http import Request
from restaurantinfo.items import RestaurantItem
import time
import sys

sys.setdefaultencoding('utf-8')

class DianpingSpider(CrawlSpider):

    name = 'restaurantinfo'

    city = 'Shanghai'

    start_urls=[

        #'http://www.dianping.com/search/category/1/10'
        #'http://www.dianping.com/search/category/1/10'
        #'http://www.dianping.com/search/category/1/10/g3243r9'
        'http://www.dianping.com/search/category/1/10/g109r5938'

               ]

    location=['r5', 'r2', 'r6', 'r1', 'r3', 'r4', 'r12', 'r10', 'r7', 'r9', 'r13', 'r8', 'r5937', 'r5938', 'r5939', 'r8846', 'r8847', 'c3580', 'r801', 'r802', 'r804', 'r865', 'r860', 'r803', 'r835', 'r812', 'r842', 'r846', 'r849', 'r806', 'r808', 'r811', 'r839', 'r854']

    foodtype=['g101', 'g113', 'g132', 'g112', 'g117', 'g110', 'g116', 'g111', 'g103', 'g114', 'g508', 'g102', 'g115', 'g109', 'g106', 'g104', 'g248', 'g3243', 'g251', 'g26481', 'g203', 'g107', 'g105', 'g108', 'g215', 'g247', 'g1338', 'g1783', 'g118']


    def parse_start_url(self, response):

        #url = 'http://www.dianping.com/search/category/1/10'
        url = self.start_urls[0]

        for loc in self.location:

            for ft in self.foodtype:
                url = 'http://www.dianping.com/search/category/1/10/%s%s' % (loc, ft)

                yield Request(url,callback=self.parse_pages)

    def parse_pages(self, response):

        selector = Selector(response)
        pg = 0
        pages = selector.xpath('//div[@class="page"]/a/@data-ga-page').extract()

        if len(pages) > 0:
            pg = pages[len(pages) - 2]

        pg=int(str(pg))+1

        page_url = str(response.url)

        for p in range(1,pg):
            u = page_url+'p'+str(p)

            yield Request(u,callback=self.parse_restaurants)

    def parse_restaurants(self, response):

        item = RestaurantItem()
        selector = Selector(response)
        div = selector.xpath('//div[@id="shop-all-list"]/ul/li')

        for dd in div:
            shopnames = dd.xpath('div[2]/div[1]/a[1]/h4/text()').extract()
            item['shopname']=shopnames[0]
            print shopnames[0]

            shopurls = dd.xpath('div[2]/div[1]/a[1]/@href').extract()
            item['shopurl'] = 'http://www.dianping.com'+str(shopurls[0])

            shoplevels = dd.xpath('div[2]/div[2]/span/@title').extract()
            item['shoplevel'] = shoplevels[0]

            commentnums = dd.xpath('div[2]/div[2]/a[1]/b/text()').extract()
            if len(commentnums)>0:
                item['commentnum'] = commentnums[0]
            else:
                item['commentnum'] = '0'

            avgcosts = dd.xpath('div[2]/div[2]/a[2]/b/text()').extract()

            if len(avgcosts) > 0:
                item['avgcost'] = filter(str.isdigit, str(avgcosts[0]))

            else:
                item['avgcost'] = '0'

            tastes = dd.xpath('div[2]/span/span[1]/b/text()').extract()
            if len(tastes) > 0:
                item['taste'] = tastes[0]
            else:
                item['taste'] = '0'

            envis = dd.xpath('div[2]/span/span[2]/b/text()').extract()
            if len(envis) > 0:
                item['envi'] = envis[0]
            else:
                item['envi'] = '0'

            services = dd.xpath('div[2]/span/span[3]/b/text()').extract()
            if len(services) > 0:
                item['service'] = services[0]
            else:
                item['service'] = '0'

            foodtypes = dd.xpath('div[2]/div[3]/a[1]/span/text()').extract()
            item['foodtype'] = foodtypes[0]

            locs = dd.xpath('div[2]/div[3]/a[2]/span/text()').extract()
            item['loc'] = locs[0]

            addresses = dd.xpath('div[2]/div[3]/span/text()').extract()
            item['address'] = addresses[0]

            item['city'] = self.city

            yield item
