import re
import boto3
# Trigger for this function is When S3 object is created
internalIp = ['xxx.xxx.xxx.xxx']

s3_client = boto3.client('s3')

def logfilter(file_path, filtered_path):
    f = open(file_path, 'r')
    w = open(filtered_path, 'w')
    patternip = '|'.join(internalIp)
    pattern = '.*('+patternip+').*'
    print(pattern)
    for line in f.readlines():
        if not re.match(pattern, line):
            w.write(line)
    f.close()
    w.close()

def lambda_handler(event, context):

    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']
        download_path = '/tmp/{}'.format(key)
        upload_path = '/tmp/filtered-{}'.format(key)

        s3_client.download_file(bucket, key, download_path)
        logfilter(download_path, upload_path)
        
        s3_client.upload_file(upload_path,
             '{}-filtered'.format(bucket),
             'filtered-{}'.format(key))
        
