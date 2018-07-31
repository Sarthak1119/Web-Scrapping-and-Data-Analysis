
import pymysql
import matplotlib.pyplot as plt
from matplotlib import rcParams
from scrape.scrape.configreader import ConfigReader


file_Path = '/home/sarthak/Documents/scrape/scrape/config.ini'
config = ConfigReader(file_Path)
conn = pymysql.connect(host=config.ConfigSectionMap("DBConnection")["host"], user=config.ConfigSectionMap("DBConnection")["user"],
                                    passwd =config.ConfigSectionMap("DBConnection")['passwd'], db= config.ConfigSectionMap("DBConnection")["db"], use_unicode=True,
                                    charset="utf8")
cur = conn.cursor()

state = input("Enter State: ")
state.strip()
cur.execute('select id from state where name = %s', state)
for i in cur:
    st_id = i[0]
cur.execute('select city,id from city where state_id= %s', st_id)
ct_name = []
ct_id = []
for c in cur:
    ct_name.append(c[0])
    ct_id.append(c[1])

total_hotels = []
for ct in ct_id:
    cur.execute('select count(id) from hotels_desc where city_id=%s', ct)
    for c in cur:
        total_hotels.append(c[0])
total = sum(total_hotels)/100.0
autopct = lambda x: "%d" % round(x*total)

rcParams.update({'figure.autolayout': True, 'axes.titlepad':20})

fig1, ax1 = plt.subplots()
ax1.pie(total_hotels, labels=ct_name, autopct=autopct, shadow=True, startangle=140 )
plt.tight_layout()
plt.axis('equal')
plt.legend(loc='upper left')
plt.title(state.upper() + ' City Wise Hotels', fontsize=15, pad=3, loc='left')
plt.show()
conn.close()
