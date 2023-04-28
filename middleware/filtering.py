import datetime

# Filter Sumber Berita
def source(df, db = ['cnn', 'detik', 'inews', 'kompas', 'liputan', 'sindo', 'tempo']) :
    filtered_df = df.loc[df['source'].isin(db)]
    return filtered_df

# Filter Waktu 
def date(df, start = None, end = None) :
    if start is None and end is None:
        start = df['added_at'].min()
        end = df['added_at'].max()
    filtered_df = df[(df['added_at'] >= start) & (df['added_at'] <= end)]
    return filtered_df



# Gabungan semua filter
def filter (df, db, start=None, end=None) :
    # Filter Sumber Berita  
    df = source(df, db)
    
    # Filter Date
    if start is None and end is None:
        df = date(df)
    elif start is not None and end is not None:
        df = date(df, start, end)
    else :
        raise ValueError("Start and error must BOTH be provided, or vice versa")
    
    # Filter kategori coming soon
    return df