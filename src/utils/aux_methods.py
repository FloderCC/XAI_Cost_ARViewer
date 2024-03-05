import json
import pandas as pd
from pandas import DataFrame


def divide_dataframe_regarding_mcc(df: DataFrame):
    condition = df['MCC'] > 0.8
    return {
        'high-performance': df[condition],
        'low-performance': df[~condition]
    }

def generate_correlation_matrices(json_file_path, mode):
    with open(json_file_path, 'r') as file:
        data = json.load(file)

    correlation_matrices = {}

    for first_key, second_level in data.items():
        correlation_matrices[first_key] = {}

        for second_key, third_level in second_level.items():
            for third_key, fourth_level in third_level.items():
                second_level[second_key][third_key] = second_level[second_key][third_key][mode]

        for second_key, third_level in second_level.items():
            # Convert the third level values into a DataFrame
            df = pd.DataFrame(third_level)

            # renaming columns
            df.rename(columns={'LIME (ALL)': 'LIME'}, inplace=True)
            df.rename(columns={'Permutation Importance': 'PI'}, inplace=True)

            # Calculate the correlation matrix
            correlation_matrix = df.corr()

            # Store the correlation matrix in the result dictionary
            correlation_matrices[first_key][second_key] = correlation_matrix

    return correlation_matrices

def get_correlation_level(value):
    if value > 0.75: return 'High Positive Correlation (p > 0.75)'
    if value > 0.25: return 'Positive Correlation (p>0.25)'
    if value < -0.75: return 'High Negative Correlation (p < -0.75)'
    if value < -0.25: return 'Negative Correlation (p<-0.25)'
    return 'No Meaningful Relationship (-0.25< p <0.25)'