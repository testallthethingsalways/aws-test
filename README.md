
# Approach
* Create an aws account and generate a key/secret pair
* An EC2 launch template specifying an AMI ID (ami-9887c6e7), Instance type (T2.micro) and tag (key: type, value:aws-test) was created using the AWS UI. This could have been created using the API but was thought to be out of scope for this test
* Use a makefile to manage bootstrapping, high level config and executing commands
* Use a virtualenv and requirements.txt to manage python dependencies
* Use boto3 to interact with the AWS API
* Use pytest as the test framework
* Add linting

## Run tests
`make test-api`

## Coverage
One E2E test to start and terminate an EC2 instance with assertions for:
* the expected instance region
* the instance having the expected type
* the instance having the expected tag
The test also confirms the expected instance to be running

## Further tests
If the EC2 instance never reaches the expected state (running/terminated) the test will not end. Next I would add pytest-timeout and give the test a reasonable timeout.

If the state of the AWS region is important we could assert on the number and type of instances already existing

If testing the API itself is important we could add tests to cover
* putting the instance in a specific subnet
* putting the instance in a specific availability zone
* adding a security group
* we could batch requests if starting many instances
* define the launch template as part of the test
* etc

We could also mock aws using a project like https://github.com/spulec/moto. This would likely give us faster feedback and not be dependent on making real calls to AWS. 

# How to execute and be ready to be deployed on a CI server.
* Given this is currently opensource we could easily add a CI tool like Travis. Other tools like Jenkins, AWS CodeBuild, Drone etc could also be used
* The project already bootstraps all its dependencies and only requires python3, pip and virtualenv to be installed on a CI server
* The CI server would simply need to execute the command `make test-api` to run the tests
* The aws config should be kept private and for that reason is not committed to the repo. This could be set as an environment variable on the CI server. If the tests instead mocked AWS security would not be an issue
