from flask import Flask, render_template, url_for, request
from static import doodlePredict
import json

app = Flask(__name__)

#app.Route for the home page
@app.route("/")
def index():
    return render_template("doodlePage.html")

#app.Route to handle user post request with canvas data
@app.route("/predict", methods=['POST'])
def predict():
    #print(request.values["canvas"])
    img64 = request.values["canvas"].split(',')
    img64 = img64[1]
    predictions = doodlePredict.predict(img64)
    print(predictions)
    predictions = predictions.tolist()
    return predictions

if __name__ == "__main__":
    app.run(debug=True)