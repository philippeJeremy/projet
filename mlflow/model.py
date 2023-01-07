import os
import io
import time
import joblib
import mlflow
import fr_core_news_lg

import pandas as pd
import tensorflow as tf 
import plotly.express as px
import matplotlib.pyplot as plt
import plotly.graph_objects as go

from sklearn.model_selection import train_test_split
from mlflow.models.signature import infer_signature
from spacy.lang.fr.stop_words import STOP_WORDS

from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler, OneHotEncoder 

nlp = fr_core_news_lg.load()

if __name__ == "__main__":
    pass