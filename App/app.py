from flask import Flask, render_template, redirect, url_for,Blueprint, request, flash, g,session,  jsonify , send_from_directory,abort
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from flask_sqlalchemy  import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_wtf.csrf import CSRFProtect
import os
import random

#BASE_DIR = os.path.abspath(os.path.dirname(__file__))
csrf = CSRFProtect()
app = Flask(__name__)
csrf.init_app(app)
app.config['SECRET_KEY'] = 'Thisissupposedtobesecret!'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./database.db'

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

Bootstrap(app)
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


class Product(db.Model):
    __tablename__ = 'product'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    name = db.Column(db.String(20))
    price = db.Column(db.Integer)
    category = db.Column(db.String(20))
    description = db.Column(db.String(200))
    num = db.Column(db.Integer)
    seller = db.Column(db.String(20))
    img = db.Column(db.String(200))
    comments = db.Column(db.String(2000))
    tOD = db.Column(db.String(200))
    mOD = db.Column(db.String(200))
    rating = db.Column(db.DECIMAL(2,1))
    total = db.Column(db.Integer)
    count = db.Column(db.Integer)
    per = db.Column(db.String(2000))

    def __init__(self,name,price,category,description,num,seller,img,tOD,mOD):
        self.name = name
        self.price = price
        self.category =category
        self.description = description
        self.num = num
        self.seller = seller
        self.img = img
        self.tOD = tOD
        self.mOD = mOD
        self.comments = ''
    def __repr__(self):
        return "product {name:%r , price:%r , category:%r , num:%r}" % (self.name,self.price,self.category,self.num)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))
    cart = db.Column(db.String(200))
    history = db.Column(db.String(200))
    rating = db.Column(db.DECIMAL(2,1))
    total = db.Column(db.Integer)
    count = db.Column(db.Integer)
    per = db.Column(db.String(2000))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('remember me')


class RegisterForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])


"""@app.before_request
def csrf_protect():
    if request.method == "POST":
        token = session.pop('_csrf_token', None)
        if not token or token != request.form.get('_csrf_token'):
            abort(403)

def generate_csrf_token():
    if '_csrf_token' not in session:
        chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
        session['_csrf_token'] = some_random_string(50,chars)
    return session['_csrf_token']

random = random.SystemRandom()

def some_random_string(length=12,allowed_chars='abcdefghijklmnopqrstuvwxyz'
'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'):
    return ''.join(random.choice(allowed_chars) for i in range(length))

app.jinja_env.globals['csrf_token'] = generate_csrf_token"""

@app.route('/')
def index():
    return render_template('index.html')
mod_products = Blueprint('products',__name__)



@app.route("/upload", methods=["POST"])
def upload():
    if not current_user.is_authenticated:
        return redirect(url_for('index'))        
    target = os.path.join(APP_ROOT, 'images/')
    # target = os.path.join(APP_ROOT, 'static/')
    print(target)
    if not os.path.isdir(target):
        os.mkdir(target)
    else:
        print("Couldn't create upload directory: {}".format(target))
    print(request.files.getlist("file"))
    for upload in request.files.getlist("file"):
        print(upload)
        print("{} is the file name".format(upload.filename))
        filename = upload.filename
        destination = "/".join([target, filename])
        print ("Accept incoming file:", filename)
        print ("Save it to:", destination)
        upload.save(destination)

    # return send_from_directory("images", filename, as_attachment=True)
    return redirect(url_for('dashboard')) #render_template("lay.html", image_name=filename)

@app.route('/upload/C:/fakepath/<filename>')
def send_image(filename):
    return send_from_directory("images", filename)

@app.route('/products' , methods=['GET','POST'])
@csrf.exempt
def get_all_products():
    st = request.form['str']
    products = Product.query.all()
    p_array = []
    for p in products:
        data = {'name': str(p.name),'price':str(p.price),'category':str(p.category),'num':str(p.num),'description':str(p.description),'seller':str(p.seller),'img':str(p.img),'tOD':str(p.tOD),'mOD':str(p.mOD)}
        stri = data['category']+'1'
        if(data['name'] == st):
            p_array.append(data)
            break
        if(data['category'] == st[22:len(st)] or st[22:len(st)] == "dashboard" or stri == st[22:len(st)] or st[22:len(st)] == "sell"):
            p_array.append(data)
    return jsonify(products=p_array)

