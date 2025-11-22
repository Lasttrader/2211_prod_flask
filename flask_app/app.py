#import
import pickle
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
from sklearn.neighbors import KNeighborsClassifier
from flask import (Flask, #сервер фреймворк
                   request, #для работы с методами POST GET
                   render_template) #взаимодействие с html

print("import удачно")

#for API

#load_models
#LE
job_LE = pickle.load(open('../flask_app/models/tech_models/job_LE.pkl', 'rb'))
marital_LE	= pickle.load(open('../flask_app/models/tech_models/marital_LE.pkl', 'rb'))
education_LE = pickle.load(open('../flask_app/models/tech_models/education_LE.pkl', 'rb'))	
default_LE	= pickle.load(open('../flask_app/models/tech_models/default_LE.pkl', 'rb'))
housing_LE= pickle.load(open('../flask_app/models/tech_models/housing_LE.pkl', 'rb'))	
loan_LE	= pickle.load(open('../flask_app/models/tech_models/loan_LE.pkl', 'rb'))
contact_LE= pickle.load(open('../flask_app/models/tech_models/contact_LE.pkl', 'rb'))	
month_LE = pickle.load(open('../flask_app/models/tech_models/month_LE.pkl', 'rb'))	
poutcome_LE = pickle.load(open('../flask_app/models/tech_models/poutcome_LE.pkl', 'rb'))
y_LE = pickle.load(open('../flask_app/models/tech_models/y_LE.pkl', 'rb'))
#scaler
num_scaler = pickle.load(open('../flask_app/models/tech_models/num_scaler_v11.pkl', 'rb'))
#ML models
kNN = pickle.load(open('../flask_app/models/ml_models/kNN.pkl', 'rb'))
print('модели загружены успешно')

#app
app = Flask(__name__)

@app.route('/', methods = ['POST', 'GET'])
def main():
    if request.method == 'GET':
        return render_template('main.html')
    
    if request.method == 'POST':
        ## get_data from html FORM 
        #categorical
        job = request.form['job']
        marital = request.form['marital']
        education = request.form['education']
        default= request.form['default']
        housing= request.form['housing']
        loan= request.form['loan']
        contact= request.form['contact']
        month= request.form['month']
        poutcome= request.form['poutcome']
        #num
        age	= float(request.form['age'])
        balance	= float(request.form['balance'])
        day	= float(request.form['day'])
        duration= float(request.form['duration'])
        campaign= float(request.form['campaign'])
        pdays	= float(request.form['pdays'])
        previous= float(request.form['previous'])
        ## preprocessing
        ### categorical
        X_cat_from_form = [job,	
                        marital,	
                        education,	
                        default,	
                        housing,	
                        loan,	
                        contact,	
                        month,	
                        poutcome]
        le_list = [job_LE,	
                    marital_LE,	
                    education_LE,	
                    default_LE,	
                    housing_LE,	
                    loan_LE,	
                    contact_LE,	
                    month_LE,	
                    poutcome_LE]
        X_le_list = [] #под закодированные значения
        for i in range(len(X_cat_from_form)):
            x_cat = le_list[i].transform([X_cat_from_form[i]])[0]
            X_le_list.append(x_cat)
        print('x_cat_list', X_le_list)
        
        ### num features
        X_nums_from_form = [age,	
                            balance,	
                            day,	
                            duration,	
                            campaign,	
                            pdays,	
                            previous]
        X = []
        X.extend(X_le_list)
        X.extend(X_nums_from_form)
        print('общий X на вход модели', X)
        #scale
        X_scaled = num_scaler.transform([X])
        ## predict 
        prediction = kNN.predict(X_scaled)
        #result
        result = y_LE.inverse_transform(prediction)
        print('result', result)
        ##return result
        return render_template('predict.html', result = result)

#инсрукция для сервера
if __name__ == '__main__':
    app.run(debug = True)