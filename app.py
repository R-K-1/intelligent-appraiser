from flask import Flask, request, jsonify, render_template, Response
from flask.logging import create_logger
import logging
import os

import pandas as pd
from sklearn.externals import joblib
from sklearn.preprocessing import StandardScaler
x = os.path.dirname(os.path.realpath(__file__))


app = Flask(__name__, template_folder=os.path.dirname(os.path.realpath(__file__)))
LOG = create_logger(app)
LOG.setLevel(logging.INFO)

def scale(payload):
    """Scales Payload"""

    LOG.info(f"Scaling Payload: \n{payload}")
    scaler = StandardScaler().fit(payload.astype(float))
    scaled_adhoc_predict = scaler.transform(payload.astype(float))
    return scaled_adhoc_predict

def format_input(CHAS, RM, TAX, PTRATIO, B, LSTAT):
    """format input to look like this:
        
        {
        "CHAS":{
        "0":0
        },
        "RM":{
        "0":6.575
        },
        "TAX":{
        "0":296.0
        },
        "PTRATIO":{
        "0":15.3
        },
        "B":{
        "0":396.9
        },
        "LSTAT":{
        "0":4.98
        }
        
        """
    return eval("{'CHAS': {'0': " + CHAS[0] + "}, 'RM': {'0': " + RM[0] + "}, 'TAX': {'0': " + TAX[0] + "}, 'PTRATIO': {'0': " + PTRATIO[0] + "}, 'B': {'0': " + B[0] + "}, 'LSTAT': {'0': " + LSTAT[0] + "}}")

@app.route("/")
def home():
    html = "<h3 style='background-color: green;'>Sklearn Prediction Home</h3>"
    #return html.format(format)
    return render_template('index.html')

@app.route("/predict", methods=['POST'])
def predict():
    """Performs an sklearn prediction
        
        input looks like:
        {
        "CHAS":{
        "0":0
        },
        "RM":{
        "0":6.575
        },
        "TAX":{
        "0":296.0
        },
        "PTRATIO":{
        "0":15.3
        },
        "B":{
        "0":396.9
        },
        "LSTAT":{
        "0":4.98
        }
        
        result looks like:
        { "prediction": [ <val> ] }
        
        """
    
    # Logging the input payload
    LOG.info("ABOUT TO PRINT REQUEST.FORM")
    LOG.info(f"\n{request.form}")
    LOG.info("ABOUT TO PRINT REQUEST.ARGS")
    LOG.info(f"\n{request.args}")
    json_payload = ''
    if not request.json is None:
        json_payload = request.json
        LOG.info("PATH 1")
    else:
        json_payload = format_input(request.form.getlist('CHAS'),
                                            request.form.getlist('RM'),
                                            request.form.getlist('TAX'),
                                            request.form.getlist('PTRATIO'),
                                            request.form.getlist('B'),
                                            request.form.getlist('LSTAT'))
        LOG.info("PATH 2")
    LOG.info(f"JSON payload: \n{json_payload}")
    LOG.info(f"payload datatype:\n{type(json_payload)}")
    inference_payload = pd.DataFrame(json_payload)
    LOG.info(f"Inference payload DataFrame: \n{inference_payload}")
    # scale the input
    scaled_payload = scale(inference_payload)
    # get an output prediction from the pretrained model, clf
    prediction = list(clf.predict(scaled_payload))
    # TO DO:  Log the output prediction value
    LOG.info(f"Scaled payload: \n{scaled_payload}")
    LOG.info(f"predicion: \n{prediction}")
    return jsonify({'prediction': prediction})

if __name__ == "__main__":
    # load pretrained model as clf
    clf = joblib.load("./model_data/boston_housing_prediction.joblib")
    app.run(host='0.0.0.0', port=80, debug=True) # specify port=80
