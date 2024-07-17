from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///crudlist.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    contents = db.relationship('Content', backref='entry', lazy=True)

class Content(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content_text = db.Column(db.Text, nullable=False)
    entry_id = db.Column(db.Integer, db.ForeignKey('entry.id'), nullable=False)

@app.route('/')
def index():
    entries = Entry.query.all()
    return render_template('index.html', entries=entries)

@app.route('/add', methods=['POST'])
def add_entry():
    title = request.form['title']
    new_entry = Entry(title=title)
    db.session.add(new_entry)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/add_content/<int:id>', methods=['POST'])
def add_content(id):
    content_text = request.form['content_text']
    new_content = Content(content_text=content_text, entry_id=id)
    db.session.add(new_content)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_entry(id):
    entry = Entry.query.get(id)
    if request.method == 'POST':
        entry.title = request.form['title']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit.html', entry=entry)

@app.route('/edit_content/<int:id>', methods=['GET', 'POST'])
def edit_content(id):
    content = Content.query.get(id)
    if request.method == 'POST':
        content.content_text = request.form['content_text']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit_content.html', content=content)

@app.route('/delete/<int:id>', methods=['POST'])
def delete_entry(id):
    entry = Entry.query.get(id)
    for content in entry.contents:
        db.session.delete(content)
    db.session.delete(entry)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete_content/<int:id>', methods=['POST'])
def delete_content(id):
    content = Content.query.get(id)
    db.session.delete(content)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
