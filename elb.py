import boto3
import boto3.session

#session = boto3.Session(profile_name='ekendall')
#client = session.client('elb', region_name='us-east-1')
#response = client.modify_load_balancer_attributes(
# LoadBalancerName='test',
#    LoadBalancerAttributes={
#   'AccessLog':{ 
#            'Enabled': True
#        }
#    }
#)

client = boto3.client('elbv2')

#x = client.describe_tags (  ResourceArns = [ 'arn:aws:elasticloadbalancing:us-east-1:858737304353:loadbalancer/app/test/49c9399c87f90ae5'])

#y=x.get('TagDescriptions')
#for tag in y[0].get('Tags'):
#  for key, val in tag.items():
#    print(f"{val}")


# x.get('TagDescriptions')[0]['Tags'][0]['Value']
#lenA=len(x.get('TagDescriptions')[0])
#lenB=len(x.get('TagDescriptions')[0]['Tags'][0])

tags = client.describe_tags( ResourceArns = [ 'arn:aws:elasticloadbalancing:us-east-1:858737304353:loadbalancer/app/test/49c9399c87f90ae5'])
tag_descriptions=tags.get('TagDescriptions')
elb_prefix = 'undefined'
for row in range(len(tag_descriptions[0].get('Tags'))):
  for key, val in tag_descriptions[0].get('Tags')[row].items():
    if val == "Environment":
      elb_prefix = tag_descriptions[0]['Tags'][row]['Value']
      break;
print(elb_prefix)
