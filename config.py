import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql://kyra:ladies1271@localhost:5433/recipe_spinner'
    SECRET_KEY = 'super-secret'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
