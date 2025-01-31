import json

import pytest
import boto3
from botocore.stub import Stubber

from tagger import app

test_tags = {
    "stage": "test",
    "foo": "bar",
}

test_types = [
    "test:type",
]

test_event = {
    "tags": test_tags,
    "resource_types": test_types,
}

test_arn = 'arn:aws:test-service:test-region:ACCOUNT:test/test'

mock_found_arns = [test_arn,]

mock_get_response = {
    'ResourceTagMappingList': [
        {'ResourceARN': test_arn},
    ]
}

mock_tag_response = {}

mock_tag_failed_response = {
    'FailedResourcesMap': {
        test_arn: {
            'StatusCode': 0,
            'ErrorMessage': "Test",
        }
    }
}


def test_find_resources():
    with Stubber(app.tag_client) as stub:
        stub.add_response('get_resources', mock_get_response)
        result = app.find_resources(test_types)
        assert result == mock_found_arns
        stub.assert_no_pending_responses()


def test_tag_resources():
    with Stubber(app.tag_client) as stub:
        stub.add_response('tag_resources', mock_tag_response)
        app.tag_resources(test_tags, mock_found_arns)
        stub.assert_no_pending_responses()


def test_tag_resources_failed():
    with Stubber(app.tag_client) as stub:
        stub.add_response('tag_resources', mock_tag_failed_response)
        with pytest.raises(RuntimeError) as excinfo:
            app.tag_resources(test_tags, mock_found_arns)
            assert str(excinfo.value) == mock_tag_failed_response
        stub.assert_no_pending_responses()


def test_lambda_handler(mocker):
    mocker.patch('tagger.app.find_resources', return_value=mock_found_arns)
    mocker.patch('tagger.app.tag_resources')

    # assert no exceptions
    app.lambda_handler(test_event, None)
