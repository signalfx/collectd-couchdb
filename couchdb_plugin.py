#!/usr/bin/python

import json
import logging
import sfx_collectd_utilities as sfx
import urllib2
# import urllib_ssl_handler     #Disabled temporarily to fix the import issue of urllib_ssl_handler
import couchdb_metrics
import base64

try:
    import collectd
except ImportError:
    try:
        import dummy_collectd as collectd
    except:
        pass

# Plugin name
PLUGIN_NAME = 'couchdb'

# Plugin name is registered in the logger.
log = logging.getLogger(PLUGIN_NAME)

# Global count of the number of instances of the module.
INSTANCE_COUNT = 0

"""
The config callback method will get the configuration details from the 'conf' object.
'conf' object contains information like host, port, username, password and other dimensions.
The method will use the conf details and connect to the database to get the version of the database.
The read method of the corresponding COUCHDB class is registered as read callback. 

"""
def config(conf):

    data = {
        'InstanceID' : "{0}-{1}".format(PLUGIN_NAME,INSTANCE_COUNT),
        'LogLevel' : logging.INFO,
        'Dimensions' : {}
    }
    read_callback = None
    plugin_config = {}
    username = None
    password = None
    required_keys = ('Host', 'Port')
    ssl_keys = {}

    for kv in conf.children:
        log.debug(str(kv))

        if kv.key == 'LogLevel':
            data['LogLevel'] = sfx.get_log_level_from_config(kv.values[0])
            log.setLevel(data['LogLevel'])
        elif kv.key == 'Interval':
            data[kv.key] =  float(kv.values[0])
        elif kv.key == 'Dimension':
            if len(kv.values) >=2:
                key = str(kv.values[0])
                val = str(kv.values[1])
                data['Dimensions'][key] = val
            else:
                log.warning("Unable to parse dimensions {}".format(kv.values))
        elif kv.key in required_keys:
            plugin_config[kv.key] = kv.values[0]
        elif kv.key == 'Username':
            log.info(kv.values[0])
            username = kv.values[0]
        elif kv.key == 'Password':
            log.info(kv.key)
            password = kv.values[0]
        elif kv.key == 'ssl_keyfile':
            ssl_keys['ssl_keyfile'] = kv.values[0]
        elif kv.key == 'ssl_certificate':
            ssl_keys['ssl_certificate'] = kv.values[0]
        elif kv.key == 'ssl_ca_certs':
            ssl_keys['ssl_ca_certs'] = kv.values[0]

    log.info("Using config settings")
    for key in required_keys:
        val = plugin_config.get(key)
        if val is None:
            raise ValueError("Missing required config setting: {0}".format(key))


    base_url = "http://{0}:{1}".format(plugin_config['Host'], plugin_config['Port'])

    # Https handler is created if the database is configured and the configuration is provided in conf file.
    # It is temporarily disabled.
    https_handler = None
    if 'ssl_certificate' in ssl_keys and 'ssl_keyfile' in ssl_keys:
        base_url = ('https'+base_url[4:])
        # https_handler = urllib_ssl_handler.HTTPSHandler(key_file=ssl_keys['ssl_keyfile'],
        #             cert_file=ssl_keys['ssl_certificate'], ca_certs=ssl_keys['ssl_ca_certs'])

    # Auth handler to handle basic http authentication.
    auth = urllib2.HTTPPasswordMgrWithDefaultRealm()
    if username is None and password is None:
        username = password = ''
    else:
        # Some CouchDB databases does not send 'WWW-authenticate' header with the 401 response as it would hinder the futon features.
        # The absence of the above header will break urllib2 library.
        # auth_header is sent as an extra measure to prevent the urllib2 from failing.
        auth_header = "Basic {0}".format(base64.b64encode("{0}:{1}".format(username, password)))
        data['auth_header'] = auth_header
    auth.add_password(None, uri=base_url, user=username, passwd=password)
    auth_handler = urllib2.HTTPBasicAuthHandler(auth)
    if https_handler is not None:
        # opener = urllib2.build_opener(auth_handler, https_handler)
        pass
    else:
        opener = urllib2.build_opener(auth_handler)
    data['base_url'] = base_url
    data['opener'] = opener
    data['username'] = username
    data['password'] = password
    data['plugin_config'] = plugin_config
    
    # The api call to base_url will provide the information of the database, which can be used to determine its version.
    db_details = _api_call(base_url)
    db_version = str(db_details['version'])
    couchdb = None
    metrics = {}
   
    # The read call back is registered depending on the version of the database.
    if db_version.startswith('1.'):
        couchdb = CouchDB1()
        metrics = couchdb_metrics.couchdb_metrics['couchdb1']
    elif db_version.startswith('2.'):
        couchdb = CouchDB2()
        # Currently only basic metrics are sent. Other advanced metrics' support will enabled soon.
        node_metrics = couchdb_metrics.couchdb_metrics['couchdb2']['couchdb']
        node_metrics.extend(couchdb_metrics.couchdb_metrics['couchdb2']['mem3'])
        metrics['node_metrics'] = node_metrics
        metrics['db_metrics'] = couchdb_metrics.couchdb_metrics['couchdb2']['db_metrics']
    else:
        raise ValueError("Unknown version {0}".format(db_version))

    read_callback = couchdb.read
    data['metrics'] = metrics

    if 'Interval' in data:
        collectd.register_read(read_callback, data['Interval'], data=data, name=data['InstanceID'])
    else:
        collectd.register_read(read_callback, data=data, name=data['InstanceID'])

    global INSTANCE_COUNT
    INSTANCE_COUNT = INSTANCE_COUNT + 1


