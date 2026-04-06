import os
import boto3
import pickle
import tempfile
import pandas as pd
from pathlib import Path


class CourseCompletionModel:
    def __init__(self, skip_loading: bool = False):
        # ✅ ENV-based bucket name (best practice)
        self.bucket_name = os.getenv("S3_BUCKET", "course-completion-ml-artifacts")
        self.model_key = "artifacts/model.pkl"
        self.local_model_path = Path(tempfile.gettempdir()) / "model.pkl"
        self.model = None
        self.skip_loading = skip_loading  # for testing

    def load_model(self):
        if self.skip_loading:
            return

        if self.model is not None:
            return

        try:
            s3 = boto3.client("s3", region_name="eu-north-1")

            # Download only if not exists
            if not self.local_model_path.exists():
                s3.download_file(
                    self.bucket_name,
                    self.model_key,
                    str(self.local_model_path)
                )

            # Load model
            with open(self.local_model_path, "rb") as f:
                self.model = pickle.load(f)

        except Exception as e:
            print(f"Error loading model: {e}")

    def predict(self, input_data: dict):
        if self.model is None:
            if self.skip_loading:
                return 0  # safe fallback for tests
            self.load_model()
            if self.model is None:
                raise RuntimeError("Model could not be loaded.")

        mapped_data = {
            'age': input_data['age'],
            'hours_per_week': input_data['hours_per_week'],
            'assignments_submitted': input_data['assignments_submitted'],
            'Mobile': input_data['mobile'],
            'Pager': input_data['pager'],
            'Smart TV': input_data['smart_tv'],
            'Tablet': input_data['tablet']
        }

        df = pd.DataFrame([mapped_data])

        expected_order = [
            'age',
            'hours_per_week',
            'assignments_submitted',
            'Mobile',
            'Pager',
            'Smart TV',
            'Tablet'
        ]

        df = df[expected_order]

        return int(self.model.predict(df)[0])