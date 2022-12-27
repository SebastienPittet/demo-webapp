from flask import render_template
import socket
import time
import math                   # used in heavy_computation
from random import randrange  # used in heavy_computation
from requests import get
from flask import make_response
from functools import wraps, update_wrapper
from datetime import datetime
from app import app

# Metrics in prometheus format
from prometheus_client import make_wsgi_app
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.serving import run_simple
from flask_prometheus_metrics import register_metrics


# Add OpenSearch handler to python logger
import logging
from opensearch_logger import OpenSearchHandler

handler = OpenSearchHandler(
    index_name="demo-webapp",
    hosts=["https://opensearch.pittet.org:9200"],
    http_auth=("admin", "somepassword"),
    http_compress=True,
    use_ssl=True,
    verify_certs=False,
    ssl_assert_hostname=False,
    ssl_show_warn=False,
)


APP_TITLE = "Demo Webapp"

# Tuned in for returning a response in 1 to 5 seconds in average on Exoscale
seed = 50_000_000

def nocache(view): # avoid caching
    @wraps(view)
    def no_cache(*args, **kwargs):
        response = make_response(view(*args, **kwargs))
        response.headers['Last-Modified'] = datetime.now()
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '-1'
        return response
    return update_wrapper(no_cache, view)


def heavy_computation():
    """
    Performs an unreasonably long CPU-bound calculation,
    and returns the result and the time it took.
    """
    start = time.time()
    x = 0.0001
    for _ in range(0, randrange(seed)):
        x += math.sqrt(x)
    end = time.time()
    elapsed_time = f"{end - start:.2f}"
    logger.info(f"Database operation took {elapsed_time} seconds")
    return x, elapsed_time

def getRandomAdvice():
    try:
        r = get('https://api.adviceslip.com/advice').json()
        randomAdvice = {
            "id" : r['slip']['id'],
            "advice" : r['slip']['advice'],
        }
    except requests.exceptions.TooManyRedirects:
        # Tell the user their URL was bad and try a different one
        randomAdvice = {
            "id" : r['slip']['Error'],
            "advice" : r['slip']['Too many redirects.'],
        }
    except requests.exceptions.Timeout:
        # Maybe set up for a retry, or continue in a retry loop
        randomAdvice = {
            "id" : r['slip']['Error'],
            "advice" : r['slip']['Timeout.'],
        }
    except requests.exceptions.ConnectionError:
        # DNS failure, refused connection, etc
        randomAdvice = {
            "id" : r['slip']['Error'],
            "advice" : r['slip']['Connection Error.'],
        }
    except requests.exceptions.HTTPError:
        # invalid HTTP response
        randomAdvice = {
            "id" : r['slip']['Error'],
            "advice" : r['slip']['Invalid HTTP response.'],
        }
    except requests.exceptions.RequestException as e:
        # catastrophic error. bail.
        randomAdvice = {
            "id" : r['slip']['Error'],
            "advice" : r['slip']['Catastrophic Error.'],
        }

    return randomAdvice

@app.route("/")
@app.route("/index")
@nocache  # avoid caching on this view
def main():
    hostname = socket.gethostname()
    ip_addr = get('https://api.ipify.org').text
    time_request = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    server_name = {'hostname': hostname,
              'ipaddr': ip_addr,
              'time_request':time_request}

    return render_template('index.html',
                           title=APP_TITLE + " - Home",
                           server=server_name)


@app.route("/slow")
@nocache  # avoid caching on this view
def slow():

    number, seconds = heavy_computation()

    return render_template('slow.html',
                           title=APP_TITLE + " - Slow",
                           number=number,
                           duration=seconds)


@app.route("/api-proxy")
@nocache  # avoid caching on this view
def apiproxy():
    return render_template('api-proxy.html',
                           title=APP_TITLE + " - API Proxy",
                           advice=getRandomAdvice())


@app.route("/database")
@nocache  # avoid caching on this view
def database():
    # open database, create schema if not exist
    # load data from ..?
    # create some statistics

    return render_template('database.html',
                           title=APP_TITLE + " - Database",)


@app.route("/pingtimes")
@nocache  # avoid caching on this view
def pingtimes():
    return render_template('pingtimes.html',
                           title=APP_TITLE + " - Pingtimes",)


@app.route("/links")
@nocache  # avoid caching on this view
def links():
    return render_template('links.html',
                           title=APP_TITLE + " - Links",)


# Testing to check if it works
@app.route('/test')
def test():
    return "OK!"


if __name__ == "__main__":
    app.run()

# Log
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(handler)

# provide app's version and deploy environment/config name to set a gauge metric
register_metrics(app, app_version="v0.1.2", app_config="staging")

# Plug metrics WSGI app to your main app with dispatcher
dispatcher = DispatcherMiddleware(app.wsgi_app, {"/metrics": make_wsgi_app()})

run_simple(hostname="localhost", port=5000, application=dispatcher)