"""
_api_call will handle all the calls to the api.
It adds http basic authentication header if provided.
The response of the api call is then deserialized from json to dict.
"""
def _api_call(url, opener=None, auth_header=None):
    resp = None
    try:
        if opener is not None:
            urllib2.install_opener(opener)
        req = urllib2.Request(url)
        if auth_header is not None:
            req.add_header('Authorization', str(auth_header))
        resp = urllib2.urlopen(req)
    except (urllib2.HTTPError, urllib2.URLError) as e:
        log.warning("Error making API call ({0}) {1}".format(e, url))
        return None
    try:
        return json.load(resp)
    except ValueError as e:
        log.warning("Erro parsing JSON for API call ({0}) {1}".format(e, url))
        return None

"""
flattenDict method will take a nested 'dict' as a parameter and 
converts it to a single nested dict by merging all the nested keys to a single key with '.' using recursion.
"""
def flattenDict(d, result=None):
    if result is None:
        result = {}
    for key in d:
        value = d[key]
        if isinstance(value, dict):
            value1 = {}
            for keyIn in value:
                value1[".".join([key,keyIn])]=value[keyIn]
            flattenDict(value1, result)
        elif isinstance(value, (list, tuple)):
            for indexB, element in enumerate(value):
                if isinstance(element, dict):
                    value1 = {}
                    index = 0
                    for keyIn in element:
                        newkey = ".".join([key,keyIn])
                        value1[".".join([key,keyIn])]=value[indexB][keyIn]
                        index += 1
                    for keyA in value1:
                        flattenDict(value1, result)
                elif isinstance(element, list):
                    if len(element)==2:
                        keyB = ".".join([key, str(element[0])])
                        result[keyB] = element[1]   
        else:
            result[key]=value
    return result


"""
CouchDB1 class has read method required to read the stats of the v1.* of CouchDB.
"""
class CouchDB1:

    def read(self, data):
        global log
        log = logging.getLogger(data['InstanceID'])

        log.info("READING CALLBACK")

        opener = data['opener']
        base_url = data['base_url']
        auth_header = None
        if "auth_header" in data:
            auth_header = data['auth_header']

        stats_url = "{0}/_stats".format(base_url)
        stats = _api_call(stats_url, opener, auth_header)
        stats = flattenDict(stats)
        metrics = data['metrics']
        dpm_count = 0
        for(k,v) in metrics:
            dpm_count = dpm_count+1
            val = stats.get("{0}.current".format(k))
            if val is None:
                val = 0
            type_instance = 'couchdb.'+str(k)

            sfx.dispatch_values(values=[val], dimensions=data['Dimensions'], plugin=PLUGIN_NAME,
                                plugin_instance=data['InstanceID'], type=v, type_instance=type_instance,
                                host=data['plugin_config']['Host'])
        log.info("Number of data points sent : "+str(dpm_count))



