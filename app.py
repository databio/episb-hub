import json, urllib, os
from flask import Flask, render_template, request, redirect, jsonify

app = Flask(__name__)

es_host = '172.17.0.1'

@app.route('/segment/<start>/<stop>')
def render_segments(start,stop):
  url = "http://" + es_host + ":8080/episb-rest-server/get/fromSegment/" + start + "/" + stop
  try:
    url_req = urllib.urlopen(url)
    query_json = json.load(url_req)
    return render_template("response.html", query_json=query_json, start=start, stop=stop)
  except urllib.error.URLError as e:
    print(e.reason)

@app.route('/api/segment/<start>/<stop>')
def render_segments_json(start,stop):
  url = "http://" + es_host + ":8080/episb-rest-server/get/fromSegment/" + start + "/" + stop
  try:
    url_req = urllib.urlopen(url)
    query_json = json.load(url_req)
    return jsonify(query_json)
  except urllib.error.URLError as e:
    print(e.reason)

@app.route("/get", methods=["GET","POST"])
def get_segments():
  start = request.form.get("start")
  stop = request.form.get("stop")
  url = "http://episb.org/segment/" + start + "/" + stop
  return redirect(url, code=302)

@app.route('/')
def index():
  return render_template("home.html")

if __name__ == '__main__':
  app.run(host='0.0.0.0',port=80,debug=True)
