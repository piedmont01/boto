import boto3
import boto3.session

class ListResources:
  def __init__(self, profile, region, resource):
    self.profile = profile
    self.region = region
    self.resource = resource

    self.session = boto3.Session(profile_name=self.profile)

  def AWSResourceList(self):
  
    if self.resource == 'ec2':
      server_list=self.session.resource(self.resource, region_name=self.region)
      for server in server_list.instances.all():
        print(f"server id: {server.id}")
      
    if self.resource == 's3':
      bucket_list = self.session.resource(self.resource, region_name=self.region)
      for bucket  in bucket_list.buckets.all():
        print(f"bucket name: {bucket.name}")

    if self.resource == 'rds':
      print (f"RDS instances for {self.profile}")
      client = self.session.client('rds', region_name=self.region)
      rds_instance = client.describe_db_instances()

    if self.resource == 'dynamodb':
      client = self.session.client('dynamodb', region_name=self.region)
      response = client.list_tables()
      if len(response['TableNames']) > 0:
        for table in response['TableNames']:
          print(f"DyanmoDB Table: {table}")

    if self.resource == 'redshift':
      client = self.session.client('redshift', region_name=self.region)
      response = client.describe_clusters()
      if len(response['Clusters']) > 0:
        for cluster in response['Clusters']:
          print(f"Redshift Cluster: {cluster['ClusterIdentifier']}")
        



profile_list = [ '133', '202', '230', '272', '353', '439',] 

region_names={	'us-east-1',
		'us-east-2',
		'us-west-1',
		'us-west-2',
             }

resource_list = ['ec2' ]

for region in region_names:
  for profile_name in profile_list:
    print (f"Region name is: {region} - Profile is: {profile_name}")
    for resource in resource_list:
      thing = ListResources(profile_name, region, resource)
      thing.AWSResourceList()
    print (f"--------------------------------")
    print (f"")
