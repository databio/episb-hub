import json, urllib2, os
from flask import Flask, render_template, request, redirect, jsonify
app = Flask(__name__)

# uncomment the following five lines if running on localhost
# with episb-provider running in default setup
#es_host=127.0.0.1'
#es_path=''
#es_port='8080'
#flask_host='127.0.0.1'
#flask_port='5000'

# production mode settings on "live" episb.org server
es_host='10.250.124.183'
es_path='/episb-provider'
es_port='8080'
flask_host='episb.org'
flask_port=''

@app.route('/region/<chrom>/<start>/<stop>')
def render_segments(chrom,start,stop):
  check_start_stop(start,stop)
  url = "http://" + es_host + ":" + es_port + es_path + "/segments/get/fromSegment/" + chrom + "/" + start + "/" + stop
  try:
    url_req = urllib2.urlopen(url)
    query_json = json.load(url_req)
    return render_template("response.html", query_json=query_json, chrom=chrom,  start=start, stop=stop)
  except urllib2.URLError as e:
    print(e.reason)

@app.route('/api/v1/region/<chrom>/<start>/<stop>')
def render_segments_json(chrom,start,stop):
  url = "http://" + es_host + ":" + es_port + es_path + "/segments/get/fromSegment/" + chrom + "/" + start + "/" + stop
  try:
    url_req = urllib2.urlopen(url)
    query_json = json.load(url_req)
    return jsonify(query_json)
  except urllib2.URLError as e:
    print(e.reason)

@app.route('/api/v1/segmentations')
def render_segmentations():
  url = "http://" + es_host + ":" + es_port + es_path + "/segmentations/get/all"
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
  chrom = request.form.get("chrom")
  start = request.form.get("start")
  stop = request.form.get("stop")
  check_start_stop(start,stop)
  if flask_port == '':
    url = "http://" + flask_host + "/region/" + chrom + "/" + start + "/" + stop
  else:
    url = "http://" + flask_host + ":" + flask_port + "/region/" + chrom + "/" + start + "/" + stop
  return redirect(url, code=302)

@app.route('/')
def index():
  url = "http://" + es_host + ":" + es_port + es_path + "/segmentations/get/all"
  try:
    url_req = urllib2.urlopen(url)
    segmentation_json = json.load(url_req)
    return render_template("home.html", segmentation_json=segmentation_json)
  except urllib2.URLError as e:
    print(e.reason)

def check_start_stop(start,stop):
  if not start:
    start = '0'
  if not stop:
    stop = '0'
  if (stop <= start):
    return render_template("error.html", errmsg="STOP value must be greater than or equal to START value")

if __name__ == '__main__':
  app.run(host='0.0.0.0',port=8888,debug=True)
