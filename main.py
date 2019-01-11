import json, urllib2, os
from flask import Flask, render_template, request, redirect, jsonify
app = Flask(__name__)

es_host = '10.250.124.183'

@app.route('/region/<start>/<stop>')
def render_segments(start,stop):
  check_start_stop(start,stop)
  url = "http://" + es_host + ":8080/episb-provider/get/fromSegment/" + start + "/" + stop
  try:
    url_req = urllib2.urlopen(url)
    query_json = json.load(url_req)
    return render_template("response.html", query_json=query_json, start=start, stop=stop)
  except urllib2.URLError as e:
    print(e.reason)

@app.route('/api/v1/region/<start>/<stop>')
def render_segments_json(start,stop):
  url = "http://" + es_host + ":8080/episb-provider/get/fromSegment/" + start + "/" + stop
  try:
    url_req = urllib2.urlopen(url)
    query_json = json.load(url_req)
    return jsonify(query_json)
  except urllib2.URLError as e:
    print(e.reason)

@app.route('/api')
def render_api():
  return render_template("api.html")

@app.route('/about')
def render_about():
  return render_template("about.html")

@app.route('/subscriptions')
def render_subscriptions():
  return render_template("subscriptions.html")

@app.route("/get", methods=["GET","POST"])
def get_segments():
  start = request.form.get("start")
  stop = request.form.get("stop")
  check_start_stop(start,stop)
  url = "http://episb.org/region/" + start + "/" + stop
  return redirect(url, code=302)

@app.route('/')
def index():
  return render_template("home.html")

def check_start_stop(start,stop):
  if not start:
    start = '0'
  if not stop:
    stop = '0'
  if (stop <= start):
    return render_template("error.html", errmsg="STOP value must be greater than or equal to START value")

if __name__ == '__main__':
  app.run(host='0.0.0.0',port=8888,debug=True)
