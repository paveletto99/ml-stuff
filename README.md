# ML STUFF

Datasets [here](https://unsw-my.sharepoint.com/personal/z5025758_ad_unsw_edu_au/_layouts/15/onedrive.aspx?ga=1&id=%2Fpersonal%2Fz5025758%5Fad%5Funsw%5Fedu%5Fau%2FDocuments%2FUNSW%2DNB15%20dataset%2FCSV%20Files)

> ⚠️ if `pip` crash run `pip install --no-cache-dir -r requirements.txt`


```
docker run -p 8501:8501 -it --name=tf_serving --mount type=bind,source=$(pwd)/build/release/ohlcv_forecast,target=/models/ohlcv_forecast -e MODEL_NAME=ohlcv_forecast -t tensorflow/serving
```

docker run -p 5000:8500 -it --name=ohlcv-predictor -t ohlcv-predictor