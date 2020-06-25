# -*- coding: utf-8 -*-
"""
Created on Fri Jun 19 12:27:02 2020

@author: edhell
"""

from sasctl import Session
from sasctl.services import microanalytic_score as mas

###################################
####### Variables #################

host = 'localhost'
#host = 'pdcesx15130.exnet.sas.com'

publishdestination = 'maslocal'

modelname = 'python_jk_lreg_iris'

project = 'iris_os'

user = 'sasdemo'

password = 'Orion123'

#astore_table = 'gb_astore'
#astore_caslib = 'public'

###################################
####### Getting astore table ######

s = Session(host, user, password,
            verify_ssl = False) 

module = mas.get_module(modelname)


module = mas.define_steps(module)
steps = mas.list_module_steps(module)

steps[0]['id']

steps[0]['links']

print(help(module.predict))

res = module.predict(5.0, 2.0, 3.5, 1.0)
res2 = module.predict_proba(5.0, 2.0, 3.5, 1.0)

print(res , res2)
"""
DATA SAMPLE
{'Sepal_Length': {60: 5.0},
 'Sepal_Width': {60: 2.0},
 'Petal_Length': {60: 3.5},
 'Petal_Width': {60: 1.0},
 'Species': {60: 'versicolor'}}
"""
