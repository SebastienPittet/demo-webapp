# gunicorn -w 1 -b 0.0.0.0:8000 wsgi:demowebapp

from views import demowebapp

if __name__ == "__main__":
    demowebapp.run()