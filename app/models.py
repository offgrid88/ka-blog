from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(50), index=True, unique=True)
    middleName = db.Column(db.String(50), index=True, unique=True)
    lastName = db.Column(db.String(50), index=True, unique=True)
    mobile = db.Column(db.String(15), index=True, unique=True)
    email = db.Column(db.String(50), index=True, unique=True)
    password_hash = db.Column(db.String(32))

    registeredAt = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    lastLogin = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    intro = db.Column(db.String(50), index=True, unique=True)
    PROFILE = db.Column(db.String(50), index=True, unique=True)
    posts= db.relationship('Post', backref='author', lazy= 'dynamic')
    def __repr__(self):
        return '<User {}>'.format(self.username)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    authorId = db.Column(db.String(50), index=True, unique=True)
    parentId = db.Column(db.String(50), index=True, unique=True) 
    title= db.Column(db.String(50), index=True, unique=True)
    metaTitle= db.Column(db.String(50), index=True, unique=True)
    slug= db.Column(db.String(50), index=True, unique=True)
    summary= db.Column(db.String(50), index=True, unique=True)
    published
    createdAt= db.Column(db.DateTime, index=True, default=datetime.utcnow)
    updatedAt= db.Column(db.DateTime, index=True, default=datetime.utcnow)
    publishedAt= db.Column(db.DateTime, index=True, default=datetime.utcnow)
    content= db.Column(db.String(140))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    def __repr__(self):
        return '<Post {}>'.format(self.body)
