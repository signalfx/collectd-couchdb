# collectd couchdb Plugin

An couchdb [collectd](http://www.collectd.org/) plugin which users can use to send metrics from couchdb instances to SignalFx

## Installation

* Checkout this repository somewhere on your system accessible by collectd. The suggested location is `/usr/share/collectd/`
* Install the Python requirements with sudo ```pip install -r requirements.txt```
* Configure the plugin (see below)
* Restart collectd

## Requirements

* collectd 4.9 or later (for the Python plugin)
* Python 2.6 or later
* couchdb 2.0.0 or later

## Configuration
The following are required configuration keys:

* Host - Required. Hostname or IP address of the CouchDB member
* Port - Required. The port of the CouchDB member
* Node - Required. The name of the node in the cluster

Optional configurations keys include:

* Interval - Interval between metric calls. Default is 10s
* Username - Username required for authentication of CouchDB.
* Pasword - Password required for authentication of CouchDB.
* Node - Name of the CouchDB node in the cluster.
* LogLevel - Specifies the level of logging. 
* Cluster - Name of the Cluster.
* EnhancedMetrics - Flag to enable enhanced metrics. Default is False.
* IncludeMetric - Metrics emitted by `_stats` endpoint can be included individually.
* ExcludeMetric - Metrics emitted by `_stats` endpoint can be excluded individually.
* Dimension - Add extra dimensions to your metrics

Specify path to keyfile and certificate if certificate based authentication of clients is enabled on your couchdb server
* ssl_keyfile - path to file
* ssl_certificate - path to file

Provide a custom file that lists trusted CA certificates, required when keyfile and certificate are provided
* ssl_ca_certs - path to file

Note that multiple couchdb members can be configured in the same file.

```
LoadPlugin python
<Plugin python>
  ModulePath "/usr/share/collectd/collectd-couchdb"

  Import couchdb_plugin
  <Module couchdb_plugin>
        Host "127.0.0.1"
        Port "15984"
        Interval 10
        LogLevel "debug"
        Cluster "Dev"
        Username "admin"
        Password "admin"
        EnhancedMetrics "True"
        IncludeMetric "counter.couchdb.rexi.buffered"
        ExcludeMetric "counter.couchdb.couchdb.httpd.temporary_view_reads"
        Node "couchdb@couchdb1"
    </Module>

    <Module couchdb_plugin>
        Host "127.0.0.1"
        Port "25984"
        Interval 20
        LogLevel "debug"
        Cluster "Dev"
        Username "admin"
        Password "admin"
        Node "couchdb@couchdb2"
    </Module>
</Plugin>
```