import datetime
import logging
import os
import sys

import requests
from flask import Flask, abort, redirect, render_template, request, url_for
from prometheus_flask_exporter import PrometheusMetrics
from werkzeug.exceptions import Aborter, HTTPException, default_exceptions
from werkzeug.http import HTTP_STATUS_CODES

now = datetime.datetime.now()
timeString = now.strftime("%Y-%m-%d %H:%M:%S")

backend_url = os.environ.get("BACKEND_URL")
backend_port = os.environ.get("BACKEND_PORT")
backend = f"http://{backend_url}:{backend_port}"

# test

# backend = "http://192.168.1.61:8080"


class BadRequest(HTTPException):
    code = 444


default_exceptions[444] = BadRequest
HTTP_STATUS_CODES[444] = "You got noticed!"
abort = Aborter()

app = Flask(__name__)
metrics = PrometheusMetrics(app)


@app.before_request
def block_method():
    ip = request.remote_addr
    res = requests.post(f"{backend}/getblack")
    logging.info("list of blocked ip addresses: " + res.text)
    if ip in res.text and request.path != "/unlock":
        abort(403)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if "blacklisted" in request.form:
            return redirect(url_for("blacklisted"))
        if "metrics" in request.form:
            return redirect("/metrics")
        if "healthz" in request.form:
            return redirect(url_for("healthz"))
        if "debug" in request.form:
            return redirect(url_for("debug"))
        else:
            pass
    elif request.method == "GET":
        return render_template("index.html")


@app.route("/blacklisted")
def blacklisted():
    dictToSend = {"ip": request.remote_addr, "date": timeString, "path": request.url}
    res = requests.post(f"{backend}/addtoblack", json=dictToSend)
    logging.info("response from server: " + res.text)
    abort(444)


@app.route("/debug")
def debug():
    dictToSend = {"ip": request.remote_addr, "date": timeString, "path": request.url}
    res = requests.post(f"{backend}/debug", json=dictToSend)
    logging.info("response from server: " + res.text)
    return res.json()


@app.errorhandler(444)
def abort_code(e):
    return e, 444


@app.route("/healthz")
def healthz():
    status = None
    try:
        r = requests.get(backend)
    except requests.exceptions.ConnectionError:
        status = "Network Error while connecting to {}".format(backend)
    if r and str(r.status_code)[0] not in ("2", "3"):
        status = "URL {} returned {}".format(backend, requests.status_code)
    else:
        status = "Connection established to {}".format(backend)
    return "OK", status


@app.route("/unlock", methods=["GET", "POST"])
def unlock():
    if request.method == "POST":
        if "yes" in request.form:
            dictToSend = {"ip": request.remote_addr}
            res = requests.post(f"{backend}/unlock", json=dictToSend)
            logging.info("response from server: " + res.text)
            return redirect(url_for("index"))
        elif "no" in request.form:
            return redirect(url_for("index"))
        else:
            pass
    elif request.method == "GET":
        return render_template("unlock.html")


if __name__ == "__main__":
    FORMAT = "%(asctime)-15s %(name)s: %(message)s"
    logging.basicConfig(format=FORMAT, stream=sys.stdout, level=logging.INFO)
    app.run(debug=False, port=8081, host="0.0.0.0")
