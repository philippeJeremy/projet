import os
import time
import mlflow
import fr_core_news_lg

import numpy as np
import pandas as pd
import tensorflow as tf
# import tensorflow_hub as hub


from spacy.lang.fr.stop_words import STOP_WORDS
from sklearn.model_selection import train_test_split
from mlflow.models.signature import infer_signature

from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler, OneHotEncoder, LabelEncoder

nlp = fr_core_news_lg.load()

if __name__ == "__main__":

    print("training model...")
    start_time = time.time()

    EXPERIMENT_NAME = "vin"
    mlflow.set_tracking_uri(os.environ["APP_URI"])
    mlflow.tensorflow.autolog()
    mlflow.set_experiment(EXPERIMENT_NAME)
    experiment = mlflow.get_experiment_by_name(EXPERIMENT_NAME)

    df = pd.read_csv("./data_plus.csv")

    df["plat_clean"] = df["plat"].apply(lambda x: ''.join(
        ch for ch in x if ch.isalnum() or ch == " "))
    df["plat_clean"] = df["plat_clean"].apply(
        lambda x: x.replace(" +", " ").lower().strip())
    df["plat_clean"] = df["plat_clean"].apply(lambda x: " ".join(
        token.text for token in nlp(x) if token.text not in STOP_WORDS))
    label = LabelEncoder()
    df['target_encoded'] = label.fit_transform(df["target"])

    mask = df["plat_clean"].isna() == False
    df = df[mask]

    tokenizer = tf.keras.preprocessing.text.Tokenizer(
        num_words=1000)  # instanciate the tokenizer
    tokenizer.fit_on_texts(df["plat_clean"])
    df["plat_encoded"] = tokenizer.texts_to_sequences(df.plat_clean)
    df["len_plat"] = df["plat_encoded"].apply(lambda x: len(x))
    df = df[df["len_plat"] != 0]

    plat_pad = tf.keras.preprocessing.sequence.pad_sequences(
        df.plat_encoded, padding="post")

    full_ds = tf.data.Dataset.from_tensor_slices(
        (plat_pad, df['target_encoded'].values))

    TAKE_SIZE = int(0.7*df.shape[0])

    train_data = full_ds.take(TAKE_SIZE).shuffle(TAKE_SIZE)
    train_data = train_data.batch(64)

    test_data = full_ds.skip(TAKE_SIZE)
    test_data = test_data.batch(64)

    for plat, target in train_data.take(1):
        plat, target

    vocab_size = len(tokenizer.word_index)
    model = tf.keras.Sequential([
        tf.keras.layers.Embedding(
            vocab_size+1, 256, input_shape=[plat.shape[1],], name="embedding"),
        tf.keras.layers.LSTM(units=256, return_sequences=True),
        tf.keras.layers.Dropout(0.3),
        tf.keras.layers.LSTM(units=128, return_sequences=False),
        tf.keras.layers.Dropout(0.3),
        tf.keras.layers.Dense(64, activation='selu'),
        tf.keras.layers.Dropout(0.2),
        tf.keras.layers.Dense(32, activation='selu'),
        tf.keras.layers.Dropout(0.2),
        tf.keras.layers.Dense(32, activation='selu'),

        tf.keras.layers.Dense(17, activation="softmax", name="last")
    ])

    optimizer = tf.keras.optimizers.Adam(learning_rate=0.001)

    model.compile(optimizer='adam',
                  loss=tf.keras.losses.SparseCategoricalCrossentropy(
                      from_logits=True),
                  metrics=[tf.keras.metrics.SparseCategoricalAccuracy()])

    weights = 1/(df["target_encoded"]).value_counts()
    weights = weights * len(df)/17
    weights = {index: values for index,
               values in zip(weights.index, weights.values)}

    with mlflow.start_run(experiment_id=experiment.experiment_id):

        model.fit(train_data,
                  epochs=10,
                  validation_data=test_data,
                  class_weight=weights,
                  verbose=1)

# joblib.dump(model, "model.joblib")

    print("...Done!")
    print(f"---Total training time: {time.time()-start_time}")
