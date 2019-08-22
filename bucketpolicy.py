import boto3

s3 = boto3.resource('s3')
bucket_policy = s3.BucketPolicy('mytestbucketforelb')

v = bucket_policy.policy

spl = v.split(',')
count = 0
start = []
end = []

for i in spl:
  if i.startswith('{'):
    start.append(count)
  if i.endswith('}'):
    end.append(count)
  count += 1

print(start)
print(end)
