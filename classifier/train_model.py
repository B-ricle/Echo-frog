from sklearn.linear_model import LogisticRegression
from classifier.features import build_training_data
import joblib

if __name__ == "__main__":
    X,y = build_training_data()
    model = LogisticRegression()
    model.fit(X,y)
    joblib.dump(model, 'classifier/model.joblib')


    predictions = model.predict(X)

    print(predictions)
    print(y)
