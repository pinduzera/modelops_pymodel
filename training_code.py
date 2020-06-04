# -*- coding: utf-8 -*-
"""
Created on Thu Jun  4 15:07:00 2020

@author: edhell
"""
###
from sklearn.linear_model import LogisticRegression
from sklearn import model_selection
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder
import pandas as pd
import swat
import pickle

#####

f = open("session_id.txt", "r")
session_id = f.read()
f.close()


conn = swat.CAS('pdcesx06182.exnet.sas.com', port=8777, protocol = 'http',
             #'localhost',
            caslib = 'casuser', username = 'sasdemo01',
            password = 'Orion123') #, session = session_id)

ctbl = conn.CASTable(name = 'hmeq', 
                    caslib = 'public')
table = ctbl.to_frame()
table
### avoid using variable names with . it will have error with DS2
X = table.drop('BAD',axis =1)
Y = table.BAD.astype('category')
test_size = 0.33
seed = 7

X_train, X_test, Y_train, Y_test = model_selection.train_test_split(
        table.drop('BAD', axis = 1),
        table['BAD'], 
        test_size=test_size, 
        random_state=seed)

Y_train
# Fit a sci-kit learn model

model = Pipeline(steps=[
                ('imputer', SimpleImputer(strategy='most_frequent')),
                ('lab_encoder', OneHotEncoder()),
                ('lreg', LogisticRegression(max_iter=1000))])

model.fit(X, Y)

model.named_steps['lreg'].coef_

# save the model to disk
filename = 'pylreg.pickle'
pickle.dump(model, open(filename, 'wb'))