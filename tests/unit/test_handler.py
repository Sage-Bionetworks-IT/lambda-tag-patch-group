import json

import pytest

from tagger import app


@pytest.fixture()
def eb_event():
    """ Generates API GW Event"""

    return {
        "tags": {
            "foo": "bar",
            "stage": "test",
        },
        "resource_types": [
            "ec2:instance",
            "rds:db",
        ],
    }


def test_lambda_handler(eb_event, mocker):

    # assert no exceptions
    app.lambda_handler(eb_event, "")
