import pandas as pd
import numpy as np
import csv
import scipy
from sklearn import preprocessing
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation
from keras.optimizers import SGD, Adam, RMSprop
from keras.wrappers.scikit_learn import KerasRegressor
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from sklearn.model_selection import train_test_split

data_f1 = pd.read_csv('data/combine_data_all_b.txt', sep="\t", header = None)
data_f1.columns=['pid','uid','p_postDate','p_commentCount',
'p_hasPeople','p_titleLen','p_desLen',
'p_tagCount','u_avgView','u_groupCount',
'u_avgMemberCount','p_Score','uidFull','pidFull']
data_f1.drop(['p_tagCount', 'p_hasPeople', 'p_postDate', 'p_commentCount'], axis=1, inplace=True)


data_f2 = pd.read_csv('data/follower&contact.csv', sep=",", header = 0)
data_f2.columns=['uidFull','u_follower','u_contact']



data_f3 = pd.read_csv('data/Output.csv', sep=",", header = 0)
data_f3.columns=['uidFull','pidFull','p_commentCount','p_viewCount',
'p_tagCount','p_postDate','p_hasPeople',
'p_groupCount','p_favoriteCount','u_photoCount',
'p_avgMemberCount','p_avgPhotoCount']


data_f4=pd.merge(data_f1, data_f2, on='uidFull')
data_f5=pd.merge(data_f4, data_f3, on=['uidFull','pidFull'])


#data_f5 = pd.read_csv('final0606.csv', sep=",", header = 0)
#data_f5.drop(['Unnamed: 0'], axis=1, inplace=True)
cols=data_f5.columns.tolist()

"""
features_cols=['p_titleLen', 'p_desLen',
'u_avgView', 'u_groupCount', 'u_avgMemberCount','u_follower',
'u_contact', 'p_commentCount','p_viewCount', 'p_tagCount',
'p_groupCount', 'p_favoriteCount','u_photoCount',
'p_avgMemberCount', 'p_avgPhotoCount']
"""

features_cols=['p_titleLen', 'p_desLen',
'u_avgView', 'u_groupCount', 'u_avgMemberCount','u_follower',
'p_commentCount','p_viewCount', 'p_tagCount',
'p_groupCount', 'p_favoriteCount']


X =np.array(data_f5[features_cols].values,float)
y =np.array(data_f5['p_Score'].values,float)
nor = X.max(axis=0)
X = X/X.max(axis=0)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=42)

def baseline_model():
    # create model
    model = Sequential()
    model.add(Dense(120, input_dim = 11, init="normal", activation='relu'))
    model.add(Dense(120, init="normal", activation='relu'))
    model.add(Dense(1, init="normal"))
    sgd = SGD(lr=0.01, decay=1e-6, momentum=0.0, nesterov=True)
    # Compile model
    model.compile(loss='mse', optimizer='adam')
    return model




model.fit(X, y, nb_epoch=200, batch_size=20, validation_split=0.1, verbose=0, shuffle=True)


seed = 7
np.random.seed(seed)
# evaluate model with standardized dataset
estimator = KerasRegressor(build_fn=baseline_model, nb_epoch=200, batch_size=20,validation_split=0.1, verbose=1, shuffle=True)


kfold = KFold(n_splits=10, random_state=seed)
results = cross_val_score(estimator, X, y, cv=kfold)
print("Results: %.2f (%.2f) MSE" % (results.mean(), results.std()))
