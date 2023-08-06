# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 CESNET
#
# CIS theses repository is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""DataCite-based data model for Invenio."""
from celery import shared_task
from invenio_db import db
from invenio_files_rest.signals import file_deleted, file_uploaded
from invenio_indexer.signals import before_record_index

from . import config
from .metadata_extensions import MetadataExtensions, add_es_metadata_extensions
from .tasks import update_record_files_async


class InvenioRDMRecords(object):
    """Invenio-RDM-Records extension."""

    def __init__(self, app=None):
        """Extension initialization."""
        if app:
            self.init_app(app)

    def init_app(self, app):
        """Flask application initialization."""
        self.init_config(app)
        self.metadata_extensions = MetadataExtensions(
            app.config['RDM_RECORDS_METADATA_NAMESPACES'],
            app.config['RDM_RECORDS_METADATA_EXTENSIONS']
        )
        self._register_signals(app)

        app.extensions['invenio-rdm-records'] = self

    def init_config(self, app):
        """Initialize configuration."""
        supported_configurations = [
            'FILES_REST_PERMISSION_FACTORY',
            'PIDSTORE_RECID_FIELD',
            'RECORDS_REST_ENDPOINTS',
            'RECORDS_REST_FACETS',
            'RECORDS_REST_SORT_OPTIONS',
            'RECORDS_REST_DEFAULT_SORT',
            'RECORDS_UI_ENDPOINTS',
            'RECORDS_FILES_REST_ENDPOINTS',
            'RECORDS_PERMISSIONS_RECORD_POLICY',
            'THEME_SITEURL',
        ]

        for k in dir(config):
            if k in supported_configurations or k.startswith('RDM_RECORDS_'):
                app.config.setdefault(k, getattr(config, k))

    def _register_signals(self, app):
        """Register signals."""
        before_record_index.dynamic_connect(
            before_record_index_hook, sender=app, weak=False,
            index='records-record-v1.0.0'
        )

        file_deleted.connect(update_record_files_async, weak=False)
        file_uploaded.connect(update_record_files_async, weak=False)


def before_record_index_hook(
        sender, json=None, record=None, index=None, **kwargs):
    """Do Hook to transform Deposits before indexing in ES.

    :param sender: The entity sending the signal.
    :param json: The dumped Record dict which will be indexed.
    :param record: The corresponding Record object.
    :param index: The index in which the json will be indexed.
    :param kwargs: Any other parameters.
    """
    # All thee operations mutate the json
    add_es_metadata_extensions(json)  # TODO: Change for prepare
