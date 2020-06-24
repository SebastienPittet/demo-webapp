from flask import Flask, render_template
import socket
import time
from requests import get

demowebapp = Flask(__name__)

@demowebapp.route("/")
@demowebapp.route("/index")
def main():
    hostname = socket.gethostname()
    ip_addr = get('https://api.ipify.org').text
    time_request = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    server_name = {'hostname': hostname,
              'ipaddr': ip_addr,
              'time_request':time_request}

    return render_template('index.html',
                           title="Exoscale ping times",
                           server = server_name)


if __name__ == "__main__":
    demowebapp.run()