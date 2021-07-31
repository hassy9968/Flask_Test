from flask import Flask, render_template, request, redirect, url_for, session
import pandas as pd
from datetime import datetime


app = Flask(__name__)
app.secret_key = "aaa"

#databaseをpandas DataFrameで呼び出す
def load_csv():
    df = pd.read_csv(r"db/database.csv",names=["memo","date","name","avatar"])
    return df

#DataFrameに memo の内容と 今日の日付 を加えてdatabaseに書き込む
def save_csv(df1, memo, name, avatar):
    save_date = datetime.now().strftime('%y/%m/%d-%H:%M')
    df2 = pd.DataFrame(data=[[memo, save_date, name, avatar]], columns=["memo","date","name","avatar"])
    df3 = df1.append(df2,ignore_index=True)
    df3.to_csv(r"db/database.csv", header=False, index=False)


        
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/login')
def login():
    your_name = request.args.get("username","")
    your_avatar = request.args.get("avatar","")
    
    if your_name and your_avatar:
        session["name"] = your_name
        session["avatar"] = your_avatar
        return redirect(url_for("memo"))
    else:
        return redirect(url_for("index"))


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for("index"))
    
    
@app.route('/delete/<msg>')
def delete(msg):
    if msg:
        df = load_csv()
        df_d = df[df["memo"] != msg]
        df_d.to_csv(r"db/database.csv", header=False, index=False)
    
    return redirect(url_for("memo"))


@app.route('/memo', methods=["GET","POST"])
def memo():
    print(session["name"], session["avatar"])
    print(session)
    res=[]
    df = load_csv()
    if request.method == "POST":    
        data = request.form.get("memo","")
        if data:
            save_csv(df, data, session["name"], session["avatar"])

 #別解--getで送信して内容を削除する。クエリストリングに削除内容が乗るからかっこ悪いが一応可能--   
#    if request.method == "GET":
 #       key = request.args.get("cont","")
  #      if key:
   #         df = load_csv()
    #        df_d = df[df["memo"] != key]
     #       df_d.to_csv(r"db/database.csv", header=False, index=False)
        
        
    df_s = load_csv()
    for i in df_s.itertuples():
        msg = i[1]
        day = i[2]
        uname = i[3]
        avat = i[4]
        d = dict(msg = i[1], day = i[2], uname = i[3], avat = i[4])
        res.append(d)
    return render_template("memo.html", res=res)

#コマンドプロンプトで python main.py と入力すればサーバーが動き出す
if __name__ == "__main__":
    app.run(debug=True)
