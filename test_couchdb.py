import collections
import mock
import sys
import pytest
import sample_responses

class MockCollectd(mock.MagicMock):

	@staticmethod
	def log(log_str):
		print log_str

	debug = log
	info = log
	warning = log
	error = log

sys.modules['collectd'] = MockCollectd()

def mock_api_call(url, opener=None, auth_header=None):
    if '/_membership' in url:
        return sample_responses.cluster_nodes

    if '/_all_dbs' in url:
        return sample_responses.all_dbs

    if '/test_db' in url:
        return sample_responses.db_stats

    if '/_node/test_node/_stats' in url:
        return sample_responses.node_stats


import couchdb_plugin

ConfigOption = collections.namedtuple('ConfigOption', ('key', 'values'))

fail_mock_config_required_params = mock.Mock()
fail_mock_config_required_params.children = [
	ConfigOption('Host', ('localhost',)),
	ConfigOption('Testing', ('True'))
]

def test_config_fail():
    with pytest.raises(ValueError):
        couchdb_plugin.config(fail_mock_config_required_params)

mock_config = mock.Mock()
mock_config.children = [
    ConfigOption('Host', ('localhost', )),
    ConfigOption('Port', ('5984', )),
    ConfigOption('Interval', ('10', )),
    ConfigOption('Cluster', ('MockCouchDbCluster', )),
    ConfigOption('Username', ('username', )),
    ConfigOption('Password', ('password', )),
    ConfigOption('Testing', ('True', ))
]


def test_default_config():
    module_config = couchdb_plugin.config(mock_config)
    assert module_config['plugin_config']['Host'] == 'localhost'
    assert module_config['plugin_config']['Port'] == '5984'
    assert module_config['interval'] == 10
    assert module_config['username'] == 'username'
    assert module_config['password'] == 'password'
    assert module_config['base_url'] == "http://localhost:5984"
    assert module_config['metrics'] is not None
    assert module_config['metrics']['node_metrics'] is not None
    assert module_config['metrics']['db_metrics'] is not None


mock_config_ssl = mock.Mock()
mock_config_ssl.children = [
    ConfigOption('Host', ('localhost', )),
    ConfigOption('Port', ('5984', )),
    ConfigOption('Interval', ('10', )),
    ConfigOption('Cluster', ('MockCouchDbCluster', )),
    ConfigOption('Username', ('username', )),
    ConfigOption('Password', ('password', )),
    ConfigOption('ssl_keyfile', ('ssl_keyfile', )),
    ConfigOption('ssl_certificate', ('ssl_certificate', )),
    ConfigOption('ssl_ca_certs', ('ssl_ca_certs', )),
    ConfigOption('Testing', ('True', ))
]

def test_config_ssl():
    module_config = couchdb_plugin.config(mock_config_ssl)
    assert module_config['plugin_config']['Host'] == 'localhost'
    assert module_config['plugin_config']['Port'] == '5984'
    assert module_config['interval'] == 10
    assert module_config['username'] == 'username'
    assert module_config['password'] == 'password'
    assert module_config['base_url'] == "https://localhost:5984"
    assert module_config['metrics'] is not None
    assert module_config['metrics']['node_metrics'] is not None
    assert module_config['metrics']['db_metrics'] is not None


@mock.patch('couchdb_plugin._api_call', mock_api_call)
def test_with_default_metrics():
    couchdb_plugin.read(couchdb_plugin.config(mock_config))
