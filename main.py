import csv
import matplotlib.pyplot as plt
import pandas as pd


# plot with the exchange rate of the Orlen company
x = []
y = []
counter = 0
with open('orlen.csv', 'r') as csvfile:
    plots = csv.reader(csvfile, delimiter=',')

    for row in plots:
        counter += 1
        if counter == 1:
            continue
        print(row[0] + " " + row[3])
        x.append(row[0])
        y.append(float(row[3]))

x = pd.to_datetime(x)
DF = pd.DataFrame()
DF['value'] = y
DF = DF.set_index(x)
plt.plot(DF)
plt.gcf().autofmt_xdate()
plt.title('Exchange rate of the Orlen company 2019-2023', fontsize= 15)
plt.xlabel('Date')
plt.ylabel('Share price')
plt.show()
