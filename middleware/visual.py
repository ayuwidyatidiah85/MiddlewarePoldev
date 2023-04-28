# CLASS VERSION

import matplotlib.pyplot as plt
import math
from middleware import importdata, filtering

class Visualisation:
    def __init__(self):
        self.df = importdata.loaddata()

    def filter(self, db, start=None, end=None):
        # load and filter data
        self.df = filtering.filter(self.df, db, start, end)
        return self.df

    def timeseries(self, db, start=None, end=None):
        # Filter data
        self.df = self.filter(db, start, end)

        # Kalkulasi berita per hari
        grouped = self.df.groupby([self.df['added_at'].dt.date, 'source'])['_id'].count().reset_index()
        pivoted = grouped.pivot(index='added_at', columns='source', values='_id').fillna(0)
        pivoted['total'] = pivoted.sum(axis=1)
        # pivoted = pivoted.loc[:, ['total']] # gunakan line ini bila yang diperlukan hanya informasi total berita per hari

        # Buat plot time series menggunakan matplotlib
        fig, ax = plt.subplots(figsize=(10, 6))
        pivoted.plot(ax=ax)
        ax.set_xlabel('Tanggal')
        ax.set_ylabel('Jumlah Berita')
        ax.set_title('Jumlah Total Berita Berbagai Sumber')
        plt.show()

        return pivoted

    def percentage(self, db, col, start=None, end=None):
        # Filter data
        self.df = self.filter(db, start, end)

        # count percentage
        count = self.df[col].value_counts()
        percent = count / len(self.df) * 100
        df_new = pd.concat([count, percent], axis=1)
        df_new.columns = ['count', 'percentage']
        df_new.index.name = col
        df_new.reset_index(inplace=True)

        # PIE PLOT, bisa dihapus misal ga dibutuhin
        fig, ax = plt.subplots()
        ax.pie(count, labels=df_new[col], autopct='%1.1f%%', startangle=90)
        ax.axis('equal')

        return df_new

    def rankseries(self, db, col, start=None, end=None):
        # Filter data
        self.df = self.filter(db, start, end)

        # Kalkulasi per hari
        grouped = self.df.groupby([self.df['added_at'].dt.date, col])['_id'].count().reset_index()
        pivoted = grouped.pivot(index='added_at', columns=col, values='_id').fillna(0)

        # Lakukan ranking untuk setiap baris
        rank_df = pivoted.rank(axis=1, method='min',ascending=False)

        # Buat plot time series menggunakan matplotlib
        fig, ax = plt.subplots(figsize=(10, 6))
        rank_df.plot(ax=ax)
        ax.set_xlabel('Tanggal')
        ax.set_ylabel('Peringkat ')
        ax.set_title('Peringkat Berita Terpopuler setiap harinya')
        ax.set_yticklabels(reversed(range(len(rank_df))))
        plt.show()

        return rank_df
