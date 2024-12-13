import os

import numpy as np
import pandas as pd
from flask import Flask, jsonify, request, send_file
from matplotlib import pyplot as plt
from sklearn.preprocessing import MinMaxScaler

os.environ["KERAS_BACKEND"] = "torch"

# Note that Keras should only be imported after the backend
# has been configured. The backend cannot be changed once the
# package is imported.
import keras as kr

# from keras.api.models import Sequential
# from keras.layers import Dense, Activation
# from keras.layers import LSTM

app = Flask(__name__)

# Load the model
MODEL_PATH = "build/release/ohlcv_forecast.keras"  # Update with your model path
# model = keras.saving.load_model(MODEL_PATH)
model = kr.models.Sequential()


@app.route("/image", methods=["GET"])
def image():
    # IMPORTING DATASET
    df = pd.read_csv("apple_share_price.csv", usecols=[1, 2, 3, 4])
    df = df.reindex(index=df.index[::-1])
    ohlcv_avg = df.mean(axis=1)
    ohlcv_avg = np.reshape(ohlcv_avg.values, (len(ohlcv_avg), 1))  # 1664
    scaler = MinMaxScaler(feature_range=(0, 1))
    ohlcv_avg = scaler.fit_transform(ohlcv_avg)
    training_size = int(len(ohlcv_avg) * 0.5)
    x_train = ohlcv_avg[training_size:]
    X, Y = new_dataset(x_train, 1)
    X = np.reshape(X, (X.shape[0], 1, X.shape[1]))
    # Make predictions
    pred = model.predict(X)
    # DE-NORMALIZING
    ohlcv_avg = scaler.inverse_transform(ohlcv_avg)
    pred = scaler.inverse_transform(pred)
    # CREATING SIMILAR DATASSET TO PLOT TEST PREDICTIONS
    testPredictPlot = np.empty_like(ohlcv_avg)
    testPredictPlot[:, :] = np.nan
    testPredictPlot[len(pred) + (2) + 1 : len(ohlcv_avg) - 1, :] = pred
    plt.cla()
    plt.clf()
    plt.plot(ohlcv_avg, "g", label="original dataset")
    plt.plot(testPredictPlot, "b", label="predicted stock price")
    plt.legend(loc="upper right")
    plt.xlabel("Time in Days")
    plt.ylabel("OHLC Value of Apple Stocks")
    plt.savefig("testplot.png")
    return send_file("testplot.png", mimetype="image/png")


@app.route("/predict", methods=["POST"])
def predict():
    """
    Endpoint to make predictions.
    Expects JSON input with key "instances".
    """
    # try:
    # Parse the input JSON
    input_data = request.get_json()
    # IMPORTING DATASET
    df = pd.read_csv("apple_share_price.csv", usecols=[1, 2, 3, 4])
    df = df.reindex(index=df.index[::-1])
    ohlcv_avg = df.mean(axis=1)
    ohlcv_avg = np.reshape(ohlcv_avg.values, (len(ohlcv_avg), 1))  # 1664
    scaler = MinMaxScaler(feature_range=(0, 1))
    ohlcv_avg = scaler.fit_transform(ohlcv_avg)
    training_size = int(len(ohlcv_avg) * 0.5)
    x_train = ohlcv_avg[:training_size]

    X, Y = new_dataset(x_train, 1)
    X = np.reshape(X, (X.shape[0], 1, X.shape[1]))

    # Make predictions
    pred = model.predict(X)

    # DE-NORMALIZING
    pred = scaler.inverse_transform(pred)
    # # Ensure "instances" key is in input data
    # if "instances" not in input_data:
    #     return jsonify({"error": "Missing 'instances' in request data"}), 400
    # # Convert input data to a numpy array
    # instances = np.array(input_data["instances"])
    # # Make predictions
    # predictions = model.predict(instances)
    # Return predictions as a JSON response
    response = {"predictions": pred.tolist()}
    return jsonify(response)

    # except Exception as e:
    #     # Handle errors and return a meaningful response
    #     return jsonify({"error": str(e)}), 500


# FUNCTION TO CREATE 1D DATA INTO TIME SERIES DATASET
def new_dataset(dataset, step_size):
    data_X, data_Y = [], []
    for i in range(len(dataset) - step_size - 1):
        a = dataset[i : (i + step_size), 0]
        data_X.append(a)
        data_Y.append(dataset[i + step_size, 0])
    return np.array(data_X), np.array(data_Y)


if __name__ == "__main__":
    # Run the Flask app
    app.run(host="0.0.0.0", port=5000)
