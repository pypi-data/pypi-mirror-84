import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.feature_selection import RFE
from sklearn.linear_model import LogisticRegression
import statsmodels.api as sm
from tensorflow.keras.layers import Dense, BatchNormalization, Input
from tensorflow.keras.models import Sequential
from tensorflow.keras.wrappers.scikit_learn import KerasClassifier
from sklearn.model_selection import RandomizedSearchCV
from tensorflow.keras.utils import to_categorical


le = LabelEncoder()

def EDA(dataset, columns_drop, one_hot_encode, label_encode, normalize, standardize, target_variable, test_size, random_state):
    
    if (normalize==True) and (standardize==True):
        raise ValueError('Select one between Normalization or Standardiation')
    elif (one_hot_encode==True) and (label_encode==True):
        raise ValueError('Select one of the categorical encoding schemes')

    if columns_drop!=None:
        for i in columns_drop:
            dataset.drop([i], axis=1, inplace=True)
    
    x_cols = [x for x in dataset.columns if x!=target_variable]
    X = dataset[x_cols]
    Y = dataset.loc[:, target_variable]
    
    label_enc = LabelEncoder()
    Y = label_enc.fit_transform(Y)
    
    numerical_X = X.select_dtypes(include=[np.number])
    categorical_X = X.select_dtypes(exclude=[np.number])
     
    if (one_hot_encode==True) and (label_encode==False):
        cat_X = pd.get_dummies(categorical_X, columns=categorical_X.columns)
    elif (one_hot_encode==False) and (label_encode==True):
        for col_name in categorical_X.columns:
            categorical_X[col_name] = le.fit_transform(categorical_X[col_name])
        cat_X = categorical_X
   
    if (normalize==True) and (standardize==False):
        for col_name in numerical_X.columns:
            numerical_X[col_name] = (numerical_X[col_name] - np.min(numerical_X[col_name]))/(np.max(numerical_X[col_name]) - np.min(numerical_X[col_name]))
        num_X = numerical_X
    elif (normalize==False) and (standardize==True):
        for col_name in numerical_X.columns:
            numerical_X[col_name] = (numerical_X[col_name] - np.mean(numerical_X[col_name]))/np.std(numerical_X[col_name])
        num_X = numerical_X
        
    data_cleaned = pd.concat([num_X, cat_X], axis=1)
    
    x_train, x_test, y_train, y_test = train_test_split(data_cleaned, Y, test_size=test_size, random_state=random_state)
    
    return x_train, x_test, y_train, y_test


def feature_extraction(train_X, train_Y, test_X, test_Y, rfe, dim_out, distribution):
        
    if rfe==True:
        log_reg = LogisticRegression(max_iter=3000)
        
        try:
            dim_features = int(dim_out)
        except:
            raise ValueError("'dim_out' has to be an integer")
        rfe = RFE(log_reg, dim_features)
        rfe.fit(train_X, train_Y)
        col = train_X.columns[rfe.support_]
        x_train = train_X[col]
        x_test = test_X[col]
        
        if distribution=='binomial':
            family_req = sm.families.Binomial()
        elif distribution=='gamma':
            family_req = sm.families.Gamma()
        elif distribution=='gaussian':
            family_req = sm.families.Gaussian()
        elif distribution=='inverse_gaussian':
            family_req = sm.families.InverseGaussian()
        elif distribution=='negative_binomial':
            family_req = sm.families.NegativeBinomial()
        elif distribution=='poisson':
            family_req = sm.families.Poisson()
        else:
            raise ValueError("'distribution' accepts: 'binomial', 'gamma', 'gaussian', 'inverse_gaussian', 'negative_gaussian' or 'poisson'")
            
        glm = sm.GLM(exog=np.asarray(x_train), endog=np.asarray(train_Y), family=family_req)
        result = glm.fit()
        print(result.summary())
        return x_train, x_test
    
    elif (rfe==False) and (dim_out==None) and (distribution==None):
        return train_X, test_X
    else:
        raise ValueError("Error related to combinations, refer to documentation for combinations")


