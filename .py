# crée une db qui represante date close et volume
# pour chaque ticker
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

dfapl = pd.read_csv("appl_1d.csv")

pd.set_option('display.float_format', lambda x: '%.3f' % x)

dfapl['time'] = pd.to_datetime(dfapl['time'], unit='s')



print (dfapl)

dfapl = dfapl.drop("Volume MA", axis=1)
dfapl.dropna(inplace=True)
dfapl = dfapl[(dfapl != 0).all(axis=1)]
dfapl.set_index("time", inplace=True)

print(dfapl.loc["2021-01-01":"2022-05-31"])


plt.plot(dfapl.index, dfapl["close"])

dfapl["200ma"] = dfapl["close"].rolling(200).mean()
dfapl["50ma"] = dfapl["close"].rolling(50).mean()

plt.plot(dfapl.index, dfapl["50ma"], color="red")
plt.plot(dfapl.index, dfapl["200ma"], color="green")



plt.legend(["close", "200ma", "50ma"])  

dfapl["buy"] = [1 if dfapl.loc[day, "50ma"] > dfapl.loc[day, "200ma"] else 0 for day in dfapl.index]
dfapl["sell"] = [1 if dfapl.loc[day, "50ma"] < dfapl.loc[day, "200ma"] else 0 for day in dfapl.index]

print(dfapl)
plt.plot(dfapl.index, dfapl["buy"], color="green")
plt.plot(dfapl.index, dfapl["sell"], color="red")




balance = 1000
position = None

# Initialiser une liste pour stocker les balances
balances = []

for index, row in dfapl.iterrows():
    if row["buy"] == 1 and position == None:
        buy_price = row["close"]
        usd_size = balance
        position = {"buy_price": buy_price, "usd_size": usd_size}
        print(f"buy apple at {buy_price}$ for {usd_size}$")
    elif row["sell"] == 1 and position != None:
        sell_price = row["close"]
        trade = (sell_price - position["buy_price"]) / position["buy_price"]
        balance = balance + trade * position["usd_size"]
        print(f"sell apple at {sell_price}$ for {usd_size}$ ({round(trade * 100, 2)}%)")
        position = None

    # Ajouter la balance actuelle à la liste
    balances.append(balance)

# Ajouter la colonne des balances au DataFrame
dfapl['balance'] = balances

# Tracer le volume en fonction du temps
dfapl.reset_index().plot(x="time", y="volume", color="red", figsize=(10, 7), kind="scatter", marker="x", s=10)

# Tracer la balance en fonction du temps
dfapl.reset_index().plot(x="time", y="balance", color="blue", figsize=(10, 7))

# Afficher le graphique
plt.show()



plt.show()

