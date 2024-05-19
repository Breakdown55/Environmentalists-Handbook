import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import pathlib

file = (str(pathlib.Path(__file__).parent.resolve())+"/Dirt Data/")

csv_files = [
    file + "lowFert.csv",
    file + "midFert.csv",
    file + "highFert.csv"
]

all_data = []


for file in csv_files:
    data = pd.read_csv(file)
    all_data.append(data)


data = pd.concat(all_data, ignore_index=True)

X = data[['N', 'pH', 'EC', 'Zn', 'Fe']]  
y = data['Output']


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


model = LinearRegression()

model.fit(X_train, y_train)

y_pred = model.predict(X_test)

mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print('Mean Squared Error:', mse)
print('R-squared:', r2)


def run_model(N, pH, EC, Zn, Fe):
    new_data = pd.DataFrame({
        'N': [N],
        'pH': [pH],
        'EC': [EC],
        'Zn': [Zn],
        'Fe': [Fe]
    })

    return model.predict(new_data)