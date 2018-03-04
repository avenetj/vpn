import boto3

def kill_vpn(resources, tag):
    instances = resources.instances.filter(Filters=[{'Name': 'instance-state-name','Values': ['running']}])
    for instance in instances:
        if tag in instance.tags[0]['Value']:
            instance.terminate()
            return True
    else:
            return False

key=''
secret=''
ec2 = boto3.client('ec2', aws_access_key_id=key, aws_secret_access_key=secret)
resources = boto3.resource('ec2', aws_access_key_id=key, aws_secret_access_key=secret)
tag = 'vpn'
  
if kill_vpn(resources, tag):
    print('Vpn killed')
else:
    print('Not Running')
