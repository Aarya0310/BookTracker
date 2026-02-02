from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.secret_key = "devops_pro_key"

# Database Configuration
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'books.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(200), nullable=False)
    genre = db.Column(db.String(100))
    status = db.Column(db.String(50)) # Read Already, In Progress, To Be Read
    rating = db.Column(db.Integer)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    books = Book.query.all()
    total = len(books)
    done = len([b for b in books if b.status == 'Read Already'])
    progress = int((done / total * 100)) if total > 0 else 0
    avg_rating = round(sum([b.rating for b in books]) / total, 1) if total > 0 else 0
    
    return render_template('index.html', books=books, total=total, done=done, progress=progress, avg=avg_rating)

@app.route('/add', methods=['POST'])
def add_book():
    title = request.form.get('title')
    if title:
        new_book = Book(
            title=title,
            author=request.form.get('author'),
            genre=request.form.get('genre'),
            status=request.form.get('status'),
            rating=int(request.form.get('rating'))
        )
        db.session.add(new_book)
        db.session.commit()
        flash(f"Added '{title}' to your collection!")
    return redirect(url_for('index'))

@app.route('/delete/<int:id>')
def delete(id):
    book = Book.query.get_or_404(id)
    db.session.delete(book)
    db.session.commit()
    flash("Book removed.")
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)