from operator import methodcaller
import sqlite3
from datetime import timedelta 
from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)

app.secret_key = 'avg36'
app.permanent_session_lifetime = timedelta(minutes=60)

# 新規登録ページを表示
@app.route("/form", methods = ["GET"])
def regist_get():
    return render_template("regist.html")


# 登録ページで入力した情報をDBに登録し、送信する
@app.route("/form", methods = ["POST"])
def regist_post() :
    # 入力フォームに入ってきた値を受け取る
    last_name = request.form.get("last_name")
    first_name = request.form.get("first_name")
    mail = request.form.get("mail")
    tel = request.form.get("tel")
    password = request.form.get("password")

    # avg36.dbを接続する
    conn = sqlite3.connect("avg36.db")
    # sqliteで接続したものを操作する,ということを変数に代入
    c = conn.cursor()

    # 同意するにチェックが入っているかの確認
    if "agree" == False :
        return "利用規約に同意してください"

    # 入力フォームが全て埋まっているかの確認
    elif last_name != "" and first_name != "" and mail != ""\
        and tel != "" and password != "" :

        # ()内のSQL文を実行してね（バインド変数）
        c.execute("insert into register values (NULL, ?, ?, ?, ?, ?)", (last_name, first_name, mail, tel, password))

        # DBに追加するので、変更内容を保存する
        conn.commit()

        # color.dbとの接続を終了
        c.close()
        return render_template("login.html")

    else :
        return "入力フォームを全て記入してください"

@app.route("/login/<int:register_id>", methods = ["POST", "GET"])
def login(register_id):
  if request.method == "POST":
    session.permanent = True  
    session["id"] = register_id
    return redirect("/login")
  else:
    if "id" in session: 
      return redirect("/login")
    return render_template("/editpage/<int:register_id>") 


# ログインページを表示
@app.route("/login", methods = ["GET"])
def login_get():
    return render_template("login.html")

# ログインで情報をやり取りする
@app.route("/login", methods = ["POST"])
def login_post():
    last_name = request.form.get("last_name")
    first_name = request.form.get("first_name")
    password = request.form.get("password")

    # avg36.dbを接続する
    conn = sqlite3.connect("avg36.db")
    # sqliteで接続したものを操作する,ということを変数に代入
    c = conn.cursor()
    # ()内のSQL文を実行してね（バインド変数）
    c.execute("select id from register where last_name = ?\
         and first_name = ? and password = ?", (last_name, first_name, password))
    
    user_id = c.fetchone()
    session["id"]=

    # color.dbとの接続を終了
    c.close()
    if user_id not in session :
        return render_template("login.html")
    else:
        return redirect("/editpage/<int:register_id>"), render_template(lastname=last_name,\
            firstname=first_name, register_id=user_id)  

@app.route("/editpage/<int:register_id>", methods = ["GET"])
def editmypage_get(register_id):
    return render_template("mypage_edit.html")

# マイページを編集してデータベースに変更を加える
@app.route("/editpage/<int:register_id>", methods = ["GET", "POST"])
def editmypage(register_id):

    if "user_id" in session :
        name = request.form.get("name")
        img = request.form.get("img_url")
        management = request.form.get("management")
        portfolio = request.form.get("portfolio")
        min = request.form.get("min")
        max = request.form.get("max")
        twitter = request.form.get("t_url")
        insta = request.form.get("i_url")
        facebook = request.form.get("f_url")
        appear = request.form.get("appear")

        # avg36.dbを接続する
        conn = sqlite3.connect("avg36.db")
        c = conn.cursor()
        c.execute("SELECT register_id FROM members")
        id_list = c.fetchall()
        conn.commit()
        c.close()

        conn = sqlite3.connect("avg36.db")
        c = conn.cursor()
        if register_id in id_list :
            c.execute("UPDATE members SET name=?, img=?, price_min=?, price_max=?,\
            portfolio=?, twitter=?, insta=?, facebook=?, manager=?, appear=?, \
                WHERE register_id=?",(name, img, min, max, portfolio,\
                    twitter, insta, facebook, management, appear, register_id))
        else :
            c.execute("INSERT INTO members values (NULL, name, img, price_min, price_max\
                portfolio, twitter, insta, facebook, manager, appear, register_id)",\
                    (name, img, min, max, portfolio, twitter, insta, facebook, management, appear, register_id))

        conn.commit()
        c.close()
        return "変更を保存しました"
    else :
        return render_template("login.html")

    


# 404error
@app.errorhandler(404) # 404エラーが発生した場合の処理
def error_404(error):
    # return render_template('404.html')
    return "ここは404エラー！"


if __name__ == "__main__" :

    app.run(debug=True)