#!/usr/bin/python

import json
import logging
import sfx_collectd_utilities as sfx
import urllib2
import urllib_ssl_handler
import couchdb_metrics
import base64
import six

try:
    import collectd
except ImportError:
    try:
        import dummy_collectd as collectd
    except ImportError:
        pass

# Plugin name
PLUGIN_NAME = 'couchdb'

# Plugin name is registered in the logger.
log = logging.getLogger(PLUGIN_NAME)

# Global count of the number of instances of the module.
INSTANCE_COUNT = 0


def config(conf):

    """
    The config callback will get configuration details from 'conf' object.
    'conf' object contains information like host, port, username, password etc.
    The read method is registered as read callback along with module_config.
    """
    plugin_config = {}
    username = None
    password = None
    custom_dimensions = {}
    required_keys = ('Host', 'Port', 'Node')
    log_level = logging.INFO
    interval = None
    ssl_keys = {}
    enhanced_metrics = False
    testing = False
    instance_id = "{0}-{1}".format(PLUGIN_NAME, str(INSTANCE_COUNT))

    for kv in conf.children:
        log.debug(str(kv))

        if kv.key == 'LogLevel':
            log_level = sfx.get_log_level_from_config(kv.values[0])
            log.setLevel(log_level)
        elif kv.key == 'Interval':
            interval = float(kv.values[0])
        elif kv.key == 'Dimension':
            if len(kv.values) >= 2:
                key = str(kv.values[0])
                val = str(kv.values[1])
                custom_dimensions[key] = val
            else:
                log.warning("Unable to parse dimensions {}".format(kv.values))
        elif kv.key in required_keys:
            plugin_config[kv.key] = kv.values[0]
        elif kv.key == 'Username' and kv.values[0]:
            username = kv.values[0]
        elif kv.key == 'Password' and kv.values[0]:
            password = kv.values[0]
        elif kv.key == 'Cluster' and kv.values[0]:
            custom_dimensions['Cluster'] = kv.values[0]
        elif kv.key == 'ssl_keyfile' and kv.values[0]:
            ssl_keys['ssl_keyfile'] = kv.values[0]
        elif kv.key == 'ssl_certificate' and kv.values[0]:
            ssl_keys['ssl_certificate'] = kv.values[0]
        elif kv.key == 'ssl_ca_certs' and kv.values[0]:
            ssl_keys['ssl_ca_certs'] = kv.values[0]
        elif kv.key == 'EnhancedMetrics' and kv.values[0]:
            enhanced_metrics = sfx.str_to_bool(kv.values[0])
        elif kv.key == 'Testing' and kv.values[0]:
            testing = sfx.str_to_bool(kv.values[0])

    log.info("Using config settings")
    for key in required_keys:
        val = plugin_config.get(key)
        if val is None:
            raise ValueError("Missing required config setting: {0}".format(key))

    base_url = "http://{0}:{1}".format(plugin_config['Host'], plugin_config['Port'])

    https_handler = None
    if 'ssl_certificate' in ssl_keys and 'ssl_keyfile' in ssl_keys:
        base_url = ('https' + base_url[4:])
        https_handler = urllib_ssl_handler.HTTPSHandler(key_file=ssl_keys['ssl_keyfile'],
                                                        cert_file=ssl_keys['ssl_certificate'],
                                                        ca_certs=ssl_keys['ssl_ca_certs'])

    # Auth handler to handle basic http authentication.
    auth = urllib2.HTTPPasswordMgrWithDefaultRealm()
    auth_header = None
    if username is None and password is None:
        username = password = ''
    else:
        # Some CouchDB databases does not send 'WWW-authenticate' header
        # with the 401 response as it would hinder the futon features.
        # The absence of the above header will break urllib2 library.
        # auth_header is sent as an extra measure to prevent
        # urllib2 from failing.
        auth_header = "Basic {0}".format(base64.b64encode("{0}:{1}".format(username, password)))
    auth.add_password(None, uri=base_url, user=username, passwd=password)
    auth_handler = urllib2.HTTPBasicAuthHandler(auth)
    if https_handler is not None:
        opener = urllib2.build_opener(auth_handler, https_handler)
    else:
        opener = urllib2.build_opener(auth_handler)

    node_metrics = couchdb_metrics.couchdb_metrics['basic_metrics']['node_metrics']

    if enhanced_metrics is True:
        node_metrics.extend(couchdb_metrics.couchdb_metrics['enhanced_metrics']['node_metrics'])

    db_metrics = couchdb_metrics.couchdb_metrics['basic_metrics']['db_metrics']

    metrics = {
        'node_metrics': node_metrics,
        'db_metrics': db_metrics
    }

    instance_id = "{0}-{1}".format(PLUGIN_NAME, str(plugin_config['Node']))
    plugin_instance = '{0}:{1}'.format(plugin_config['Host'], plugin_config['Port'])
    # If there are any custom_dimensions, those will be added to plugin_instance
    if any(custom_dimensions):
        formatted_dim = []
        for k, v in six.iteritems(custom_dimensions):
            formatted_dim.extend(["{0}={1}".format(k, v)])
        dim_str = '({0})'.format(str(formatted_dim).replace('\'', '').
                                 replace(' ', '').replace('\"', '').replace('[', '').
                                 replace(']', ''))
        plugin_instance += dim_str

    module_config = {
        'instance_id': instance_id,
        'log_level': log_level,
        'interval': interval,
        'plugin_instance': plugin_instance,
        'dimensions': custom_dimensions,
        'base_url': base_url,
        'opener': opener,
        'auth_header': auth_header,
        'username': username,
        'password': password,
        'plugin_config': plugin_config,
        'metrics': metrics,
    }

    if testing:
        return module_config

    if interval:
        collectd.register_read(read, interval, data=module_config, name=base_url)
    else:
        collectd.register_read(read, data=module_config, name=base_url)


