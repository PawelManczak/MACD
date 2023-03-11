import csv
import matplotlib.pyplot as plt
import pandas as pd


class Diagram:
    N = 1000
    ALFA = 0
    x = []
    y = []
    MACD = []
    SIGNAL = []

    def __init__(self):
        self.load_data()
        self.ALFA = 2 / (self.N + 1)

    def load_data(self):
        counter = 0
        with open('orlen.csv', 'r') as csvfile:
            plots = csv.reader(csvfile, delimiter=',')

            for row in plots:
                if counter == 0:
                    counter += 1
                    continue
                print(row[0] + " " + row[3])
                self.x.append(row[0])
                self.y.append(float(row[3]))

                self.MACD.append(self.calculate_MACD(counter))
                counter += 1

    def create_orlen_diagram(self):
        # plot with the exchange rate of the Orlen company
        x = pd.to_datetime(self.x)
        DF = pd.DataFrame()
        DF['value'] = self.y
        DF = DF.set_index(x)
        plt.plot(DF)

        DF = pd.DataFrame()
        DF['value'] = self.MACD
        DF = DF.set_index(x)
        plt.plot(DF)

        plt.gcf().autofmt_xdate()
        plt.title('Exchange rate of the Orlen company 2019-2023', fontsize=15)
        plt.xlabel('Date')
        plt.ylabel('Share price')
        plt.show()

    def calculate_MACD(self, counter):
        EMA26 = self.calculate_EMA(26, counter)
        EMA12 = self.calculate_EMA(12, counter)

        return EMA12 - EMA26

    def calculate_EMA(self, amount, counter):
        nominator = 0
        denominator = 0

        if amount > counter:
            amount = counter

        for i in range(amount):
            denominator += pow((1 - self.ALFA), i)
            nominator += denominator * self.y[counter-(i+1)]

        return nominator/denominator


if __name__ == '__main__':
    diagram = Diagram()
    diagram.create_orlen_diagram()
