
import pandas as pd
import matplotlib.pyplot as plt



class FindBestHotel:

    def __init__(self, city, id):
        self.city = city
        self.ct_id = id

    def toprated(self, conn):

        query = 'select id, name, review_summary, Average_price from hotels_desc where review_summary IS NOT NULL and city_id = %s'%(self.ct_id)
        df_hotels = pd.read_sql(query, con=conn, index_col='id')

        df_hotels = df_hotels.drop(df_hotels[df_hotels.Average_price == 0].index)
        df_hotels = df_hotels.drop(df_hotels[df_hotels.review_summary == "None"].index)

        df_hotels = df_hotels.sort_values(by = ['review_summary','Average_price'], ascending=[True, False]).tail(10)

        name_list = []
        for n in df_hotels['name']:
            name_list.append(n)
        name_list[:] = ((elem[:20] + '...') if len(elem) > 27 else elem for elem in name_list)

        df_hotels = df_hotels.assign(name=name_list)


        rev_sum=[]
        for i in range(len(df_hotels)):
            rev_sum.append(float(df_hotels['review_summary'].values[i].split(' ')[0]))

        df_hotels = df_hotels.assign(rev_sum=rev_sum)

        fig1, ax1 = plt.subplots()
        df_hotels.plot(x='name', y='rev_sum',ax=ax1, kind ='bar', title='Top Rated hotels of ' + (self.city.upper()),figsize=(18,10),legend=False)
        ax1.set_ylabel('Reviews',fontsize=15)
        ax1.set_xlabel('Hotels',fontsize=15)
        value = []
        for r in df_hotels['Average_price']:
            value.append(r)

        x_offset = -0.4
        y_offset = 0.02
        for p, r in zip(ax1.patches,value):
            b = p.get_bbox()
            val = '₹ ' + str(r)
            ax1.annotate(val, ((b.x1 + b.x0)/2 + x_offset, b.y1 + y_offset))

        plt.tight_layout(pad=3)
        plt.xticks(rotation=15)
        plt.show()


    def mostreviewed(self,conn):
        query1 = 'select id,name ,Total_review from hotels_desc where Total_review IS NOT NULL and city_id=%s' % (self.ct_id)
        df_reviews = pd.read_sql(query1, con=conn, index_col='id')
        df_reviews = df_reviews.drop(df_reviews[df_reviews.Total_review == 0].index)
        df_reviews = df_reviews.sort_values(by=['Total_review', 'name'], ascending=[True, False]).tail(10)
        name_list=[]
        for n in df_reviews['name']:
            name_list.append(n)
        name_list[:]=((elem[:20]+'...') if len(elem)>27 else elem for elem in name_list)

        df_reviews = df_reviews.assign(name=name_list)

        fig1, ax1 = plt.subplots()
        df_reviews.plot(x='name', y='Total_review',ax=ax1, kind ='bar', title='Top 10 Reviewed Hotels of ' + (self.city.upper()),figsize=(10,5),legend=False)
        ax1.set_ylabel('Total Reviews',fontsize=15)
        ax1.set_xlabel('Hotels', fontsize=15)
        plt.xticks(rotation=15, fontsize=7)
        x_offset = -0.2
        y_offset = 0.02
        for p in ax1.patches:
            b = p.get_bbox()

            val = b.y0 +b.y1
            ax1.annotate(int(val), ((b.x1 + b.x0) / 2 + x_offset, b.y1 + y_offset))
        plt.tight_layout()
        plt.show()