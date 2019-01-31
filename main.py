import json, urllib2, os, signal, sys, ConfigParser

from flask import Flask, render_template, request, redirect, jsonify, g, session
from flask.json import JSONEncoder

# global variables (yuck!) for init purposes
default_provider=''
flask_host=''
flask_port=''

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

  def __getitem__(self, key):
    return getattr(self, key)

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

class OpFeedback:
  def __init__(self, success, msg):
    self.success = success
    self.msg = msg

def kill_flask():
  os.kill(os.getpid(),signal.SIGKILL)

# check if it is a real provider or just a random URL
# expects a normalized url
def is_real_provider(nurl):
  try:
    urlrq = urllib2.urlopen(nurl+'/provider-interface')
    js = json.load(urlrq)
    # are we clear to process the result list?
    return (js.has_key('error') and js['error']=="None" and js.has_key('result'))
  except Exception as e:
    return False

# normalize the url
def normalize_provider_url(url):
  if url.endswith("/"):
    url = url[:-1]
  if url.endswith("/provider-interface"):
    url = url[:-19]
  if not url.startswith('http://'):
    url = url + 'http://'
  return url

# get normalized provider url from config file or die
def read_config_file():
  global default_provider
  global flask_host
  global flask_port
  config = ConfigParser.SafeConfigParser()
  try:
    config.read('episb-hub.cfg')
    default_provider = normalize_provider_url(config.get('Providers', 'DefaultProvider'))
    if is_real_provider(default_provider):
      print("Read in default_provider=%s from config file." % default_provider)
    else:
      print("Provider in config file does not respond to provider-interface API. Aborting.")
      kill_flask()
    flask_host = config.get('HubServer', 'ServerHost')
    flask_port = config.get('HubServer', 'ServerPort')
  except Exception as e:
    print("No config file found or configuration is bad. Reason: %s. Aborting." % e.message)
    kill_flask()

app = Flask(__name__)
app.secret_key = "episb-secret-key"
app.json_encoder = EpisbJSONEncoder
app.before_first_request(read_config_file)

# check if we need to initialize providers session
def need_to_init_providers():
  if (not 'providers' in session) or session['providers']==None or not provider_in_session_object(default_provider):
    return True
  else:
    False

# see if a url is already in session object
def provider_in_session_object(url):
  # make sure provider url doesn't already exist
  if 'providers' in session:
    for p in session['providers']:
      if p['url'] == url:
        return True
  return False

# initialize providers session entry
# default_provider value should have been initialized on entry to app
def init_providers():
  # add a default provider here
  if need_to_init_providers():
    (res, reason) = add_provider(default_provider)
    if not res:
      print("Error adding provider. Reason: ", reason)
    else:
      print("Provider %s added successfully" % default_provider)

