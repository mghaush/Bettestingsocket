web: gunicorn app:app
heroku ps:scale web=1
python -m websockets wss://bettingsocket-d89de658d946.herokuapp.com/
