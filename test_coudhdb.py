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

def mock_api_call(data, url):
	parsed_url = url.split('/')


sys.modules['collectd'] = MockCollectd()

import couchdb_plugin

ConfigOption = collections.namedtuple('ConfigOption', ('key', 'values'))

fail_mock_config_required_params = mock.Mock()
fail_mock_config_required_params.children = [
	ConfigOption('Host', ('localhost',)),
	ConfigOption('Testing', ('True'))
]

