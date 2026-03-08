import pandas as pd
import numpy as np

#pentru o obtine ac set de date cand rulam codul
np.random.seed(42)

#
total = 800
rata_spam = 0.35
numar_spam = int(total * 0.35)
numar_non_spam = total - numar_spam

def generare_email(n, spam = True):
    data = {
        "dimensiune": np.random.normal(loc=300 if spam else 150, scale = 50, size = n).astype(int),
        "numar_linkuri": np.random.poisson(3 if spam else 1, size = n),
        "attachments": np.random.choice(["da", "nu"], size = n, p = [0.7, 0.3] if spam else [0.2, 0.8]),
        "semne_exclamare": np.random.poisson(5 if spam else 1, size = n),
        "domeniu": np.random.choice(["spamdomain.com", "freegames.biz", "gmail.com", "yahoo.com", "ubisoft.com"],
        size = n, p = [0.4, 0.2, 0.15, 0.15, 0.1] if spam else [0.05, 0.05, 0.4, 0.3, 0.2]),
        "litere_mari": np.random.poisson(10 if spam else 2, size = n),
        "oferte": np.random.choice([1, 0], size = n, p = [0.8, 0.2] if spam else [0.1, 0.9]),
        "e_spam": [1 if spam else 0] * n
    }
    return pd.DataFrame(data)

df_spam = generare_email(numar_spam, spam=True)
df_non_spam = generare_email(numar_non_spam, spam=False)

df_all = pd.concat([df_spam, df_non_spam], ignore_index = True)
df_all = df_all.sample(frac = 1, random_state = 42).reset_index(drop = True)

df_train = df_all.iloc[:500]
df_test = df_all.iloc[500:700]

df_train.to_csv("train.csv", index = False)
df_test.to_csv("test.csv", index = False)

print("Data au fost salvate in csv-uri.")
