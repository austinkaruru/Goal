from flask import render_template, request, redirect, url_for, abort, flash
from .forms import UpdateProfile, GoalForm, CommentForm
from ..models import User, Category, Pitch, Comment
from .. import db, photos
from flask_login import login_required, current_user

from . import main

# Views


@main.route('/')
@login_required
def index():
    '''
    View root page function that returns the index page and its data
    '''
    title = 'Goals Pitching!!'
    message = "Welcome to Goals pitching. Post your pitches and view others. Don't forget to comment and vote!! Enjoy!!"
    return render_template('index.html', message=message, title=title)


@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username=uname).first()

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user=user)


@main.route('/pitch//new', methods=['GET', 'POST'])
@login_required
def new_pitch():
    '''
       view function that defines the routes decorater for the pitch
        '''

    form = GoalForm()
    if form.validate_on_submit():
        pitch = Pitch(title=form.title.data,
                      body=form.body.data, user_id=current_user.id)
        db.session.add(pitch)
        db.session.commit()
        flash('Your pitch has been created succesfully')
        return redirect(url_for('main.new_pitch'))

    pitch = Pitch.query.all()

    return render_template('goal.html', form=form, pitch_list=[pitch])


@main.route('/comment/new', methods=['GET', 'POST'])
@login_required
def new_comment():
    '''
      view  function that defines the routes decorater for the comments
        '''

    comment_form = CommentForm()
    if comment_form.validate_on_submit():
        comment = Comment(comment=comment_form.comment.data)
        db.session.add(comment)
        db.session.commit()
        flash('Your comment has been posted succesfully')
        return redirect(url_for('main.new_comment'))
    comment = Comment.query.all()
    return render_template('comment.html', comment_form=comment_form, comment_list=comment)


@main.route('/user/<uname>/update', methods=['GET', 'POST'])
def update_profile(uname):
    user = User.query.filter_by(username=uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile', uname=user.username))

    return render_template('profile/update.html', form=form)


@main.route('/user/<uname>/update/pic', methods=['POST'])
def update_pic(uname):
    user = User.query.filter_by(username=uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        # user_photo = PhotoProfile(pic_path=path, user=user)
        # db.session.commit()
    return redirect(url_for('main.profile', uname=uname))
