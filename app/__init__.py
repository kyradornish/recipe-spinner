from flask import Flask
from flask_bootstrap import Bootstrap
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'

from app import routes, models

bootstrap = Bootstrap(app)

# if __name__ == '__main__':
#     app.run(debug=True, host="0.0.0.0", port=8082)

# Connecting to API SDK
# from rapidconnect import RapidConnect
# import unirest
# rapid = RapidConnect('recipe-spinner_5ac3931ee4b0a62b51d0cfe3', '175250b7-3cd5-4660-8b45-58e0cc706f32')

#TO TEST API - CAN"T FIGURE OUT YET
# rapid.call('NasaAPI', 'getPictureOfTheDay', {'{}'})


# API
# from requests_html import HTMLSession
# session = HTMLSession()

# response = session.get("https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/recipes/findByIngredients?number=5&ingredients=apples%2Cflour%2Csugar&ranking=1",
#                        headers={
#                            "X-Mashape-Key": "OcWXtWKiwJmsh9je6Ev8yYDRO2Bpp1bHFrqjsnMcAjT0dmqtZg",
#                            "X-Mashape-Host": "spoonacular-recipe-food-nutrition-v1.p.mashape.com"
#                        }
#                        )
