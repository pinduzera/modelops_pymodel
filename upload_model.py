# -*- coding: utf-8 -*-
"""
Created on Thu Jun  4 11:22:46 2020

@author: edhell
"""

from sasctl import Session
from sasctl import register_model, publish_model
from sasctl.services import model_repository
from pathlib import Path
import pickle
import pandas as pd
import pzmm
import sys
import swat

####### Variables

host = 'localhost'
host = 'pdcesx16159.exnet.sas.com'

modelname = 'python_jk_lreg'

project = 'hmeq_os'

publishdestination = 'maslocal'

data_path = './data/hmeq_score.csv'

model_filename= 'pylreg.pickle'

########

conn = swat.CAS(host, port=8777, protocol = 'http',
            #'localhost', port = 5570, ## bug on swat 1.6.0
            caslib = 'casuser', username = 'sasdemo01',
            password = 'Orion123') #, session = session_id)

s = Session(host, 'sasdemo', 'Orion123', verify_ssl = False)

model = pickle.load(open(model_filename, 'rb'))


ctbl = conn.CASTable(name = 'hmeq', 
                    caslib = 'public')
table = ctbl.to_frame()

### avoid using variable names with . it will have error with DS2
inputs = table.drop('BAD',axis =1)
# Need one example of each var for guessing type
### can't have NaN
#inputs['DEBTINC'] = .5 

outputs = table.columns.to_list()[0]
outputs = pd.DataFrame(columns=[str(outputs), 'P_BAD0', 'P_BAD1'])

outputs.loc[len(outputs)] = [1, 0.5, 0.5]
#model.predict_proba(inputs[:1])

### DON'T DO THAT IN PRODUCTION

model_exists = model_repository.get_model(modelname, refresh=False)

#model_repository.delete_model(modelname)
if model_exists == None:
    print('Creating new model')
    register_model(model = model, 
                   name= modelname, 
                   project= project,
                   input = inputs, ## somehow using a pd.df bug but SASdf don't
                   force=True)
else:
    print('Model exists, creting new verision')
    register_model(model = model, 
                   name= modelname, 
                   project= project,
                   input = inputs,
                   force=True,
                   version = 'latest')
    
### adding extra files
### not needed but good practice
path = Path.cwd()

####
#### Creating input & output files
JSONFiles = pzmm.JSONFiles()

### write inputVar.json
JSONFiles.writeVarJSON(inputs, isInput=True, jPath=path)

### write outputVar.json
JSONFiles.writeVarJSON(outputs, isInput=False, jPath=path)

#### missing files files

filenames = {'file':['inputVar.json','outputVar.json', 'training_code.py'],
            'role':['input','output', 'train']}
            
#### uploading files

for i in range(len(filenames['file'])):

    with open(path / filenames['file'][i], "rb") as _file:

        model_repository.add_model_content(
                      model = modelname, 
                      file = _file, 
                      name = filenames['file'][i], 
                      role= filenames['role'][i])
        
        print('uploaded ' + filenames['file'][i] + ' as ' + filenames['role'][i])
        _file.close()

#### Publish model

### need to raise exception because
### when there is no change on the actual items
### even if you delete the old container
### it just restores with the older ID
### and throws an error

try:

    publish_model(modelname, publishdestination,
                  replace = True)

except Exception as e:
    
    result = str(e).find('The image already exists')
    conn.terminate()
    
    if result != -1:
        print('The image already exists, probably no change for new version')
    else:
        print('Another error, check logs')
        sys.exit(1)
