# -*- coding: utf-8 -*-
import scrapy
from scrapy.exceptions import CloseSpider


XPATH_ADDRESS = '/html/body/div[3]/div/div[1]/div[1]/div/div/div/div/h4/a/text()'
XPATH_NAME = '/html/body/div[3]/div/div[1]/div[1]/div/div/div/div/h1/text()'
XPATH_LATITUDE = '/html/body/div[3]/div/div[1]/div[1]/div/div/div/div/h1/@data-lat'
XPATH_LONGITUDE = '/html/body/div[3]/div/div[1]/div[1]/div/div/div/div/h1/@data-lng'
XPATH_DETAIL_PAGE = '/html/body/div[3]/div/div/div/div[1]/div[2]/div/div/div/div/div/div/h4/a/@href'
XPATH_PAGINATION = '/html/body/div[3]/div/div/div/div[1]/div[2]/div/div[21]/div/div[1]/ul/li/a/@href'


class MapofplaySpider(scrapy.Spider):
    """
    scrapy spider to get information from mapofplay.kaboom.org for all cities
    """
    name = "mapofplay"
    allowed_domains = ["mapofplay.kaboom.org"]
    base_url = "https://mapofplay.kaboom.org/cities/%s"
    failed_counter = 0

    def start_requests(self):
        """
        generate the initial requests to get the list cities pages
        :yield: request to the list page
        """
        for i in range(26000):
            yield scrapy.Request(
                url=self.base_url % i,
                callback=self.parse_list_page
            )

    def parse_list_page(self, response):
        """
        parse the list playgrounds pages to get the detail pages url and paginates to the next pages
        :param response:
        :return:
        """
        if response.status == 200:
            self.failed_counter = 0
            # details page
            for url in response.xpath(XPATH_DETAIL_PAGE).extract():
                yield scrapy.Request(
                    url=response.urljoin(url),
                    callback=self.parse_detail_page
                )

            # pagination
            for url in response.xpath(XPATH_PAGINATION).extract():
                yield scrapy.Request(
                    url=response.urljoin(url),
                    callback=self.parse_list_page
                )

        else:
            self.failed_counter += 1
            if self.failed_counter > 2000:
                raise CloseSpider("Done")

    def parse_detail_page(self, response):
        """
        extracts address, latitude, longitude and name from the detail page
        :param response:
        :return: json object includes address, latitude, longitude and name of the playground
        """
        #

        yield {
            "address": response.xpath(XPATH_ADDRESS).extract_first(),
            "name": response.xpath(XPATH_NAME).extract_first(),
            "latitude": response.xpath(XPATH_LATITUDE).extract_first(),
            "longitude": response.xpath(XPATH_LONGITUDE).extract_first()
        }
