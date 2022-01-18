"""There is no need of this code since the Event is already filterying""" 
"""Regex and Boto3 modules"""
import re
import boto3


def lambda_handler(event, context):
    """Send a message for tasks that were stopped due to OutOfMemoryError"""

    sns_arn = "arn:aws:sns:eu-west-1:ACCOUNT:ECSHealthy"
    last_status = event.get('detail', '').get('lastStatus', '')
    containers = event.get('detail', '').get('containers', '')
    reason = [item['reason'] for item in containers if 'reason' in item]

    if (re.search(r"\b" + re.escape("OutOfMemoryError") + r"\b", reason[0])
        and last_status == 'STOPPED'
            and reason):

        cluster = event.get('detail', '').get('clusterArn', '')
        service = event.get('detail', '').get('group', '')
        task_arn = [item['taskArn']
                    for item in containers if 'taskArn' in item]
        message = (
            f"Cluster: {cluster}\nService: {service}\n"
            f"Task ARN: {task_arn[0]}\nReason: {reason[0]}"
        )

        client = boto3.client('sns')
        response = client.publish(
            TargetArn=sns_arn,
            Message=message
        )

        message_id = response.get('MessageId', '')
        print(f"SNS message sent: {message_id}")
