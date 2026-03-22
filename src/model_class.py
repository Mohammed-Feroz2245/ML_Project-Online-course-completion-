import boto3
import pickle
import os
import pandas as pd

class CourseCompletionModel:
    def __init__(self):
        self.bucket_name = "course-completion-ml-artifacts"
        self.model_key = "artifacts/model.pkl"
        self.local_model_path = "/tmp/model.pkl"
        self.model = None

    def load_model(self):
        # Skip model loading in CI environment
        if os.getenv("CI") == "true":
            return

        if self.model is not None:
            return

        s3 = boto3.client("s3", region_name="eu-north-1")

        try:
            if not os.path.exists(self.local_model_path):
                print(f"Downloading model from {self.bucket_name}...")
                s3.download_file(
                    self.bucket_name,
                    self.model_key,
                    self.local_model_path
                )

            with open(self.local_model_path, "rb") as f:
                self.model = pickle.load(f)
            print("Model loaded successfully.")
        except Exception as e:
            print(f"Error loading model: {e}")

    def predict(self, input_data: dict):
        if self.model is None:
            self.load_model()
        
        # 1. Map the API input names to the Training column names
        # This ensures 'mobile' becomes 'Mobile', etc.
        mapped_data = {
            'age': input_data['age'],
            'hours_per_week': input_data['hours_per_week'],
            'assignments_submitted': input_data['assignments_submitted'],
            'Mobile': input_data['mobile'],
            'Pager': input_data['pager'],
            'Smart TV': input_data['smart_tv'],
            'Tablet': input_data['tablet']
        }
        
        # 2. Convert to DataFrame
        df = pd.DataFrame([mapped_data])
        
        # 3. Ensure columns are in the EXACT order the model expects
        # (Note: 'Desktop' is usually dropped by drop_first=True in training)
        expected_order = [
            'age', 'hours_per_week', 'assignments_submitted', 
            'Mobile', 'Pager', 'Smart TV', 'Tablet'
        ]
        df = df[expected_order]
        
        return int(self.model.predict(df)[0])