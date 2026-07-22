import boto3
from datetime import datetime, timezone

# script to tag old files so the compliance team can review them before manual deletion.
# TODO: move the threshold days to an env variable later.
def tag_old_files(bucket, prefix, threshold_days=90):
    s3 = boto3.client('s3')
    now = datetime.now(timezone.utc)
    
    paginator = s3.get_paginator('list_objects_v2')
    pages = paginator.paginate(Bucket=bucket, Prefix=prefix)
    
    count = 0
    for page in pages:
        if 'Contents' not in page:
            continue
            
        for obj in page['Contents']:
            days_old = (now - obj['LastModified']).days
            
            if days_old > threshold_days:
                # print(f"tagging {obj['Key']}") # debug
                s3.put_object_tagging(
                    Bucket=bucket,
                    Key=obj['Key'],
                    Tagging={
                        'TagSet': [
                            {'Key': 'AuditStatus', 'Value': 'Pending'},
                            {'Key': 'DaysOld', 'Value': str(days_old)}
                        ]
                    }
                )
                count += 1
                
    return count
