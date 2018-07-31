import pymysql
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scrape.scrape.configreader import ConfigReader


class AmenitiesPlot:

    def __init__(self,city,id):
        self.city=city
        self.c_id =id
        #self.file_Path = '/home/sarthak/Documents/scrape/scrape/config.ini'
        #self.config = ConfigReader(self.file_Path)
        #self.conn = pymysql.connect(host=self.config.ConfigSectionMap("DBConnection")["host"], user=self.config.ConfigSectionMap("DBConnection")["user"],
         #                           passwd =self.config.ConfigSectionMap("DBConnection")['passwd'], db= self.config.ConfigSectionMap("DBConnection")["db"], use_unicode=True,
         #                           charset="utf8")
        #self.cur =self.conn.cursor()
        self.count_rs, self.count_ac, self.count_p, self.count_bk, self.count_fp, self.count_fw =0,0,0,0,0,0

    def create_df(self,conn):

       self.df_ament = pd.read_sql('select hotel_id,amenities from hoteldetails where city_id=%s'%(self.c_id), con=conn, index_col='hotel_id')
       self.df_ament = self.df_ament.drop(self.df_ament[self.df_ament.amenities == 'None'].index)
       self.create_list(self.df_ament)


    def create_list(self, df_ament):
        list_amenities=['Free Parking', 'Free Wifi', 'Breakfast', 'Pool', 'Air Conditioning', 'Room Service']
        for i in range(len(df_ament)):
            list_ament = df_ament['amenities'].values[i].split(',')
            for a in list_ament:
                if a == 'Free Wifi':
                    self.count_fw = self.count_fw + 1
                if a == 'Free Parking':
                    self.count_fp = self.count_fp + 1
                if a == 'Breakfast included':
                    self.count_bk =self.count_bk +1
                if a == 'Pool':
                    self.count_p = self.count_p +1
                if a == 'Air Conditioning':
                    self.count_ac= self.count_ac +1
                if a == 'Room Service':
                    self.count_rs = self.count_rs +1

        amenities_count = []
        amenities_count.append(self.count_fw)
        amenities_count.append(self.count_fp)
        amenities_count.append(self.count_bk)
        amenities_count.append(self.count_p)
        amenities_count.append(self.count_ac)
        amenities_count.append(self.count_rs)


        self.create_plot(list_amenities, amenities_count)

    def create_plot(self,list_amenities, amenities_count):
        y_pos= np.arange(len(list_amenities))

        plt.bar(y_pos, amenities_count, align='center',alpha=0.6,color=('r','m','g','c','b','y'))
        plt.xticks(y_pos, list_amenities)
        plt.xlabel('Amenities')
        plt.ylabel('Number of Hotels')
        plt.title('Service Provided By ' + self.city.upper() + ' Hotels')
        plt.show()




