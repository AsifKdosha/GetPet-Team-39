import os
import uuid

from flask import render_template
from flask import url_for, flash, redirect, send_from_directory, request
from flask_login import current_user
from flask_login import login_user, logout_user, login_required
from sqlalchemy.orm import query
from werkzeug.utils import secure_filename

from flaskblog import app, db, bcrypt
from flaskblog.forms import RegistrationForm, LoginForm, AsosRegistrationForm, BusRegistrationForm, PostForm, \
    UpdateAccountForm, SendPetCoinForm
from flaskblog.models import User, Post, PostReport
from sqlalchemy.sql import func


@app.route('/images/<path:path>')
def serve_images(path):
    return send_from_directory('images', path)


@app.route('/uploads/<path:path>')
def serve_uploads(path):
    return send_from_directory('uploads', path)


@app.route("/")
@app.route("/home")
def home():
    if current_user.is_authenticated:
        return redirect(url_for('homelogged'))
    return render_template('home.html')


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register")
def register():
    return render_template('register.html', title='Register')


def get_and_save_image(f):
    base_dir = os.path.dirname(os.path.dirname(__file__))
    unique_filename = f'{uuid.uuid4()}_{f.filename}'
    filename = secure_filename(unique_filename)
    f.save(os.path.join(base_dir, 'flaskblog', 'uploads', filename))
    return filename


