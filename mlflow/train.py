import os
import time
import mlflow
import fr_core_news_lg

import numpy as np
import pandas as pd
import tensorflow as tf
import tensorflow_hub as hub


from mlflow.models.signature import infer_signature
from sklearn.model_selection import train_test_split
from mlflow.models.signature import infer_signature

from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler, OneHotEncoder, LabelEncoder


if __name__ == "__main__":

    print("training model...")
    start_time = time.time()

    EXPERIMENT_NAME = "vin"
    mlflow.set_tracking_uri(os.environ["APP_URI"])
    mlflow.sklearn.autolog()
    mlflow.set_experiment(EXPERIMENT_NAME)
    experiment = mlflow.get_experiment_by_name(EXPERIMENT_NAME)

    df = pd.read_csv("./data_final.csv")
    label = LabelEncoder()
    df['target_encoded'] = label.fit_transform(df["target"])

    X_train, X_test, y_train, y_test = train_test_split(df["plat"], df["target"], test_size=0.3)

    train_data = tf.data.Dataset.from_tensor_slices((X_train, y_train))
    val_data = tf.data.Dataset.from_tensor_slices((X_test, y_test))   

    embedding = "https://tfhub.dev/google/nnlm-en-dim50/2"
    hub_layer = hub.KerasLayer(embedding, input_shape=[],
                               dtype=tf.string, trainable=True)

    model = tf.keras.Sequential()
    model.add(hub_layer)
    model.add(tf.keras.layers.Dense(32, activation='relu'))
    model.add(tf.keras.layers.Dense(13, activation="softmax", ))
    model.compile(optimizer='adam',
                  loss=tf.keras.losses.SparseCategoricalCrossentropy(),
                  metrics=['accuracy'])

    model.fit(train_data.shuffle(10000).batch(512),
              epochs=1,
              validation_data=val_data.batch(512),
              verbose=1)
    mlflow.tensorflow.log_model(model, 'models.joblib')

    mlflow.set_tag("developer", "jeremy")

    print("Fit model on training data")

    # joblib.dump(model, "model.joblib")
