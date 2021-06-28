# -*- coding: utf-8 -*-
"""
Created on Wed Jun 24 17:33:24 2020

@author: edhell
"""

###
from sklearn.linear_model import LogisticRegression
from sklearn import model_selection
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
#from sklearn.preprocessing import OneHotEncoder
import pandas as pd
import swat
import pickle

#####

#f = open("session_id.txt", "r")
#session_id = f.read()
#f.close()

conn = swat.CAS(#'hostname.com', port=8777, protocol = 'http',
            'localhost', port = 5570, ## bug on swat 1.6.0
            caslib = 'casuser', username = 'username',
            password = 's3cr3t!') #, session = session_id)

ctbl = conn.CASTable(name = 'iris', 
                    caslib = 'public')
table = ctbl.to_frame()
table

### avoid using variable names with . it will have error with DS2
X = table.drop('Species',axis =1)
Y = table.Species.astype('category')
test_size = 0.4
seed = 7

X_train, X_test, Y_train, Y_test = model_selection.train_test_split(
        table.drop('Species', axis = 1),
        table['Species'], 
        test_size=test_size, 
        random_state=seed)

Y_train
# Fit a sci-kit learn model

model = Pipeline(steps=[
                ('imputer', SimpleImputer(strategy='most_frequent')),
                #('lab_encoder', OneHotEncoder()),
                ('lreg', LogisticRegression(max_iter=1000))])

model.fit(X, Y)


model.named_steps['lreg'].coef_

##### MODEL VALIDATION

from sklearn.model_selection import cross_validate
acc = cross_validate(model, X, Y, cv = 5, scoring = ['accuracy'])

print('\nAccuracy Validation per 5 fold!')

print(acc['test_accuracy'])


print('\nTesting Model')

x = X.iloc[100:101, :]
#x[1] = None
x
model.predict(x)

model.predict_proba(x)
# save the model to disk
filename = 'pylreg.pickle'
pickle.dump(model, open(filename, 'wb'))
#
conn.terminate()
