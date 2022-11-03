from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///book-collection.db"
app.app_context().push()
db = SQLAlchemy(app)
db.init_app(app)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(224), unique=True, nullable=False)
    author = db.Column(db.String(224), nullable=False)
    rating = db.Column(db.Float, nullable=False)

db.create_all()

@app.route('/')
def home():
    books = db.session.execute(db.select(Book).order_by(Book.id)).scalars()
    return render_template('index.html', books=books)


@app.route("/add", methods=['POST', 'GET'])         #add entry to db
def add():
    if request.method == 'POST':
        rf = request.form
        new_book = Book(title=rf['title'], author=rf['author'], rating=rf['rating'])
        db.session.add(new_book)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('add.html')

@app.route('/edit/<id>', methods=['POST', 'GET'])   #edit rating for entry
def edit(id):
    book = db.get_or_404(Book, id)
    if request.method == 'POST':
        rf = request.form
        book.rating = rf['rating']
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('edit.html', book=book)

@app.route('/delete')       #deletes entry from db (no warning)
def delete():
    book_id = request.args.get('id')
    bye_book = db.get_or_404(Book, book_id)
    db.session.delete(bye_book)
    db.session.commit()
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)

