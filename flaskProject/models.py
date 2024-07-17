from app import db

class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    contents = db.relationship('Content', backref='entry', lazy=True)

class Content(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content_text = db.Column(db.Text, nullable=False)
    is_done = db.Column(db.Boolean, default=False)
    entry_id = db.Column(db.Integer, db.ForeignKey('entry.id'), nullable=False)
