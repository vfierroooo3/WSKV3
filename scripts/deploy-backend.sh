#!/bin/bash
# Rebuilds the Flask backend image, pushes it to Lightsail, and deploys it.
set -euo pipefail
cd "$(dirname "$0")/.."

SERVICE_NAME="wskv3-backend"
REGION="us-east-1"
LABEL="wskv3-server"

set -a
source server/.env
set +a

echo "Building image (linux/amd64)..."
docker build --platform linux/amd64 -t wskv3-server ./server

echo "Pushing image to Lightsail..."
PUSH_OUTPUT=$(aws2 lightsail push-container-image \
  --service-name "$SERVICE_NAME" \
  --label "$LABEL" \
  --image wskv3-server:latest \
  --region "$REGION")

IMAGE_REF=$(echo "$PUSH_OUTPUT" | grep -oE ":${SERVICE_NAME}\.${LABEL}\.[0-9]+" | tail -1)
echo "Registered as $IMAGE_REF"

TMP_DIR=$(mktemp -d)
trap 'rm -rf "$TMP_DIR"' EXIT

cat > "$TMP_DIR/containers.json" <<EOF
{
    "$LABEL": {
        "image": "$IMAGE_REF",
        "ports": { "5000": "HTTP" },
        "environment": { "MONGODB_SERVER": "$MONGODB_SERVER" }
    }
}
EOF

cat > "$TMP_DIR/public-endpoint.json" <<EOF
{
    "containerName": "$LABEL",
    "containerPort": 5000,
    "healthCheck": {
        "path": "/get_hw_info",
        "successCodes": "200-399",
        "intervalSeconds": 10,
        "timeoutSeconds": 5,
        "healthyThreshold": 2,
        "unhealthyThreshold": 3
    }
}
EOF

echo "Deploying to Lightsail..."
aws2 lightsail create-container-service-deployment \
  --service-name "$SERVICE_NAME" \
  --containers "file://$TMP_DIR/containers.json" \
  --public-endpoint "file://$TMP_DIR/public-endpoint.json" \
  --region "$REGION" > /dev/null

echo "Waiting for deployment to go live..."
while true; do
  STATE=$(aws2 lightsail get-container-services --service-name "$SERVICE_NAME" --region "$REGION" --query "containerServices[0].state" --output text)
  echo "  state: $STATE"
  [ "$STATE" = "RUNNING" ] && break
  sleep 10
done

URL=$(aws2 lightsail get-container-services --service-name "$SERVICE_NAME" --region "$REGION" --query "containerServices[0].url" --output text)
echo "Backend live at: $URL"
