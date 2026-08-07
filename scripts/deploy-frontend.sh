#!/bin/bash
# Rebuilds the frontend against the live backend URL and deploys it to Amplify.
set -euo pipefail
cd "$(dirname "$0")/.."

APP_ID="d1yz2bpebssgfc"
BRANCH="main"
REGION="us-east-1"
BACKEND_URL="https://wskv3-backend.cmz0503mqga1c.us-east-1.cs.amazonlightsail.com"

echo "Building frontend..."
cd client
VITE_API_URL="$BACKEND_URL" npm run build
cd ..

TMP_DIR=$(mktemp -d)
trap 'rm -rf "$TMP_DIR"' EXIT
ZIP_PATH="$TMP_DIR/build.zip"

(cd client/dist && zip -rq "$ZIP_PATH" . -x ".*")

echo "Creating deployment..."
DEPLOYMENT=$(aws2 amplify create-deployment --app-id "$APP_ID" --branch-name "$BRANCH" --region "$REGION")
JOB_ID=$(echo "$DEPLOYMENT" | python3 -c "import sys,json; print(json.load(sys.stdin)['jobId'])")
UPLOAD_URL=$(echo "$DEPLOYMENT" | python3 -c "import sys,json; print(json.load(sys.stdin)['zipUploadUrl'])")

echo "Uploading build..."
curl -s -X PUT -T "$ZIP_PATH" "$UPLOAD_URL"

echo "Starting deployment job $JOB_ID..."
aws2 amplify start-deployment --app-id "$APP_ID" --branch-name "$BRANCH" --job-id "$JOB_ID" --region "$REGION" > /dev/null

while true; do
  JOB_STATE=$(aws2 amplify get-job --app-id "$APP_ID" --branch-name "$BRANCH" --job-id "$JOB_ID" --region "$REGION" --query "job.summary.status" --output text)
  echo "  status: $JOB_STATE"
  [ "$JOB_STATE" = "SUCCEED" ] && break
  [ "$JOB_STATE" = "FAILED" ] && { echo "Deployment failed"; exit 1; }
  sleep 10
done

DOMAIN=$(aws2 amplify get-app --app-id "$APP_ID" --region "$REGION" --query "app.defaultDomain" --output text)
echo "Frontend live at: https://$BRANCH.$DOMAIN"
