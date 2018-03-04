import boto3
import time

def get_image(ec2, tag):
    images = ec2.describe_images(Owners=['self'])['Images']
    for image in images:
        if tag == image['Description']:
            return image['ImageId']

def get_elastic_ip(ec2, tag):
    addresses = ec2.describe_addresses()
    for eip in addresses['Addresses']:
        if tag in eip['Tags'][0]['Value']:
            return eip['AllocationId']
    #else:
    # create eip and tag it with tag 
    # push new eip to the vpn conf 

def get_security_group(ec2, tag):
    sgs = ec2.describe_security_groups(GroupNames=['vpn'])
    return sgs['SecurityGroups'][0]['GroupId']

def associate(ec2, instance, eip):
    return ec2.associate_address(AllocationId=eip, InstanceId=instance)

def is_present(resources, tag):
    instances = resources.instances.filter(Filters=[{'Name': 'instance-state-name','Values': ['running']}])
    for instance in instances:
        if tag in instance.tags[0]['Value']:
            return True
    else:
            return False

key=''
secret=''
ec2 = boto3.client('ec2', aws_access_key_id=key, aws_secret_access_key=secret)
resources = boto3.resource('ec2', aws_access_key_id=key, aws_secret_access_key=secret)
tag = 'vpn'
sg = str(get_security_group(ec2, tag))
  
if not is_present(resources, tag):
    ami = get_image(ec2, tag)
    vpn_id = resources.create_instances(ImageId=ami, MinCount=1, MaxCount=1, InstanceType='t2.nano', TagSpecifications=[{'ResourceType':'instance', 'Tags': [{'Key': 'type','Value': 'vpn'}]}], SecurityGroupIds=[sg])
    id = str(vpn_id[0])
    id = id[17:36]
    eip = get_elastic_ip(ec2, tag)
    time.sleep(120)
    association = associate(ec2, id, eip)
