import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib

df = pd.read_csv("data/train.csv")

print("=" * 50)
print("FIRST 5 ROWS")
print("=" * 50)
print(df.head())

print("\n")

print("=" * 50)
print("DATASET SHAPE")
print("=" * 50)
print(df.shape)

print("\n")

print("=" * 50)
print("COLUMN NAMES")
print("=" * 50)
print(df.columns)

print("\n")

print("=" * 50)
print("DATASET INFORMATION")
print("=" * 50)
print(df.info())

print("\n")
pd.set_option('display.max_rows', None)
print("=" * 50)
print("MISSING VALUES")
print("=" * 50)
print(df.isnull().sum())

df = df.drop(columns=["PoolQC","MiscFeature","Alley","Fence"])

print("\n")
print("=" * 50)
print("NEW DATASET SHAPE")
print("=" * 50)
print(df.shape)

print("\n")
pd.set_option('display.max_rows', None)
print("=" * 50)
print("MISSING VALUES")
print("=" * 50)
print(df.isnull().sum())

df["LotFrontage"] = df["LotFrontage"].fillna(df["LotFrontage"].median())
df["MasVnrArea"] = df["MasVnrArea"].fillna(df["MasVnrArea"].median())
df["Electrical"] = df["Electrical"].fillna(df["Electrical"].mode()[0])

basement_columns = [
    "BsmtQual",
    "BsmtCond",
    "BsmtExposure",
    "BsmtFinType1",
    "BsmtFinType2"
]

for column in basement_columns:
    df[column] = df[column].fillna("None")


garage_columns = [
    "GarageType",
    "GarageFinish",
    "GarageQual",
    "GarageCond"
]

for column in garage_columns:
    df[column] = df[column].fillna("None")


df["GarageYrBlt"] = df["GarageYrBlt"].fillna(df["GarageYrBlt"].median())

df = pd.get_dummies(df, drop_first=True)

print("\n")
print("=" * 50)
print("DATASET SHAPE AFTER ENCODING")
print("=" * 50)
print(df.shape)

X = df.drop("SalePrice", axis=1)
y = df["SalePrice"]

print("\n")
print("=" * 50)
print("FEATURES SHAPE")
print("=" * 50)
print(X.shape)

print("\n")
print("=" * 50)
print("TARGET SHAPE")
print("=" * 50)
print(y.shape)

X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.2,random_state=42)

print("\n")
print("=" * 50)
print("TRAINING DATA")
print("=" * 50)
print(X_train.shape)
print(y_train.shape)

print("\n")
print("=" * 50)
print("TESTING DATA")
print("=" * 50)
print(X_test.shape)
print(y_test.shape)

model = LinearRegression()
model.fit(X_train, y_train)
predictions = model.predict(X_test)

print("\n")

print("=" * 50)
print("FIRST 10 PREDICTIONS")
print("=" * 50)
print(predictions[:10])

mae = mean_absolute_error(y_test, predictions)
mse = mean_squared_error(y_test, predictions)
rmse = mse ** 0.5
r2 = r2_score(y_test, predictions)

print("\n")
print("=" * 50)
print("LINEAR REGRESSION RESULTS")
print("=" * 50)

print("MAE :", mae)
print("MSE :", mse)
print("RMSE:", rmse)
print("R2  :", r2)

tree_model = DecisionTreeRegressor(max_depth=5,random_state=42)
tree_model.fit(X_train, y_train)
tree_predictions = tree_model.predict(X_test)

tree_mae = mean_absolute_error(y_test, tree_predictions)
tree_mse = mean_squared_error(y_test, tree_predictions)
tree_rmse = tree_mse ** 0.5
tree_r2 = r2_score(y_test, tree_predictions)

print("\n")
print("=" * 50)
print("DECISION TREE RESULTS")
print("=" * 50)

print("MAE :", tree_mae)
print("MSE :", tree_mse)
print("RMSE:", tree_rmse)
print("R2  :", tree_r2)

train_predictions = tree_model.predict(X_train)
train_r2 = r2_score(y_train, train_predictions)

print("\n")
print("=" * 50)
print("DECISION TREE TRAINING R2")
print("=" * 50)
print(train_r2)

forest_model = RandomForestRegressor(n_estimators=100,random_state=42)
forest_model.fit(X_train, y_train)
forest_predictions = forest_model.predict(X_test)

forest_mae = mean_absolute_error(y_test, forest_predictions)
forest_mse = mean_squared_error(y_test, forest_predictions)
forest_rmse = forest_mse ** 0.5
forest_r2 = r2_score(y_test, forest_predictions)

print("\n")
print("=" * 50)
print("RANDOM FOREST RESULTS")
print("=" * 50)

print("MAE :", forest_mae)
print("MSE :", forest_mse)
print("RMSE:", forest_rmse)
print("R2  :", forest_r2)

joblib.dump(forest_model, "models/house_price_model.pkl")
joblib.dump(X.columns.tolist(), "models/model_columns.pkl")

