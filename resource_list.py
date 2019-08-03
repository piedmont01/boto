import boto3
import boto3.session

class ListResources:
  def __init__(self, profile, region, resource):
    self.profile = profile
    self.region = region
    self.resource = resource

    self.session = boto3.Session(profile_name=self.profile)


    self.resource_list = []

  def AWSResourceList(self):
  
    if self.resource == 'ec2':
      server_list=self.session.resource(self.resource, region_name=self.region)
      for server in server_list.instances.all():
        # print(f"server id: {server.id}")
        self.resource_list.append(server)
      
    if self.resource == 's3':
      bucket_list = self.session.resource(self.resource, region_name=self.region)
      for bucket  in bucket_list.buckets.all():
        self.resource_list.append(bucket)

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

    if self.resource == 'route53':
      client = self.session.client('route53', region_name=self.region)

    return(self.resource_list)


profile_list = [ '133', '202', '230', '272', '353', '439',] 

region_names={	'us-east-1',
		'us-east-2',
		'us-west-1',
		'us-west-2',
             }

resource_list = ['ec2', ]

for region in region_names:
  for profile_name in profile_list:
    for resource in resource_list:
      resource_item = ListResources(profile_name, region, resource)
      x = resource_item.AWSResourceList()
    if  len(x) > 0 :
      print(f"list of servers {x} in region {region} profile name {profile_name} and count is {len(x)}")
