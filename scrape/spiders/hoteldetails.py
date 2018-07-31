#!/usr/bin pypy
from ..configreader import ConfigReader
import scrapy
import pymysql
import time


class Database:

    def __init__(self):
        file_path = '/home/sarthak/Documents/scrape/scrape/config.ini'
        tags_path = '/home/sarthak/Documents/scrape/scrape/htmlTags.ini'
        self.path = ConfigReader(tags_path)
        self.config = ConfigReader(file_path)
        self.conn = pymysql.connect(host=self.config.ConfigSectionMap("DBConnection")["host"], user= self.config.ConfigSectionMap("DBConnection")["user"],
                                    passwd=self.config.ConfigSectionMap("DBConnection")['passwd'], db= self.config.ConfigSectionMap("DBConnection")["db"], use_unicode=True,
                                    charset="utf8")
        self.cur = self.conn.cursor()
        self.name = None
        self.total_db_time = 0
        self.url = None
        self.res_time = 0
        self.total_time = 0

    def select_city(self, name):
        self.cur.execute("SELECT url,id FROM city WHERE City= %s", name)

        for r in self.cur:
            self.url = str(r[0])
            self.id = str(r[1])

    def extract_name(self, response):
        initime = time.time()
        self.name = str(response.xpath(self.path.ConfigSectionMap("HotelDashboard")['hotelname']).extract_first())
        self.cur.execute('INSERT INTO hotels_desc(name,city_id) SELECT * FROM (SELECT %s, %s) AS tmp WHERE NOT EXISTS( SELECT name, city_id from hotels_desc WHERE name=%s and city_id=%s)',(self.name, self.id, self.name, self.id))
        self.conn.commit()
        exetime = time.time()
        self.total_db_time = self.total_db_time+(exetime-initime)
        return self.name

    def extract_revsum(self, response):
        initime = time.time()
        rev_sum = response.xpath(self.path.ConfigSectionMap("HotelDashboard")['revsum']).extract_first()
        self.cur.execute('update hotels_desc set review_summary=%s WHERE name=%s and city_id=%s',
                            ( rev_sum, self.name, self.id))
        self.conn.commit()
        exetime = time.time()
        self.total_db_time += (exetime - initime)
        return rev_sum

    def extract_streetadd(self, response):
        self.street_address = str(response.xpath(self.path.ConfigSectionMap("HotelDashboard")['streetadd']).extract_first())
        return self.street_address

    def extract_extnd(self, response):
        initime = time.time()
        extended_add = str(response.xpath(self.path.ConfigSectionMap("HotelDashboard")['extendedadd']).extract_first())
        location = '|'.join([self.street_address, extended_add])
        self.cur.execute('update hotels_desc set location=%s where name=%s and city_id=%s',
                            (location, self.name, self.id))
        self.conn.commit()
        exetime = time.time()
        self.total_db_time += (exetime - initime)
        return extended_add

    def extract_topamenities(self, response):
        amenities=[]
        initime = time.time()
        for item in response.xpath(self.path.ConfigSectionMap("HotelDashboard")['topamenities']):
            amenities.append(item.xpath('text()').extract_first())

        stramen = ','.join(amenities)

        self.cur.execute('SELECT id FROM hotels_desc WHERE city_id=%s and name=%s', (self.id, self.name))
        for r in self.cur:
            h_id = r[0]
        self.cur.execute(
            'INSERT INTO hoteldetails(hotel_id,Amenities) SELECT * FROM (SELECT %s,%s) '
            'As tmp WHERE NOT EXISTS( SELECT hotel_id from hoteldetails WHERE hotel_id= %s)',
            (h_id, stramen, h_id))
        self.conn.commit()
        exetime = time.time()
        self.total_db_time += (exetime - initime)
        return amenities

    def extract_price(self, response):
        initime = time.time()
        price=response.xpath(self.path.ConfigSectionMap("HotelDashboard")['price']).extract_first()
        self.cur.execute('update hotels_desc set Price=%s WHERE name=%s and city_id=%s',
                         (price,
                          self.name, self.id))
        self.conn.commit()
        exetime = time.time()
        self.total_db_time += (exetime - initime)
        return price

    def extract_total_review(self,response):
        rev = response.xpath(self.path.ConfigSectionMap("HotelDashboard")['totalrev']).extract_first()
        if rev == None:
            rev = 0
        else:
            rev = rev.split('(')
            rev = rev[1].split(')')
            rev = rev[0].split(',')
            rev = int(''.join(rev))
        self.cur.execute('update hotels_desc set Total_review=%s where city_id=%s and name=%s',(rev, self.id, self.name))
        return rev


class HotelInformation(scrapy.Spider):

    name = "hotels"
    total_parse_time = 0
    total_page_time = 0
    ini_page = 0
    total_time = 0
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

        for href in response.css(self.db.path.ConfigSectionMap("HotelDashboard")['href']):
            yield response.follow(href, self.get_hotels_details)

        for href in response.css(self.db.path.ConfigSectionMap("HotelDashboard")['pagination']):
            yield response.follow(href, self.parse)

        self.total_parse_time = exe_parse - self.ini_parse

    def get_hotels_details(self, response):
        yield{
            'Name': self.db.extract_name(response),
            'review_sum': self.db.extract_revsum(response),
            'street': self.db.extract_streetadd(response),
            'extended': self.db.extract_extnd(response),
            'amentites': self.db.extract_topamenities(response),
            'price': self.db.extract_price(response),
            'Total': self.db.extract_total_review(response)
        }

    def closed(self, reason):
        exe_time = time.time()
        self.total_time = exe_time - self.ini_time
        print("Total database time: ", self.db.total_db_time)
        print("Total request and response time: ", self.total_time-self.db.total_db_time)
        print("Total parse time: ", self.total_parse_time)
        print("total pagination time", self.total_page_time)
