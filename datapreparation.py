import pandas as pd
import numpy as np


class DataPreparation:
    def __init__(self, file, train):
        self.file = pd.read_csv(file, header=None)
        self.train = train
        self.i = int(self.train * len(self.file))
        self.stock_train = self.file[0: self.i]
        self.stock_test = self.file[self.i:]
        self.input_train = []
        self.output_train = []
        self.input_test = []
        self.output_test = []

    def gen_train(self, seq_len):
        """
        Generates training data
        X_train - 2 dimension array, each row is the continuous values of seg_len
        Y_train is the price of the next day for prediction
        :param seq_len: length of window
        :return: X_train and Y_train
        """
        for i in range(len(self.stock_train) - seq_len):
            x = np.array(self.stock_train.iloc[i: i + seq_len, 1])
            y = np.array([self.stock_train.iloc[i + seq_len, 1]], np.float64)
            self.input_train.append(x)
            self.output_train.append(y)
        self.X_train = np.array(self.input_train)
        self.Y_train = np.array(self.output_train)

    def gen_test(self, seq_len):
        """
        Generates test data
        X_test - 2 dimension array, each row is the continuous values of seg_len
        Y_test is the price of the next day for prediction
        :param seq_len: Length of window
        :return: X_test and Y_test
        """
        for i in range(len(self.stock_test) - seq_len):
            x = np.array(self.stock_test.iloc[i: i + seq_len, 1])
            y = np.array([self.stock_test.iloc[i + seq_len, 1]], np.float64)
            self.input_test.append(x)
            self.output_test.append(y)
        self.X_test = np.array(self.input_test)
        self.Y_test = np.array(self.output_test)

if __name__ == "__main__":
    process = DataPreparation("stock_prices.csv", 0.9)
    process.gen_train(15)