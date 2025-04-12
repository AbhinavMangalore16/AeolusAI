import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
import joblib


def create_features(df: pd.DataFrame, save_path: str = None):
    """
    Apply feature engineering steps to the input dataframe.

    Parameters:
    df (pd.DataFrame): The raw input dataframe
    save_path (str): If provided, the pipeline will be saved to this path

    Returns:
    pd.DataFrame: Transformed dataframe ready for modeling
    """

    if 'datetime' in df.columns:
        df['datetime'] = pd.to_datetime(df['datetime'])
        df['hour'] = df['datetime'].dt.hour
        df['dayofweek'] = df['datetime'].dt.dayofweek


    numeric_features = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
    categorical_features = df.select_dtypes(include=['object', 'category']).columns.tolist()


    if 'target' in numeric_features:
        numeric_features.remove('target')
    if 'target' in categorical_features:
        categorical_features.remove('target')


    numeric_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())
    ])

    categorical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='most_frequent')),
        ('onehot', OneHotEncoder(handle_unknown='ignore'))
    ])

    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, numeric_features),
            ('cat', categorical_transformer, categorical_features)
        ]
    )

    pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor)
    ])

    df_transformed = pipeline.fit_transform(df)

    if save_path:
        joblib.dump(pipeline, save_path)

    return df_transformed