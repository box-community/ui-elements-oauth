<img src="images/box-dev-logo-clip.png" 
alt= “box-dev-logo” 
style="margin-left:-10px;"
width=40%;>

# Getting started with Box OAuth 2.0 using Python & Flask
> This is the companion app to illustrate [this medium article](https://medium.com/@barbosa-rmv/getting-started-with-box-oauth-2-0-using-python-flask-77607441170d). Check it out.

## Installation

> Get the code
```bash
git clone git@github.com:barduinor/ui-elements-oauth.git
cd ui-elements-oauth
```

> Set up your virtual environment
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

> Create your application environment
```bash
cp .env.example .env
```

> Generate a secret key for your app
```bash
python -c "import os; print(os.urandom(24).hex())"
```

> Generate a fernet (encryption) key for your app
```bash
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key())"
```

> Edit your .env file and fill in the information
```
# True for development, False for production
DEBUG=True

# Flask ENV
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY='YOUR_SECRET_KEY'
FERNET_KEY='YOU_ENCRYPTION_KEY'

# Box OAuth
CLIENT_ID='YOUR_CLIENT_ID'
CLIENT_SECRET='YOUR_CLIENT_SECRET'
REDIRECT_URI='http://localhost:5000/oauth/callback'
```

> Update your box application settings in the box developer console
> Include your redirect URI in the list of allowed redirect URIs

>http://localhost:5000/oauth/callback
>
>Include your allowed origins in the CORS Domain section

>http://localhost:5000/oauth/callback

> Run your server
```bash
flask run --host localhost --port 5000
```

> Point your browser to the server (e.g http://localhost:5000).
> Inspect your browser console to see the javascript events.
> Server events will be printed on the terminal.