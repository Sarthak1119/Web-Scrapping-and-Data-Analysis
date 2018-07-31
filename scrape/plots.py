from scrape.scrape.Amenities import AmenitiesPlot
from scrape.scrape.tophotels import TopHotels
from scrape.scrape.Besthotels import FindBestHotel
from scrape.scrape.configreader import ConfigReader
import pymysql


class ShowPlot:
    def __init__(self):
        self.file_Path = '/home/sarthak/Documents/scrape/scrape/config.ini'
        self.config = ConfigReader(self.file_Path)
        self.conn = pymysql.connect(host=self.config.ConfigSectionMap("DBConnection")["host"],
                                    user=self.config.ConfigSectionMap("DBConnection")["user"],
                                    passwd=self.config.ConfigSectionMap("DBConnection")['passwd'],
                                    db=self.config.ConfigSectionMap("DBConnection")["db"], use_unicode=True,
                                    charset="utf8")
        self.cur = self.conn.cursor()
        self.city = input("Enter city: ")
        self.cur.execute("select id from city where city =%s", self.city)
        for c in self.cur:
            self.ct_id = c[0]

    def amenities(self):
        obj = AmenitiesPlot(self.city, self.ct_id)
        obj.create_df(self.conn)

    def top_hotels(self):
        obj2 = TopHotels(self.city, self.ct_id)
        obj2.extract_hotels(self.conn)

    def top_rated(self):
        obj3 = FindBestHotel(self.city, self.ct_id)
        obj3.toprated(self.conn)

    def most_reviewed(self):
        obj4 = FindBestHotel(self.city, self.ct_id)
        obj4.mostreviewed(self.conn)


Choice = input("1. Plot for Amenities provided by hotels"
               "\n2. Plot for top 10 hotels of a city"
               "\n3. Plot top rated hotels of a city"
               "\n4. Plot most reviewed hotels of a city"
               "\n\nEnter your choice:")

if Choice == '1':
    obj1 = ShowPlot()
    obj1.amenities()

if Choice == '2':
    obj1 = ShowPlot()
    obj1.top_hotels()

if Choice == '3':
    obj1 = ShowPlot()
    obj1.top_rated()

if Choice == '4':
    obj1 = ShowPlot()
    obj1.most_reviewed()
