from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from cloudipsp import Api, Checkout

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///magaz.db'
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
db = SQLAlchemy(app)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    isActive = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return self.title

@app.route('/')
def index():
    items = Item.query.order_by(Item.price).all()
    return render_template('index.html', data=items)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/cart/<int:id>')
def cart(id):
    item = Item.query.get(id)
    return render_template('cart.html', data=item)

@app.route('/checkout_url')
def checkout_url():
    return render_template('checkout_url.html')

@app.route('/buy/<int:id>')
def item_buy(id):
    item = Item.query.get(id)
    api = Api(merchant_id=1396424,
              secret_key='test')
    checkout = Checkout(api=api)
    data = {
        "currency": "BYN",
        "amount": str(item.price) + "00"
    }
    url = checkout.url(data).get('checkout')
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
            return 'ERROR'
    else:
        return render_template('create.html')



with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=False)
