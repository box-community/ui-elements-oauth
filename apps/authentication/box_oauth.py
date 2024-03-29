from datetime import datetime, timedelta
from flask_login import current_user
from apps.authentication.cypto import decrypt_token, encrypt_token
from apps.config import Config
from apps import db
from boxsdk import OAuth2, Client
from apps.authentication.models import Users


class RefreshTokenExpired(Exception):
    """Refresh token expired"""

    def __init__(self, message="Refresh token expired"):
        self.message = message
        super().__init__(self.message)


def get_authorization_url():
    """
    Get the authorization url for the user
    """
    user = Users.query.filter_by(id=current_user.id).first()

    # user must be logged in
    if user == None:
        return None, None

    oauth = OAuth2(
        client_id=Config.CLIENT_ID,
        client_secret=Config.CLIENT_SECRET,
    )

    auth_url, csrf_token = oauth.get_authorization_url(Config.REDIRECT_URI)

    if user:
        user.csrf_token = csrf_token
        db.session.commit()

    return auth_url, csrf_token


def authenticate(code: str) -> None:
    oauth = OAuth2(client_id=Config.CLIENT_ID, client_secret=Config.CLIENT_SECRET, store_tokens=store_tokens)
    oauth.authenticate(code)


def access_token_get() -> str:
    """
    Get the access token for the current user
    """

    user = Users.query.filter_by(id=current_user.id).first()
    if user is None or user.access_token is None or user.refresh_token is None:
        return None

    access_token = decrypt_token(user.access_token)
    refresh_token = decrypt_token(user.refresh_token)
    oauth = OAuth2(
        client_id=Config.CLIENT_ID,
        client_secret=Config.CLIENT_SECRET,
        access_token=access_token,
        refresh_token=refresh_token,
        store_tokens=store_tokens,
    )
    # in some cases the access token may not exist yet
    try:
        user = Users.query.filter_by(id=current_user.id).first()
        return decrypt_token(user.access_token)
    except:
        return None


def store_tokens(access_token: str, refresh_token: str) -> bool:
    """
    Store the access and refresh tokens for the current user
    """

    user = Users.query.filter_by(id=current_user.id).first()

    if user:
        user.access_token = encrypt_token(access_token)
        user.access_token_expires_on = datetime.now() + timedelta(seconds=Config.ACCESS_TOKEN_EXPIRES_IN_SECONDS)

        user.refresh_token = encrypt_token(refresh_token)
        user.refresh_token_expires_on = datetime.now() + timedelta(days=Config.REFRESH_TOKEN_EXPIRES_IN_DAYS)

        db.session.commit()
        return True
    return False


def downscoped_access_token_get() -> str:
    """
    Get the access token for the current user
    """
    user = Users.query.filter_by(id=current_user.id).first()

    if user == None:
        return None

    if user.downscope_token_expires_on and user.downscope_token_expires_on >= datetime.now():
        return decrypt_token(user.downscope_token)

    # get new downscope token
    client = box_client()
    scope = [
        "base_explorer",
        "item_preview",
        "item_download",
        "item_rename",
        "item_share",
        "item_delete",
        "base_picker",
        "item_upload",  # , 'item_share'
        "base_preview",
        "annotation_edit",
        "annotation_view_all",
        "annotation_view_self",  # , 'item_download'
        "base_sidebar",
        "item_comment",  #'item_task', # , 'item_rename', 'item_upload'
        "base_upload",
    ]
    downscoped_token = client.downscope_token(scopes=scope)
    print(f"downscoped_token: {downscoped_token}")
    store_downscope_token(downscoped_token.access_token)
    return downscoped_token.access_token


def store_downscope_token(downscope_token: str) -> None:
    """
    Store the downscope token for the current user
    """

    user = Users.query.filter_by(id=current_user.id).first()
    if user:
        user.downscope_token = encrypt_token(downscope_token)
        user.downscope_token_expires_on = datetime.now() + timedelta(seconds=Config.ACCESS_TOKEN_EXPIRES_IN_SECONDS)
        db.session.commit()


def box_client() -> Client:
    """
    Get the box client for the current user
    """

    user = Users.query.filter_by(id=current_user.id).first()
    if user == None:
        return None

    access_token = decrypt_token(user.access_token)
    refresh_token = decrypt_token(user.refresh_token)

    oauth = OAuth2(
        client_id=Config.CLIENT_ID,
        client_secret=Config.CLIENT_SECRET,
        access_token=access_token,
        refresh_token=refresh_token,
        store_tokens=store_tokens,
    )
    client = Client(oauth)

    if user.refresh_token_expires_on < datetime.now():
        # refresh token expired, need to reauthorize the app
        raise RefreshTokenExpired()

    if user.access_token_expires_on < datetime.now():
        # access token expired, force a refresh of the access token
        client.auth.refresh(access_token)
    return client
