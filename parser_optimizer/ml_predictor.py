import numpy as np
import pandas as pd
import joblib
import os
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report
from django.conf import settings

class ParserMLPredictor:
    """Machine Learning predictor for optimal parser selection"""
    
    def __init__(self):
        self.scaler = StandardScaler()
        self.ann_model = None
        self.svm_model = None
        self.models_dir = settings.ML_MODELS_DIR
        
        # Create models directory if it doesn't exist
        os.makedirs(self.models_dir, exist_ok=True)
        
        # Parser mapping
        self.parser_mapping = {
            0: 'DOM',
            1: 'SAX',
            2: 'StAX',
            3: 'ElementTree',
            4: 'lxml'
        }
    
    def load_dataset(self, dataset_path):
        """Load training dataset"""
        df = pd.read_csv(dataset_path)
        
        # Features
        X = df[['file_size_mb', 'total_elements', 'max_depth', 'processor_cores']].values
        
        # Target
        y = df['best_parser'].values
        
        return X, y
    
    def train_ann_model(self, X_train, y_train):
        """Train Artificial Neural Network model"""
        print("Training ANN model...")
        
        self.ann_model = MLPClassifier(
            hidden_layer_sizes=(128, 64, 32),
            activation='relu',
            solver='adam',
            max_iter=500,
            random_state=42,
            early_stopping=True,
            validation_fraction=0.1
        )
        
        self.ann_model.fit(X_train, y_train)
        print("ANN model trained successfully")
        
        return self.ann_model
    
    def train_svm_model(self, X_train, y_train):
        """Train Support Vector Machine model"""
        print("Training SVM model...")
        
        self.svm_model = SVC(
            kernel='rbf',
            C=10,
            gamma='scale',
            random_state=42,
            probability=True
        )
        
        self.svm_model.fit(X_train, y_train)
        print("SVM model trained successfully")
        
        return self.svm_model
    
    def evaluate_model(self, model, X_test, y_test, model_name):
        """Evaluate model performance"""
        y_pred = model.predict(X_test)
        
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred, average='weighted', zero_division=0)
        recall = recall_score(y_test, y_pred, average='weighted', zero_division=0)
        f1 = f1_score(y_test, y_pred, average='weighted', zero_division=0)
        
        print(f"\n{model_name} Performance:")
        print(f"Accuracy: {accuracy:.4f}")
        print(f"Precision: {precision:.4f}")
        print(f"Recall: {recall:.4f}")
        print(f"F1-Score: {f1:.4f}")
        
        # Get unique classes in test set
        unique_classes = sorted(set(y_test) | set(y_pred))
        target_names = [self.parser_mapping[i] for i in unique_classes]
        
        print(f"\nClassification Report:")
        print(classification_report(y_test, y_pred, labels=unique_classes, target_names=target_names, zero_division=0))
        
        return {
            'accuracy': accuracy,
            'precision': precision,
            'recall': recall,
            'f1_score': f1
        }
    
    def train_and_save_models(self, dataset_path):
        """Complete training pipeline"""
        # Load data
        print(f"\n📊 Loading dataset from: {dataset_path}")
        X, y = self.load_dataset(dataset_path)
        
        # Check dataset info
        unique_classes = np.unique(y)
        print(f"✓ Dataset loaded: {len(X)} samples")
        print(f"✓ Features: {X.shape[1]}")
        print(f"✓ Unique parsers in dataset: {unique_classes}")
        print(f"✓ Parser distribution:")
        for parser_id in unique_classes:
            parser_name = self.parser_mapping.get(parser_id, f"Unknown-{parser_id}")
            count = np.sum(y == parser_id)
            print(f"   {parser_name}: {count} samples ({count/len(y)*100:.1f}%)")
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        print(f"\n✓ Train set: {len(X_train)} samples")
        print(f"✓ Test set: {len(X_test)} samples")
        
        # Scale features
        print("\n⚙️  Scaling features...")
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Train ANN
        print("\n" + "="*60)
        print("Training Artificial Neural Network (ANN)")
        print("="*60)
        self.train_ann_model(X_train_scaled, y_train)
        ann_metrics = self.evaluate_model(self.ann_model, X_test_scaled, y_test, "ANN")
        
        # Train SVM
        print("\n" + "="*60)
        print("Training Support Vector Machine (SVM)")
        print("="*60)
        self.train_svm_model(X_train_scaled, y_train)
        svm_metrics = self.evaluate_model(self.svm_model, X_test_scaled, y_test, "SVM")
        
        # Save models
        print("\n💾 Saving models...")
        ann_path = os.path.join(self.models_dir, 'ann_model.pkl')
        svm_path = os.path.join(self.models_dir, 'svm_model.pkl')
        scaler_path = os.path.join(self.models_dir, 'scaler.pkl')
        
        joblib.dump(self.ann_model, ann_path)
        joblib.dump(self.svm_model, svm_path)
        joblib.dump(self.scaler, scaler_path)
        
        print(f"✓ ANN model saved: {ann_path}")
        print(f"✓ SVM model saved: {svm_path}")
        print(f"✓ Scaler saved: {scaler_path}")
        
        print("\n✅ Models saved successfully!")
        
        return {
            'ann_metrics': ann_metrics,
            'svm_metrics': svm_metrics
        }
    
    def load_models(self):
        """Load trained models"""
        try:
            ann_path = os.path.join(self.models_dir, 'ann_model.pkl')
            svm_path = os.path.join(self.models_dir, 'svm_model.pkl')
            scaler_path = os.path.join(self.models_dir, 'scaler.pkl')
            
            self.ann_model = joblib.load(ann_path)
            self.svm_model = joblib.load(svm_path)
            self.scaler = joblib.load(scaler_path)
            
            print("✓ Models loaded successfully")
            return True
        except Exception as e:
            print(f"✗ Error loading models: {e}")
            return False
    
    def predict(self, features, model_type='ANN'):
        """
        Predict best parser for given features
        
        Args:
            features: [file_size_mb, total_elements, max_depth, processor_cores]
            model_type: 'ANN' or 'SVM'
        
        Returns:
            dict with parser name, confidence, and probabilities
        """
        # Validate features
        if len(features) != 4:
            raise ValueError("Features must have 4 values: [file_size_mb, total_elements, max_depth, processor_cores]")
        
        # Convert to array and scale
        features_array = np.array(features).reshape(1, -1)
        features_scaled = self.scaler.transform(features_array)
        
        # Select model
        if model_type == 'ANN':
            if self.ann_model is None:
                raise ValueError("ANN model not loaded. Please load models first.")
            model = self.ann_model
        else:  # SVM
            if self.svm_model is None:
                raise ValueError("SVM model not loaded. Please load models first.")
            model = self.svm_model
        
        # Make prediction
        prediction = model.predict(features_scaled)[0]
        probabilities = model.predict_proba(features_scaled)[0]
        
        # Get parser name
        parser_name = self.parser_mapping.get(prediction, 'Unknown')
        confidence = max(probabilities) * 100
        
        # Create probability dictionary for all parsers
        prob_dict = {}
        for i, prob in enumerate(probabilities):
            if i in self.parser_mapping:
                prob_dict[self.parser_mapping[i]] = round(prob * 100, 2)
        
        return {
            'parser': parser_name,
            'parser_id': int(prediction),
            'confidence': round(confidence, 2),
            'probabilities': prob_dict,
            'model_used': model_type
        }
    
    def compare_models(self, features):
        """
        Compare predictions from both ANN and SVM models
        
        Args:
            features: [file_size_mb, total_elements, max_depth, processor_cores]
        
        Returns:
            dict with predictions from both models
        """
        ann_pred = self.predict(features, model_type='ANN')
        svm_pred = self.predict(features, model_type='SVM')
        
        return {
            'ann_prediction': ann_pred,
            'svm_prediction': svm_pred,
            'agreement': ann_pred['parser'] == svm_pred['parser']
        }
