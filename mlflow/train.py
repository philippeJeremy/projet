import os
import time
import joblib
import mlflow

import pandas as pd

from sklearn.model_selection import train_test_split
from mlflow.models.signature import infer_signature

from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler, OneHotEncoder 

if __name__ == "__main__":

    print("training model...")
    start_time = time.time()

    EXPERIMENT_NAME="price_car"
    mlflow.set_tracking_uri(os.environ["APP_URI"])
    mlflow.sklearn.autolog() 
    mlflow.set_experiment(EXPERIMENT_NAME)
    experiment = mlflow.get_experiment_by_name(EXPERIMENT_NAME)

    df = pd.read_csv("./data_final.csv")
  
       
    with mlflow.start_run(experiment_id = experiment.experiment_id):

        model.fit(x_train, y_train)

        predictions = model.predict(x_train)
        
        mlflow.sklearn.log_model(
            sk_model=model,
            artifact_path="price_car",
            registered_model_name="price_car_model",
            signature=infer_signature(x_train, predictions)
        )

    # joblib.dump(model, "model.joblib")

    print("...Done!")
    print(f"---Total training time: {time.time()-start_time}")