@app.route("/registeruser", methods=['GET', 'POST'])
def registeruser():
    if current_user.is_authenticated:
        return redirect(url_for('homelogged'))

    form = RegistrationForm()
    if form.validate_on_submit():
        f = form.image.data
        filename = None
        if f:
            filename = get_and_save_image(f)
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(name=form.name.data, email=form.email.data, password=hashed_password, image=filename)
        db.session.add(user)
        db.session.commit()
        flash(f'Your account have been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('registeruser.html', title='Register User', form=form)


@app.route("/registerbusiness", methods=['GET', 'POST'])
def registerbus():
    if current_user.is_authenticated:
        return redirect(url_for('homelogged'))
    form = BusRegistrationForm()

    if form.validate_on_submit():
        f = form.image.data
        filename = None
        if f:
            filename = get_and_save_image(f)
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(name=form.name.data, email=form.email.data, password=hashed_password, bus_id=form.bus_id.data,
                    is_bus=True, image=filename)
        db.session.add(user)
        db.session.commit()
        flash(f'Your account have been created! You are now able to log in', 'success')
        return redirect(url_for('login'))

    return render_template('registerbus.html', title='Register Bussines', form=form)


@app.route("/registerassociation", methods=['GET', 'POST'])
def registerasos():
    if current_user.is_authenticated:
        return redirect(url_for('homelogged'))
    form = AsosRegistrationForm()

    if form.validate_on_submit():
        f = form.image.data
        filename = None
        if f:
            filename = get_and_save_image(f)
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(name=form.name.data, email=form.email.data, password=hashed_password, address=form.address.data,
                    is_asos=True, image=filename)
        db.session.add(user)
        db.session.commit()
        flash(f'Your account have been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('registerasos.html', title='Register Assosition', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('homelogged'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('homelogged'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/send_pet_coin", methods=['POST'])
@login_required
def send_pet_coin():
    form = SendPetCoinForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            if user == current_user:
                flash('You can not send yourself pet coins', 'danger')
                return redirect(request.referrer)

            if user.is_asos or user.is_bus:
                flash('You can not send pet coins', 'danger')
                return redirect(request.referrer)

            if current_user.is_bus:
                flash('You can not send pet coins', 'danger')
                return redirect(request.referrer)

            if current_user.is_asos:
                user.pet_coin += form.amount.data
                db.session.commit()
                flash('Transaction completed', 'success')
                return redirect(request.referrer)
            else:
                if current_user.pet_coin_capacity >= form.amount.data:
                    user.pet_coin += form.amount.data
                    current_user.pet_coin -= form.amount.data
                    db.session.commit()
                    flash('Transaction completed', 'success')
                else:
                    flash('Not enough founds', 'danger')
        else:
            flash('User with this email does not exist', 'danger')
            return redirect(request.referrer)
    else:
        flash('Transaction error', 'danger')
    return redirect(request.referrer)


@app.route("/home_in", methods=['GET', 'POST'])
@login_required
def homelogged():
    create_post_form = PostForm()
    if current_user.is_bus:
        create_post_form.type.choices = ['product', 'discount']
    else:
        create_post_form.type.choices = ['adopt', 'foster']

    return render_template(
        'homelogged.html',
        title='Home',
        all_posts=Post.query.filter_by(is_update=False, is_events=False, is_tips=False).join(User).order_by(
            User.pet_coin.desc()),  # add desc
        adopt_posts=Post.query.filter_by(is_adopt=True),
        foster_posts=Post.query.filter_by(is_foster=True),
        product_posts=Post.query.filter_by(is_product=True),
        discount_posts=Post.query.filter_by(is_discount=True),
        create_post_form=create_post_form,
        send_pet_coin_form=SendPetCoinForm()
    )


@app.route("/reports", methods=['GET'])
@login_required
def reports():
    users = []
    for user in User.query.all():
        user_dict = user.__dict__
        user_dict['amount_posts'] = len(user.posts)
        user_dict['amount_reports_created'] = PostReport.query.filter_by(user_id=user.id).count()
        user_dict['amount_reported'] = 0

        for post in user.posts:
            user_dict['amount_reported'] += PostReport.query.filter_by(post_id=post.id).count()

        users.append(user_dict)


    return render_template(
        'reports.html',
        title='Reports',
        users=users,
        amount_posts=Post.query.count(),
        amount_users=User.query.count()-1,
        amount_pet_coint=db.session.query(func.sum(User.pet_coin)-50).filter(User.is_bus == False, User.is_asos == False)[0][0],
        regular=User.query.filter_by(is_bus=False, is_asos=False),
        buisnesses=User.query.filter_by(is_bus=True),
        asos=User.query.filter_by(is_asos=True)
    )


@app.route("/delete_post/<post_id>", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get(post_id)
    if post:
        if post.user_id == current_user.id or current_user.is_admin:
            if (current_user.pet_coin>=50 and current_user.is_bus==False and current_user.is_asos== False):
                current_user.pet_coin -= 50
            db.session.delete(post)
            db.session.commit()
            flash(f'Your post has been deleted!', 'success')
        else:
            flash(f'You cannot delete this post', 'danger')
    else:
        flash(f'Post with id - {post_id} does not exist', 'danger')
    return redirect(request.referrer)


@app.route("/create_post", methods=['POST'])
@login_required
def create_post():
    form = PostForm()

    if form.validate_on_submit():
        user_id = current_user.id
        f = form.image.data
        filename = None
        if f:
            filename = get_and_save_image(f)
        selected_type = form.type.data

        is_adopt = selected_type == 'adopt'
        is_foster = selected_type == 'foster'
        is_product = selected_type == 'product'
        is_discount = selected_type == 'discount'
        is_events = selected_type == 'events'
        is_tips = selected_type == 'tips'
        is_update = selected_type == 'update'

        post_created = Post(title=form.title.data, content=form.content.data, user_id=user_id, image=filename,
                            is_adopt=is_adopt, is_foster=is_foster, is_product=is_product, is_discount=is_discount,
                            price=form.price.data, is_tips=is_tips, is_events=is_events, is_update=is_update)
        if current_user.is_bus == False and current_user.is_asos == False:
            current_user.pet_coin += 50
        db.session.add(post_created)
        db.session.commit()
        flash('Post created successfully', 'success')
    else:
        flash('Failed to create post', 'danger')

    return redirect(request.referrer)


@app.route("/update_post/<post_id>", methods=['POST'])
@login_required
def update_post(post_id):
    post = Post.query.get(post_id)
    if post:
        if post.user_id == current_user.id:
            form = PostForm()
            form.type.data = 'adopt'  # we add this to ignore type validations
            if form.validate_on_submit():
                f = form.image.data
                if f:
                    post.image = get_and_save_image(f)
                post.title = form.title.data
                post.content = form.content.data
                if form.price.data:
                    post.price = form.price.data
                db.session.commit()
                flash('Post updated successfully', 'success')
            else:
                flash('Failed to update post', 'danger')
        else:
            flash(f'You cannot delete this post', 'danger')
    else:
        flash(f'Post with id - {post_id} does not exist', 'danger')

    return redirect(request.referrer)


@app.route("/report_post/<post_id>", methods=['POST'])
@login_required
def report_post(post_id):
    post = Post.query.get(post_id)
    if post:
        if PostReport.query.filter_by(user_id=current_user.id, post_id=post_id).count() > 0:
            flash(f'Report already exist', 'danger')
        else:
            post_report = PostReport(user_id=current_user.id, post_id=post_id)
            db.session.add(post_report)

            if PostReport.query.filter_by(post_id=post_id).count() > 2:
                db.session.delete(post)
                user = User.query.get(post.user_id)
                user.pet_coin = 0

            db.session.commit()
            flash(f'Your report has been created!', 'success')
    else:
        flash(f'Post with id - {post_id} does not exist', 'danger')
    return redirect(request.referrer)


@app.route("/account", methods=['GET', 'POST'])
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.email = form.email.data
        f = form.image.data
        if f:
            current_user.image = get_and_save_image(f)

        db.session.commit()
        flash('Your Account is updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.name.data = current_user.name
        form.email.data = current_user.email
        form.image.date = current_user.image

    return render_template(
        'account.html', title='Account', form=form,
        all_posts=Post.query.filter_by(user_id=current_user.id),
        create_post_form=PostForm())


@app.route("/association_news", methods=['GET', 'POST'])
@login_required
def asosnews():
    create_post_form = PostForm()
    if current_user.is_asos:
        create_post_form.type.choices = ['events', 'tips']

    return render_template(
        'asosnews.html',
        title='Association News',
        all_posts=Post.query.filter_by(is_discount=False, is_product=False, is_foster=False, is_adopt=False),
        asos_events_posts=Post.query.filter_by(is_events=True),
        asos_tips_posts=Post.query.filter_by(is_tips=True),
        create_post_form=create_post_form
    )


@app.route("/business_news", methods=['GET', 'POST'])
def busupdate():
    create_post_form = PostForm()
    if current_user.is_bus:
        create_post_form.type.choices = ['update']

    return render_template(
        'busupdate.html',
        title='Business Updates',
        update_posts=Post.query.filter_by(is_update=True),
        create_post_form=create_post_form
    )
