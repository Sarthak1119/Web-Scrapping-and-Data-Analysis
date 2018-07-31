
import pandas as pd

import matplotlib.pyplot as plt


class TopHotels:

    def __init__(self, city, id):
        self.city = city
        self.ct_id = id

    def extract_hotels(self, conn):

        query = 'select id, name, Total_review, review_summary from hotels_desc where ' \
                'Total_review IS NOT NULL and review_summary IS NOT NULL and city_id =%s' % self.ct_id
        df_top = pd.read_sql(query, con = conn, index_col='id')
        df_top = df_top.drop(df_top[df_top.review_summary == "None"].index)
        df_top = df_top.drop(df_top[df_top.Total_review == 0].index)
        df_top = df_top.sort_values(by=['Total_review', 'review_summary', 'name'], ascending=[True, False, False]).tail(50)
        rev_sum = []
        for i in range(len(df_top)):
            rev_sum.append(float(df_top['review_summary'].values[i].split(' ')[0]))

        df_top = df_top.assign(rev_sum=rev_sum)
        df_top = df_top.sort_values(by=['rev_sum','name'], ascending=[True, False]).tail(10)
        self.plot(df_top)

    def plot(self, df_top):
        name_list = []
        for n in df_top['name']:
            name_list.append(n)
        name_list[:] = ((elem[:20] + '...') if len(elem) > 27 else elem for elem in name_list)

        df_top = df_top.assign(name=name_list)

        fig1, ax1 = plt.subplots()
        df_top.plot(x='name', y='Total_review', ax=ax1, kind='bar',
                        title='Top 10 Hotels of ' + (self.city.upper()), figsize=(10, 5), legend=False)
        ax1.set_ylabel('Total Reviews', fontsize=15)
        ax1.set_xlabel('Hotels', fontsize=15)
        plt.xticks(rotation=15, fontsize=7)
        value = []
        for r in df_top['rev_sum']:
            value.append(r)

        x_offset = -0.1
        y_offset = 0.02
        for p, r in zip(ax1.patches, value):
            b = p.get_bbox()
            val =  r
            ax1.annotate(val, ((b.x1 + b.x0) / 2 + x_offset, b.y1 + y_offset))
        plt.tight_layout()
        plt.show()


