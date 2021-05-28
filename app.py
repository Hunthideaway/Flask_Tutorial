# import the flask library
from flask import Flask, render_template, request, redirect

# this is used for the data base
from flask_sqlalchemy import SQLAlchemy

# import datetime so that we can get the current time from the user computer
from datetime import datetime

# creates a flask app, references the file.
app = Flask(__name__)

# to create the data base file, you will use python in terminal specifying the following:
# from file import db , which file = python file with the db in it, db = database
# db.create_all() , which will create the database with all the data in mind. data = db.name
# this is the set up for the data base, tell flask where data base is stored/post.db creates a new file named it.
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy(app)

# all of the information below will be imported into the database once created.
# this is where the models and fields are for the data base.
# to add to the database you must import it, from file import database, file = file worked in(app), database = class (BlogPost)
# to show the contents of the class class.query.all(), (BlogPost.query.all())
# add data: db.session.add(class(title = 'stuff', content='stuff', author= ' stuff')). all of this is stored within the database created.
# to see the data within the class: class.query.all()[#].subject . # = the number which the specific class is located. subject = the data desired, authr, content, title...
# to delete a post in database(in python): db.session.delete(class.query.get(#)). the number starts at 1 not 0 here.
# then you have to commit it to the session(in python): db.session.commit()
# to change any data within a database: class.query.get(#).subject = 'name' . # = primary key, subject = author,title,content , name = replacement data.
# after changing or deleting anything you have to commit it. If you want to use ' when changing anything use "stuff's" instead.


class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(20), nullable=False, default="NA")
    date = db.Column(db.DateTime, nullable=False, default=datetime.now)

# define the method for the database


def __repr__(self):
    return 'Blog Post' + str(self.id)


# dumby data that will be used to show the given information to html file.
# this data is not required and can be delete since we are using a databas, i am leaving it for future reference.
all_posts = [
    {
        'title': 'post 1',
        'content': 'this is the content for post 1',
        'author': 'rj'
    },
    {
        'title': 'post 2',
        'content': 'this is the content for post 2'
    }
]

# default route
# this defines the url. the domain would be plugged in below.
# the following code runs when you get to the url.


@app.route('/')
def index():
    return render_template('index.html')

# route that bases data from here to html
# in order to allow the user to give and get posts change methods to GET, POST.


@app.route('/posts', methods=['GET', 'POST'])
def posts():
    # request.method =='POST': will take the data entered by the user and verify that the user entered a post and then add it to database.
    if request.method == 'POST':
        # this takes the information entered by the user and stores it in the class BlogPost
        post_title = request.form['title']
        post_author = request.form['author']
        post_content = request.form['content']
        new_post = BlogPost(
            title=post_title, content=post_content, author=post_author)
        # add it to the database.
        db.session.add(new_post)
        # to save the data entered in the database and not just to the session -> db.session.commit()
        db.session.commit()
        # return the new data to the page.
        return redirect('/posts')
    # display the blog post as normal if the user didnt enter any data.
    else:
        # all_posts is the original file, BlogPost is the class, orer_by sorts the posts in the desired order, all refers to all posts in th class.
        all_posts = BlogPost.query.order_by(BlogPost.date).all()
    return render_template('posts.html', posts=all_posts)

#this route is used for creating a new post. 
@app.route('/posts/new', methods=['GET', 'POST'])
def new_post():
    if request.method == 'POST':
        post_title = request.form['title']
        post_author = request.form['author']
        post_content = request.form['content']
        new_post = BlogPost(title=post_title, author=post_author, content=post_content)
        db.session.add(new_post)
        db.session.commit()
        return redirect('/posts')
    else:
        return render_template('new_post.html')

# define the route for delete. referenced in posts.html. the or 404 will return the 404 error so that the program doesnt break.
@app.route('/posts/delete/<int:id>')
def delete(id):
    post = BlogPost.query.get_or_404(id)
    # delete the psot from the database
    db.session.delete(post)
    # commit the changes
    db.session.commit()
    # redirect back to the page.
    return redirect('/posts')

# create route for edit. reference in post.html, the user should be able to get and post.


@app.route('/posts/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    # take the data that is within the post that you want to edit.
    post = BlogPost.query.get_or_404(id)
    if request.method == 'POST':
        post.title = request.form['title']
        post.author = request.form['author']
        post.content = request.form['content']
        db.session.commit()
        return redirect('/posts')
    # reference the edit.html file.
    else:
        # post = post gives post acccess to the post library above.
        return render_template('edit.html', post=post)

# decorator that defines the url. Below is the base url..


@app.route('/home/users/<string:name>/posts/<int:id>')
# function that will run when you access the url.
def hello(name, id):
    return "hello," + name + ", your id is " + str(id)

# method is used to show what the user can only get.


@app.route('/onlyget', methods=['GET'])
def get_req():
    return 'you can only get this webpage.'


# turns on debug mode.
if __name__ == "__main__":
    app.run(debug=True)
