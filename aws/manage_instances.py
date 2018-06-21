import boto3
from time import sleep


class ManageInstances():
    """
    Class to manage starting and terminating EC2 instances
    """
    def __init__(self, template_id, region, aws_config_file):
        self.template_id = template_id

        # Get AWS key and secret
        with open(aws_config_file, 'r') as f:
            lines = f.readlines()
            for l in lines:
                if 'aws_access_key_id' in l:
                    _, access_key = l.split(
                        'aws_access_key_id =')
                    self.access_key = access_key.strip()
                if 'aws_secret_access_key' in l:
                    _, secret_key = l.split(
                        'aws_secret_access_key =')
                    self.secret_key = secret_key.strip()

        # Aws client to make calls directly to aws ec2 api
        self.client = boto3.client(
            'ec2',
            region_name=region,
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key,
        )

    def get_instances_by_id(self, instance_id):
        """Method to get list of instances which match instance id"""

        filters = [
            {
                'Name': 'instance-id',
                'Values': [instance_id]
            }
        ]

        # Filter the instances based on filters above
        return self.client.describe_instances(
            Filters=filters)['Reservations']

    def run_instances(self, num_of_instances):
        """
        Method to run new instances
        """

        print('Running %s new instances...' % num_of_instances)
        resp = self.client.run_instances(
            MaxCount=num_of_instances,
            MinCount=num_of_instances,
            LaunchTemplate={
                'LaunchTemplateName': self.template_id,
                'Version': '$Latest'
            }
        )
        return resp['Instances']

    def wait_for_instance_state(self, instance_id, state):
        """Method to wait for an instance to have a desired state"""

        instance_list = self.get_instances_by_id(instance_id)

        for part in instance_list:
            instances = part['Instances']
            for inst in instances:
                if inst['InstanceId'] == instance_id and \
                        inst['State']['Name'] == state:
                    return
                else:
                    sleep(1)
                    self.wait_for_instance_state(instance_id, state)

    def terminate_instance_by_id(self, instance_id):
        "Method to terminate instance by id"

        print('Terminated all instances...')

        self.client.terminate_instances(InstanceIds=[instance_id])
