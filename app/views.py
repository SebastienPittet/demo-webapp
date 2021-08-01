from flask import render_template
import socket
import time
from requests import get
from flask import make_response
from functools import wraps, update_wrapper
from datetime import datetime
from app import app


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

def getRandomAdvice():
    try:
        r = get('https://api.adviceslip.com/advice').json()
        randomAdvice = {
            "id" : r[ 'slip'][ 'id'],
            "advice" : r[ 'slip'][ 'advice'],
        }
    except requests.exceptions.TooManyRedirects:
        # Tell the user their URL was bad and try a different one
        randomAdvice = {
            "id" : r[ 'slip'][ 'Error'],
            "advice" : r[ 'slip'][ 'Too many redirects.'],
        }
    except requests.exceptions.Timeout:
        # Maybe set up for a retry, or continue in a retry loop
        randomAdvice = {
            "id" : r[ 'slip'][ 'Error'],
            "advice" : r[ 'slip'][ 'Timeout.'],
        }
    except requests.exceptions.ConnectionError:
        # DNS failure, refused connection, etc
        randomAdvice = {
            "id" : r[ 'slip'][ 'Error'],
            "advice" : r[ 'slip'][ 'Connection Error.'],
        }
    except requests.exceptions.HTTPError:
        # invalid HTTP response
        randomAdvice = {
            "id" : r[ 'slip'][ 'Error'],
            "advice" : r[ 'slip'][ 'Invalid HTTP response.'],
        }
    except requests.exceptions.RequestException as e:
        # catastrophic error. bail.
        randomAdvice = {
            "id" : r[ 'slip'][ 'Error'],
            "advice" : r[ 'slip'][ 'Catastrophic Error.'],
        }

    return randomAdvice

@app.route("/")
@app.route("/index")
@nocache # avoid caching on this view
def main():
    hostname = socket.gethostname()
    ip_addr = get('https://api.ipify.org').text
    time_request = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    server_name = {'hostname': hostname,
              'ipaddr': ip_addr,
              'time_request':time_request}

    return render_template('index.html',
                           title="Demo webapp",
                           server=server_name,
                           advice=getRandomAdvice())


if __name__ == "__main__":
    app.run()
