import get_stock_prices as sp
import tensorflow as tf
from datapreparation import DataPreparation

start = "2003-01-01"
end = "2019-10-014"

sp.get_stock_data("AAPL", start_date=start, end_date=end)
data = DataPreparation("stock_prices.csv", 0.9)
data.gen_train(10)
data.gen_test(10)

X_train = data.X_train / 200
Y_train = data.Y_train / 200

X_test = data.X_test / 200
Y_test = data.Y_test / 200

# The simplest model is defined with the Sequential class which is a linear stack of layers
model = tf.keras.models.Sequential()
# three layer fully connected network
model.add(tf.keras.layers.Dense(units=100, activation=tf.nn.relu))
model.add(tf.keras.layers.Dense(100, activation=tf.nn.relu))
model.add(tf.keras.layers.Dense(1, activation=tf.nn.relu))


# model compilation creates efficient structures used by the underlying backend, in this case TensorFlow
# also need to specify optimizer (to update weights) and loss function (navigate the weight space)
model.compile(optimizer="adam", loss="mean_squared_error")

# model is trained on numpy arrays using fit
model.fit(X_train, Y_train, epochs=100)

# evaluate for the test data
print('Evaluating the model on test data: {}'.format(model.evaluate(X_test, Y_test)))

# save your model
model.save('price_prediction_model.h5')

