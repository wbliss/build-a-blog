from flask import Flask, render_template, flash, session, redirect, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:build-a-blog@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'asdjklfakjshdfajhsdfjkadf4345DFeFDAeD'

class Post(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    text = db.Column(db.String(5000))

    def __init__(self, title, text):
        self.title = title
        self.text = text

@app.route('/posts')
def posts():

    posts = Post.query.all()
    return render_template('blogs.html', posts=posts)

@app.route('/blog', methods=['GET'])
def view_blog():
    id = request.args.get('id')
    blog_post = Post.query.filter_by(id=id).first()
    title = blog_post.title
    text = blog_post.text
    return render_template('blog.html', title=title, text=text)


@app.route('/newpost', methods=['POST', 'GET'])
def new_post():
    
    if request.method == 'POST':
        title = request.form['title']
        text = request.form['text']

        if title != "" and text != "":
            new_post = Post(title, text)
            db.session.add(new_post)
            db.session.commit()
            id = str(new_post.id)
            return redirect('/blog?id='+id)
        else:
            flash("Please make sure neither field is empty!")
            return render_template('newpost.html', title=title, text=text)

    
    return render_template('newpost.html')

if __name__ == '__main__':
    app.run()