def _api_call(url, opener=None, auth_header=None):
    """
    _api_call will handle all the calls to the api.
    It adds http basic authentication header if provided.
    The response of the api call is then deserialized from json to dict.
    """
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


def flatten_dict(d, result=None):
    """
    flatten_dict method will take a nested 'dict' as a parameter and
    converts it to a single nested dict by merging all the nested keys
    to a single key with '.' using recursion.
    """
    if result is None:
        result = {}
    for key in d:
        value = d[key]
        if isinstance(value, dict):
            value1 = {}
            for keyIn in value:
                value1[".".join([key, keyIn])] = value[keyIn]
            flatten_dict(value1, result)
        elif isinstance(value, (list, tuple)):
            for indexB, element in enumerate(value):
                if isinstance(element, dict):
                    value1 = {}
                    index = 0
                    for keyIn in element:
                        newkey = ".".join([key, keyIn])
                        value1[newkey] = value[indexB][keyIn]
                        index += 1
                    for keyA in value1:
                        flatten_dict(value1, result)
                elif isinstance(element, list):
                    if len(element) == 2:
                        keyB = ".".join([key, str(element[0])])
                        result[keyB] = element[1]
        else:
            result[key] = value
    return result


def read(conf):

    """
    The read method will get the different nodes present in cluster.
    Gets the stats(metrics)for all the nodes.
    Gets all the dbs present and gets db metrics for them.
    Dispatches all the metrics.
    """
    global log
    log = logging.getLogger(conf['instance_id'])

    log.info("READING CALLBACK")

    base_url = conf['base_url']
    up_url = "{0}/_up".format(base_url)
    try:
        status = (_api_call(up_url))['status']
    except ValueError:
        status = "fail"
    if status == 'ok':
        node_stats = {}
        auth_header = None
        if "auth_header" in conf:
            auth_header = conf['auth_header']
        opener = conf['opener']
        node = conf['plugin_config']['Node']

        metrics = conf['metrics']

        # API call to the stats_url will provide the stats of the node
        stats_url = "{0}/_node/{1}/_stats".format(base_url, str(node))
        node_stats = flatten_dict(_api_call(stats_url, opener=opener, auth_header=auth_header))
        # Node name is added to the dimensions to filter them easily.
        conf['dimensions']['node'] = str(node)
        node_metrics = metrics['node_metrics']

        # To keep track of number of dpm sent.
        dpm_count = 0

        for (k, v) in node_metrics:
            if k not in node_stats:
                continue
            val = node_stats.get(k)
            if val is None:
                val = 0
            # Removing the '.value' string from the key - to make metric name simple
            k = k.replace(".value", "")
            type_instance = "couchdb.{0}".format(str(k))
            sfx.dispatch_values(values=[val],
                                dimensions=conf['dimensions'],
                                plugin=PLUGIN_NAME,
                                plugin_instance=conf['plugin_instance'],
                                type=v,
                                type_instance=type_instance)
            dpm_count = dpm_count + 1
        conf['dimensions'].pop('node', None)

        # API call to the nodes_list_url will provide the list of
        # all the nodes present in the cluster.
        nodes_list_url = "{0}/_membership".format(base_url)
        membership = _api_call(nodes_list_url, opener=opener, auth_header=auth_header)
        up_nodes_list = list(set(membership['cluster_nodes']) & set(membership['all_nodes']))
        up_nodes_list.sort(reverse=True)

        if node == up_nodes_list[0]:
            # API call to the all_dbs_url will provide the list of db's present in CouchDB.
            all_dbs_url = "{0}/_all_dbs".format(base_url)
            dbs_list = _api_call(all_dbs_url, opener=opener, auth_header=auth_header)
            # The stats for each db like disk_size, doc_count etc are collected.
            for db in dbs_list:
                db_url = "{0}/{1}".format(base_url, str(db))
                db_metrics = flatten_dict(_api_call(db_url, opener=opener, auth_header=auth_header))
                for (k, v) in metrics['db_metrics']:
                    if k not in db_metrics:
                        continue
                    val = db_metrics.get(k)
                    if val is None:
                        val = 0
                    type_instance = "couchdb.{0}".format(str(k))
                    conf['dimensions']['db'] = db
                    sfx.dispatch_values(values=[val], dimensions=conf['dimensions'],
                                        plugin=PLUGIN_NAME,
                                        plugin_instance=conf['plugin_instance'],
                                        type=v,
                                        type_instance=type_instance)
                    conf['dimensions'].pop('db', None)
                    dpm_count = dpm_count + 1

        log.info("{0} data points sent for instance : {1}".format(str(dpm_count), conf['instance_id']))
    else:
        log.info("The instance is down")


def init():
    """
    The init() method will be registered as init callback which will log when plugin is initiated.
    """
    collectd.info("Initiating couchdb collectd plugin")


def shutdown():
    """
    The shutdown() method will be registered as shutdown callback which will log when plugin is shutdown.
    """
    collectd.info("Shutting down couchdb collectd plugin")


if __name__ == "__main__":
    pass
else:
    collectd.register_config(config)
    collectd.register_init(init)
    collectd.register_shutdown(shutdown)
