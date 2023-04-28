# FILE : importdata.py
import pymongo
import pandas as pd

from middleware import preprocess

def loaddata():
    # connect to server 
    client = pymongo.MongoClient("mongodb://root:h86IOY01VA81@185.223.207.149:27017/")
    db = client['news']
    
    # read database collection in mongdb
    db_cnn = db['cnn_indonesia_com'].find()
    db_detik = db['detik_com'].find()
    db_inews = db['inews_id'].find()
    db_kompas = db['kompas_com'].find()
    db_liputan = db['liputan6_com'].find()
    db_sindo = db['sindonews_com'].find()
    db_tempo = db['tempo_co'].find()

    # convert collection to pandas dataframe
    cnn = pd.DataFrame(list(db_cnn))
    detik = pd.DataFrame(list(db_detik))
    inews = pd.DataFrame(list(db_inews))
    kompas = pd.DataFrame(list(db_kompas))
    liputan = pd.DataFrame(list(db_liputan))
    sindo = pd.DataFrame(list(db_sindo))
    tempo = pd.DataFrame(list(db_tempo))

    cnn['source'] = 'cnn'
    detik['source'] = 'data'
    inews['source'] = 'inews'
    kompas['source'] = 'kompas'
    liputan['source'] = 'liputan'
    sindo['source'] = 'sindo'
    tempo['source'] = 'tempo'

    input = [cnn, detik, inews, kompas, liputan, sindo, tempo]
    df = pd.concat(input, ignore_index=True)
    df = preprocess.editing(df)

    # close mongodb connection
    client.close()
    return df
