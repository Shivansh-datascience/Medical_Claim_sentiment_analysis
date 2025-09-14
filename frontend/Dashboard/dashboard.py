from explainerdashboard import ClassifierExplainer, ExplainerDashboard
import joblib
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction.text import TfidfVectorizer
import warnings
warnings.filterwarnings('ignore')

# File paths - use consistent separators
file_path_lr = r"D:\AI_powered_Medical_sentiment_analysis\notebooks\logistic_regression.pkl"
file_path_vectorizer = r"D:\AI_powered_Medical_sentiment_analysis\notebooks\Vectorize.pkl"
file_path_training = r"D:\AI_powered_Medical_sentiment_analysis\notebooks\X_train (3).csv"
file_path_testing = r"D:\AI_powered_Medical_sentiment_analysis\notebooks\X_test (2).csv"
file_path_y_train = r"D:\AI_powered_Medical_sentiment_analysis\notebooks\y_train (1).csv"

def load_and_prepare_data():
    """Load and prepare all necessary data for the dashboard"""
    
    print("Loading model and vectorizer...")
    try:
        # Load model and vectorizer
        lr_model = joblib.load(file_path_lr)
        vectorizer = joblib.load(file_path_vectorizer)
        print("✓ Model and vectorizer loaded successfully")
    except Exception as e:
        print(f"✗ Error loading model/vectorizer: {e}")
        return None, None, None, None, None
    
    print("Loading training data...")
    try:
        # Load the vectorized training data
        X_train = pd.read_csv(file_path_training)
        y_train = pd.read_csv(file_path_y_train).values.ravel()
        print(f"✓ Training data loaded: X_train shape {X_train.shape}, y_train shape {y_train.shape}")
    except Exception as e:
        print(f"✗ Error loading training data: {e}")
        return None, None, None, None, None
    
    # Initialize and fit label encoder
    le = LabelEncoder()
    y_train_encoded = le.fit_transform(y_train)
    print(f"✓ Labels encoded. Classes: {le.classes_}")
    
    # Get feature names from vectorizer
    try:
        feature_names = vectorizer.get_feature_names_out()
    except AttributeError:
        try:
            feature_names = vectorizer.get_feature_names()
        except AttributeError:
            print("Warning: Could not get feature names from vectorizer")
            feature_names = [f"feature_{i}" for i in range(X_train.shape[1])]
    
    # Ensure X_train has proper column names
    if len(X_train.columns) != len(feature_names):
        print(f"Warning: Column count mismatch. X_train has {len(X_train.columns)} columns, "
              f"vectorizer has {len(feature_names)} features")
        # Adjust based on actual data
        if X_train.shape[1] == len(feature_names):
            X_train.columns = feature_names
        else:
            print("Using existing column names")
    else:
        X_train.columns = feature_names
    
    print(f"✓ Feature names set: {X_train.shape[1]} features")
    
    return lr_model, vectorizer, X_train, y_train_encoded, le

def validate_model_compatibility(model, X_sample):
    """Validate that model works with the provided data"""
    try:
        # Test prediction
        pred_proba = model.predict_proba(X_sample.iloc[:5])
        pred = model.predict(X_sample.iloc[:5])
        print(f"✓ Model validation successful. Sample predictions: {pred}")
        print(f"✓ Sample probabilities shape: {pred_proba.shape}")
        return True
    except Exception as e:
        print(f"✗ Model validation failed: {e}")
        return False

def create_dashboard(model, X_sample, y_sample, le) -> ExplainerDashboard:
    """Create and run the explainer dashboard"""
    
    print("Creating classifier explainer...")
    
    # Create descriptions for better dashboard experience
    descriptions = {
        'target': 'Medical Claim Sentiment Analysis',
    }
    
    # Add class descriptions
    for i, class_name in enumerate(le.classes_):
        descriptions[f'target_{i}'] = str(class_name).title()
    
    try:
        classifier_explainer = ClassifierExplainer(
            model=model,
            X=X_sample,
            y=y_sample,
            shap="guess",  # Let explainer choose best SHAP method
            model_output="probability",
            descriptions=descriptions,
            labels=le.classes_  # Add explicit labels
        )
        
        print("✓ Classifier explainer created successfully")
        
    except Exception as e:
        print(f"✗ Error creating explainer: {e}")
        # Try with simpler configuration
        print("Trying with simplified configuration...")
        classifier_explainer = ClassifierExplainer(
            model=model,
            X=X_sample,
            y=y_sample,
            descriptions=descriptions
        )
    
    print("Creating dashboard...")
    dashboard = ExplainerDashboard(
        explainer=classifier_explainer,
        title="Medical Claim Sentiment Analysis Dashboard",
        # Add some dashboard customizations
        whatif=True,          # Enable what-if analysis
        shap_dependence=True, # Enable SHAP dependence plots
        decision_trees=False  # Disable decision trees for logistic regression
    )
    
    print("Starting dashboard server...")
    dashboard.run(port=8076, host='127.0.0.1')
    
    return dashboard

def main():
    """Main function to run the dashboard"""
    
    print("=== Medical Sentiment Analysis Dashboard ===")
    print("Loading data and model...")
    
    # Load all data
    lr_model, vectorizer, X_train, y_train_encoded, le = load_and_prepare_data()
    
    if lr_model is None:
        print("Failed to load required data. Exiting...")
        return
    
    # Sample the data for dashboard (adjust sample size based on performance needs)
    sample_size = min(500, len(X_train))  # Use up to 500 samples
    print(f"Sampling {sample_size} records for dashboard...")
    
    X_sample = X_train.sample(n=sample_size, random_state=42)
    y_sample = y_train_encoded[X_sample.index]
    
    print(f"✓ Sample data prepared: {X_sample.shape[0]} samples, {X_sample.shape[1]} features")
    print(f"✓ Target distribution: {np.bincount(y_sample)}")
    
    # Validate model compatibility
    if not validate_model_compatibility(lr_model, X_sample):
        print("Model validation failed. Please check your data and model compatibility.")
        return
    
    # Create and run dashboard
    try:
        dashboard = create_dashboard(lr_model, X_sample, y_sample, le)
        print("✓ Dashboard created successfully!")
        print("Access dashboard at: http://localhost:8076")
        
    except Exception as e:
        print(f"✗ Error creating dashboard: {e}")
        print("\nTroubleshooting tips:")
        print("1. Ensure all file paths are correct")
        print("2. Check that X_train contains TF-IDF vectors, not raw text")
        print("3. Verify model and vectorizer are compatible")
        print("4. Try reducing sample size if memory issues occur")

# Additional utility functions for debugging
def debug_data_info(X_train, y_train, vectorizer, le):
    """Print debugging information about the data"""
    
    print("\n=== DEBUG INFO ===")
    print(f"X_train shape: {X_train.shape}")
    print(f"X_train dtypes: {X_train.dtypes.value_counts()}")
    print(f"y_train shape: {y_train.shape}")
    print(f"y_train unique values: {np.unique(y_train)}")
    print(f"Label classes: {le.classes_}")
    print(f"Vectorizer type: {type(vectorizer)}")
    
    if hasattr(vectorizer, 'vocabulary_'):
        print(f"Vectorizer vocabulary size: {len(vectorizer.vocabulary_)}")
    
    print(f"X_train non-zero values: {np.count_nonzero(X_train.values)}")
    print(f"X_train sparsity: {1 - np.count_nonzero(X_train.values) / X_train.size:.3f}")
    print("===================\n")

if __name__ == "__main__":
    main()
