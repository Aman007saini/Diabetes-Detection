from flask import Flask, request, app, render_template
import pickle
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler


application = Flask(__name__)
app=application
## importing the models
log_reg=pickle.load(open('models/modelforPrediction.pkl','rb'))
StdScaler= pickle.load(open('models/StandardScaler.pkl','rb'))

@app.route("/")
def index():
    return render_template ('index.html')

@app.route("/predictdata",methods=['GET','POST'])
def predict_datapoint():
    result=""
    if request.method=='POST':
        Pregnancies= float(request.form.get('Pregnancies'))
        Glucose= float(request.form.get('Glucose'))
        BloodPressure= float(request.form.get('BloodPressure'))
        SkinThickness= float(request.form.get('SkinThickness'))
        Insulin= float(request.form.get('Insulin'))
        BMI= float(request.form.get('BMI'))
        DiabetesPedigreeFunction= float(request.form.get('DiabetesPedigreeFunction'))
        Age= float(request.form.get('Age'))
        
        new_scaled_data= StdScaler.transform([[Pregnancies,Glucose,BloodPressure,SkinThickness,Insulin,BMI,DiabetesPedigreeFunction,Age]])
        predict= log_reg.predict(new_scaled_data)
        if predict[0]==1:
            result= 'Diabetic'
        else:
            result= 'Non-Diabetic'
        
        return render_template ('single_prediction.html', result= result)
    else:
        return render_template('home.html')


if __name__=="__main__":
    app.run(host="0.0.0.0")