def build_best_model(x, y):
    
    X = x
    Y = y
    
    classes = y.shape[1]
    
    def create_model(n1=64, n2=64, n3=64, n4=64, n5=64, n6=64, activation='sigmoid', optimizer='adam', loss='binary_crossentropy'):
        model = Sequential()
        model.add(Input((X.shape[1],)))
        model.add(Dense(n1, kernel_initializer='glorot_normal', activation='relu'))
        model.add(Dense(n2, kernel_initializer='glorot_normal', activation='relu'))
        model.add(BatchNormalization())
        model.add(Dense(n3, kernel_initializer='glorot_normal', activation='relu'))
        model.add(Dense(n4, kernel_initializer='glorot_normal', activation='relu'))
        model.add(BatchNormalization())
        model.add(Dense(n5, kernel_initializer='glorot_normal', activation='relu'))
        model.add(Dense(n6, kernel_initializer='glorot_normal', activation='relu'))
        model.add(Dense(classes, activation=activation))
        model.compile(loss=loss, optimizer=optimizer, metrics=['accuracy'])
        return model
    
    wrapper_object = KerasClassifier(build_fn=create_model, batch_size=32, epochs=20)
    n1 = [8, 16, 32, 64, 128, 256]
    n2 = [8, 16, 32, 64, 128, 256]
    n3 = [8, 16, 32, 64, 128, 256]
    n4 = [8, 16, 32, 64, 128, 256]
    n5 = [8, 16, 32, 64, 128, 256]
    n6 = [8, 16, 32, 64, 128, 256]
    optimizer = ['adam', 'sgd', 'rmsprop']
    activation = ['sigmoid', 'softmax']
    batch_size = [16, 32, 64, 128]
    loss = ['binary_crossentropy', 'categorical_crossentropy']
    params_dict = dict(n1=n1, n2=n2, n3=n3, n4=n4, n5=n5, n6=n6, optimizer=optimizer, loss=loss, activation=activation, batch_size=batch_size)
    search_obj = RandomizedSearchCV(estimator=wrapper_object, param_distributions=params_dict, n_iter=47, cv=10)
    results = search_obj.fit(X, Y)
    return results


def model_create(x, y, activation, n1, n2, n3, n4, n5, n6, optimizer, loss, batch_size, epochs):

    try:
        n1 = int(n1)
    except:
        raise ValueError("'n1' expected an integer type value; got string")

    try:
        n2 = int(n2)
    except:
        raise ValueError("'n2' expected an integer type value; got string")

    try:
        n3 = int(n3)
    except:
        raise ValueError("'n3' expected an integer type value; got string")

    try:
        n4 = int(n4)
    except:
        raise ValueError("'n4' expected an integer type value; got string")

    try:
        n5 = int(n5)
    except:
        raise ValueError("'n5' expected an integer type value; got string")

    try:
        n6 = int(n6)
    except:
        raise ValueError("'n6' expected an integer type value; got string")

    try:
        epochs = int(epochs)
    except:
        raise ValueError("'epochs' expected an integer type value; got string")

    X = x
    Y = y
    classes = Y.shape[1]
    model = Sequential()
    model.add(Input((X.shape[1],)))
    model.add(Dense(n1, kernel_initializer='glorot_normal', activation='relu'))
    model.add(Dense(n2, kernel_initializer='glorot_normal', activation='relu'))
    model.add(BatchNormalization())
    model.add(Dense(n3, kernel_initializer='glorot_normal', activation='relu'))
    model.add(Dense(n4, kernel_initializer='glorot_normal', activation='relu'))
    model.add(BatchNormalization())
    model.add(Dense(n5, kernel_initializer='glorot_normal', activation='relu'))
    model.add(Dense(n6, kernel_initializer='glorot_normal', activation='relu'))
    model.add(Dense(classes, activation=activation))
    model.compile(loss=loss, optimizer=optimizer, metrics=['accuracy'])
    history = model.fit(X, Y, batch_size=batch_size, epochs=epochs, validation_split=0.1)
    return history

