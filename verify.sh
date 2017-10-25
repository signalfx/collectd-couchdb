#!/bin/bash
flake8 --ignore E501 couchdb_plugin.py couchdb_metrics.py sfx_collectd_utilities.py urllib_ssl_handler.py

if [ "$?" -ne 0 ]; then
	exit 1;
fi

py.test test_couchdb.py