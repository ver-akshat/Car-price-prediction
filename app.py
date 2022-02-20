from flask import Flask,render_template,request
import requests
import pickle
import numpy as np
import sklearn
import joblib

app=Flask(__name__)
model=pickle.load(open("vot_reg.pkl","rb"))
@app.route('/',methods=['GET'])
def home():
    return render_template('main.html')

@app.route("/predict",methods=['POST'])
def predict():
    if request.method=='POST':
        year=int(request.form['year'])
        
        hp=int(request.form['hp'])

        no_of_cylinders=int(request.form['no_of_cylinders'])
        year=2022-year

        transmission_type=request.form.get('transmission_type')
        if(transmission_type=='automatic'):
            transmission_type_automatic=1
            transmission_type_manual=0
            transmission_type_automated_manual=0
        elif(transmission_type=='manual'):
            transmission_type_automatic=0
            transmission_type_manual=1
            transmission_type_automated_manual=0
        else:
            transmission_type_automatic=0
            transmission_type_manual=0
            transmission_type_automated_manual=1

        no_of_doors=int(request.form['no_of_doors'])
        vehicle_size=request.form.get('vehicle_size')
        if(vehicle_size=='large'):
            vehicle_size_large=1
            vehicle_size_midsize=0
            vehicle_size_compact=0
        elif(vehicle_size=='midsize'):
            vehicle_size_large=0
            vehicle_size_midsize=1
            vehicle_size_compact=0
        else:
            vehicle_size_large=0
            vehicle_size_midsize=0
            vehicle_size_compact=1

        highway_mpg=int(request.form['highway_mpg'])
        
        city_mpg=int(request.form['city_mpg'])
        
        inp_data=np.array([[year,hp,no_of_cylinders,transmission_type_automatic,transmission_type_manual,
        transmission_type_automated_manual,no_of_doors,
        vehicle_size_large,vehicle_size_compact,vehicle_size_midsize,highway_mpg,city_mpg]])
        
        prediction=model.predict(inp_data)
        
        output=round(prediction[0],2)
        if output<0:
            return render_template('main.html',prediction_text="Sorry this car cannot be sold")
        else:
            return render_template('main.html',prediction_text="This car can be sold at {} USD".format(output))
    else:
        return render_template('main.html')

if __name__=="__main__":
    app.run(debug=True)


