
from flask_login import current_user
from apps.config import Config
from apps import db,login_manager
from boxsdk import OAuth2, Client
from apps.authentication.models import Users


def get_authorization_url():
    """
    Get the authorization url for the user
    """
    user = Users.query.filter_by(id=current_user.id).first()

    oauth = OAuth2(
        client_id=Config.CLIENT_ID,
        client_secret=Config.CLIENT_SECRET,
    )

    auth_url, csrf_token = oauth.get_authorization_url(Config.REDIRECT_URI)

    if user:
        user.csrf_token = csrf_token
        db.session.commit()

    return auth_url, csrf_token

def authenticate(code:str) -> str:
    
    oauth = OAuth2(
        client_id=Config.CLIENT_ID,
        client_secret=Config.CLIENT_SECRET,
        store_tokens=store_tokens
    )
    access_token, refresh_token = oauth.authenticate(code)

    user = Users.query.filter_by(id=current_user.id).first()

    return user.access_token



def access_token_get()->str:
    """
    Get the access token for a user
    """
    
    user = Users.query.filter_by(id=current_user.id).first()

    if user:
        oauth = OAuth2(client_id=Config.CLIENT_ID
                     , client_secret=Config.CLIENT_SECRET
                     , access_token=user.access_token
                     , refresh_token=user.refresh_token
                     , store_tokens=store_tokens
                     )

        client = Client(oauth)

        try:
            client.user().get() # this should force a refresh of the access token
            user = Users.query.filter_by(id=current_user.id).first()
            return user.access_token
        except:
            # if there is an error, we need to re authorize the app
            return None
    return None

def store_tokens(access_token:str, refresh_token:str)->bool:
    """
    Store the access and refresh tokens for a user
    """

    user = Users.query.filter_by(id=current_user.id).first()

    if user:
        user.access_token = access_token
        user.refresh_token = refresh_token
        db.session.commit()
        return True
    return False


def box_client() -> Client:
    """
    Get the client for a user
    """

    user = Users.query.filter_by(id=current_user.id).first()

    if user:
        oauth = OAuth2(client_id=Config.CLIENT_ID
                     , client_secret=Config.CLIENT_SECRET
                     , access_token=user.access_token
                     , refresh_token=user.refresh_token
                     , store_tokens=store_tokens
                     )

        client = Client(oauth)

        try:
            client.user().get() # this should force a refresh of the access token
            return client
        except:
            # if there is an error, we need to re authorize the app
            return None
    return None

