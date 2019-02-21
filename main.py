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
# FIXME: how do we propagate errors?!
def fetch_provider_data(provider, api_url):
  provider_res = {}
  if (not 'providers' in session) or ('providers' in session and session['providers']==None):
    init_providers()
  if provider=="":
    for provider in session['providers']:
      (feedback, data) = fetch_provider_data_individual(provider['url'], api_url)
      if feedback.success:
        provider_res[provider['url']] = data
  else:
    (feedback, data) = fetch_provider_data_individual(provider, api_url)
    if feedback.success:
      provider_res[provider] = data
  return provider_res

@app.route('/annotations/<regionID>')
def render_annotations_regionid(regionID):
  url = '/experiments/get/ByRegionID/' + regionID
  provider_res = fetch_provider_data("",url)
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
  return jsonify(fetch_provider_data("",url))

@app.route('/region/<chrom>/<start>/<stop>')
def render_segments(chrom,start,stop):
  res = check_start_stop(start,stop)
  if res:
    return render_template("error.html", errmsg="STOP value must be greater than or equal to START value")
  # organize results by provider
  url = "/segments/get/fromSegment/" + chrom + "/" + start + "/" + stop
  provider_res = fetch_provider_data("",url)
  # now after we are done with all providers, display results
  if flask_port != '':
    fh = flask_host+':'+flask_port 
  else:
    fh = flask_host
  return render_template("response_regions_query.html",provider_res=provider_res,chrom=chrom,start=start,stop=stop,flask_host=fh)

@app.route('/api/v1/region/<chrom>/<start>/<stop>')
def render_segments_json(chrom,start,stop):
  url = "/segments/get/fromSegment/" + chrom + "/" + start + "/" + stop
  return jsonify(fetch_provider_data("",url))

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
  return jsonify(fetch_provider_data("",url))

def get_segmentations():
  url = "/segmentations/list/all"
  return fetch_provider_data("",url)

