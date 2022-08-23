from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from cloudipsp import Api, Checkout
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=True)
    isActive = db.Column(db.Boolean, default=True)


def __repr__(self):
    return self.title


@app.route('/')
def index():
    items = Item.query.order_by(Item.price).all()
    return render_template('index.html', data=items)

@app.route('/products')
def products():
    items = Item.query.order_by(Item.price).all()
    return render_template('products.html',items=items)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/buy/<int:id>')
def buy(id):
    item = Item.query.get(id)
    api = Api(merchant_id=1396424,
              secret_key='test')
    checkout = Checkout(api=api)
    data = {
        "currency": "RUB",
        "amount": str(item.price) + '00'
    }
    url = checkout.url(data).get('checkout_url')

    return redirect(url)

@app.route('/create', methods=['POST', 'GET'])
def create():
    if request.method == 'POST':
        title = request.form['title']
        price = request.form['price']
        item = Item(title=title, price=price)

        try:
            db.session.add(item)
            db.session.commit()
            return redirect('/')
        except:
            return "Произошла ошибка"
    else:
        return render_template('create.html')

@app.route('/products/<int:id>/update', methods = ['POST','GET'])
def update(id):
    item = Item.query.get(id)
    if request.method == 'POST':
        item.title = request.form['title']
        item.price = request.form['price']

        try:
            db.session.commit()
            return redirect('/products')
        except:
            return 'При добавлении статьи произошла ошибка'
    else:
        item = Item.query.get(id)
        return render_template('update.html', item=item)

@app.route('/products/<int:id>/del')
def deletе(id):
    item = Item.query.get_or_404(id)
    try:
        db.session.delete(item)
        db.session.commit()
        return redirect("/products")
    except:
        return "При удалении товара произошла ошибка"

@app.route('/products/<int:id>')
def detail(id):
    item = Item.query.get(id)
    return render_template('detail.html',item=item)

if __name__ == '__main__':
    app.run(debug=True)
