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

def init_providers():
  add_provider("http://provider.episb.org/episb-provider/")

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
  if 'providers' in session:
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
  if (not 'providers' in session) or ('providers' in session and session['providers']==None):
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
  if (not 'providers' in session) or ('providers' in session and session['providers']==None):
    return render_template("subscriptions.html", providers=[])
  else:
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
  
@app.route('/segmentations', methods=["GET","POST"])
def render_segmentation_dropdown():
  segm=[]
  # a list of quintuples describing each experiment (name, min, mid, max, step)
  # passed to form for better control/checking when selecting multiple experiments
  # and filters on such experiments
  exp_pass_to_template = {}
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
        # get all experiment names with associated min/max ranges
        api_url = "/experiments/list/full/BySegmentationName/" + segmName
        (status, exps_by_segmentation) = fetch_provider_data_individual(providerUrl, api_url)
        for e in exps_by_segmentation["result"]:
          minVal = float(e["annotationRangeStart"])
          maxVal = float(e["annotationRangeEnd"])
          midVal = (maxVal - minVal) / 2
          step = (maxVal-minVal) / 100.0
          exp_pass_to_template[e["experimentName"]] = (minVal,midVal,maxVal,step)
    return render_template("home.html",
                             show_segmentations=True,
                             provider_res=session['providers'],
                             providerUrl=providerUrl,
                             segmName=segmName,
                             expName=expName,
                             segm=segm_by_provider[providerUrl],
                             exps=exp_pass_to_template)

@app.route('/')
def index():
  if (not 'providers' in session) or ('providers' in session and session['providers']==None):
    init_providers()
  return render_template("home.html",
                         show_regions=True,
                         provider_res=session['providers'],
                         providerUrl="- Select a provider -",
                         segmName="- Select a segmentation -",
                         expName="- Select an experiment -",
                         segm="",
                         exps={})

def check_start_stop(start,stop):
  if not start:
    start = '0'
  if not stop:
    stop = '0'
  return (int(stop) <= int(start))

if __name__=='__main__':
  app.run(host='0.0.0.0',port=8888,debug=True)
