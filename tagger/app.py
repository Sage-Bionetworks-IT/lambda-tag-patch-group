import logging

Config = {
    "resource_types": [
        "AWS::DMS::ReplicationInstance",
        "AWS::EC2::Instance",
        "AWS::EC2::ReservedInstance",
        "AWS::ECS::ContainerInstance",
        "AWS::OpsWorks::Instance",
        "AWS::RDS::DBInstance",
        "AWS::RDS::ReservedDBInstance",
        "AWS::SSM::ManagedInstance",
        "AWS::SageMaker::NotebookInstance",
    ]
}

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
        logging.basicConfig(level=logging.DEBUG)
        logging.info(f"Config: {Config}")
        logging.info(f"Event: {event}")
        logging.info(f"Context: {context}")
    except Exception as exc:
        logging.exception(exc)

    # Any return value will be discarded by Event Bridge
    # https://docs.aws.amazon.com/lambda/latest/dg/python-handler.html#python-handler-return
