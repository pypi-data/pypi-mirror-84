# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 CESNET.
#
# CIS theses repository is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Command-line tools for demo module."""
import datetime
import random
import uuid

import click
from edtf.parser.grammar import level0Expression
from faker import Faker
from flask.cli import with_appcontext
from flask_principal import Identity
from invenio_access import any_user
from invenio_db import db
from invenio_indexer.api import RecordIndexer
from invenio_pidstore import current_pidstore
from invenio_records_files.api import Record
from invenio_search import current_search

# from .services import BibliographicRecordService
# from .vocabularies import Vocabularies


def fake_resource_type():
    """Generate a fake resource_type."""
    #vocabulary = Vocabularies.get_vocabulary('resource_type')
    _type = "xx"
    subtype = "xxx"
    return {
        "type": _type,
        "subtype": subtype
    }


def fake_edtf_level_0():
    """Generate a fake publication_date string."""
    def fake_date(end_date=None):
        fake = Faker()
        date_pattern = ['%Y', '%m', '%d']
        # make it less and less likely to get less and less parts of the date

        if random.choice([True, False]):
            date_pattern.pop()
            if random.choice([True, False]):
                date_pattern.pop()

        return fake.date("-".join(date_pattern), end_datetime=end_date)

    f_date = fake_date()

    # if interval
    if random.choice([True, False]):
        # get f_date as date object
        parser = level0Expression("level0")
        parsed_date = parser.parseString(f_date)[0]
        date_tuple = parsed_date.lower_strict()[:3]
        f_date_object = datetime.date(*date_tuple)

        interval_start = fake_date(end_date=f_date_object)

        return "/".join([interval_start, f_date])

    return f_date


def create_fake_record():
    """Create records for demo purposes."""
    fake = Faker()
    data_to_use = {
        "_access": {
            "metadata_restricted": False,
            "files_restricted": False
        },
        "_created_by": 2,
        "_default_preview": "previewer one",
        "_internal_notes": [{
            "user": "inveniouser",
            "note": "RDM record",
            "timestamp": fake.date(pattern='%Y-%m-%d')
        }],
        "_owners": [1],
        "access_right": "open",
        "embargo_date": fake.future_date(end_date='+1y').strftime("%Y-%m-%d"),
        "contact": "info@inveniosoftware.org",
        "resource_type": fake_resource_type(),
        "identifiers": {
            "DOI": "10.9999/rdm.9999999",
            "arXiv": "9999.99999",
        },
        "creators": [{
            "name": fake.name(),
            "type": "Personal",
            "identifiers": {
                "Orcid": "0000-0002-1825-0097",
            },
            "affiliations": [{
                "name": fake.company(),
                "identifiers": {
                    "ror": "03yrm5c26"
                }
            }]
        }],
        "titles": {"cs": "neco"},
        "publication_date": fake_edtf_level_0(),
        "subjects": [{
            "subject": {"cs": "neco"},
            "identifier": "subj-1",
            "scheme": "no-scheme"
        }],
        "contributors": [{
            "name": fake.name(),
            "type": "Personal",
            "affiliations": [{
                "name": fake.company(),
                "identifiers": {
                    "ror": "03yrm5c26"
                }
            }],
            "role": "RightsHolder"
        }],
        "dates": [{
            # No end date to avoid computations based on start
            "start": fake.date(pattern='%Y-%m-%d'),
            "description": "Random test date",
            "type": "Other"
        }],
        "language": "eng",
        "related_identifiers": [{
            "identifier": "10.9999/rdm.9999988",
            "scheme": "DOI",
            "relation_type": "Requires",
            "resource_type": fake_resource_type()
        }],
        "version": "v0.0.1",
        "licenses": [{
            "license": {"cs": "neco"},
            "uri": "https://opensource.org/licenses/BSD-3-Clause",
            "identifier": "BSD-3",
            "scheme": "BSD-3",
        }],
        "descriptions": {"cs": "neco"},
        "locations": [{
            "point": {
                "lat": str(fake.latitude()),
                "lon": str(fake.longitude())
            },
            "place": fake.location_on_land()[2],
            "description": {"cs": "neco"},
        }],
        "references": [{
            "reference_string": "Reference to something et al.",
            "identifier": "9999.99988",
            "scheme": "GRID"
        }]
    }

    # identity providing `any_user` system role
    identity = Identity(1)
    identity.provides.add(any_user)

    # draft_service = BibliographicRecordService()
    #
    # identified_draft = draft_service.create(
    #     data=data_to_use, identity=identity
    # )
    #
    # identified_record = draft_service.publish(
    #     id_=identified_draft.id, identity=identity
    # )
    #
    # return identified_record
    return data_to_use


@click.group()
def rdm_records():
    """Do InvenioRDM records commands."""
    pass


@rdm_records.command('demo')
@with_appcontext
def demo():
    """Create 10 fake records for demo purposes."""
    click.secho('Creating demo records...', fg='blue')

    for _ in range(10):
        create_fake_record()

    click.secho('Created records!', fg='green')
