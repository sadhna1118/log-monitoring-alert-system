"""
Machine Learning module for anomaly detection in logs.
"""

import os
import pickle
from typing import List, Tuple
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.feature_extraction.text import TfidfVectorizer
from datetime import datetime


class MLAnomalyDetector:
    """Machine Learning based anomaly detection."""
    
    def __init__(self, model_path: str = "models/anomaly_detector.pkl"):
        """
        Initialize ML detector.
        
        Args:
            model_path: Path to save/load model
        """
        self.model_path = model_path
        self.vectorizer = TfidfVectorizer(max_features=100)
        self.model = IsolationForest(
            contamination=0.1,
            random_state=42,
            n_estimators=100
        )
        self.is_trained = False
        
        # Try to load existing model
        self._load_model()
    
    def _ensure_model_directory(self):
        """Create models directory if it doesn't exist."""
        model_dir = os.path.dirname(self.model_path)
        if model_dir and not os.path.exists(model_dir):
            os.makedirs(model_dir)
    
    def _load_model(self):
        """Load trained model from disk."""
        if os.path.exists(self.model_path):
            try:
                with open(self.model_path, 'rb') as f:
                    data = pickle.load(f)
                    self.vectorizer = data['vectorizer']
                    self.model = data['model']
                    self.is_trained = True
                print(f"✅ ML model loaded from {self.model_path}")
            except Exception as e:
                print(f"Warning: Could not load ML model: {str(e)}")
    
    def _save_model(self):
        """Save trained model to disk."""
        self._ensure_model_directory()
        
        try:
            with open(self.model_path, 'wb') as f:
                pickle.dump({
                    'vectorizer': self.vectorizer,
                    'model': self.model,
                    'trained_date': datetime.now().isoformat()
                }, f)
            print(f"✅ ML model saved to {self.model_path}")
        except Exception as e:
            print(f"Warning: Could not save ML model: {str(e)}")
    
    def train(self, log_messages: List[str]):
        """
        Train the anomaly detection model.
        
        Args:
            log_messages: List of log messages to train on
        """
        if len(log_messages) < 10:
            print("Warning: Need at least 10 log messages to train ML model")
            return
        
        print(f"Training ML model on {len(log_messages)} log messages...")
        
        # Vectorize log messages
        X = self.vectorizer.fit_transform(log_messages)
        
        # Train model
        self.model.fit(X.toarray())
        self.is_trained = True
        
        # Save model
        self._save_model()
        
        print("✅ ML model training complete")
    
    def predict(self, log_message: str) -> Tuple[bool, float]:
        """
        Predict if a log message is anomalous.
        
        Args:
            log_message: Log message to analyze
            
        Returns:
            Tuple of (is_anomaly, anomaly_score)
        """
        if not self.is_trained:
            return False, 0.0
        
        try:
            # Vectorize message
            X = self.vectorizer.transform([log_message])
            
            # Predict
            prediction = self.model.predict(X.toarray())
            score = self.model.score_samples(X.toarray())
            
            # -1 means anomaly, 1 means normal
            is_anomaly = prediction[0] == -1
            anomaly_score = float(-score[0])  # Higher score = more anomalous
            
            return is_anomaly, anomaly_score
            
        except Exception as e:
            print(f"Warning: ML prediction failed: {str(e)}")
            return False, 0.0
    
    def batch_predict(self, log_messages: List[str]) -> List[Tuple[bool, float]]:
        """
        Predict anomalies for multiple log messages.
        
        Args:
            log_messages: List of log messages
            
        Returns:
            List of (is_anomaly, anomaly_score) tuples
        """
        if not self.is_trained or not log_messages:
            return [(False, 0.0)] * len(log_messages)
        
        try:
            # Vectorize messages
            X = self.vectorizer.transform(log_messages)
            
            # Predict
            predictions = self.model.predict(X.toarray())
            scores = self.model.score_samples(X.toarray())
            
            results = []
            for pred, score in zip(predictions, scores):
                is_anomaly = pred == -1
                anomaly_score = float(-score)
                results.append((is_anomaly, anomaly_score))
            
            return results
            
        except Exception as e:
            print(f"Warning: Batch ML prediction failed: {str(e)}")
            return [(False, 0.0)] * len(log_messages)
    
    def retrain_incremental(self, new_log_messages: List[str]):
        """
        Retrain model with new data (incremental learning).
        
        Args:
            new_log_messages: New log messages to train on
        """
        if len(new_log_messages) < 5:
            return
        
        print(f"Retraining ML model with {len(new_log_messages)} new messages...")
        
        # This is a simple approach - for production, implement proper incremental learning
        self.train(new_log_messages)