import logging

import boto3


LOG = logging.getLogger(__name__)
LOG.setLevel(logging.DEBUG)


tag_client = boto3.client('resourcegroupstaggingapi')


def find_resources(r_types):
    """
    list of resource types
    """
    arns = []
    pager = tag_client.get_paginator('get_resources')

    for page in pager.paginate(ResourceTypeFilters=r_types):
        r_list = page['ResourceTagMappingList']
        for tag_map in r_list:
            arn = tag_map['ResourceARN']
            arns.append(arn)

    return arns


def tag_resources(tags, arns):
    """
    event tags, resource list
    """
    result = tag_client.tag_resources(ResourceARNList=arns, Tags=tags)
    LOG.debug(f"Tagged resources: {result}")
    failed = result.get('FailedResourcesMap', {})
    if failed != {}:
        LOG.error("Failed to tag some resources")
        raise RuntimeError(failed)

def lambda_handler(event, context):
    """Sample pure Lambda function

    Parameters
    ----------
    event: dict, required
        EventBridge Input Format

        Event doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-input-format
        https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-run-lambda-schedule.html

    context: object, required
        Lambda Context runtime methods and attributes

        Context doc: https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html
    """

    try:
        LOG.debug(f"Event: {event}")
        tags = event['tags']
        r_types = event['resource_types']
        found = find_resources(r_types)
        LOG.info(f"Tagging resources: {found}")
        tag_resources(tags, found)
    except Exception as exc:
        LOG.exception(exc)
        raise

    # Any return value will be discarded by Event Bridge
    # https://docs.aws.amazon.com/lambda/latest/dg/python-handler.html#python-handler-return
