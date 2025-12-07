#!/bin/bash

# Optional: make itself executable (safe to run multiple times)
chmod +x deploy.sh

# Stop old container if running
docker stop food-menu-api || true
docker rm food-menu-api || true

# Login to ECR (replace with your region and account ID)
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 712416034180.dkr.ecr.us-east-1.amazonaws.com

# Pull the latest Docker image
docker pull 712416034180.dkr.ecr.us-east-1.amazonaws.com/food-menu-api:latest

# Run the container
docker run -d -p 8000:8000 --name food-menu-api 712416034180.dkr.ecr.us-east-1.amazonaws.com/food-menu-api:latest
