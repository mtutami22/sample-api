# import package
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel  # parent class untuk buat schema di request body
import pandas as pd
from datetime import datetime  # untuk mendapatkan waktu terkini

# membuat objek FastAPI
app = FastAPI()


# membuat endpoint -> ketentuan untuk client membuat request
# function (get, put, post, delete)
# url (/...)

# endpoint pertama/root untuk mendapatkan pesan "selamat datang"
@app.get("/")
def getWelcome():  # function untuk menghandle endpoint diatas
    return {
        "msg": "Selamat Datang!"
    }

# endpoint untuk menampilkan semua isi dataset
@app.get("/data")
def getData():
    # melakukan proses pengambilan data dari csv
    df = pd.read_csv("dataset.csv")

    # mengembalikan response isi dataset
    return df.to_dict(orient="records")

# routing/path parameter -> url dinamis -> menyesuaikan dengan data yang ada di server
# endpoint untuk menampilkan data sesuai dengan lokasi
# data dari Rusia -> /data/russia
# data dari Zimbabwe -> /data/zimbabwe
@app.get("/data/{location}")
def getData(location: str):
    # melakukan proses pengambilan data dari csv
    df = pd.read_csv("dataset.csv")

    # filter data berdasarkan parameter
    result = df[df.location == location]

    # validate hasil ada
    if len(result) == 0:
        # menampilkan pesan error -> data tidak ditemukan
        raise HTTPException(status_code=404, detail="Data not found!")

    # mengembalikan response isi dataset
    return result.to_dict(orient="records")

# endpoint untuk menghapus data berdasarkan id
@app.delete("/data/{id}")
def deleteData(id: int):
    # melakukan proses pengambilan data dari csv
    df = pd.read_csv("dataset.csv")

    # cek apakah datanya ada
    result = df[df.id == id]

    if len(result) == 0:
        # jika tidak ada
        # menampilkan pesan error -> data tidak ditemukan
        raise HTTPException(status_code=404, detail="Data not found!")

    # proses hapus data
    # condition
    result = df[df.id != id]

    # update csv/dataset nya
    result.to_csv('dataset.csv', index=False)

    return {
        "msg": "Data has been deleted!"
    }

# schema/model untuk request body
class Profile(BaseModel):
    id: int
    name: str
    age: int
    location: str

# endpoint untuk nambah data baru
# perlu ada request body -> perlu membuat schema/model
@app.post("/data")
def createData(profile: Profile):
    # melakukan proses pengambilan data dari csv
    df = pd.read_csv("dataset.csv")

    # proses menambah baris data
    newData = pd.DataFrame({
        "id": [profile.id],
        "name": [profile.name],
        "age": [profile.age],
        "location": [profile.location],
        "created_at": [datetime.now().date()],
    })

    # concat
    df = pd.concat([df, newData])

    # update csv/dataset nya
    df.to_csv('dataset.csv', index=False)

    return {
        "msg": "Data has been created!"
    }


# untuk matiin fastapi
# ctrl + c
