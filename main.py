# import package
from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel
import pandas as pd
from datetime import datetime


# membuat objek FastAPI
app = FastAPI()

# membuat endpoint -> ketentuan untuk client membuat request
# function (get, put, post, delete)
# url (/...)

#endpoint pertama (root) untuk mendapatkan pesan "Selamat datang"
@app.get('/')
def GetWelcome(): # function untuk handle endpoint di atas
    return {
        'msg': 'Selamat datang!'
    }

# end point untuk menampilkan semua isi dataset
@app.get('/data')
def GetData():
    # melakukan proses pengambilan data dari csv
    df = pd.read_csv('dataset.csv')

    # mengembalikan response isi dataset
    return df.to_dict(orient='records')

# routing / path parameter -> url dinamis -> menyesuaikan data yang ada di server
# endpoint untuk menampilkan data sesuai dengan lokasi
# data dari Rusia -> /data/russia
# data dari zimbabwe
@app.get('/data/{location}')
def GetData(location: str):

    #melakukan proses pengambilan data dari csv
    df = pd.read_csv('dataset.csv')

    # filter data berdasarkan parameter
    result = df[df.location == location]

    # validate hasil ada
    if len(result) == 0:
        # menampilkan pesan error -> data tidak ditemukan
        raise HTTPEexception(status_code = 404, detail = 'Data not found!')

    # mengembalikan response pengambilan data dari csv
    return result.to_dict(orient='records')

password = 'satu1'

# endpoint untuk menghapus data berdasarkan id
@app.delete('/data/{id}')
def DeleteData(id: int, api_key: str = Header(None)):
    # proses authentication
    if api_key != None or api_key != password:
        #kalau ada, lanjut ke proses delete
        # kalau tidak ada, kasih pesan error -> Tidak ada akses
        raise HTTPException(status_code=401, detail="You don't have access!")

    #melakukan proses pengambilan data dari csv
    df = pd.read_csv('dataset.csv')

    # cek apakah datanya ada
    result = df[df.id == id]

    # validate hasil ada
    if len(result) == 0:
        # menampilkan pesan error -> data tidak ditemukan
        raise HTTPEexception(status_code = 404, detail = 'Data not found!')

    # proses hapus data
    result = df[df.id != id]

    # update csv / dataset
    result.to_csv('dataset.csv', index=False)

    return {
        "msg": "Data has been deleted"
    }

class Profile(BaseModel):
    name: str
    age: int
    location: str

# endpoint untuk menambah data baru
# perlu ada request body -> perlu membuat schema/model
@app.post('/data')
def CreateData(profile: Profile):
    # melakukan proses pengambilan data dari csv
    df = pd.read_csv('dataset.csv')

    # proses menambah baris data
    # concat
    newData = pd.DataFrame({
        'id': [profile.id],
        'name': [profile.name],
        'age': [profile.age],
        'location': [profile.location],
        'created_at': [datetime.now().date()],
    })

    print(profile)

    # concat
    df = pd.concat([df, newData])

    df.to_csv('dataset.csv', index=False)

    return {
        "msg": "Data has been created!"
    }
    

# menyalakan 'fastapi dev' untuk nama file main, lainnya tambah nama file
# mematikan ctrl + c

