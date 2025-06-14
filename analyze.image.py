import boto3
import os
from datetime import datetime
from decimal import Decimal

# Environment Variables for GitHub Secrets
s3_bucket = os.environ['S3_BUCKET']
branch = os.environ.get("BRANC_NAME", "not-main")
env = os.environ.get('DEPLOY_ENV', 'beta')
table_name = os.environ['DYNAMODB_TABLE_BETA'] if env == 'beta' else os.environ['DYNAMODB_TABLE_PROD']
print("S3_BUCKET =", os.environ.get('S3_BUCKET'))

#AWS Clients from GitHub Secrets
session = boto3.Session(
    aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
    aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'],
    region_name=os.environ.get('AWS_DEFAULT_REGION', 'us-east-1')
)
s3 = session.client('s3')
rekognition = session.client('rekognition')
dynamodb = session.resource('dynamodb')
table = dynamodb.Table(table_name)

# Upload and Store Labels for Images
def process_image(local_path, s3_key):
    s3.upload_file(local_path, s3_bucket, s3_key)
    labels = rekognition.detect_labels(
        Image={'S3Object': {'Bucket': s3_bucket, 'Name': s3_key}},
        MaxLabels=10
    )['Labels']

    structured = [
        {
            'Name': l['Name'], 
            'Confidence': Decimal(str(round(l['Confidence'], 2)))
            } for l in labels
    ]
    table.put_item(Item={
        'filename': s3_key,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'branch': branch,
        'labels': structured
    })
    print(f"✅ Processed {s3_key}")

#Main
def main():
    images = {
        'images/audi_q5.jpeg': 'rekognition-input/audi_q5.jpeg',
        'images/desktop.jpg': 'rekognition-input/desktop.jpg'
    }
    for local, remote in images.items():
        process_image(local, remote)

if __name__ == '__main__':
    main()




