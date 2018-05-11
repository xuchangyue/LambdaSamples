import re
import boto3
# Trigger for this function is CloudWatch Scheduled Events

internalIp = ['xxx.xxx.xxx.xxx']
new_log_bucket_name = 'fakelogs'
all_log_bucket_name = 'allfakelogs'
filtered_log_bucket_name = 'fakelogs-filtered'

s3_resource = boto3.resource('s3')
all_bucket = s3_resource.Bucket(all_log_bucket_name)
src_bucket = s3_resource.Bucket(new_log_bucket_name)
filtered_bucket = s3_resource.Bucket(filtered_log_bucket_name)


def logfilter(file_path, filtered_path):
    f = open(file_path, 'r')
    w = open(filtered_path, 'a')
    patternip = '|'.join(internalIp)
    pattern = '.*(' + patternip + ').*'
    for line in f.readlines():
        if not re.match(pattern, line):
            w.write(line)
    f.close()
    w.close()


def lambda_handler(event, context):
    for obj in src_bucket.objects.all():
        download_path = '/tmp/{}'.format(obj.key)
        upload_path = '/tmp/filtered-{}'.format(obj.key[0:13])
        logfilter(download_path, upload_path)
        s3_resource.Object(filtered_log_bucket_name, obj.key[0:13]).upload_file(upload_path)
        copy_source = {
            'Bucket': new_log_bucket_name,
            'Key': obj.key
        }
        new_obj = all_bucket.Object(obj.key)
        new_obj.copy(copy_source)
        obj.delete()
