# -*- coding:utf8 -*-
from flask import Flask,render_template, session
from flask import request, redirect,url_for
import parse
import json


app = Flask(__name__)

@app.route('/')
def index():
    return redirect(url_for('fdc'))

@app.route('/fdc', methods=['GET', 'POST'])
def fdc():
    fdcCSS = url_for("static",filename="css/fdc.css")
    bootstrapCSS = url_for("static",filename="css/bootstrap.min.css")
    display = url_for("static",filename="js/fdc.js")
    words = [[]]

    if request.method == 'GET':
        text = "电脑是一种利用电子学原理，根据一系列指令对数据进行处理的工具。"
        return render_template('fdc.html',fdcCSS=fdcCSS, bootstrapCSS=bootstrapCSS, display=display, text=text)
    else:
        text = request.form['text']
        form = request.form['format']
        session['text'] = text
        session['format'] = form

        content = parse.get_dependency(text)
        fixcontent = parse.fdc(content)

        if form == "conll":
            content = parse.changetoconll(content)
            fixcontent = parse.changetoconll(fixcontent)

        session['content'] = content
        session['fixcontent'] = fixcontent

        return render_template('fdc.html',  **locals())

@app.route('/DCG', methods=['GET','POST'])
def visualizeDCG():

    form = session['format']
    content = session['content']

    if form =='conll':
        content = parse.changetoconll(content)

    link = parse.visualize_data(content)

    return render_template('visualize.html',links = json.dumps(link))

@app.route('/FDCG', methods=['GET', 'POST'])
def visualizeFDCG():
    form = session['format']
    fixcontent = session['fixcontent']

    if form == "conll":
        fixcontent = parse.changetojson(fixcontent)
        fixcontent = json.loads(fixcontent)

    link = parse.visualize_data(fixcontent)

    return render_template('visualize.html', links=json.dumps(link))

app.secret_key = '\xb7\xe4\xc1W6wg\t\xc4\x05\xb3\xedd\xc8\x86%\xfev\x82\x95\xfd+\x1f\xe7'

if __name__ == "__main__":
    app.config['JSON_AS_ASCII'] = False
    app.run()
    #app.run(debug=True) # debug模式

