import json, urllib2, os

from flask import Flask, render_template, request, redirect, jsonify, g, session
from flask.json import JSONEncoder

class Provider:
  def __init__(self, url, name, desc, inst, admin, contact, provider, segs, regions, anns, exps):
    self.url = url
    self.name = name
    self.desc = desc
    self.inst = inst
    self.admin = admin
    self.contact = contact
    self.provider = provider
    self.segs = segs
    self.regions = regions
    self.anns = anns
    self.exps = exps

class EpisbJSONEncoder(JSONEncoder):
  def default(self, obj):
    if isinstance(obj, Provider):
      return {
        'url': obj.url,
        'name': obj.name,
        'desc': obj.desc,
        'inst': obj.inst,
        'admin': obj.admin,
        'contact': obj.contact,
        'provider': obj.provider,
        'segs': obj.segs,
        'regions': obj.regions,
        'anns': obj.anns,
        'exps': obj.exps
      }
    return super(EpisbJSONEncoder, self).default(obj)

app = Flask(__name__)
app.secret_key = "episb-secret-key"
app.json_encoder = EpisbJSONEncoder

# uncomment the following five lines if running on localhost
# with episb-provider running in default setup
#es_host='localhost'
#es_path=''
#es_port='8080'
#flask_host='localhost'
#flask_port='5000'

# production mode settings on "live" episb.org server
#es_host='10.250.124.183'
#es_path='/episb-provider'
#es_port='8080'
flask_host='episb.org'
flask_port=''

# we are expecting a provider-interface kind of an URL
# returns False if provided was not added, otherwise True
def add_provider(url):
  # strip out '/' at the end of the url
  if url.endswith('/'):
    url = url[:-1]
  # and then strip out the provider-interface part
  if url.endswith('provider-interface'):
    url = url[:-19]
  # make sure provider url doesn't already exist
  for p in session['providers']:
    if p['url'] == url:
      return (False, "Provider already exists")
  try:
    urlrq = urllib2.urlopen(url+'/provider-interface')
    js = json.load(urlrq)
    # are we clear to process the result list?
    if js.has_key('error') and js['error']=="None":
      # yes
      if js.has_key('result'):
        res = js['result'][0]
        # add the provider here
        provider = Provider(url,
                            res['providerName'],
                            res['providerDescription'],
                            res['providerInstitution'],
                            res['providerAdmin'],
                            res['providerAdminContact'],
                            res['segmentationsProvided'],
                            res['segmentationsNo'],
                            res['regionsNo'],
                            res['annotationsNo'],
                            res['experimentsNo'])
        session['providers'].append(provider)
        session.modified = True
        return (True,"")
      else:
        # error of some sort, this is not a provider!
        return (False,"Returned JSON has no key \"result\"")
    else:
      if js.has_key('error'):
        return(False, "Error in returned JSON. " + js['error'])
      else:
        return (False, "Returned JSON has no key \"error\"")
  except urllib2.URLError as e:
    return (False, e.reason)
  except KeyError as k:
    return (False, k)

@app.route("/provider", methods=["GET","POST"])
def get_provider_info():
  url = request.form.get("url")
  (res,errmsg) = add_provider(url)
  if res == True:
    # here we recreate the table to display providers
    return render_template("subscriptions.html", providers=session['providers'])
  else:
    return render_template("error.html", errmsg=errmsg)
  
@app.route('/region/<chrom>/<start>/<stop>')
def render_segments(chrom,start,stop):
  return check_start_stop(start,stop)
  # organize results by provider
  provider_res = {}
  url = "/segments/get/fromSegment/" + chrom + "/" + start + "/" + stop
  try:
    for provider in session['providers']:
      url_req = urllib2.urlopen(provider['url'] + url)
      query_json = json.load(url_req)
      provider_res[provider['url']] = query_json
    # now after we are done with all providers, display results
    if flask_port != '':
      fh = flask_host+':'+flask_port 
    else:
      fh = flask_host
    return render_template("response.html",provider_res=provider_res,chrom=chrom,start=start,stop=stop,flask_host=fh)
  except urllib2.URLError as e:
    print(e.reason)

