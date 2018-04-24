from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
import cgi


app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:kittens@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
app.secret_key = 'kittens'

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(500))
    public = db.Column(db.Boolean, default=False)
    
    def __init__(self, title, body):
        self.title = title
        self.body = body

@app.route('/mainpage', methods=['POST', 'GET'])
def mainpage():
    blogs = Blog.query.filter_by().all()
    return render_template('mainpage.html',title="Mainpage", blogs=blogs)

@app.route('/addablog', methods=['POST', 'GET'])
def addablog():
    if request.method == 'POST':
        if not request.form['title'] or not request.form['body']:
            post_error = "Your body or title is blank!"
            return render_template('addablog.html', post_error=post_error)
        blog_title = cgi.escape(request.form['title'])
        blog_body = cgi.escape(request.form['body'])

        
        new_blog = Blog(blog_title, blog_body)
        db.session.add(new_blog)
        db.session.commit()
        return render_template('base.html', blog=blog)
    return render_template('addablog.html', title="Add a blog!")

@app.route('/blogpage', methods=['POST', 'GET'])
def blogpage():
    blog_id=int(request.args.get('blog-id'))
    blog = Blog.query.get(blog_id)
    return render_template('blogpage.html', blog=blog)

if __name__ == '__main__':
    app.run()