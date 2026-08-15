import sys
import os
import django

# Setup Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'xml_optimizer.settings')
django.setup()

from parser_optimizer.ml_predictor import ParserMLPredictor
from django.conf import settings

def main():
    print("=" * 60)
    print("XML Parser Optimizer - ML Model Training")
    print("=" * 60)
    
    dataset_path = os.path.join(settings.DATASETS_DIR, 'parser_performance.csv')
    
    if not os.path.exists(dataset_path):
        print(f"Error: Dataset not found at {dataset_path}")
        print("Please generate the dataset first using: python datasets/generate_dataset.py")
        return
    
    predictor = ParserMLPredictor()
    results = predictor.train_and_save_models(dataset_path)
    
    print("\n" + "=" * 60)
    print("Training Complete!")
    print("=" * 60)
    print(f"ANN Accuracy: {results['ann_metrics']['accuracy']:.4f}")
    print(f"SVM Accuracy: {results['svm_metrics']['accuracy']:.4f}")

if __name__ == "__main__":
    main()
