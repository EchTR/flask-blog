# github.com/echtr | MIT LICENSE
import sqlite3 as sql
from flask import Flask, render_template, url_for, request
import os
import datetime

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")
@app.route("/posts")
def posts():
    baglanti = sql.connect("blog.db")
    im = baglanti.cursor()
    im.execute("SELECT * FROM gonderiler")
    veriler = im.fetchall()
    gonderi_sayisi = len(veriler)
    print(gonderi_sayisi)
    return render_template("posts.html", gonderi_sayisi = gonderi_sayisi, veriler = veriler)

@app.route("/gonderi_olustur", methods = ["GET", "POST"])
def gonderi_ekle():
    if request.method == "GET": return render_template("giris_sayfasi.html")
    else:
        y_nick = request.form.get("nick")
        y_sifre = request.form.get("sifre")
        baglanti = sql.connect("blog.db")
        im = baglanti.cursor()
        im.execute("SELECT * FROM admin")
        veriler = im.fetchall()
        _nick = veriler[0][0]
        _sifre = veriler[0][1]
        if y_nick == _nick and y_sifre == _sifre: return render_template("gonderi_olustur.html")
        else: return "hatalı kombinasyon!"
        
@app.route("/gonderi_olusturuluyor", methods = ["GET", "POST"])
def gonderi_olusturuluyor():
    if request.method == "POST":
        baglanti = sql.connect("blog.db")
        im = baglanti.cursor()
        _baslik = request.form.get("yazi_baslik")
        _resim = request.form.get("yazi_resim")
        _yazi = request.form.get("yazi_yazi")
        _tarih = datetime.datetime.now()
        _tarih = str(_tarih.strftime("%d")) + "." + str(_tarih.strftime("%m")) + "." + str(_tarih.year)
        im.execute(f"""INSERT INTO gonderiler(baslik, yazi, tarih, resimURL) VALUES("{_baslik}", "{_yazi}", "{_tarih}", "{_resim}")""")
        baglanti.commit()
        baglanti.close()
        return "gönderi oluşturuldu..."
    else: return "yetkisiz giriş."


if __name__ == "__main__":
    app.run()