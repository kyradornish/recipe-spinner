from app import app, db 
from flask import render_template, url_for, redirect, flash, request, session
from app.forms import LoginForm, RegistrationForm, RecipeSearch, AddIngredient
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User
from werkzeug.urls import url_parse


@app.route("/", methods=['GET', 'POST'])
def index():
    form = RecipeSearch()
    ingredients = session["ingredients"]
    if form.validate_on_submit():
        ingredient=form.ingredient.data
        return redirect(url_for('results', ingredient=ingredient, remove='False'))
    return render_template("index.html", form=form, title="Home")

@app.route("/results/<ingredient>/<remove>", methods=['GET', 'POST'])
def results(ingredient, remove):
    form = RecipeSearch()
    ingredients = session["ingredients"]
    if ingredient not in ingredients:
        ingredients.append(ingredient)
    elif remove == ingredient:
        for i in range(len(ingredients)):
            if ingredient == ingredients[i]:
                session['ingredients'].pop(i)
                break
                print(ingredients)
    if form.validate_on_submit():
        if form.ingredient.data:
            if form.ingredient.data in ingredients:
                flash('You already entered that ingredient.')
            else:
                ingredients.append(form.ingredient.data)
    ingredient_list = ""
    print(ingredients)
    ingredients = session["ingredients"]
    print(ingredients)    
    for ingredient in ingredients:
        ingredient_list += ingredient + ","
    resultjson = form.getRecipeByIngredients(ingredient_list)
    session["resultjson"] = resultjson
    resultid = []
    for result in resultjson:
        resultid.append(result["id"])
    recipeinfo = []
    for id in resultid:
        recipeinfo.append(form.getRecipeURL(id))
    return render_template('results.html', results=resultjson, recipeinfo=recipeinfo, ingredients=ingredients, form=form, title="Results")

@app.route('/remove/<ingredient>')
def remove(ingredient):
    ingredients = session["ingredients"]
    for i in range(len(ingredients)):
        if ingredient == ingredients[i]:
            print(ingredients[i])
            print(ingredient)
            print(ingredients)
            session['ingredients'].pop(i)
            print(ingredients)
            return redirect(url_for('results', ingredients=ingredients))
    

@app.route('/clear')
def clear():
  session["ingredients"].clear()
  flash("You have cleared your list of ingredients, start a new search by entering ingredients.")
  return redirect(url_for('index'))

@app.route('/profile/<username>')
@login_required
def profile(username):
    user = User.query.filter_by(username=username).first()
    return render_template('profile.html', user=user, title="Profile")


@app.route("/planner")
def planner():
    return render_template("planner.html")


@app.route("/saved")
def saved():
    return render_template("saved.html")


@app.route("/recipe")
def recipe():
    return render_template("recipe.html")


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
    logout_user()
    return redirect(url_for('login'))
