import pymysql
from scrape.scrape.configreader import ConfigReader


file_Path = '/home/sarthak/Documents/scrape/scrape/config.ini'
config = ConfigReader(file_Path)
conn = pymysql.connect(host=config.ConfigSectionMap("DBConnection")["host"], user=config.ConfigSectionMap("DBConnection")["user"],
                                    passwd =config.ConfigSectionMap("DBConnection")['passwd'], db= config.ConfigSectionMap("DBConnection")["db"], use_unicode=True,
                                    charset="utf8")

cur =conn.cursor()
avgdict={}

cur.execute('select Price, id from hotels_desc where city_id=33')
for n in cur:
    h_id=n[1]
    print(h_id)
    print(n[0].strip())
    if n[0]== ' Suites' or n[0] == 'None' or n[0] == 'Family Rooms' or n[0]=='' or n[0]=='Non-Smoking Rooms' or n[0]=='Suites, Family Rooms' or n[0]=='Suites, Kitchenette, Non-Smoking Rooms, Family Rooms' or n[0]=='Suites' or n[0]=='Non-Smoking Rooms, Family Rooms' or n[0]=='Suites, Non-Smoking Rooms, Family Rooms, Smoking rooms available' \
            or n[0] =='Smoking rooms available' or n[0]=='Non-Smoking Rooms, Family Rooms, Accessible rooms' or n[0]=='Kitchenette, Non-Smoking Rooms, Smoking rooms available' or n[0]=='Kitchenette' or n[0]=='Suites, Non-Smoking Rooms, Smoking rooms available' or n[0]=='Kitchenette, Non-Smoking Rooms, Family Rooms' \
            or n[0]=='Suites, Kitchenette, Non-Smoking Rooms, Family Rooms, Smoking rooms available, Accessible rooms' or n[0]==' Best Value Hotel in Jaipur' or n[0]=='Suites, Kitchenette' or n[0]=='Non-Smoking Rooms, Kitchenette, Family Rooms' or n[0]=='Kitchenette, Family Rooms' \
            or n[0]=='Family Rooms, Smoking rooms available' or n[0]==' Spa Hotel in Jodhpur' or n[0]=='Suites, Kitchenette, Family Rooms' \
            or n[0]=='Family Rooms, Non-Smoking Rooms, Smoking rooms available' or n[0]=='Suites, Kitchenette, Family Rooms, Smoking rooms available' or n[0]=='Non-Smoking Rooms, Smoking rooms available' or n[0]=='Suites, Non-Smoking Rooms, Family Rooms, Smoking rooms available, Accessible rooms' \
            or n[0]=='Suites, Non-Smoking Rooms, Accessible rooms' or n[0]=='Suites, Non-Smoking Rooms, Family Rooms, Smoking rooms available, Kitchenette' \
            or n[0]=='Kitchenette, Non-Smoking Rooms' or n[0] == 'Non-Smoking Rooms, Family Rooms, Smoking rooms available' or n[0] == 'Non-Smoking Rooms, Kitchenette':

        #print("None")
        avgdict[h_id]=0
        #cur.execute('update hotels_desc set Average_price= %s where id=%s', (0,h_id))
        #conn.commit()

    else:
        str1=n[0]
        #print(str1)
        str1=str1.split(' ')
        #print(str1)
        min = str1[0].lstrip('₹ ')
        #print(min)
        min1 = min.lstrip('? ')
        #print(min1)
        min1=min1.split(',')
        #print("hello",min1)
        min1=int(''.join(min1))
        #print(min1)
        max=str1[2].lstrip('₹ ')
        max2 = max.lstrip('? ')
        max2 = max2.split(',')
        max2=int(''.join(max2))
        avg= (min1+max2)/2
        avgdict[h_id]=avg





for i in avgdict:
    print(avgdict[i])
    cur.execute('update hotels_desc set Average_price= %s where id=%s', (avgdict[i], i))
conn.commit()



'''cur.execute('select hotel_id, Price from hotelprice')
for n in cur:
    #print(n)
    h_id=n[0]
    price=str(n[1])
    #print(h_id)

    #print(price)
    pricelist.append(n)

for i in pricelist:
    h_id=i[0]
    price=i[1]
    print(h_id)
    print(price)
    cur.execute('update hotels_desc set Price =%s WHERE id=%s',(price,h_id))

conn.commit()

print(pricelist)



#cur.execute('update hotels_desc set Price=%s WHERE id=%s',(price, h_id))'''
