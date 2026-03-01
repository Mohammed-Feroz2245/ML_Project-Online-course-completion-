# Course Completion ML System

## Problem
Predict whether a student will complete an online course.

## Architecture
- Training: Python + scikit-learn
- Model storage: S3
- API: FastAPI
- Deployment: Docker + ECS
- Retraining: Lambda triggered by S3

## How to Run Locally
docker build ...
docker run ...

## Automation
- Upload dataset to S3 triggers Lambda
- Lambda retrains model
- Model saved back to S3
