# LambdaSamples
log_fliter is used to filter logs that is internal access of aws, just keep access logs from remote IP addresses.

lambda role permission: fulls3, cloudwatch

log_filter.py trigger: when s3 object is created

log_filer_per_hour.py trigger: cloudwatch scheduled events: corn(0 * * * ? *)