def get_annotations(provider, exp, op1, val1, op2, val2):
  url = "/experiments/get/ByName/" + exp

  if op1=="ge": operator1="gte"
  elif op1=="le": operator1="lte"
  elif op1=="eq": operator1="eq"
  else: operator1=""
  if op2=="ge": operator2="gte"
  elif op2=="le": operator2="lte"
  elif op2=="eq": operator2="eq"
  else: operator2=""

  # FIXME: we should not really have operator1 ever be ""
  # but the episb-provider API will catch this anyways
  url = url + "?op1=" + operator1 + "&val1=" + val1
  if operator2 != "":
    url = url + "&op2=" + operator2 + "&val2=" + val2
  return fetch_provider_data(provider, url)

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

  #for k in request.form.keys():
  #  print("key=%s, value=%s" % (k, request.form.get(k)))

  # get all experiments that have been passed into the form, if any
  exps = [k for k in request.form.keys() if k.startswith("experiment")]
  #print("exps=%s" % exps)

  # if no experiments and operators have been passed - offer up the form to choose from
  if request.form.has_key("selected_provider") and request.form.get("selected_provider") != "- Select a provider -":
    providerUrl = request.form.get("selected_provider")
    if request.form.has_key("segmentation_name") and request.form.get("segmentation_name") != "- Select a segmentation -":
      form_seg_name = request.form.get("segmentation_name")
      #print("form_seg_name=%s" % form_seg_name)
      if form_seg_name.find("!") != -1:
        # here we already chose a segmentation
        # now we need to get the segmentations for the provider
        s = request.form.get("segmentation_name").split('!')
        if len(s)>1:
          providerUrl = s[0]
          segmName = s[1]
      else:
        # get all experiment names with associated min/max ranges
        segmName = form_seg_name
      #print("len(exps)=%d" % len(exps))
      #print("form(experiment0)=%s" % request.form.get("experiment0"))
      if len(exps)==0 or (len(exps)==1 and exps[0]=="experiment0" and request.form.get("experiment0")=="- Select an experiment -"):
        api_url = "/experiments/list/full/BySegmentationName/" + segmName
        #print("privider=%s, segName=%s, apiUrl=%s" % (providerUrl, segmName, api_url))
        (status, exps_by_segmentation) = fetch_provider_data_individual(providerUrl, api_url)
        for e in exps_by_segmentation["result"]:
          minVal = float(e["annotationRangeStart"])
          maxVal = float(e["annotationRangeEnd"])
          midVal = (maxVal - minVal) / 2
          step = (maxVal-minVal) / 100.0
          exp_pass_to_template[e["experimentName"]] = (minVal,midVal,maxVal,step)
      else:
        # the user actually pressed the search button and we have experiments to extract
        # get names of experiments
        exp_names = dict([(e[10:],request.form.get(e).split("!")[2]) for e in exps])
        ops = dict([(op[8:],request.form.get(op)) for op in [k for k in request.form.keys() if k.startswith("operator")]])
        vals = dict([(val[5:],request.form.get(val)) for val in [k for k in request.form.keys() if k.startswith("value")]])
        #print(exp_names)
        #print(ops)
        #print(vals)
        # make a dictonary indexed by an experiment name
        exp_dict = {}
        for k in exp_names:
          exp_name = exp_names[k]
          if exp_dict.has_key(exp_name):
            exp_dict[exp_name].append((ops[k],vals[k]))
          else:
            exp_dict[exp_name] = [(ops[k],vals[k])]
        #print exp_dict
        # try and get data out of these
        # the difficulty is in consolidating multiple operators on the same experiment
        # see if we can consolidate all ops to the smallest number of them
        exp_dict_consolidated = {}
        for k in exp_dict.keys():
          exp_lst = exp_dict[k]
          op_dict={}
          for (op,val) in exp_lst:
            if op_dict.has_key(op):
              op_dict[op].append(val)
            else:
              op_dict[op] = [val]
          
          for op in op_dict.keys():
            if op=="ge":
              if len(op_dict[op])>1:
                op_dict[op] = min(op_dict[op])
              else:
                op_dict[op] = op_dict[op][0]
            elif op=="le":
              if len(op_dict[op])>1:
                op_dict[op] = max(op_dict[op])
              else:
                op_dict[op] = op_dict[op][0]
          exp_dict_consolidated[k] = op_dict
        #print(exp_dict_consolidated)

        json_output = []

        for k in exp_dict_consolidated.keys():
          #print("Experiment=", k)
          exp_consolidated = exp_dict_consolidated[k]
          # do we have an "eq" key?
          # each "eq" query is separate
          if exp_consolidated.has_key("eq"):
            for eq_val in exp_consolidated[op]:
              data = get_annotations(providerUrl, k, "eq", eq_val, "", "")
              json_output.append(("eq", eq_val, eq_val, data[providerUrl]))
              #print("exp=%s, op=EQ, data=%s" % (k, data))
          if exp_consolidated.has_key("ge") and exp_consolidated.has_key("le"):
            data = get_annotations(providerUrl, k, "ge", exp_consolidated["ge"], "le", exp_consolidated["le"])
            json_output.append(("ge/le", exp_consolidated["ge"], exp_consolidated["le"], data[providerUrl]))
            #print("exp=%s, op=GE&&LE, data=%s" % (k, data))
          else:
            if exp_consolidated.has_key("ge"):
              data = get_annotations(providerUrl, k, "ge", exp_consolidated["ge"], "", "")
              json_output.append(("ge", exp_consolidated["ge"], exp_consolidated["ge"], data[providerUrl]))
              #print("exp=%s, op=GE, data=%s" % (k, data))
            elif exp_consolidated.has_key("le"):
              data = get_annotations(providerUrl, k, "le", exp_consolidated["le"], "", "")
              json_output.append(("le", exp_consolidated["le"], exp_consolidated["le"], data[providerUrl]))
              #print("exp=%s, op=LE, data=%s" % (k, data))
            # in a functional language like Scala we would always have an else clause
        # we will just pass in the list of json results
        if len(json_output)>0:
          return render_template("response_segfilter_query.html",
                         json_output=json_output)
        else:
          return render_template("error.html", errmsg="Search returned no results.")

    return render_template("home.html",
                           show_segmentations=True,
                           provider_res=session['providers'],
                           providerUrl=providerUrl,
                           segmName=segmName,
                           expName=expName,
                           segm=segm_by_provider[providerUrl],
                           exps=exp_pass_to_template)
  else:
    return render_template("error.html", errmsg="Search initiated without values. Please return and choose value from form.")
    

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
