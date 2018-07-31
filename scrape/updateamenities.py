import pymysql
from scrape.scrape.configreader import ConfigReader

file_Path = '/home/sarthak/Documents/scrape/scrape/config.ini'
config = ConfigReader(file_Path)
conn = pymysql.connect(host=config.ConfigSectionMap("DBConnection")["host"],
                            user=config.ConfigSectionMap("DBConnection")["user"],
                            passwd=config.ConfigSectionMap("DBConnection")['passwd'],
                            db=config.ConfigSectionMap("DBConnection")["db"], use_unicode=True,
                            charset="utf8")
cur = conn.cursor()
cur1 = conn.cursor()
id_list=[2,3,4,5,6,7,8,9,11,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33]
for i in id_list:
    cur.execute('select id from hotels_desc where city_id =%s',(i))
    for r in cur:
        cur1.execute('update hoteldetails set city_id =%s where hotel_id=%s',(i, r[0]))

conn.commit()