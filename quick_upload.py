import boto3

# Let's use Amazon S3
s3 = boto3.resource('s3')

# Print out bucket names
for bucket in s3.buckets.all():
    print(bucket.name)

# Upload a new file
data = open('/home/pi/images/diybio_2016-07-13_01_10_54.139134.jpg', 'rb')
s3.Bucket('familabbiocam').put_object(Key='test.jpg', Body=data)
