import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df_train = pd.read_csv("train.csv")
df_test = pd.read_csv("test.csv")

sns.set(style="whitegrid")

def analiza_valori_lipsa(df, nume):
    print(f"\n {nume} - Valori lipsa:")
    lipseste = df.isnull().sum()
    procent = (lipseste * len(df)) / 100
    print(pd.DataFrame({"Valori lipsa": lipseste, "Procent": procent}))

analiza_valori_lipsa(df_train, 1)
analiza_valori_lipsa(df_test, 2)

print("Statistici numerice 1:")
print(df_train.describe())

print("Statistici categorice:")
print(df_train.select_dtypes(include = 'object').describe())

plt.figure()
sns.histplot(df_train["dimensiune"], kde = True, bins = 30)
plt.title(f"Distributia dimensiunii emailurilor")
plt.xlabel("Dimensiune cuvinte")
plt.ylabel("Cantitate")
plt.show()

plt.figure()
sns.countplot(x = "attachments", data = df_train)
plt.title(f"Distributie atasamente")
plt.xlabel("Are atasament")
plt.ylabel("Cantitate")
plt.show()

plt.figure()
sns.boxplot(x = df_train["semne_exclamare"])
plt.title(f"Boxplot: semne exclamare")
plt.xlabel("Numar semne de exclamare")
plt.show()

plt.figure(figsize=(8,6))
num = ["dimensiune", "numar_linkuri", "semne_exclamare", "litere_mari", "oferte"]
sns.heatmap(df_train[num + ["e_spam"]].corr(), annot=True, cmap="coolwarm")
plt.title("Matrice de corelatie")
plt.show()

plt.figure()
sns.violinplot(x="e_spam", y = "numar_linkuri", data = df_train)
plt.title("Numar linkuri vs spam")
plt.xlabel("Este spam (0 = nu, 1 = da)")
plt.ylabel("Numar linkuri")
plt.show()