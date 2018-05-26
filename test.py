import joblib, features, sys

def main():
    url=sys.argv[1]

    features_test=features.main(url)

    clf = joblib.load('random_forest.pkl')

    pred=clf.predict(features_test)
    prob=clf.predict_proba(features_test)

    if int(pred[0])==1:
        print ("This is a safe website.")
    elif int(pred[0])==-1:
        print ("This is a phishing website..!")

if __name__=="__main__":
    main()