@app.route('/searchproducts/<filename>' , methods=['POST','GET'])
def get_search_products(filename):
    if not current_user.is_authenticated:
        return redirect(url_for('index'))
    products = Product.query.all()
    leng = 0
    p_array = []
    for p in products:
        data = {'name': str(p.name),'price':str(p.price),'category':str(p.category),'num':str(p.num),'description':str(p.description),'seller':str(p.seller),'img':str(p.img),'tOD':str(p.tOD),'mOD':str(p.mOD)}
        stri = data['category']+'1'
        if(data['name'] == filename):
            p_array.append(data)
            leng = leng + 1
    if(leng == 0):
        return render_template('in.html',allProducts = "notfound",naam = current_user.username)    
    return render_template('in.html', allProducts = p_array[0],naam=current_user.username)

@app.route('/searchproducts1/<filename>' , methods=['POST','GET'])
def get_search1_products(filename):
    products = Product.query.all()
    leng = 0
    p_array = []
    for p in products:
        data = {'name': str(p.name),'price':str(p.price),'category':str(p.category),'num':str(p.num),'description':str(p.description),'seller':str(p.seller),'img':str(p.img),'tOD':str(p.tOD),'mOD':str(p.mOD)}
        stri = data['category']+'1'
        if(data['name'] == filename):
            p_array.append(data)
            leng = leng + 1
    if(leng == 0):
        return render_template('in1.html', allProducts = "notfound")
    return render_template('in1.html', allProducts = p_array[0])

@app.route('/details/<filename>' , methods=['GET' , 'POST'])
def details(filename):
    if not current_user.is_authenticated:
        return redirect(url_for('index'))
    products = Product.query.all()
    p_array = []
    for p in products:
        data = {'name': str(p.name),'price':str(p.price),'category':str(p.category),'num':str(p.num),'description':str(p.description),'seller':str(p.seller),'img':str(p.img),'tOD':str(p.tOD),'mOD':str(p.mOD),'rating':str(p.rating),'count':str(p.count),'comments':str(p.comments)}
        if(data['name'] == filename):
            users = User.query.all()
            for c in users:
                d = str(c.username)
                if(d == data['seller']):
                    rat = c.rating
                    rats = c.count
                    if(str(rat) == "None"):
                        rat = 0
                        rats = 0
                    break
            if(str(data['rating']) == "None"):
                data['rating'] = 0
                p.rating = 0
                db.session.commit()
            p_array.append(data)
            break
    #return jsonify(products=p_array)
    return render_template('details.html', allProducts = p_array[0],naam=current_user.username,sellerrating = rat,sellerratings = rats)

@app.route('/<filename>/addcomment',methods=['GET','POST'])
def addcomment(filename):
    if not current_user.is_authenticated:
        return redirect(url_for('index'))
    comment = request.form['comment']
    products = Product.query.all()
    p_array = []
    for p in products:
        data = {'name': str(p.name),'price':str(p.price),'category':str(p.category),'num':str(p.num),'description':str(p.description),'seller':str(p.seller),'img':str(p.img),'tOD':str(p.tOD),'mOD':str(p.mOD),'rating':str(p.rating),'count':str(p.count),'comments':str(p.comments)}
        if(data['name'] == filename):
            if(str(p.comments) == "None"):
                p.comments = current_user.username + str(':<br/>') +comment
                db.session.commit()
            else:
                p.comments = current_user.username + str(':<br/>') + comment + str('<br/><br/>') + p.comments
                db.session.commit()
            p_array.append(data)
            break
    return p.comments

@app.route('/<filename>/addratingseller',methods=['GET','POST'])
def addratingseller(filename):
    if not current_user.is_authenticated:
        return redirect(url_for('index'))
    rate = request.form['rating']
    users = User.query.all()
    users = User.query.all()
    for c in users:
        data = str(c.username)
        if(data == filename):
            if(str(c.count) == "None" or str(c.total) == "None" or str(c.rating) == "None" or str(c.per) == "None"):
                c.total = 0
                c.count = 0
                c.rating = 0
                c.per = ''
            db.session.commit()
            person = c.per
            pers = person.split(',')
            for index in range(len(pers)):
                if( current_user.username == pers[index]):
                    return str("already added rating")
            c.per =  current_user.username + str(',') + str(c.per)
            c.count = int(c.count) + 1
            c.total = c.total + float(rate)
            db.session.commit()
            c.rating = float(c.total)/c.count
            db.session.commit()
            break
    return str(c.rating)

