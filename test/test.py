from flask import Flask, request, render_template,url_for,session
from flask_wtf import FlaskForm
from werkzeug.utils import redirect
from wtforms import StringField, SubmitField

app = Flask(__name__)

app.secret_key = 'kable'

class Asd(FlaskForm):
    name = StringField('Name')
    l_name = StringField('ForName')
    test = StringField('Test')
    submit = SubmitField('Submit')

@app.route('/', methods=['GET', 'POST'])
def test():
    # test = False
    form = Asd()

    if request.method == "POST":
        if request.form["action"] == "one":
            session['name'] = form.name.data
            session['l_name'] = form.l_name.data
            session['test'] = form.name.data
            return redirect(url_for('sub'))

        elif request.form["action"] == "two":
            session['name'] = form.name.data
            session['l_name'] = form.l_name.data
            session['test'] = form.l_name.data
            return redirect(url_for('sub'))

    elif request.method =='GET':
        return render_template('home.html', form=form)

@app.route('/test', methods=['GET', 'POST'])
def sub():
    form = Asd()
    if request.method == "POST":
        if request.form["action"] == "one":
            session['name'] = form.name.data
            session['l_name'] = form.l_name.data
            session['test'] = form.name.data
            return redirect(url_for('sub'))

        elif request.form["action"] == "two":
            session['name'] = form.name.data
            session['l_name'] = form.l_name.data
            session['test'] = form.l_name.data
            return redirect(url_for('sub'))

    elif request.method =='GET':

        form.name.data = session['name']
        form.l_name.data = session['l_name']
        form.test.data = session['test']
    return render_template('home.html', form=form)



if __name__ == '__main__':
    app.run()