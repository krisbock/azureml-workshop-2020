# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license.

import joblib
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler,OneHotEncoder
from sklearn_pandas import DataFrameMapper
import os
import pandas as pd
import numpy as np
import shutil
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from azureml.core import Run, Dataset, Workspace

ws = Run.get_context().experiment.workspace
run = Run.get_context()

os.makedirs('./outputs', exist_ok=True)

attritionData = Dataset.get_by_name(ws,'IBM-Employee-Attrition').to_pandas_dataframe()

# Dropping Employee count as all values are 1 and hence attrition is independent of this feature
attritionData = attritionData.drop(['EmployeeCount'], axis=1)
# Dropping Employee Number since it is merely an identifier
attritionData = attritionData.drop(['EmployeeNumber'], axis=1)
attritionData = attritionData.drop(['Over18'], axis=1)
# Since all values are 80
attritionData = attritionData.drop(['StandardHours'], axis=1)

attritionData["Attrition_numerical"] = attritionData["Attrition"]
target = attritionData["Attrition_numerical"]

attritionXData = attritionData.drop(['Attrition_numerical', 'Attrition'], axis=1)

# Creating dummy columns for each categorical feature
categorical = []
for col, value in attritionXData.iteritems():
    if value.dtype == 'object':
        categorical.append(col)

# Store the numerical columns in a list numerical
numerical = attritionXData.columns.difference(categorical)

numeric_transformations = [([f], Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', StandardScaler())])) for f in numerical]
    
categorical_transformations = [([f], OneHotEncoder(handle_unknown='ignore', sparse=False)) for f in categorical]

transformations = numeric_transformations + categorical_transformations

# Append classifier to preprocessing pipeline.
# Now we have a full prediction pipeline.
clf = Pipeline(steps=[('preprocessor', DataFrameMapper(transformations)),
                      ('classifier', LogisticRegression(solver='lbfgs'))])

# Split data into train and test
from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(attritionXData, 
                                                    target, 
                                                    test_size = 0.2,
                                                    random_state=0,
                                                    stratify=target)

# write x_text out as a pickle file for later visualization
x_test_pkl = 'x_test.pkl'
with open(x_test_pkl, 'wb') as file:
    joblib.dump(value=x_test, filename=os.path.join('./outputs/', x_test_pkl))

# preprocess the data and fit the classification model
model = clf.fit(x_train, y_train)
#model = clf.steps[-1][1]

# Make Multiple Predictions
y_predictions = model.predict(x_test)

accuracy = accuracy_score(y_test, y_predictions)
# (Method 2 with svm model) accuracy = svm_model_linear.score(x_test, y_test)

print('Accuracy of LogisticRegression classifier on test set: {:.2f}'.format(accuracy))

# Set Accuracy metric to the run.log to be used later by Azure ML's tracking and metrics capabilities
run.log("Accuracy", float(accuracy))

# creating a confusion matrix
cm = confusion_matrix(y_test, y_predictions)
print(cm)

# Save the model as .pkl file and
# save model file to the outputs/ folder - this will auto upload the model to the run in AzureML
model_file_name = 'log_reg.pkl'

#TODO: Write out the real model file :)
from interpret.ext.blackbox import TabularExplainer
from azureml.interpret import ExplanationClient
# create an explanation client to store the explanation (contrib API)
client = ExplanationClient.from_run(run)
print('create explainer')
# create an explainer to validate or debug the model
tabular_explainer = TabularExplainer(clf.steps[-1][1],
                                     initialization_examples=x_train,
                                     features=attritionXData.columns,
                                     classes=["Not leaving", "leaving"],
                                     transformations=transformations)

# explain overall model predictions (global explanation)
# passing in test dataset for evaluation examples - note it must be a representative sample of the original data
# more data (e.g. x_train) will likely lead to higher accuracy, but at a time cost
global_explanation = tabular_explainer.explain_global(x_test)

print('upload explanation')
# uploading model explanation data for storage or visualization
comment = 'Global explanation on classification model trained on IBM employee attrition dataset'
client.upload_model_explanation(global_explanation, comment=comment)


# save model in the outputs folder so it automatically get uploaded
with open(model_file_name, 'wb') as file:
    joblib.dump(value=clf, filename=os.path.join('./outputs/', model_file_name))


run.upload_file('x_test_ibm.pkl', os.path.join('./outputs/', x_test_pkl))

# Upload the model (just take the one from the repo...needs to be changed)
shutil.copy2('original_model.pkl', 'outputs/original_model.pkl')

# Register model
#original_model = run.register_model(model_name='IBM_attrition_model', model_path='original_model.pkl')
