"""
This file contains exhaustive list of all the metrics those can be collected from different versions of the CouchDB.
"""

couchdb_metrics = {
    "couchdb1" : [
        ("couchdb.auth_cache_misses", "counter"),
        ("couchdb.auth_cache_hits", "counter"),
        ("couchdb.database_writes", "counter"),
        ("couchdb.database_reads", "counter"),
        ("couchdb.open_databases", "counter"),
        ("couchdb.open_os_files", "counter"),
        ("couchdb.request_time", "counter"),
        ("httpd.bulk_requests", "counter"),
        ("httpd.requests", "counter"),
        ("httpd.temporary_view_reads", "counter"),
        ("httpd.view_reads", "counter"),
        ("httpd_request_methods.COPY", "counter"),
        ("httpd_request_methods.DELETE", "counter"),
        ("httpd_request_methods.GET", "counter"),
        ("httpd_request_methods.HEAD", "counter"),
        ("httpd_request_methods.MOVE", "counter"),
        ("httpd_request_methods.POST", "counter"),
        ("httpd_request_methods.PUT", "counter"),
        ("httpd_status_codes.200", "counter"),
        ("httpd_status_codes.201", "counter"),
        ("httpd_status_codes.202", "counter"),
        ("httpd_status_codes.301", "counter"),
        ("httpd_status_codes.304", "counter"),
        ("httpd_status_codes.400", "counter"),
        ("httpd_status_codes.401", "counter"),
        ("httpd_status_codes.403", "counter"),
        ("httpd_status_codes.404", "counter"),
        ("httpd_status_codes.405", "counter"),
        ("httpd_status_codes.409", "counter"),
        ("httpd_status_codes.412", "counter"),
        ("httpd.status_codes.500", "counter"),

    ],

    # The metrics are segrated so that they can be collected only when needed.
    # In the default plugin only 'couchdb' and 'mem3' metrics are collected.
    # Some of the metrics in 'couchdb' is deliberately disabled.
    "couchdb2" : {
        "couchdb" : [
            ("couchdb.httpd.aborted_requests", "counter"),
            ("couchdb.httpd.bulk_docs", "counter"),
            ("couchdb.httpd.bulk_requests", "counter"),
            ("couchdb.httpd.requests", "counter"),
            ("couchdb.httpd.temporary_view_reads", "counter"),
            ("couchdb.httpd.view_reads", "counter"),
            ("couchdb.httpd.clients_requesting_changes", "counter"),
            ("couchdb.auth_cache_hits", "counter"),
            ("couchdb.auth_cache_misses", "counter"),
            ("couchdb.collect_results_time", "counter"),
            ("couchdb.database_writes", "counter"),
            ("couchdb.database_reads", "counter"),
            ("couchdb.document_inserts", "counter"),
            ("couchdb.document_writes", "counter"),
            ("couchdb.local_document_writes", "counter"),
            ("couchdb.httpd_request_methods.COPY", "counter"),
            ("couchdb.httpd_request_methods.DELETE", "counter"),
            ("couchdb.httpd_request_methods.GET", "counter"),
            ("couchdb.httpd_request_methods.HEAD", "counter"),
            ("couchdb.httpd_request_methods.OPTIONS", "counter"),
            ("couchdb.httpd_request_methods.POST", "counter"),
            ("couchdb.httpd_request_methods.PUT", "counter"),
            ("couchdb.httpd_status_codes.200", "counter"),
            # ("couchdb.httpd_status_codes.201", "counter"),
            # ("couchdb.httpd_status_codes.202", "counter"),
            # ("couchdb.httpd_status_codes.204", "counter"),
            # ("couchdb.httpd_status_codes.206", "counter"),
            # ("couchdb.httpd_status_codes.301", "counter"),
            # ("couchdb.httpd_status_codes.302", "counter"),
            # ("couchdb.httpd_status_codes.304", "counter"),
            ("couchdb.httpd_status_codes.400", "counter"),
            ("couchdb.httpd_status_codes.401", "counter"),
            # ("couchdb.httpd_status_codes.403", "counter"),
            ("couchdb.httpd_status_codes.404", "counter"),
            # ("couchdb.httpd_status_codes.405", "counter"),
            # ("couchdb.httpd_status_codes.406", "counter"),
            # ("couchdb.httpd_status_codes.409", "counter"),
            # ("couchdb.httpd_status_codes.412", "counter"),
            # ("couchdb.httpd_status_codes.413", "counter"),
            # ("couchdb.httpd_status_codes.414", "counter"),
            # ("couchdb.httpd_status_codes.415", "counter"),
            # ("couchdb.httpd_status_codes.416", "counter"),
            # ("couchdb.httpd_status_codes.417", "counter"),
            ("couchdb.open_databases", "counter"),
            ("couchdb.open_os_files", "counter"),
            ("couchdb.couch_server.lru_skip", "counter"),
            ("couchdb.query_server.vdu_rejects", "counter")
        ],
        "couch_replicator" : [
            ("couch_replicator.changes_read_failures", "counter"),
            ("couch_replicator.changes_reader_deaths", "counter"),
            ("couch_replicator.changes_manager_deaths", "counter"),
            ("couch_replicator.changes_queue_deaths", "counter"),
            ("couch_replicator.checkpoints.success", "counter"),
            ("couch_replicator.checkpoints.failure", "counter"),
            ("couch_replicator.failed_starts", "counter"),
            ("couch_replicator.requests", "counter"),
            ("couch_replicator.responses.failure", "counter"),
            ("couch_replicator.responses.success", "counter"),
            ("couch_replicator.stream_responses.failure", "counter"),
            ("couch_replicator.stream_responses.success", "counter"),
            ("couch_replicator.worker_deaths", "counter"),
            ("couch_replicator.workers_started", "counter")

        ],
        "rexi" : [
            ("rexi.buffered", "counter"),
            ("rexi.down", "counter"),
            ("rexi.dropped", "counter"),
            ("rexi.streams.timeout.init_stream", "counter"),
            ("rexi.streams.timeout.stream", "counter"),
            ("rexi.streams.timeout.wait_for_ack", "counter")

        ],
        "couch_log" : [
            ("couch_log.level.alert", "counter"),
            ("couch_log.level.critical", "counter"),
            ("couch_log.level.debug", "counter"),
            ("couch_log.level.emergency", "counter"),
            ("couch_log.level.error", "counter"),
            ("couch_log.level.info", "counter"),
            ("couch_log.level.notice", "counter"),
            ("couch_log.level.warning", "counter")
        ],
        "pread" : [
            ("pread.exceed_eof", "counter"),
            ("pread.exceed_limit", "counter")
        ],
        "ddoc_cache" : [
            ("ddoc_cache.hit", "counter"),
            ("ddoc_cache.miss", "counter"),
            ("ddoc_cache.recovery", "counter")
        ],
        "global_changes" : [
            ("global_changes.db_writes", "counter"),
            ("global_changes.event_doc_conflict", "counter"),
            ("global_changes.listener_pending_updates", "gauge"),
            ("global_changes.rpcs", "counter"),
            ("global_changes.server_pending_updates", "counter")
        ],
        "mem3" : [
            ("mem3.shard_cache.eviction", "counter"),
            ("mem3.shard_cache.hit", "counter"),
            ("mem3.shard_cache.miss", "counter")
        ],
        "fabric" : [
            ("fabric.worker.timeouts", "counter"),
            ("fabric.read_repairs.success", "counter"),
            ("fabric.read_repairs.failure", "counter"),
            ("fabric.doc_update.errors", "counter"),
            ("fabric.doc_update.mismatched_errors", "counter"),
            ("fabric.doc_update.write_quorum_errors", "counter")
        ],
        "db_metrics" : [
            ("sizes.external", "gauge"),
            ("doc_del_count", "gauge"),
            ("doc_count", "gauge"),
            ("disk_size", "gauge"),
            ("data_size", "gauge")
        ]

    }

}

