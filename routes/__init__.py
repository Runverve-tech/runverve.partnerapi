from flask import Blueprint
from . import auth, user, activity, preferences, supplements, injuries, hydration, geocoding

def init_app(app):
    auth.init_app(app)
    user.init_app(app)
    activity.init_app(app)
    preferences.init_app(app)
    supplements.init_app(app)
    injuries.init_app(app)
    hydration.init_app(app)
    geocoding.init_app(app)