@app.route('/<filename>/addrating',methods=['GET','POST'])
def addrating(filename):
    if not current_user.is_authenticated:
        return redirect(url_for('index'))
    rate = request.form['rating']
    products = Product.query.all()
    for p in products:
        data = {'name': str(p.name),'price':str(p.price),'category':str(p.category),'num':str(p.num),'description':str(p.description),'seller':str(p.seller),'img':str(p.img),'tOD':str(p.tOD),'mOD':str(p.mOD),'rating':str(p.rating),'count':str(p.count)}
        if(data['name'] == filename):
            if(str(p.count) == "None" or str(p.total) == "None" or str(p.per) == "None"):
                p.total = 0
                p.count = 0
                p.per = ''
                #data['count'] = '0'
                #data['rating'] = '0'
            db.session.commit()
            person = p.per
            pers = person.split(',')
            for index in range(len(pers)):
                if( current_user.username == pers[index]):
                    return str("already added rating")
            p.per =  current_user.username + str(',') + str(p.per)
            p.count = int(p.count) + int(1)
            p.total = p.total + float(rate)
            db.session.commit()
            p.rating = float(p.total)/p.count
            db.session.commit()
            break
    return str(p.rating)

@app.route('/prodetails/<filename>' , methods=['GET' , 'POST'])
def prodetails(filename):
    if not current_user.is_authenticated:
        return redirect(url_for('index'))
    products = Product.query.all()
    p_array = []
    for p in products:
        data = {'name': str(p.name),'price':str(p.price),'category':str(p.category),'num':str(p.num),'description':str(p.description),'seller':str(p.seller),'img':str(p.img),'tOD':str(p.tOD),'mOD':str(p.mOD)}
        if(data['name'] == filename):
            p_array.append(data)
            break
    #return jsonify(products=p_array)
    return render_template('details2.html', allProducts = p_array[0],naam=current_user.username)

@app.route('/prodetails1/<filename>' , methods=['GET' , 'POST'])
def prodetails1(filename):
    if not current_user.is_authenticated:
        return redirect(url_for('index'))
    products = Product.query.all()
    p_array = []
    for p in products:
        data = {'name': str(p.name),'price':str(p.price),'category':str(p.category),'num':str(p.num),'description':str(p.description),'seller':str(p.seller),'img':str(p.img),'tOD':str(p.tOD),'mOD':str(p.mOD)}
        if(data['name'] == filename):
            p_array.append(data)
            break
    #return jsonify(products=p_array)
    return render_template('details3.html', allProducts = p_array[0],naam=current_user.username)

@app.route('/details1/<filename>' , methods=['GET' , 'POST'])
def details1(filename):
    products = Product.query.all()
    p_array = []
    for p in products:
        data = {'name': str(p.name),'price':str(p.price),'category':str(p.category),'num':str(p.num),'description':str(p.description),'seller':str(p.seller),'img':str(p.img),'tOD':str(p.tOD),'mOD':str(p.mOD),'rating':str(p.rating),'count':str(p.count),'comments':str(p.comments)}
        if(data['name'] == filename):
            users = User.query.all()
            for c in users:
                d = str(c.username)
                if(d == data['seller']):
                    rat = c.rating
                    rats = c.count
                    if(str(rat) == "None"):
                        rat = 0
                        rats = 0
                    break
            if(str(data['rating']) == "None"):
                data['rating'] = 0
                p.rating = 0
                db.session.commit()
            p_array.append(data)
            break
    #return jsonify(products=p_array)
    return render_template('details1.html', allProducts = p_array[0],sellerrating = rat,sellerratings = rats)

"""@app.route('/laptops/addProduct',method=['POST'])"""
@app.route('/addProduct',methods=['POST'])
def add_product():
    if not current_user.is_authenticated:
        return redirect(url_for('index'))
    product = Product(request.form['name'],request.form['price'],request.form['category'],request.form['description'],request.form['num'],request.form['seller'],request.form['img'],request.form['tOD'],request.form['mOD'])
    db.session.add(product)
    db.session.commit()
    return 'success'

@app.route('/addToCart',methods=['POST'])
def addToCart():
    if not current_user.is_authenticated:
        return redirect(url_for('index'))
    product = request.form['name']
    for p in db.session.query(Product).all():
        if(p.name == product):
            # p.num = p.num - 1
            if(p.num <= 0):
                p.num = 0
                db.session.commit()
                return 'OUT OF STOCK'
            break
   
    for c in db.session.query(User).all():
        if(c.username == current_user.username):
            if(str(c.cart) == 'None' or c.cart == ''):
                c.cart = product + str(',') + str(p.price) 
            else:
                c.cart =  product+str(',')+str(p.price)+str(',')+str(c.cart)
            break
    db.session.commit()
    return 'successfully added to the cart'

