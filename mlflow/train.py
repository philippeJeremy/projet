import os
import time
import joblib
import mlflow
import fr_core_news_lg

import numpy as np
import pandas as pd
import tensorflow as tf
import tensorflow_hub as hub
import tensorflow_datasets as tfds

from dotenv import load_dotenv
from spacy.lang.en.stop_words import STOP_WORDS
from sklearn.model_selection import train_test_split
from mlflow.models.signature import infer_signature

from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler, OneHotEncoder, LabelEncoder

nlp = fr_core_news_lg.load()

if __name__ == "__main__":
    load_dotenv()

    APP_URI = "APP_URI"

    print("training model...")
    start_time = time.time()

    EXPERIMENT_NAME="vin"
    mlflow.set_tracking_uri(APP_URI)
    mlflow.sklearn.autolog() 
    mlflow.set_experiment(EXPERIMENT_NAME)
    experiment = mlflow.get_experiment_by_name(EXPERIMENT_NAME)

    df = pd.read_csv("./data_final.csv")
    
    label = LabelEncoder()

    target = label.fit_transform(df["target"])

    xtrain, xval, ytrain, yval = train_test_split(df["plat"], target, test_size=0.3)

    train_data = tf.data.Dataset.from_tensor_slices((xtrain, ytrain))
    val_data = tf.data.Dataset.from_tensor_slices((xval, yval))


    embedding = "https://tfhub.dev/google/nnlm-en-dim50/2"
    hub_layer = hub.KerasLayer(embedding, input_shape=[], 
                           dtype=tf.string, trainable=True)
    
    model = tf.keras.Sequential()
    model.add(hub_layer)
    model.add(tf.keras.layers.Dense(16, activation='relu'))
    model.add(tf.keras.layers.Dense(1))

    model.compile(optimizer='adam',
              loss=tf.keras.losses.CategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])



    with mlflow.start_run(experiment_id = experiment.experiment_id):
      
        model.fit(train_data.shuffle(1000).batch(16),
                    epochs=10,
                    validation_data=val_data.batch(16),
                    verbose=1)

        predictions = model.predict(val_data)
        
        mlflow.sklearn.log_model(
            sk_model=model,
            artifact_path="vin",
            registered_model_name="vin_model",
            signature=infer_signature(train_data, predictions)
        )

    joblib.dump(model, "model.joblib")

    print("...Done!")
    print(f"---Total training time: {time.time()-start_time}")