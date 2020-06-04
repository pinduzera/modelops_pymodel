# -*- coding: utf-8 -*-
"""
Created on Thu Jun  4 11:22:46 2020

@author: edhell
"""

import sasctl
from sasctl import Session
from sasctl import register_model, publish_model
from sasctl.services import model_repository
import pickle


loaded_model = pickle.load(open(filename, 'rb'))
pred = loaded_model.predict(X_test)
pred_prob = result_predloaded_model.predict(X_test)
print(result)