@app.route('/viewCart',methods=['POST','GET'])
def viewCart():
    if not current_user.is_authenticated:
        return redirect(url_for('index'))
    for c in db.session.query(User).all():
        if(c.username == current_user.username):
            if(str(c.cart) == "None"):
                c.cart = ''
                db.session.commit()
            return render_template('cart.html',products = c.cart, naam=current_user.username)

@app.route('/cartcancel',methods=['POST','GET'])
def cartcancel():
    if not current_user.is_authenticated:
        return redirect(url_for('index'))
    for c in db.session.query(User).all():
        if(c.username == current_user.username):
            c.cart = ''
            break
    db.session.commit()
    return redirect(url_for('dashboard'))

@app.route('/cartbuy',methods=['POST','GET'])
def cartbuy():
    if not current_user.is_authenticated:
        return redirect(url_for('index'))
    for c in db.session.query(User).all():
        if(c.username == current_user.username):
            if(str(c.history) == 'None' or c.history == ''):
                c.history = str(c.cart)
            else:
                c.history = str(c.cart) + str(',') + str(c.history)
            str_nam = str(c.cart)
            c.cart = ''
            db.session.commit()
            str_array = str_nam.split(',')
            for index in range(len(str_array)):
                for p in db.session.query(Product).all():
                    if(p.name == str_array[index]):
                        if(p.num == 0):
                            return str("Out Of Stock")
                        p.num = p.num - 1
                        db.session.commit()
            db.session.commit()
            break
    return str(c.history)

@app.route('/viewhistory',methods=['POST','GET'])
def viewhistory():
    if not current_user.is_authenticated:
        return redirect(url_for('index'))
    for c in db.session.query(User).all():
        if(c.username == current_user.username):
            if(str(c.history) == "None"):
                c.history = ''
                db.session.commit()
    return render_template('history.html',products = c.history, naam=current_user.username)

@app.route('/clearhistory',methods=['POST','GET'])
def clearhistory():
    if not current_user.is_authenticated:
        return redirect(url_for('index'))
    for c in db.session.query(User).all():
        if(c.username == current_user.username):
            c.history = ''
            db.session.commit()
            break
    return redirect(url_for('viewhistory'))


@app.route('/mobiles',methods=['GET','POST'])
def mobiles():
    form = LoginForm()
    return render_template('ind.html' , form=form)

@login_required
@app.route('/mobiles1',methods=['GET','POST'])
def mobiles1():
    if not current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    return render_template('inde.html' , naam=current_user.username)

@app.route('/laptops',methods=['GET','POST'])
def laptops():
    return render_template('ind.html')

@app.route('/laptops1',methods=['GET','POST'])
def laptops1():
    if not current_user.is_authenticated:
        return redirect(url_for('index'))
    return render_template('inde.html', naam=current_user.username)

@app.route('/bikes',methods=['GET','POST'])
def bikes():
    return render_template('ind.html')

@app.route('/bikes1',methods=['GET','POST'])
def bikes1():
    if not current_user.is_authenticated:
        return redirect(url_for('index'))
    return render_template('inde.html', naam=current_user.username)

@app.route('/mobileaccessories',methods=['GET','POST'])
def mobileaccessories():
    return render_template('ind.html')

@app.route('/mobileaccessories1',methods=['GET','POST'])
def mobileaccessories1():
    if not current_user.is_authenticated:
        return redirect(url_for('index'))
    return render_template('inde.html', naam=current_user.username)

@app.route('/furniture',methods=['GET','POST'])
def furniture():
    return render_template('ind.html')

@app.route('/furniture1',methods=['GET','POST'])
def furniture1():
    if not current_user.is_authenticated:
        return redirect(url_for('index'))
    return render_template('inde.html', naam=current_user.username)
@app.route('/sell',methods=['GET','POST'])
def sell():
    if not current_user.is_authenticated:
        return redirect(url_for('index'))
    return render_template('lay.html', naam=current_user.username)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                return redirect(url_for('dashboard'))

        return '<h1>Invalid username or password</h1>'
    #return '<h1>' + form.username.data + ' ' + form.password.data + '</h1>'

    return render_template('login.html', form=form)



@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('dashboard'))
    #return '<h1>' + form.username.data + ' ' + form.email.data + ' ' + form.password.data + '</h1>'

    return render_template('signup.html', form=form)


@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dassh.html', naam=current_user.username)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
