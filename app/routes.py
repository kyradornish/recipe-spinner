from app import app, db 
from flask import render_template, url_for, redirect, flash, request, session
from app.forms import LoginForm, RegistrationForm, RecipeSearch, getRecipeByIngredients, getRecipeURL, EditProfileForm, ResetPasswordRequestForm, ResetPasswordForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Saved
from werkzeug.urls import url_parse
from app.email import send_password_reset_email


@app.route("/", methods=['GET', 'POST'])
def index():
    if "ingredients" not in session:
        session["ingredients"] = []
    session["ingredients"].clear()
    form = RecipeSearch()
    if form.validate_on_submit():
        ingredient=form.ingredient.data
        return redirect(url_for('results', ingredient=ingredient, remove='False'))
    return render_template("index.html", form=form, title="Home")

@app.route("/results/<ingredient>/<remove>", methods=['GET', 'POST'])
def results(ingredient, remove):
    form = RecipeSearch()
    ingredients = session["ingredients"]
    if ingredient not in ingredients and remove != ingredient:
        ingredients.append(ingredient)
    elif remove == ingredient:
        for i in range(len(ingredients)):
            if ingredient == ingredients[i]:
                session['ingredients'].pop(i)
                break
    if form.validate_on_submit():
        if form.ingredient.data:
            if form.ingredient.data in ingredients:
                flash('You already entered that ingredient.')
            else:
                ingredients.append(form.ingredient.data)
    ingredient_list = ""
    ingredients = session["ingredients"]  
    for ingredient in ingredients:
        ingredient_list += ingredient + ","
    resultjson = getRecipeByIngredients(ingredient_list)
    session["resultjson"] = resultjson
    resultid = []
    for result in resultjson:
        resultid.append(result["id"])
    recipeinfo = []
    for id in resultid:
        recipeinfo.append(getRecipeURL(id))
    return render_template('results.html', results=resultjson, recipeinfo=recipeinfo, ingredients=ingredients, form=form, title="Results")    

@app.route("/recipe/<r_id>")
def recipe(r_id):
    recipeinfo = [getRecipeURL(r_id)]
    return render_template("recipe.html", recipeinfo=recipeinfo, title="Recipe")

@app.route('/clear')
def clear():
  session["ingredients"].clear()
  flash("You have cleared your list of ingredients, start a new search by entering ingredients.")
  return redirect(url_for('results', ingredient=False, remove='False'))

@app.route('/save/<r_id>', methods=['GET', 'POST'])
def save(r_id):
    if current_user.is_anonymous:
        flash("You must be logged in to save recipes.")
        return redirect(url_for('results', ingredient=False, remove=False))
    user_recipes = Saved.query.filter_by(user_id=current_user.id).all()
    for recipe in user_recipes:
        if int(r_id) == recipe.recipe_id:
            flash("You have already saved this recipe.")
            return redirect(url_for('results', ingredient=False, remove=False))
    saved_recipe = Saved(recipe_id=r_id, user_id=current_user.id)
    db.session.add(saved_recipe)
    db.session.commit()
    flash("Recipe saved!")
    return redirect(url_for('results', ingredient=False, remove='False'))

@app.route('/remove/<r_id>', methods=['GET', 'POST'])
@login_required
def remove(r_id):
    Saved.query.filter_by(user_id=current_user.id, recipe_id=r_id).delete()
    db.session.commit()
    flash('You have successfully removed the recipe.')
    return redirect(url_for('profile', username=current_user.username))


@app.route('/profile/<username>')
@login_required
def profile(username):
    user = User.query.filter_by(username=username).first()
    user_recipes = Saved.query.filter_by(user_id=current_user.id).all()
    recipe_list = []
    for recipe in user_recipes:
        recipe_list.append(recipe.recipe_id)
    recipeinfo = []
    for r_id in recipe_list:
        recipeinfo.append(getRecipeURL(r_id))
    return render_template('profile.html', user=user, title="Profile", recipeinfo=recipeinfo)

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username, current_user.email)
    if form.validate_on_submit():
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('profile', username=current_user.username))
    elif request.method == 'GET':
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template('edit_profile.html', title='Edit Profile', form=form)

@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('Check your email for the instructions to reset your password')
        return redirect(url_for('login'))
    return render_template('reset_password_request.html', title='Reset Password', form=form)

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.')
        return redirect(url_for('login'))
    return render_template('reset_password.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Incorrect username or password. Please try again!')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('profile', username=form.username.data)
        return redirect(next_page)
    return render_template('login.html', title="Log In", form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(first_name=form.first_name.data, last_name=form.last_name.data, email=form.email.data, username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been successfully created!')
        login_user(user)
        return redirect(url_for('profile', username=form.username.data))
    return render_template('register.html', title="Register", form=form)

@app.route('/logout')
def logout():
    session["ingredients"].clear()
    logout_user()
    return redirect(url_for('login'))

@app.route("/planner")
def planner():
    return render_template("planner.html")
