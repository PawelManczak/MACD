import csv
import matplotlib.pyplot as plt
import pandas as pd


class Diagram:
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
                counter += 1

    def create_orlen_diagram(self):
        # plot with the exchange rate of the Orlen company
        x = pd.to_datetime(self.x)
        DF = pd.DataFrame()
        DF['value'] = self.y
        DF = DF.set_index(x)
        plt.plot(DF)
        plt.gcf().autofmt_xdate()
        plt.title('Exchange rate of the Orlen company 2019-2023', fontsize=15)
        plt.xlabel('Date')
        plt.ylabel('Share price')
        plt.show()


if __name__ == '__main__':
    diagram = Diagram()
    diagram.create_orlen_diagram()