"""
CouchDB2 class has read method required to read the stats of the v2.* of CouchDB1.
"""
class CouchDB2:

    """
    The read method will get the stats(metrics) of all the nodes present in the cluster and dispatches values to the collectd.
    """
    def read(self, data):
        global log
        log = logging.getLogger(data['InstanceID'])

        log.info("READING CALLBACK")
        
        node_stats = {}
        auth_header = None
        if "auth_header" in data:
            auth_header = data['auth_header']
        opener = data['opener']
        base_url = data['base_url']

        # API call to the nodes_list_url will provide the list of all the nodes present in the cluster.
        nodes_list_url = "{0}/_membership".format(base_url)
        cluster_nodes_list = (_api_call(nodes_list_url, opener=opener, auth_header=auth_header))['cluster_nodes']
        metrics = data['metrics']
        num_nodes = len(cluster_nodes_list)
        log.info("Found {0} nodes for instance {1}".format(str(num_nodes), data['InstanceID']))
        
        # The dpm_count will keep track of the number of data points sent in one read cycle.
        dpm_count = 0
        # Stats for all the nodes are collected and dispatched.
        for node in cluster_nodes_list:
            # API call to the stats_url will provide the stats of the particular node present in the cluster
            stats_url = "{0}/_node/{1}/_stats".format(base_url, str(node))
            node_stats = _api_call(stats_url, opener=opener,auth_header=auth_header)
            node_stats = flattenDict(node_stats)
            # Node name is added to the dimensions to filter them easily.
            data['Dimensions']['node'] = str(node)
            node_metrics = metrics['node_metrics']
            for (k,v) in node_metrics:
                if k not in node_stats:
                    continue
                val = node_stats.get(k)
                if val is None:
                    val = 0
                # Removing the '.value' string from the key - to make metric name simple
                k = k.replace(".value", "")
                type_instance = "couchdb.{0}".format(str(k))
                sfx.dispatch_values(values=[val], dimensions=data['Dimensions'], plugin=PLUGIN_NAME,
                                    plugin_instance=data['InstanceID'], type=v, type_instance=type_instance,
                                    host=data['plugin_config']['Host'])
                dpm_count = dpm_count + 1
            data['Dimensions'].pop('node', None)
         
         # API call to the all_dbs_url will provide the list of db's present in CouchDB.   
        all_dbs_url = "{0}/_all_dbs".format(base_url)
        dbs_list = _api_call(all_dbs_url, opener=opener, auth_header=auth_header)
        # The stats for each db like disk_size, doc_count etc are collected.
        for db in dbs_list:
            db_url = "{0}/{1}".format(base_url, str(db))
            db_metrics = _api_call(db_url, opener=opener, auth_header=auth_header)
            db_metrics = flattenDict(db_metrics)
            for (k,v) in metrics['db_metrics']:
                if k not in db_metrics:
                    continue
                val = db_metrics.get(k)
                if val is None:
                    val = 0
                type_instance = "couchdb.{0}".format(str(k))
                data['Dimensions']['db'] = db
                sfx.dispatch_values(values=[val], dimensions=data['Dimensions'], plugin=PLUGIN_NAME,
                                plugin_instance=data['InstanceID'], type=v, type_instance=type_instance,
                                host=data['plugin_config']['Host'])
                data['Dimensions'].pop('db', None)
                dpm_count = dpm_count + 1        

        log.info("{0} data points sent".format(str(dpm_count)))



"""
The init() method will be registered as init callback which will log when plugin is initiated.
"""
def init():
    collectd.info("Initiating couchdb collectd plugin")

"""
The shutdown() method will be registered as shutdown callback which will log when plugin is shutdown.
"""
def shutdown():
    collectd.info("Shutting down couchdb collectd plugin")


if __name__ == "__main__":
    pass
else:
    collectd.register_config(config)
    collectd.register_init(init)
    collectd.register_shutdown(shutdown)

