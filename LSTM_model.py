import get_stock_prices as sp
import tensorflow as tf
from datapreparation import DataPreparation
import numpy as np

start = "2007-01-01"
end = "2018-03-01"

sp.get_stock_data("AAPL", start_date=start, end_date=end)
data = DataPreparation("stock_prices.csv", 0.9)
data.gen_test(10)
data.gen_train(10)

x,y = data.X_train.shape
X_train = data.X_train.reshape((x, y, 1)) / 200
Y_train = data.Y_train / 200

x,y = data.X_test.shape
X_test = data.X_test.reshape(x, y, 1) / 200
Y_test = data.Y_test / 200

model = tf.keras.Sequential()
model.add(tf.keras.layers.LSTM(20, input_shape=(10, 1), return_sequences=True))
model.add(tf.keras.layers.LSTM(20))
model.add(tf.keras.layers.Dense(1, activation=tf.nn.relu))

model.compile(optimizer="adam", loss="mean_squared_error")

model.fit(X_train, Y_train, epochs=50)

print(model.evaluate(X_test, Y_test))

"""
data = pdr.get_data_yahoo("AAPL", "2017-12-19", "2018-01-03")
stock = data["Adj Close"]
X_predict = np.array(stock).reshape((1, 10, 1)) / 200
print(model.predict(X_predict)*200)
"""