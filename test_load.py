import joblib
import traceback
try:
    print("Loading model...")
    joblib.load('lr_model.pkl')
    print("Loading vectorizer...")
    joblib.load('tfidf_vectorizer.pkl')
    print("SUCCESS")
except Exception as e:
    print("FAILED")
    traceback.print_exc()
