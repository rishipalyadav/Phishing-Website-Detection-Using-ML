import numpy as np

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn import metrics

import sys
import joblib

labels=[]
features=[]
file=open('Training Dataset.arff').read()
list=file.split('\n')
data=np.array(list)
data_new=[i.split(',') for i in data]
data_new=data_new[0:-1]
for i in data_new:
	labels.append(i[30])
data_new=np.array(data_new)
# print(data_new)
features=data_new[:,:-1]
# print(features)
features=features[:,[0,1,2,3,4,5,6,8,9,10,11,12,13,14,15,16,17,22,23,24,25,27,29]]
# print (features)
features=np.array(features).astype(np.float)
#
# ##### HAS TO BE CHANGED TO ALL ENTRIES OF THE DATASET
features_train=features
labels_train=labels
# features_test=features[10000:]
# labels_test=labels[10000:]
# print(features_train)
# print('\n\n\n')
# print(labels_train)

#
print("\n\n ""Random Forest Algorithm Results"" ")
clf4 = RandomForestClassifier(min_samples_split=7, verbose=True)
clf4.fit(features_train, labels_train)
importances = clf4.feature_importances_
# std = np.std([tree.feature_importances_ for tree in clf4.estimators_],
             # axis=0)
indices = np.argsort(importances)[::-1]
# Print the feature ranking
print("Feature ranking:")
for f in range(features_train.shape[1]):
    print("%d. feature %d (%f)" % (f + 1, indices[f], importances[indices[f]]))


# pred4=clf4.predict(features_test)
# print(classification_report(labels_test, pred4))
# print ('The accuracy is:', accuracy_score(labels_test, pred4))
# print (metrics.confusion_matrix(labels_test, pred4))

#sys.setrecursionlimit(9999999)
joblib.dump(clf4, 'random_forest.pkl',compress=9)
