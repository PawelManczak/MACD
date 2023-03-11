import csv
import math

import matplotlib.pyplot as plt
import pandas as pd


class Diagram:
    # simulation params
    money = 1000
    factor = 2
    amount_of_shares = 0

    x = []
    y = []
    MACD = []
    SIGNAL = []

    def __init__(self):
        self.load_data()

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
                self.SIGNAL.append(self.calculate_SIGNAL(counter))
                self.simulation_step(counter)
                counter += 1

    def show_dialogs(self):
        plt.show()

    def create_orlen_diagram(self):
        plt.figure(1)
        # plot with the exchange rate of the Orlen company
        self.x = pd.to_datetime(self.x)
        DF = pd.DataFrame()
        DF['value'] = self.y
        DF = DF.set_index(self.x)
        plt.plot(DF)

        plt.gcf().autofmt_xdate()
        plt.title('Exchange rate of the Orlen company 2019-2023', fontsize=15)
        plt.xlabel('Date')
        plt.ylabel('Share price')

    def create_MACD_diagram(self):
        plt.show(block=False)
        plt.figure(2)
        DF1 = pd.DataFrame()
        DF1['value'] = self.MACD
        DF1 = DF1.set_index(self.x)
        plt.plot(DF1)

        DF1 = pd.DataFrame()
        DF1['value'] = self.SIGNAL
        DF1 = DF1.set_index(self.x)
        plt.plot(DF1)

        plt.gcf().autofmt_xdate()

    def calculate_MACD(self, counter):
        EMA26 = self.calculate_EMA(26, counter, self.y)
        EMA12 = self.calculate_EMA(12, counter, self.y)

        return EMA12 - EMA26

    def calculate_EMA(self, amount, counter, array):

        nominator = 0
        denominator = 0

        if amount > counter:
            amount = counter

        alfa = 2 / (amount + 1)

        for i in range(amount):
            denominator += pow((1 - alfa), i)
            nominator += pow((1 - alfa), i) * array[counter - 2 - i]

        return nominator / denominator

    def calculate_SIGNAL(self, counter):
        return self.calculate_EMA(9, counter, self.MACD)

    def simulation_step(self, counter):
        if counter == 1:
            return

        counter -= 1
        if self.MACD[counter] > self.SIGNAL[counter] and self.MACD[counter - 1] < self.SIGNAL[counter - 1]:
            # sell some shares
            drop_factor = abs(self.MACD[counter] - self.SIGNAL[counter])
            shares_to_sell = math.ceil(drop_factor * self.factor)

            if shares_to_sell > self.amount_of_shares:
                shares_to_sell = self.amount_of_shares

            # sell
            self.money += shares_to_sell * self.y[counter]
            self.amount_of_shares -= shares_to_sell

        elif self.MACD[counter] < self.SIGNAL[counter] and self.MACD[counter - 1] > self.SIGNAL[counter - 1]:
            # buy some shares
            growth_factor = abs(self.MACD[counter] - self.SIGNAL[counter])
            shares_to_buy = math.ceil(growth_factor * self.factor)
            price = shares_to_buy * self.y[counter]

            if price > self.money:
                shares_to_buy = math.floor(self.money / price)

            # sell
            self.money -= shares_to_buy * self.y[counter]
            self.amount_of_shares += shares_to_buy


if __name__ == '__main__':
    diagram = Diagram()
    diagram.create_orlen_diagram()
    diagram.create_MACD_diagram()
    # diagram.show_dialogs()
    print(diagram.money)
