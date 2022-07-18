from flask import Flask,render_template,url_for,request,flash,redirect
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from requests import session
from wtforms import DecimalField,SubmitField, StringField, PasswordField

FIRST_SECRET_CODE = 19940719
RUNNISG_ON_PI = True
NERUNGRA_NAME = 'Настюша'
NERUNGRA_PASS = 'mylove'

app = Flask(__name__)
app.config['SECRET_KEY'] = 'lulu'

class SecretKey(FlaskForm):
    secret_key = DecimalField('Введите секретный код',[DataRequired()])
    secret_sumbit = SubmitField('Вот вам ваш код! Держите!')


class Submit(FlaskForm):
    submit = SubmitField('Получить подсказку!')


class Nerungra(FlaskForm):
    username = StringField('Введите имя')
    password = PasswordField('Введите пароль',validators=[DataRequired()])
    submit = SubmitField('Войти!')



@app.route("/")
@app.route('/congrats_one')
def congrats_one():
    return render_template('01_FirstPageCongrats.html')


@app.route('/congrats_two')
def congrats_two():
    return render_template('02_SecondPageCongrats.html')


@app.route('/explanation')
def explanation():
    return render_template('03_Explanation.html')


@app.route('/oldman', methods=['GET', 'POST'])
def oldman():
    helper = False
    form_help = Submit()
    form_code = SecretKey()

    if form_help.validate_on_submit():
         helper = True

    if form_code.validate_on_submit():
        secret = int(form_code.secret_key.data)
        print(secret==FIRST_SECRET_CODE)
        if secret == FIRST_SECRET_CODE:
            return redirect(url_for('parfume'))
        else:
            flash('Это неверный код!')    
    return render_template('04_OldmanQuestion.html',
                            form_code=form_code,helper=helper,form_help=form_help)


@app.route('/parfume', methods=['GET','POST'])
def parfume():
    sign_detected = False
    form_sign = Submit()

    if form_sign.validate_on_submit():
        if RUNNISG_ON_PI:
            make_a_shot('shot_one.jpg')
            
        sign_detected = True
        return render_template('05_ParfumeGiftMission.html', 
                                form_sign=form_sign, sign_detected=sign_detected)
    return render_template('05_ParfumeGiftMission.html', 
                                form_sign=form_sign, sign_detected=sign_detected)


def make_a_shot(name:str):

    from time import sleep
    from picamera import PiCamera

    camera = PiCamera()
    camera.rotation = 180
    camera.resolution = (600,400)
    camera.start_preview()
    sleep(0.5)
    camera.capture('/home/pi/Documents/HPBNAS/congatulation/static/'+name)
    camera.stop_preview()
    camera.close()




@app.route('/caban_party')
def putins_code():
    return render_template('05_1_ParfumeGiftMission.html')


@app.route('/nerungra', methods=['GET','POST'])
def nerungra():
    form = Nerungra()
    key = False
    if form.validate_on_submit():
        name = form.username.data
        pwd = form.password.data
        print(name,'in form')

        if name == NERUNGRA_NAME and pwd == NERUNGRA_PASS:
            key = True
            print(key)
            return redirect(url_for('nerungra_next'))
        
    return render_template('06_PutinsNerungraCode_Form.html',form=form,key=key)


@app.route('/nerungra_next', methods=['GET','POST'])
def nerungra_next():
    form = Submit()
    key_two = False

    if form.validate_on_submit():

        if RUNNISG_ON_PI:
            make_a_shot('shot_two.jpg')

        key_two = True
        return render_template('06_PutinsNerungraCode.html',form=form,key_two=key_two)
    
    return render_template('06_PutinsNerungraCode.html',form=form,key_two=key_two)



@app.route('/warm_words', methods=['GET','POST'])
def warm_words():
    click = False
    form = Submit()

    if form.validate_on_submit():
        click = True
        return render_template('07_AnotherWarmWords.html',form=form,click=click)
    return render_template('07_AnotherWarmWords.html',form=form,click=click)


@app.route('/last_gift')
def last_gift():
    return render_template("08_LastGift.html")


@app.route('/finish')
def finish():
    return render_template('09_Finish.html')

@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r



if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)