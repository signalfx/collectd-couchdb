"""
This file contains exhaustive list of all the metrics those can be collected from different versions of the CouchDB.
"""

couchdb_metrics = {
    "couchdb1" : [
        ("couchdb.auth_cache_misses.current", "counter"),
        ("couchdb.auth_cache_hits.current", "counter"),
        ("couchdb.database_writes.current", "counter"),
        ("couchdb.database_reads.current", "counter"),
        ("couchdb.open_databases.current", "counter"),
        ("couchdb.open_os_files.current", "counter"),
        ("couchdb.request_time.current", "counter"),
        ("httpd.bulk_requests.current", "counter"),
        ("httpd.requests.current", "counter"),
        ("httpd.temporary_view_reads.current", "counter"),
        ("httpd.view_reads.current", "counter"),
        ("httpd_request_methods.COPY.current", "counter"),
        ("httpd_request_methods.DELETE.current", "counter"),
        ("httpd_request_methods.GET.current", "counter"),
        ("httpd_request_methods.HEAD.current", "counter"),
        ("httpd_request_methods.MOVE.current", "counter"),
        ("httpd_request_methods.POST.current", "counter"),
        ("httpd_request_methods.PUT.current", "counter"),
        ("httpd_status_codes.200.current", "counter"),
        ("httpd_status_codes.201.current", "counter"),
        ("httpd_status_codes.202.current", "counter"),
        ("httpd_status_codes.301.current", "counter"),
        ("httpd_status_codes.304.current", "counter"),
        ("httpd_status_codes.400.current", "counter"),
        ("httpd_status_codes.401.current", "counter"),
        ("httpd_status_codes.403.current", "counter"),
        ("httpd_status_codes.404.current", "counter"),
        ("httpd_status_codes.405.current", "counter"),
        ("httpd_status_codes.409.current", "counter"),
        ("httpd_status_codes.412.current", "counter"),
        ("httpd.status_codes.500.current", "counter"),

    ],

    # The metrics are segrated so that they can be collected only when needed.
    # In the default plugin only 'couchdb' and 'mem3' metrics are collected.
    # Some of the metrics in 'couchdb' is deliberately disabled.
    "couchdb2" : {
        "couchdb" : [
            ("couchdb.httpd.aborted_requests.value", "counter"),
            ("couchdb.httpd.bulk_requests.value", "counter"),
            ("couchdb.httpd.requests.value", "counter"),
            ("couchdb.httpd.temporary_view_reads.value", "counter"),
            ("couchdb.httpd.view_reads.value", "counter"),
            ("couchdb.httpd.clients_requesting_changes.value", "counter"),
            ("couchdb.auth_cache_hits.value", "counter"),
            ("couchdb.auth_cache_misses.value", "counter"),
            ("couchdb.collect_results_time.value.min","gauge"),
            ("couchdb.collect_results_time.value.max","gauge"),
            ("couchdb.collect_results_time.value.arithmetic_mean","gauge"),
            ("couchdb.collect_results_time.value.standard_deviation","gauge"),
            ("couchdb.collect_results_time.value.percentile.50","gauge"),
            ("couchdb.collect_results_time.value.percentile.75","gauge"),
            ("couchdb.collect_results_time.value.percentile.90","gauge"),
            ("couchdb.collect_results_time.value.percentile.99", "gauge"),
            ("couchdb.collect_results_time.value.999","gauge"),
            ("couchdb.database_writes.value", "counter"),
            ("couchdb.database_reads.value", "counter"),
            ("couchdb.document_inserts.value", "counter"),
            ("couchdb.document_writes.value", "counter"),
            ("couchdb.local_document_writes.value", "counter"),
            ("couchdb.httpd_request_methods.COPY.value", "counter"),
            ("couchdb.httpd_request_methods.DELETE.value", "counter"),
            ("couchdb.httpd_request_methods.GET.value", "counter"),
            ("couchdb.httpd_request_methods.HEAD.value", "counter"),
            ("couchdb.httpd_request_methods.OPTIONS.value", "counter"),
            ("couchdb.httpd_request_methods.POST.value", "counter"),
            ("couchdb.httpd_request_methods.PUT.value", "counter"),
            ("couchdb.httpd_status_codes.200.value", "counter"),
            # ("couchdb.httpd_status_codes.201.value", "counter"),
            # ("couchdb.httpd_status_codes.202.value", "counter"),
            # ("couchdb.httpd_status_codes.204.value", "counter"),
            # ("couchdb.httpd_status_codes.206.value", "counter"),
            # ("couchdb.httpd_status_codes.301.value", "counter"),
            # ("couchdb.httpd_status_codes.302.value", "counter"),
            # ("couchdb.httpd_status_codes.304.value", "counter"),
            ("couchdb.httpd_status_codes.400.value", "counter"),
            ("couchdb.httpd_status_codes.401.value", "counter"),
            # ("couchdb.httpd_status_codes.403.value", "counter"),
            ("couchdb.httpd_status_codes.404.value", "counter"),
            # ("couchdb.httpd_status_codes.405.value", "counter"),
            # ("couchdb.httpd_status_codes.406.value", "counter"),
            # ("couchdb.httpd_status_codes.409.value", "counter"),
            # ("couchdb.httpd_status_codes.412.value", "counter"),
            # ("couchdb.httpd_status_codes.413.value", "counter"),
            # ("couchdb.httpd_status_codes.414.value", "counter"),
            # ("couchdb.httpd_status_codes.415.value", "counter"),
            # ("couchdb.httpd_status_codes.416.value", "counter"),
            # ("couchdb.httpd_status_codes.417.value", "counter"),
            ("couchdb.open_databases.value", "counter"),
            ("couchdb.open_os_files.value", "counter"),
            # ("couchdb.couch_server.lru_skip.value", "counter"),
            # ("couchdb.query_server.vdu_rejects.value", "counter"),
            ("couchdb.request_time.value.min","gauge"),
            ("couchdb.request_time.value.max","gauge"),
            ("couchdb.request_time.value.arithmetic_mean","gauge"),
            ("couchdb.request_time.value.standard_deviation","gauge"),
            ("couchdb.request_time.value.percentile.50","gauge"),
            ("couchdb.request_time.value.percentile.75","gauge"),
            ("couchdb.request_time.value.percentile.90","gauge"),
            ("couchdb.request_time.value.percentile.99", "gauge"),
            ("couchdb.request_time.value.999","gauge"),
        ],
        "couch_replicator" : [
            ("couch_replicator.changes_read_failures.value", "counter"),
            ("couch_replicator.changes_reader_deaths.value", "counter"),
            ("couch_replicator.changes_manager_deaths.value", "counter"),
            ("couch_replicator.changes_queue_deaths.value", "counter"),
            ("couch_replicator.checkpoints.success.value", "counter"),
            ("couch_replicator.checkpoints.failure.value", "counter"),
            ("couch_replicator.failed_starts.value", "counter"),
            ("couch_replicator.requests.value", "counter"),
            ("couch_replicator.responses.failure.value", "counter"),
            ("couch_replicator.responses.success.value", "counter"),
            ("couch_replicator.stream_responses.failure.value", "counter"),
            ("couch_replicator.stream_responses.success.value", "counter"),
            ("couch_replicator.worker_deaths.value", "counter"),
            ("couch_replicator.workers_started.value", "counter")

        ],
        "rexi" : [
            ("rexi.buffered.value", "counter"),
            ("rexi.down.value", "counter"),
            ("rexi.dropped.value", "counter"),
            ("rexi.streams.timeout.init_stream.value", "counter"),
            ("rexi.streams.timeout.stream.value", "counter"),
            ("rexi.streams.timeout.wait_for_ack.value", "counter")

        ],
        "couch_log" : [
            ("couch_log.level.alert.value", "counter"),
            ("couch_log.level.critical.value", "counter"),
            ("couch_log.level.debug.value", "counter"),
            ("couch_log.level.emergency.value", "counter"),
            ("couch_log.level.error.value", "counter"),
            ("couch_log.level.info.value", "counter"),
            ("couch_log.level.notice.value", "counter"),
            ("couch_log.level.warning.value", "counter")
        ],
        "pread" : [
            ("pread.exceed_eof.value", "counter"),
            ("pread.exceed_limit.value", "counter")
        ],
        "ddoc_cache" : [
            ("ddoc_cache.hit.value", "counter"),
            ("ddoc_cache.miss.value", "counter"),
            ("ddoc_cache.recovery.value", "counter")
        ],
        "global_changes" : [
            ("global_changes.db_writes.value", "counter"),
            ("global_changes.event_doc_conflict.value", "counter"),
            ("global_changes.listener_pending_updates.value", "gauge"),
            ("global_changes.rpcs.value", "counter"),
            ("global_changes.server_pending_updates.value", "counter")
        ],
        "mem3" : [
            ("mem3.shard_cache.eviction.value", "counter"),
            ("mem3.shard_cache.hit.value", "counter"),
            ("mem3.shard_cache.miss.value", "counter")
        ],
        "fabric" : [
            ("fabric.worker.timeouts.value", "counter"),
            ("fabric.read_repairs.success.value", "counter"),
            ("fabric.read_repairs.failure.value", "counter"),
            ("fabric.doc_update.errors.value", "counter"),
            ("fabric.doc_update.mismatched_errors.value", "counter"),
            ("fabric.doc_update.write_quorum_errors.value", "counter")
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

