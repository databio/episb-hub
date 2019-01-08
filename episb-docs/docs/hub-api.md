# Hub API reference

We will ultimately build R/python packages to query these servers, so we need a standard API to do so.


<div>
<h2>Overview</h2>
<p class="lead">This describes the resources that make up the EPISB REST API v1. For questions or issues please visit discourse.episb.org.</p>
<p class="lead">General Information</p>
<ol type="i">
  <li><a href="#current-version">Current Version</a></li>
  <li><a href="#schema">Schema</a></li>
  <li><a href="#authentication">Authentication</a></li>
  <li><a href="#http-verbs">HTTP Verbs</a></li>
  <li><a href="#pagination">Pagination</a></li>
  <li><a href="#user-agent-required">User agent required</a></li>
  <li><a href="#rate-limiting">Rate Limiting</a></li>
</ol>

<p class="lead">Endpoints</p>
<ol type="i" start="8">
  <li><a href="#segments">Segments</a></li>
</ol>
</div>

<h3><a name="current-version">Current Version</a></h3>
<p>Currently the EPISB API is at <b>v1</b>. In future releases, all efforts will be made to provide backward compatibility. The deprecation
of previous API versions is unlikely.</p>

<h3><a name="schema">Schema</a></h3>
<p>API access is provided over HTTPS and is accessible from <code>https://episb.org/api/</code>. All data sent to and received from this API is in JSON.</p>

<h3><a name="authentication">Authentication</a></h3>
<p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Proin tincidunt viverra elit vitae mollis. Donec ipsum erat, ornare id suscipit non, lobortis in orci. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Sed ac ante eget purus ultrices cursus. Vivamus pretium erat in mattis feugiat. Nullam accumsan dignissim erat non auctor. Quisque elementum faucibus lacus pretium pretium. Mauris luctus, sapien id suscipit semper, eros ipsum fringilla odio, in scelerisque diam sem a libero. Ut accumsan non nibh in gravida. Pellentesque non ornare ipsum. Sed sed tellus eu arcu consectetur convallis. Aenean feugiat turpis id ex pretium ornare. Morbi sed odio sodales lorem tempus egestas ac at magna. Donec fermentum eu tortor eu dignissim. Curabitur elit diam, tempor in dui non, tincidunt rhoncus risus. Praesent pharetra nisl elit, vitae commodo odio rutrum et. Praesent ac ligula pharetra, mollis lorem tristique, convallis leo. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Nulla facilisi. Cras sit amet euismod elit, et iaculis ipsum. Fusce aliquet mauris sit amet elit euismod, in varius justo suscipit.</p>

<h3><a name="http-verbs">HTTP Verbs</a></h3>
<p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Proin tincidunt viverra elit vitae mollis. Donec ipsum erat, ornare id suscipit non, lobortis in orci. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Sed ac ante eget purus ultrices cursus. Vivamus pretium erat in mattis feugiat. Nullam accumsan dignissim erat non auctor. Quisque elementum faucibus lacus pretium pretium. Mauris luctus, sapien id suscipit semper, eros ipsum fringilla odio, in scelerisque diam sem a libero. Ut accumsan non nibh in gravida. Pellentesque non ornare ipsum. Sed sed tellus eu arcu consectetur convallis. Aenean feugiat turpis id ex pretium ornare. Morbi sed odio sodales lorem tempus egestas ac at magna. Donec fermentum eu tortor eu dignissim. Curabitur elit diam, tempor in dui non, tincidunt rhoncus risus. Praesent pharetra nisl elit, vitae commodo odio rutrum et. Praesent ac ligula pharetra, mollis lorem tristique, convallis leo. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Nulla facilisi. Cras sit amet euismod elit, et iaculis ipsum. Fusce aliquet mauris sit amet elit euismod, in varius justo suscipit.</p>
<p>Section</p>

<h3><a name="pagination">Pagination</a></h3>
<p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Proin tincidunt viverra elit vitae mollis. Donec ipsum erat, ornare id suscipit non, lobortis in orci. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Sed ac ante eget purus ultrices cursus. Vivamus pretium erat in mattis feugiat. Nullam accumsan dignissim erat non auctor. Quisque elementum faucibus lacus pretium pretium. Mauris luctus, sapien id suscipit semper, eros ipsum fringilla odio, in scelerisque diam sem a libero. Ut accumsan non nibh in gravida. Pellentesque non ornare ipsum. Sed sed tellus eu arcu consectetur convallis. Aenean feugiat turpis id ex pretium ornare. Morbi sed odio sodales lorem tempus egestas ac at magna. Donec fermentum eu tortor eu dignissim. Curabitur elit diam, tempor in dui non, tincidunt rhoncus risus. Praesent pharetra nisl elit, vitae commodo odio rutrum et. Praesent ac ligula pharetra, mollis lorem tristique, convallis leo. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Nulla facilisi. Cras sit amet euismod elit, et iaculis ipsum. Fusce aliquet mauris sit amet elit euismod, in varius justo suscipit.</p>
<p>Section</p>

<h3><a name="user-agent-required">User agent required</a></h3>
<p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Proin tincidunt viverra elit vitae mollis. Donec ipsum erat, ornare id suscipit non, lobortis in orci. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Sed ac ante eget purus ultrices cursus. Vivamus pretium erat in mattis feugiat. Nullam accumsan dignissim erat non auctor. Quisque elementum faucibus lacus pretium pretium. Mauris luctus, sapien id suscipit semper, eros ipsum fringilla odio, in scelerisque diam sem a libero. Ut accumsan non nibh in gravida. Pellentesque non ornare ipsum. Sed sed tellus eu arcu consectetur convallis. Aenean feugiat turpis id ex pretium ornare. Morbi sed odio sodales lorem tempus egestas ac at magna. Donec fermentum eu tortor eu dignissim. Curabitur elit diam, tempor in dui non, tincidunt rhoncus risus. Praesent pharetra nisl elit, vitae commodo odio rutrum et. Praesent ac ligula pharetra, mollis lorem tristique, convallis leo. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Nulla facilisi. Cras sit amet euismod elit, et iaculis ipsum. Fusce aliquet mauris sit amet elit euismod, in varius justo suscipit.</p>
<p>Section</p>

<h3><a name="rate-limiting">Rate Limiting</a></h3>
<p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Proin tincidunt viverra elit vitae mollis. Donec ipsum erat, ornare id suscipit non, lobortis in orci. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Sed ac ante eget purus ultrices cursus. Vivamus pretium erat in mattis feugiat. Nullam accumsan dignissim erat non auctor. Quisque elementum faucibus lacus pretium pretium. Mauris luctus, sapien id suscipit semper, eros ipsum fringilla odio, in scelerisque diam sem a libero. Ut accumsan non nibh in gravida. Pellentesque non ornare ipsum. Sed sed tellus eu arcu consectetur convallis. Aenean feugiat turpis id ex pretium ornare. Morbi sed odio sodales lorem tempus egestas ac at magna. Donec fermentum eu tortor eu dignissim. Curabitur elit diam, tempor in dui non, tincidunt rhoncus risus. Praesent pharetra nisl elit, vitae commodo odio rutrum et. Praesent ac ligula pharetra, mollis lorem tristique, convallis leo. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Nulla facilisi. Cras sit amet euismod elit, et iaculis ipsum. Fusce aliquet mauris sit amet elit euismod, in varius justo suscipit.</p>
<p>Section</p>

<hr />

<h3><a name="segments">Segments</a></h3>
<p>This is the segment section. Updated 12/18/2018.</p>

