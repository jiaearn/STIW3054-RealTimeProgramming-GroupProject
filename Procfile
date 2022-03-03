release: python manage.py migrate
web: gunicorn PKOB.wsgi
worker: python telegram-bot/bot.py