@app.route('/api/v1/region/<chrom>/<start>/<stop>')
def render_segments_json(chrom,start,stop):
  provider_res = {}
  url = "/segments/get/fromSegment/" + chrom + "/" + start + "/" + stop
  try:
    for provider in session['providers']:
      url_req = urllib2.urlopen(provider['url'] + url)
      query_json = json.load(url_req)
      provider_res[provider['url']] = query_json
    return jsonify(provider_res)
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
  if (not 'providers' in session) or ('providers' in session and session['providers']==None):
    return render_template("subscriptions.html", providers=[])
  else:
    return render_template("subscriptions.html", providers=session['providers'])

@app.route("/get", methods=["GET","POST"])
def get_segments():
  chrom = request.form.get("chrom")
  start = request.form.get("start")
  stop = request.form.get("stop")
  return check_start_stop(start,stop)
  if flask_port == '':
    url = "http://" + flask_host + "/region/" + chrom + "/" + start + "/" + stop
  else:
    url = "http://" + flask_host + ":" + flask_port + "/region/" + chrom + "/" + start + "/" + stop
  return redirect(url, code=302)

@app.route('/api/v1/segmentations')
def render_segmentations():
  provider_res = {}
  url = "/segmentations/get/all"
  try:
    for provider in session['providers']:
      url_req = urllib2.urlopen(provider['url'] + url)
      query_json = json.load(url_req)
      provider_res[provider['url']] = query_json
    return jsonify(providerquery_json)
  except urllib2.URLError as e:
    print(e.reason)

def get_segmentations():
  provider_res = {}
  url = "/segmentations/list/all"
  try:
    for provider in session['providers']:
      url_req = urllib2.urlopen(provider['url'] + url)
      segmentation_json = json.load(url_req)
      provider_res[provider['url']] = segmentation_json
    return provider_res
  except urllib2.URLError as e:
    return {}
  
def get_experiments_by_segmentation_name(providerUrl, segName):
  url = "/experiments/list/BySegmentationName/"
  try:
    url_req = urllib2.urlopen(providerUrl + url + segName)
    experiments_list = json.load(url_req)
    return experiments_list
  except urllib2.URLError as e:
    return None

@app.route('/segmentations', methods=["GET","POST"])
def render_segmentation_dropdown():
  segm=[]
  exps=[]
  segmName="- Select a segmentation -"
  expName="- Select an experiment -"
  segm_by_provider = get_segmentations()
  
  if request.form.has_key("selected_provider"):
    providerUrl = request.form.get("selected_provider")
    if request.form.has_key("segmentation_name"):
      # here we already chose a segemntation
      # now we need to get the segmentations for the provider
      s = request.form.get("segmentation_name").split('!')
      if len(s)>1:
        providerUrl = s[0]
        segmName = s[1]
        exps = get_experiments_by_segmentation_name(providerUrl,segmName)
      if request.form.has_key("experiment_name"):
        e = request.form.get("experiment_name").split('!')
        if len(e)>2:
          segmName = e[1]
          expName = e[2]
    return render_template("home.html",
                             show_segmentations=True,
                             provider_res=session['providers'],
                             providerUrl=providerUrl,
                             segmName=segmName,
                             expName=expName,
                             segm=segm_by_provider[providerUrl],
                             exps=exps)

@app.route('/')
def index():
  if (not 'providers' in session) or ('providers' in session and session['providers']==None):
    session['providers'] = []
    session.modified = True
    return render_template("home.html", show_regions=True)
  else:
    return render_template("home.html", show_regions=True, provider_res=session['providers'])  

def check_start_stop(start,stop):
  if not start:
    start = '0'
  if not stop:
    stop = '0'
  if (int(stop) <= int(start)):
    return render_template("error.html", errmsg="STOP value must be greater than or equal to START value")

if __name__=='__main__':
  app.run(host='0.0.0.0',port=8888,debug=True)
