event={'version': '0', 'id': '184b8950-6003-12d4-98f2-7a6f380f0450', 'detail-type': 'AWS API Call via CloudTrail', 'source': 'aws.elasticloadbalancing', 'account': '298281349047', 'time': '2019-06-25T18:02:28Z', 'region': 'us-east-1', 'resources': [], 'detail': {'eventVersion': '1.05', 'userIdentity': {'type': 'Root', 'principalId': '298281349047', 'arn': 'arn:aws:iam::298281349047:root', 'accountId': '298281349047', 'accessKeyId': 'ASIAUK4XUF636GRQRBUU', 'userName': 'erickkendall', 'sessionContext': {'sessionIssuer': {}, 'webIdFederationData': {}, 'attributes': {'mfaAuthenticated': 'true', 'creationDate': '2019-06-25T17:52:11Z'}}}, 'eventTime': '2019-06-25T18:02:28Z', 'eventSource': 'elasticloadbalancing.amazonaws.com', 'eventName': 'CreateLoadBalancer', 'awsRegion': 'us-east-1', 'sourceIPAddress': '76.18.136.253', 'userAgent': 'console.ec2.amazonaws.com', 'requestParameters': {'securityGroups': ['sg-0afaf5248e3f6ae34'], 'type': 'application', 'ipAddressType': 'ipv4', 'subnetMappings': [{'subnetId': 'subnet-059cac030fe241c1a'}, {'subnetId': 'subnet-07bf42b1ef6dd77c7'}], 'name': 'b14', 'scheme': 'internet-facing'}, 'responseElements': {'loadBalancers': [{'type': 'application', 'loadBalancerName': 'b14', 'vpcId': 'vpc-0a2a41cc2495d7a7e', 'securityGroups': ['sg-0afaf5248e3f6ae34'], 'state': {'code': 'provisioning'}, 'availabilityZones': [{'subnetId': 'subnet-059cac030fe241c1a', 'zoneName': 'us-east-1a'}, {'subnetId': 'subnet-07bf42b1ef6dd77c7', 'zoneName': 'us-east-1b'}], 'ipAddressType': 'ipv4', 'dNSName': 'b14-490328860.us-east-1.elb.amazonaws.com', 'canonicalHostedZoneId': 'Z35SXDOTRQ7X7K', 'createdTime': 'Jun 25, 2019 6:02:28 PM', 'loadBalancerArn': 'arn:aws:elasticloadbalancing:us-east-1:298281349047:loadbalancer/app/b14/e2a53ebbbc9d21f4', 'scheme': 'internet-facing'}]}, 'requestID': '651a5ae7-9773-11e9-b506-e34c1976e484', 'eventID': 'c77acbbe-d3fd-4864-9720-0eb2dd39b87a', 'eventType': 'AwsApiCall', 'apiVersion': '2015-12-01'}}

print(f"this is the Python type for event {type(event)}")
print (f"------------------------------------------------------------")
print(f"the keys are {event.keys()}")
print (f"------------------------------------------------------------")
print(f"the values are {event.values()}")
print (f"------------------------------------------------------------")
print (f"\n")

for k, v in event.items():
        print("Code : {0}, Value : {1}".format(k, v))
        print (f"------------------------------------------------------------")
        print (f"\n")

print(f"Skip to fun")
print(f"This is detail {event['detail']}")
print(f"these are keys {event['detail'].keys()}")
print (f"------------------------------------------------------------")
print (f"\n")
print (f"What I'm insterested in {event['detail']['responseElements']}")
print (f"type for response element {type(event['detail']['responseElements'])}")
print (f"keys are {event['detail']['responseElements'].keys()}")
print (f"------------------------------------------------------------")
print (f"\n")
print (f"here is what we need to parse {event['detail']['responseElements']['loadBalancers']}")
print (f"here is the type {type(event['detail']['responseElements']['loadBalancers'])}")
print (f"------------------------------------------------------------")
print (f"\n")
a = {}
x=event['detail']['responseElements']['loadBalancers']
a=x.pop()
for k,v in a.items():
  print (k,v)

print(a['loadBalancerName'])
print (f"------------------------------------------------------------")
print (f"\n")
x=event['detail']['responseElements']['loadBalancers']
print(x)
print(f"this is the {type(x)}")
for elb in x:
    for k, v in elb.items():
        print(k,v)

