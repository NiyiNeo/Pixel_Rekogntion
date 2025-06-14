# Amazon Rekognition Image Labeling CI/CD Pipeline

This project implements a CI/CD workflow that:

- Uploads images to an Amazon S3 bucket
- Calls Amazon Rekognition to detect labels
- Logs structured results (filename, labels with confidence, timestamp, branch) into DynamoDB
- Uses GitHub Actions to automate labeling on pull request and main branch merge

# AWS Resources Setup

** 1. **S3 Bucket****
  Create a bucket to store images for Rekognition.
  Use a folder prefix like rekognition-input/ for uploaded images.

**2. DynamoDB Tables**
  Create two tables:
  DYNAMODB_TABLE_BETA (for pull requests)
  DYNAMODB_TABLE_PROD (for production/merges)
  
  Each table must have:
  Primary key: filename (String)
  Repeat for DYNAMODB_TABLE_PROD
  ***NOTE: Amazon Rekognition is a managed service. Ensure your IAM user has rekognition:DetectLabels permission.

**3 .GitHub Secrets Configuration**
  In your GitHub repo → Settings → Secrets and variables → Actions → New repository secret and their value.
  Add the following:
  AWS_ACCESS_KEY_ID	
  AWS_SECRET_ACCESS_KEY	
  AWS_REGION	
  S3_BUCKET	
  DYNAMODB_TABLE_BETA	
  DYNAMODB_TABLE_PROD	

**No credentials are hardcoded — everything is injected securely via GitHub Actions.**

**4. Add Images**
  Put your images into the images/ folder of your repo.
  images/
  ├── audi_q5.jpeg
  └── desktop.jpg

**5. Create a Pull Request**
  Open a PR into the main branch.
  This triggers the on_pull_request.yml workflow.
  Images are uploaded to S3 and analyzed.
  Results are written to DYNAMODB_TABLE_BETA.
  
  Merge to Main - Merging to main triggers on_merge.yml.
  Results are written to DYNAMODB_TABLE_PROD.

**6.Verify Data in DynamoDB**
  Go to AWS DynamoDB Console
  Select the appropriate table (DYNAMODB_TABLE_BETA or PROD)
  Click Explore table items
  Look for entries with:
  filename: e.g., rekognition-input/audi_q5.jpeg
  branch: name of the Git branch used
  timestamp: when the job ran
  labels: list of objects with Name and Confidence