# we are expecting a provider-interface kind of an URL
# returns False if provided was not added, otherwise True
def add_provider(url):
  nurl = normalize_provider_url(url)
  if provider_in_session_object(nurl):
    return (False, "Provider already exists")
  try:
    urlrq = urllib2.urlopen(nurl+'/provider-interface')
    js = json.load(urlrq)
    # are we clear to process the result list?
    if js.has_key('error') and js['error']=="None":
      # yes
      if js.has_key('result'):
        res = js['result'][0]
        # add the provider here
        provider = Provider(nurl,
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
        if 'providers' not in session:
          session['providers'] = [provider]
        else:
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

# fetch data in json for an individual provider
def fetch_provider_data_individual(provider_url, api_url):
  try:
    url_req = urllib2.urlopen(provider_url + api_url)
    json_reply = json.load(url_req)
    return (OpFeedback(True, ""), json_reply)
  except urllib2.URLError as e:
    return (OpFeedback(False, e.reason), "")

# fetch data in json format from all providers in session
# returns dictionary indexed by provider url
def fetch_provider_data(api_url):
  provider_res = {}
  init_providers()
  for provider in session['providers']:
    (feedback, data) = fetch_provider_data_individual(provider['url'], api_url)
    if feedback.success:
      provider_res[provider['url']] = data
  return provider_res

@app.route('/annotations/<regionID>')
def render_annotations_regionid(regionID):
  url = '/experiments/get/ByRegionID/' + regionID
  provider_res = fetch_provider_data(url)
  if flask_port != '':
    fh = flask_host+':'+flask_port 
  else:
    fh = flask_host
  return render_template("response_annotations_query.html",
                         provider_res=provider_res,
                         regionID=regionID,
                         flask_host=fh)

@app.route('/annotations', methods=["GET","POST"])
def render_annotations():
  # try all providers for ID
  regionID = request.form.get("regionID")
  return render_annotations_regionid(regionID)

@app.route('/api/v1/annotations/<regionID>')
def render_annotations_json(regionID):
  url = '/experiments/get/ByRegionID/' + regionID
  return jsonify(fetch_provider_data(url))

@app.route('/region/<chrom>/<start>/<stop>')
def render_segments(chrom,start,stop):
  res = check_start_stop(start,stop)
  if res:
    return render_template("error.html", errmsg="STOP value must be greater than or equal to START value")
  # organize results by provider
  url = "/segments/get/fromSegment/" + chrom + "/" + start + "/" + stop
  provider_res = fetch_provider_data(url)
  # now after we are done with all providers, display results
  if flask_port != '':
    fh = flask_host+':'+flask_port 
  else:
    fh = flask_host
  return render_template("response_regions_query.html",provider_res=provider_res,chrom=chrom,start=start,stop=stop,flask_host=fh)

@app.route('/api/v1/region/<chrom>/<start>/<stop>')
def render_segments_json(chrom,start,stop):
  url = "/segments/get/fromSegment/" + chrom + "/" + start + "/" + stop
  return jsonify(fetch_provider_data(url))

@app.route('/api')
def render_api():
  return render_template("api.html")

@app.route('/about')
def render_about():
  return render_template("about.html")

@app.route('/subscriptions')
def render_subscriptions():
  init_providers()
  return render_template("subscriptions.html", providers=session['providers'])

@app.route("/get", methods=["GET","POST"])
def get_segments():
  chrom = request.form.get("chrom")
  start = request.form.get("start")
  stop = request.form.get("stop")
  res = check_start_stop(start,stop)
  if res:
    return render_template("error.html", errmsg="STOP value must be greater than or equal to START value")
  if flask_port == '':
    url = "http://" + flask_host + "/region/" + chrom + "/" + start + "/" + stop
  else:
    url = "http://" + flask_host + ":" + flask_port + "/region/" + chrom + "/" + start + "/" + stop
  return redirect(url, code=302)

@app.route('/api/v1/segmentations')
def render_segmentations():
  url = "/segmentations/get/all"
  return jsonify(fetch_provider_data(url))

def get_segmentations():
  url = "/segmentations/list/all"
  return fetch_provider_data(url)
  
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
  minVal=0.0
  maxVal=100.0
  midVal=50.0
  step=1.0
  
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
          # get the annotations for this experiment
          api_url = "/experiments/list/full/BySegmentationName/" + segmName
          (status, ei) = fetch_provider_data_individual(providerUrl, api_url)
          for e in ei["result"]:
            if e["experimentName"] == expName:
              minVal = float(e["annotationRangeStart"])
              maxVal = float(e["annotationRangeEnd"])
              midVal = (maxVal - minVal) / 2
              step = (maxVal-minVal) / 100.0
              break
          
    return render_template("home.html",
                             show_segmentations=True,
                             provider_res=session['providers'],
                             providerUrl=providerUrl,
                             segmName=segmName,
                             expName=expName,
                             segm=segm_by_provider[providerUrl],
                             exps=exps,
                             minVal=minVal,
                             maxVal=maxVal,
                             midVal=midVal,
                             step=step)

@app.route('/')
def index():
  init_providers()
  return render_template("home.html", show_regions=True, provider_res=session['providers'])  

def check_start_stop(start,stop):
  if not start:
    start = '0'
  if not stop:
    stop = '0'
  return (int(stop) <= int(start))
