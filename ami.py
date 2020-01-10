import boto3
from dateutil.parser import parse
import datetime
age = 14
aws_profile_name = 'famc-legacy'

def days_old(date):
  get_date_obj = parse(date)
  date_obj = get_date_obj.replace(tzinfo=None)
  diff = datetime.datetime.now() - date_obj
  return diff.days

session = boto3.Session(profile_name=aws_profile_name)
client = session.client('ec2', region_name='us-east-1')

amis = client.describe_images(Owners=['self'])

for ami in amis['Images']:
  create_date = ami['CreationDate']
  ami_id = ami['ImageId']
  day_old = days_old(create_date)
  if day_old > 14:
    print(ami_id)
