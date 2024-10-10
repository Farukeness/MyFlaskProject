from flask import Flask, render_template, redirect, url_for, request, make_response, abort, session
import sqlite3
import random

from weather import *
app = Flask(__name__)
app.secret_key = b"sdfskf23e__"




def giris_kotrol():
    name = ""
    login_auth = False
    if "username" in session:
        name = session["username"]
        login_auth = True
    return name, login_auth

def idgetir():
    con = sqlite3.connect("database.db")
    cur = con.cursor()
    sorular = cur.execute("SELECT * FROM sorular").fetchall()

    id = cur.execute("SELECT no FROM sorular").fetchall()
    con.commit()
    id = id[0][0]

    return id, sorular
    #id = cur.execute("SELECT no FROM sorular").fetchall()
    #con.commit()
    #id = id[0][0]





@app.route("/", methods = ['GET', 'POST'])
def Index():
    name, login_auth = giris_kotrol()
    id = random.randint(0,4)
    weathers = bilgilerigetir()
    if request.method == 'POST':
        city_name = request.form['name']
        weathers = bilgilerigetir(city_name=city_name)
        
        return render_template('index.html', login_auth=login_auth, id=id, days =days, weathers = weathers)
    else:
        return render_template('index.html', login_auth=login_auth, id=id, days=days,weathers = weathers)
    

@app.route("/kayit", methods=['GET', 'POST'])
def Kayit():
    kontrol = ""
    name, login_auth = giris_kotrol()
    if request.method == 'POST':

        girisname = request.form["kayitisim"]
        kadi = request.form["kadi"]
        sifre = request.form["kayitsifre"]
        sifreTekrar = request.form["sifreTekrar"]
        puan = 0
        sql = "SELECT isim  FROM kullanicilar where isim= '"+girisname+"'"
        afd = "SELECT kadi  FROM kullanicilar where kadi= '"+kadi+"'"
        con = sqlite3.connect("database.db")
        cur = con.cursor()
        isiml = cur.execute(sql).fetchall()
        kadil = cur.execute(afd).fetchall()

        print("userkayit")
        print(girisname,kadi)

        if girisname == "" or kadi == "" or sifre == "" or puan == "":
            kontrol = "Lütfen Bilgilerinizi Doğru Giriniz!"
        elif len(isiml) != 0 or len(kadil) != 0:
            kontrol = "Kullanıcı Adı Ve İsim Benzersiz Olmalıdır"
        elif sifreTekrar != sifre:
            kontrol = "Şifreleriniz Aynı Değil!"
        else:
            with sqlite3.connect("database.db") as con:
                con.row_factory = sqlite3.Row
                cur = con.cursor()
                sqlQuary= """ INSERT INTO kullanicilar (isim,kadi,sifre,puan)
                   VALUES ("{}","{}","{}","{}")""".format(girisname, kadi, sifre, puan)
                cur.execute(sqlQuary)
                con.commit()
            kontrol = "Kayıt Başarılı Şekilde Oluştu"




    return render_template("kayit.html", name=name, login_auth=login_auth, kontrol=kontrol)

@app.route("/logout")
def Logout():
    if "username" in session:
        del session["username"]
    return redirect(url_for("Index"))


@app.route("/giris", methods=['GET', 'POST'])
def Giris():
    error = ""
    name, login_auth = giris_kotrol()
    if request.method == "POST":
        if request.form:
            if "username" in request.form and "password" in request.form:
                username = request.form["username"]
                password = request.form["password"]
                sql = "SELECT isim, sifre  from kullanicilar where isim= '"+username+"' and sifre='"+password+"'"
                con = sqlite3.connect("database.db")
                cur = con.cursor()
                cur.execute(sql)
                user = cur.fetchall()
                print(user)
                print("useraltı")
                if len(user) != 0:
                    session["username"] = user[0][0]
                    return redirect(url_for("Index"))

                else:
                    error = "Lütfen Bilgilerinizi Eksiksiz Giriniz!"
                    #return redirect(url_for("Giris"))
                    return render_template("giris.html", name=name, login_auth=login_auth, error=error)
        abort(400)


    return render_template("giris.html", name=name, login_auth=login_auth, error=error)
@app.route("/sinav/<int:id>", methods=['GET', 'POST'])
def Sinav(id):
    kontrol = ""
    kullaniciPuani = 0
    rastgele = random.randint(0,4)
    name, login_auth = giris_kotrol()
    con = sqlite3.connect("database.db")
    cur = con.cursor()
    puan = cur.execute("SELECT puan FROM kullanicilar WHERE isim = '"+name+"'").fetchone()[0]
    print(name)
    sorular = cur.execute("SELECT * FROM sorular").fetchall()
    con.commit()
    dogrucevab = cur.execute("SELECT dogru FROM sorular ").fetchall()
    used_questions = []
    if id < 5:
        if request.method == 'POST':
            if request.form:
                cevab = request.form["cevab"]
                if cevab == dogrucevab[id][0]:
                    kullaniciPuani = puan + 1
                    print("doğru cevabb helel")
                    update = "UPDATE kullanicilar SET puan = '" + str(kullaniciPuani) + "' WHERE isim = '" + name + "'"
                    con.cursor().execute(update)
                    con.commit()
                    used_questions.append(id)
                used_questions.append(id)

                # Tüm sorular kullanıldıysa, liste sıfırlanır
                if len(used_questions) == len(sorular):
                    used_questions.clear()

                # Kullanılmayan bir soru seçmek için döngü
                while True:
                    new_id = random.randint(0, 4)
                    if new_id not in used_questions:
                        break

                return redirect(url_for("Sinav", id=new_id))


    else:
        id = 0

    return render_template("sinav.html", name=name, login_auth=login_auth, kontrol=kontrol,id=id, sorular=sorular, puan=puan, rastgele=rastgele)


@app.route("/liderlikTablosu")
def LiderlikTablosu():
    id = random.randint(0, 4)
    name, login_auth = giris_kotrol()
    con = sqlite3.connect("database.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("SELECT isim,kadi,puan from kullanicilar")
    rows = cur.fetchall()

    return render_template("liderlikTablosu.html", name=name, login_auth=login_auth, rows=rows, id=id)



if __name__ == "__main__":
    app.run(debug=True)






