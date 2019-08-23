# vimo

The Python client package for communication with model governance base **vimo**. **vimo** supports virtualization with all versions of **Python** and **R** languages from version **3.0** and package versions. At this moment supports all scikit-learn models in your environment and all models added to the base.

# Installation

## Python

```
git clone https://github.com/WojciechKretowicz/vimo.git 
cd vimo/vimo_python
pip install .
```
## R

```
devtools::install_github("WojciechKretowicz/vimo/vimo_r/vimo")
```

# Usage in Python

## Uploading model
First you need to have a trained scikit-learn model.

### Example
```
from sklearn import datasets
from sklearn.ensemble import RandomForestClassifier

data = datasets.load_wine()
model = RandomForestClassifier(n_estimators = 777)
model.fit(data.data, data.target)
```

To upload the model to the base you need to import client package and pass classifier, its name that will be visible in the **vimo**, requirements file, training dataset with target column as last one with column names and its name.

So first let's prepare our data.

```
import pandas as pd

train_data_to_upload = pd.DataFrame(data.data, data.feature_names)
train_data_to_upload['target'] = data.target
```
Due to our respect for your privacy we do not investigate your environment. To allow us to make a virtualization please run in command line:

```
pip freeze > requirements.txt
```

This will make a *Python* style requirements file.

Now we are ready to push our model to the base. Its name has to be unique in the base. Dataset name either.

```
from vimo import communication as comm

comm.upload(model, "example_model", "requirements.txt" train_data_to_upload, "example_data", "Description of the model", "Description of the dataset")
```

In this moment *model* is being uploaded to the **vimo**. If requested environment had not been already created in the **vimo**, it will be created. During this time your Python sesion will be suspended. Multithreading is being under development.

### Summary

You can also pass your model as the path (must contain **/** sign to *Python* pickle. Training data parameter can be a path to *.csv* file or *hash* of already uploaded dataset in the **vimo**. It is recommended to upload only numerical data.

## Reading an info about model

If you want to read an info about the model already uploaded in **vimo** you can run:

```
from vimo import communication as comm

comm.model_info("example_model")
```

*"example_model"* is a name of **vimo** model.

Returned value is a *Python* dictionary containing all information about the model.

## Making predictions

If you want to make a prediction, type:

```
from vimo import communication as comm

comm.predict("example_model", data)
```

*"example_model"* is the name of **vimo** model, *data* is the data frame with named columns without target column, or path to *.csv* (must contain **/** sign) file or *hash* of already uploaded data.

Be aware that some models may require from you exactly the same column names in passed data. You may easily obtain them with:

```
columns = comm.model_info("example_model")['data_info']['columns']
```

# Usage in R

## Uploading model
First you need to have a trained mlr model.

### Example
```
library(mlr)

task = makeClassifTask(data = iris, target = 'Species')
model = makeLearner("clasif.randomForest")
model = train(model, task)
```

To upload the model to the base you need to import client package and pass classifier, its name that will be visible in the **vimo**, training dataset with target column as last one with column names and its name. Names should be unique.

```
library('vimo')

upload(model, "example_model", iris, "example_data", "Description of the model", "Description of the dataset")
```

In this moment *model* is being uploaded to the **vimo**. If requested environment had not been already created in the **vimo**, it will be created. During this time your R sesion will be suspended. Multithreading is being under development.

### Summary

You can also pass your model as the path (must contain **/** sign to *R* *.rds* file. Training data parameter can be a path to *.csv* file or *hash* of already uploaded dataset in the **vimo**. It is recommended to upload only numerical data. Please, have loaded in your namespace only packages that are required to make a model.

## Reading an info about model

If you want to read an info about the model already uploaded in **vimo** you can run:

```
library('vimo')

model_info("example_model")
```

*"example_model"* is a name of **vimo** model.

Returned value is a *R* named list containing all information about the model.

## Making predictions

If you want to make a prediction, type:

```
library('vimo')

predict("example_model", data)
```

*"example_model"* is the name of **vimo** model, *data* is the data frame with named columns without target column, or path to *.csv* (must contain **/** sign) file or *hash* of already uploaded data.

Be aware that some models may require from you exactly the same column names in passed data. You may easily obtain them with:

```
columns = model_info("example_model")$data_info$columns
```
