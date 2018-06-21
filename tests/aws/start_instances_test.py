from aws.manage_instances import ManageInstances

import unittest


class ControllerTestCase(unittest.TestCase):

    def setUp(self):
        # Instantiate the manage_instances class and define the region and tag
        # to filter instances by
        self.manage_instances = ManageInstances(
            'aws-test', 'us-east-1', '.aws')
        self.num_instances_to_start = 1
        self.tag = {'Key': 'type', 'Value': 'aws-test'}

    def tearDown(self):
        for inst in self.instances:
            self.manage_instances.terminate_instance_by_id(
                instance_id=inst['InstanceId'])
            self.manage_instances.wait_for_instance_state(
                inst['InstanceId'], 'terminated')

    def test_starting_one_instance(self):
        # Run new EC2 instance
        self.instances = self.manage_instances.run_instances(
            self.num_instances_to_start)

        # AWS returns the instances which have been run
        assert len(self.instances) == self.num_instances_to_start

        for inst in self.instances:
            # wait for the instance to be run is running
            self.manage_instances.wait_for_instance_state(
                inst['InstanceId'], 'running')

            # perform assertions on the state of the instance
            assert inst['InstanceType'] == 't2.micro'
            assert 'us-east-1' in inst['Placement']['AvailabilityZone']
            self.assertIn(self.tag, inst['Tags'])


if __name__ == '__main__':
    unittest.main()
