import pandas as pd

df = pd.read_csv('directions.csv', sep=';', header=None)
print('Увеличение угла по часовой стрелке со знаком +')
try:
    delta = float((input("Введите поправку: ")))
except ValueError:
    print('Введите число в формате 10 или 10.5')
else:
    for i in range(len(df)):
        x = float(df.iloc[i, 2]) + delta
        if x >= 360:
            x -= 360
        elif x < 0:
            x += 360
        df.iloc[i, 2] = round(x, 2)

df.to_csv("directions_upd.csv", sep=';', header=False, index=False)

