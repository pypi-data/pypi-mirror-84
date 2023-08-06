# EDA FEATURE_EXTRACTOR MODEL

A python package to do EDA, feature selection and display the best hyperparameters for a pre-built classification model.

Useful for datasets with no NaNs or null values present.
Can be used for normal classification tasks, next update will work for Regression type problems and incorporate a sorted arrangement of variables.

before utilizing the package, ensure no Null or NaN values remain.

    pip install eda-fe-model

    pip install eda-fe-model==0.3.1

## Using the library
    from eda_fe_model import package

    package.EDA()
    package.feature_extraction()

Use to_categorical from keras.utils, to One Hot Encode the labels
    
    package.build_best_model()
    package.model_create()


## EDA
package.EDA accepts the following:

            dataset = dataset
            columns_drop = columns to drop as a list. Accepts None
            one_hot_encode = True/False
            label_encode = True/False
            normalize = True/False
            standardize = True/False
            target_varaible = single target, y
            test_size = percentage of the dataset to be used for testing purposes
            random_state

    If the dataset only consists of categorical variables, set normalize or standardize to True.

    returns the splitted dataset: x_train, x_test, y_train, y_test (respectively)


## FEATURE EXTRACTION
package.feature_extraction accepts the following:

            train_X = train dataset consisting of predictors
            train_Y = train labels
            test_X = test dataset consisting of predictors
            test_Y = test labels
            rfe = True/False; Do you want to use Random Feature Extractor
            dim_out = Used only if rfe=True; output dimension; number of features to be selected 
            distribution = Distibution of the dataset you want to use for GLM

    If rfe is False, set dim_out and distribution to be None, to return the input x and y for train and test datasets.
    Try changing the distribution if error due to convergence appear.

    returns x_train and x_test datasets with the user entered dimension/predictors


## BUILD BEST MODEL
package.build_best_model accepts the follwoing:

            x = train dataset consisting of predictors
            y = One HOt Encoded training labels

    returns a RandomizedSearchCV object.

    Best Score: results.best_score_
    Best Parameters: results.best_params_

## CREATING THE MODEL
package.model_create accpets the best parameters from the build_best_model() and runs the model for a user specified epochs.

            x = the new train dataset consisting of just the predictors.
            y = One Hot encoded training labels

