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
        # ⛔ Skip model loading in CI
        if os.getenv("CI") == "true":
            return

        if self.model is not None:
            return

        s3 = boto3.client("s3")

        if not os.path.exists(self.local_model_path):
            s3.download_file(
                self.bucket_name,
                self.model_key,
                self.local_model_path
            )

        with open(self.local_model_path, "rb") as f:
            self.model = pickle.load(f)


    def predict(self, input_data: dict):
        df = pd.DataFrame([input_data])
        return int(self.model.predict(df)[0])
