from flask import Flask, render_template
import socket
import time

demowebapp = Flask(__name__)

@demowebapp.route("/")
@demowebapp.route("/index")
def main():
    hostname = socket.gethostname()
    ip_addr = socket.gethostbyname(hostname)
    time_request = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    server = {'hostname': hostname,
              'ipaddr': ip_addr,
              'time_request':time_request}

    return render_template('index.html',
                           title="Exoscale powered by Lenovo",
                           server = server)

if __name__ == "__main__":
    demowebapp.run()