# vimo

The Python client package for communication with model governance base **vimo**. **vimo** supports virtualization with all versions of **Python** and **R** languages from version **3.0** and package versions.
At this moment supports all:
* scikit-learn
* keras
* mlr
* caret
* parsnip

models.

During the development **vimo** is only accessible via MINI network. However you can access it from other places via ssh, if you have account at this network.

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

## Creating an account
To be able to upload your model you need to have an account on **vimo**. So here is what you need to do:

```
from vimo import communication as comm

comm.create_user('Example user', 'example password', 'example_mail@gmail.com')
```

You will receive information if your account was created correctly.

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

To upload the model to the base you , to import client package and pass classifier, its name that will be visible in the **vimo**, its description, list of tags, training dataset with target column as last one with column names, its name, its description, requirements file, your user name and password.

So first let's prepare our data.

```
import pandas as pd

train_data_to_upload = pd.DataFrame(data.data, colums=data.feature_names)
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

comm.upload(model, 'example_model', 'This is an example model.', ['example', 'easy'], train_data_to_upload, 'example_data', 'This is an example dataset', 'requirements.txt', 'Example user', 'example password')
```

In this moment *model* is being uploaded to the **vimo**. If requested environment had not been already created in the **vimo**, it will be created. During this time your Python sesion will be suspended. Multithreading is being under development.

### Summary

You can also pass your model as the path (must contain **/** sign to *Python* pickle. Training data parameter can be a path to *.csv* file (must contain **/** sign) or *hash* of already uploaded dataset in the **vimo**. It is recommended to upload only numerical data.

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

Be aware that some models may require from you exactly the same column names in passed data. If you are passing data as an object then by default columns are fetched from original dataset. If you do not want this behaviour set *prepare_data* to *False*. You may easily manually obtain columns with:

```
columns = comm.model_info("example_model")['data_info']['columns']
```

## Searching model

You can also search for model in **vimo** with tags. Just type:

```
from vimo import communication as comm

comm.search_model(row = '>1000;<10000;', column='=12;', user='Example user', tags = ['example', 'easy'])
```

You will get all models having at least one of these tags.

# Usage in R

## Creating an account
To upload your model you need to create your account.

```
library(vimo)

create_user('Example user', 'example password', 'example_mail@gmail.com')
```

In response you will get information if your account was created succesfully.

## Uploading model
First you need to have a trained mlr model.

### Example
```
library(mlr)

task = makeClassifTask(data = iris, target = 'Species')
model = makeLearner("clasif.randomForest")
model = train(model, task)
```

To upload the model to the base you need to import client package and pass classifier, its name that will be visible in the **vimo**, its description, tags, training dataset with target column as last one with column names, its name, its description, your user name and password. Names should be unique.

```
library('vimo')

upload(model, 'example_model', 'This is an example model.', c('example', 'easy'), iris, 'example_data', 'This is an example data', 'Example user', 'example_password')
```

In this moment *model* is being uploaded to the **vimo**. If requested environment had not been already created in the **vimo**, it will be created. During this time your R sesion will be suspended. Multithreading is being under development.

### Summary

You can also pass your model as the path (must contain **/** sign to *R* *.rds* file. Training data parameter can be a path to *.csv* file (must constain **/** sign) or *hash* of already uploaded dataset in the **vimo**. It is recommended to upload only numerical data. Please, have loaded in your namespace only packages that are required to make a model.

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

Be aware that some models may require from you exactly the same column names in passed data. If you passed data as an object then column names will be fetched by default. If you do not want this behaviour pass as argument *prepare_data* value *False*. You may also easily manually obtain columns with:

```
columns = model_info("example_model")$data_info$columns
```

## Searching for model

You can also search for model with specific tags.

Just type:

```
library(vimo)

search_model(row = '>1000;<10000;', column='=12;', user='Example user', tags = c('example', 'easily'))
```

You will receive in response all models with at least one of these tags.
