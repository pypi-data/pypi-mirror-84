# ML Package

A Package through which multiple things can be done in a go like fitting a model of your own choice (regression/classification) and get final results in terms of model accuracy/ score/ mse/ mae/ confusion matrix and direct submission file which we need to upload in case of competitions.

Two things can be achieved from this package:
1. Results after fitting any Regression/classification algorithm of your own choice. Function to be used - **train_model**
2. Final submission file to be submitted directly in competitions. Function to be used - **return_csv**

### Requirements:
1. sklearn
2. numpy
3. pandas
4. Pre-processed data to be passed - data already cleaned, splitted into train and test
5. In **train_model** function, parameters to be passed:
   * x_train, y_train, x_test, y_test
   * model object
   * regression=True     *(if addressing regression problem)*
   * regression=False     *(if addressing classification problem (default is True))*
6. In **return_csv** function, parameters to be passed:
   * x_train, y_train, x_test, y_test
   * model object
   * sample submission file   *(dataframe)*
   * target column name    *(string)*
   * file location name    *(filepath where to be saved)*

### Installation & Usage
1. Make sure that your pip version is up-to-date: pip install --upgrade pip. Check version with pip -V. 
2. Select the correct package:
   * There are two packages (two versions of the package )and you should SELECT ONLY ONE OF THEM which is the latest one.
   * Install using `pip install mlpkg` with latest version
3. Import the package and use its functions: 
   `from ML_Utility import ML_package`
   