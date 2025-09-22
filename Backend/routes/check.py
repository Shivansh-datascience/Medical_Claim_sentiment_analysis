import pickle
import joblib
import warnings
warnings.filterwarnings(action='ignore')

file_path = r"D:\AI_powered_Medical_sentiment_analysis\notebooks\logistic_regression.pkl"
model = joblib.load(file_path)

#validate the learned classes 
print(model)
print("Classes:", model.classes_)
print("Best score :",model.best_score_)
print(" Best Parameters Model trained:",model.best_params_)


