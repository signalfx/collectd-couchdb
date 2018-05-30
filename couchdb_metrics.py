"""
This file contains exhaustive list of all the metrics
those can be collected to monitor CouchDB.
"""

couchdb_metrics = {
    "basic_metrics": {
        "node_metrics": [
            ("couchdb.httpd.temporary_view_reads", "counter"),
            ("couchdb.httpd.aborted_requests", "counter"),
            ("couchdb.httpd.bulk_requests", "counter"),
            ("couchdb.httpd.requests", "counter"),
            ("couchdb.httpd.view_reads", "counter"),
            ("couchdb.auth_cache_hits", "counter"),
            ("couchdb.auth_cache_misses", "counter"),
            ("couchdb.database_writes", "counter"),
            ("couchdb.database_reads", "counter"),
            ("couchdb.document_inserts", "counter"),
            ("couchdb.document_writes", "counter"),
            ("couchdb.httpd_request_methods.COPY", "counter"),
            ("couchdb.httpd_request_methods.DELETE", "counter"),
            ("couchdb.httpd_request_methods.GET", "counter"),
            ("couchdb.httpd_request_methods.HEAD", "counter"),
            ("couchdb.httpd_request_methods.OPTIONS", "counter"),
            ("couchdb.httpd_request_methods.POST", "counter"),
            ("couchdb.httpd_request_methods.PUT", "counter"),
            ("couchdb.httpd_status_codes.200", "counter"),
            ("couchdb.httpd_status_codes.201", "counter"),
            ("couchdb.httpd_status_codes.400", "counter"),
            ("couchdb.httpd_status_codes.401", "counter"),
            ("couchdb.httpd_status_codes.404", "counter"),
            ("couchdb.httpd_status_codes.500", "counter"),
            ("couchdb.request_time.arithmetic_mean", "gauge"),
            ("mem3.shard_cache.hit", "counter"),
            ("mem3.shard_cache.miss", "counter")
        ],
        "db_metrics": [
            ("sizes.active", "gauge"),
            ("sizes.file", "gauge"),
            ("doc_del_count", "gauge"),
            ("doc_count", "gauge"),
        ]
    },

    # By default only basic_metrics are enabled.
    # To enable enhanced_metrics:
    #   Uncomment the required metrics below.
    #   Add 'EnhancedMetrics' 'True' to the conf file
    "enhanced_metrics": {
        "node_metrics": [
            ("couchdb.open_databases", "counter"),
            ("couchdb.open_os_files", "counter"),
            ("couchdb.collect_results_time.arithmetic_mean", "gauge"),
            ("couchdb.collect_results_time.percentile.90", "gauge"),
            ("couchdb.request_time.percentile.90", "gauge"),
            ("couch_replicator.requests", "counter"),
            ("couch_replicator.responses.failure", "counter"),
            ("couch_replicator.responses.success", "counter"),
        ]
    }
}


def get_basic_metrics():
    return couchdb_metrics['basic_metrics']


def get_enhanced_metrics():
    return couchdb_metrics['enhanced_metrics']
