import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder

df_train = pd.read_csv("train.csv")
df_test = pd.read_csv("test.csv")

ceva = LabelEncoder()
df_train["attachments"] = ceva.fit_transform(df_train["attachments"])
df_test["attachments"] = ceva.transform(df_test["attachments"])

df_train["domeniu"] = ceva.fit_transform(df_train["domeniu"])
df_test["domeniu"] = ceva.transform(df_test["domeniu"])

x_train = df_train.drop("e_spam", axis = 1)
y_train = df_train["e_spam"]

x_test = df_test.drop("e_spam", axis = 1)
y_test = df_test["e_spam"]

model = RandomForestClassifier(random_state=42)
model.fit(x_train, y_train)

accuracy = model.score(x_test, y_test)
print(f"{int(accuracy * 100)}%")