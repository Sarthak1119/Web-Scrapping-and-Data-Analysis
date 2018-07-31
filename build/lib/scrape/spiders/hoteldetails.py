#!/usr/bin/env python
import scrapy
import pymysql
import time

class Database:

    def __init__(self):
        self.conn = pymysql.connect(host='127.0.0.1', user='root', passwd=None, db='tripadvisor2', use_unicode=True,
                                    charset="utf8")
        self.cur = self.conn.cursor()
        self.name = None
        self.totaltime = 0
        self.url = None
        self.res_time = 0
        self.total_time = 0

    def select_city(self, name):
        self.cur.execute("SELECT url,id FROM city WHERE City= %s", (name))

        for r in self.cur:
            self.url = str(r[0])
            self.id = str(r[1])

    def get_hotels_details(self, response):
        amenities = []

        def extract_name(query):
            initime = time.time()
            self.name = str(response.xpath(query).extract_first())
            self.cur.execute('INSERT INTO hotels_desc(name,city_id) SELECT * FROM (SELECT %s, %s) AS tmp WHERE NOT EXISTS( SELECT name, city_id from hotels_desc WHERE name=%s and city_id=%s)',(str(response.xpath(query).extract_first()), self.id, str(response.xpath(query).extract_first()), self.id))
            exetime = time.time()
            self.totaltime = self.totaltime+(exetime-initime)
            return response.xpath(query).extract_first()

        def extract_revsum(query):
            initime = time.time()
            self.cur.execute('update hotels_desc set review_summary=%s WHERE name=%s and city_id=%s',
                             (str(response.xpath(query).extract_first()), self.name, self.id))
            exetime = time.time()
            self.totaltime += (exetime - initime)
            return response.xpath(query).extract_first()

        def extract_streetadd(query):
            self.street_address = str(response.xpath(query).extract_first())
            return response.xpath(query).extract_first()

        def extract_extnd(query):
            initime = time.time()
            extended_add = str(response.xpath(query).extract_first())
            location = '|'.join([self.street_address, extended_add])
            self.cur.execute('update hotels_desc set location=%s where name=%s and city_id=%s',
                             (location, self.name, self.id))
            exetime = time.time()
            self.totaltime += (exetime - initime)
            return response.xpath(query).extract_first()

        def extract_topamenities(query):
            initime = time.time()
            for item in response.xpath(query):
                amenities.append(item.xpath('text()').extract()[0])

            stramen = ','.join(amenities)

            self.cur.execute('SELECT id FROM hotels_desc WHERE city_id=%s and name=%s', (self.id, self.name))
            for r in self.cur:
                h_id = r[0]
            self.cur.execute(
                'INSERT INTO hoteldetails(hotel_id,Amenities) SELECT * FROM (SELECT %s,%s) As tmp WHERE NOT EXISTS( SELECT hotel_id from hoteldetails WHERE hotel_id= %s)',
                (h_id, stramen, h_id))
            exetime = time.time()
            self.totaltime += (exetime - initime)
            return amenities

        def extract_price(query):
            initime = time.time()
            self.cur.execute('SELECT id FROM hotels_desc WHERE city_id=%s and name=%s', (self.id, self.name))
            for r in self.cur:
                h_id = r[0]
            self.cur.execute(
                'INSERT INTO hotelprice(hotel_id,Price) SELECT * FROM (SELECT %s,%s) As tmp WHERE NOT EXISTS(SELECT hotel_id from hotelprice where hotel_id=%s)',
                (h_id, response.xpath(query).extract_first(), h_id))
            exetime = time.time()
            self.totaltime += (exetime - initime)
            return response.xpath(query).extract_first()

        self.conn.commit()

        yield {
            'Name': extract_name(
                './/div[@class="ui_column is-12-tablet is-10-mobile hotelDescription"]/h1[@id="HEADING"]/text()'),
            'review_summary': extract_revsum('.//div[@class="prw_rup prw_common_bubble_rating rating"]/span/@alt'),
            'street': extract_streetadd('.//span[@class="detail"]/span[@class="street-address"]/text()'),
            'extendedadd': extract_extnd('.//span[@class="detail"]/span[@class="extended-address"]/text()'),
            'TopAmenities': extract_topamenities(
                './/div[@class="ui_columns is-gapless is-multiline details amenitiesColumn"]/div[@class="detailsMid ui_column is-12"]/div/div[@class="ui_column is-6"]/div[@class="highlightedAmenity detailListItem"]'),
            'Price': extract_price(
                './/div[@class="ui_column is-4 is-shown-at-desktop"]/div[@class="section_content"]/div[@class="sub_content"]/div[@class="textitem"]/text()')
        }




class HotelInformation(scrapy.Spider):
    name = "hotels"

    #total_time = 0
    total_parse_time = 0
    total_page_time=0
    ini_page=0
    total_time=0


    city_name = input("Enter City: ")
    city_name.lower().strip()
    db = Database()
    db.select_city(city_name)
    start_request = time.time()
    ini_parse = time.time()
    start_urls = [db.url]


    def parse(self, response):
        exe_parse = time.time()
        print(exe_parse-self.ini_parse)
        self.ini_time = time.time()

        for href in response.css('div.listing_title a::attr(href)'):
            yield response.follow(href, self.db.get_hotels_details)

        for href in response.css('div.pageNumbers a::attr(href)'):
            yield response.follow(href, self.parse)



        self.total_parse_time = exe_parse - self.ini_parse


    def closed(self, reason):
        exe_time = time.time()
        self.total_time = exe_time - self.ini_time
        print("Total database time: ", self.db.totaltime)
        print("Total request and response time: ", self.total_time-self.db.totaltime)
        print("Total parse time: ", self.total_parse_time)
        print("total pagination time",self.total_page_time)