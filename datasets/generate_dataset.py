import pandas as pd
import numpy as np
import random

def generate_parser_performance_dataset(num_samples=1000):
    """
    Generate synthetic training dataset for parser selection
    Features: file_size_mb, total_elements, max_depth, processor_cores
    Target: best_parser (0=DOM, 1=SAX, 2=StAX, 3=ElementTree, 4=lxml)
    """
    
    np.random.seed(42)
    random.seed(42)
    
    data = []
    
    # Ensure minimum samples per parser
    samples_per_parser = num_samples // 5
    
    for _ in range(num_samples):
        file_size_mb = round(random.uniform(0.1, 500), 2)
        total_elements = random.randint(10, 100000)
        max_depth = random.randint(2, 50)
        processor_cores = random.choice([2, 4, 6, 8, 12, 16])
        
        # Enhanced rule-based parser selection to ensure all parsers are used
        # Calculate score for each parser
        scores = {}
        
        # DOM - best for small files with random access
        if file_size_mb < 5 and total_elements < 1000:
            scores[0] = 10
        else:
            scores[0] = max(0, 10 - (file_size_mb / 5))
        
        # SAX - best for large files, memory efficient streaming
        if file_size_mb > 50 or total_elements > 50000:
            scores[1] = 10
        else:
            scores[1] = file_size_mb / 10
        
        # StAX - good for selective parsing with streaming
        if file_size_mb > 20 and max_depth > 15:
            scores[2] = 9
        else:
            scores[2] = (file_size_mb / 20) + (max_depth / 10)
        
        # ElementTree - general purpose, balanced
        if 1 < file_size_mb < 100 and 100 < total_elements < 50000:
            scores[3] = 10
        else:
            scores[3] = 5 + random.uniform(-2, 2)
        
        # lxml - high performance for complex queries
        if file_size_mb > 10 or max_depth > 20 or processor_cores >= 8:
            scores[4] = 10
        else:
            scores[4] = (file_size_mb / 10) + (processor_cores / 8)
        
        # Add randomness to scores
        for key in scores:
            scores[key] += random.uniform(-1, 1)
        
        # Select parser with highest score
        best_parser = max(scores, key=scores.get)
        
        # Assign performance metrics based on parser selection
        if best_parser == 0:  # DOM
            parsing_time = round(random.uniform(0.01, 0.5), 4)
            memory_usage = round(file_size_mb * 2.5, 2)
        elif best_parser == 1:  # SAX
            parsing_time = round(random.uniform(0.1, 2), 4)
            memory_usage = round(file_size_mb * 0.5, 2)
        elif best_parser == 2:  # StAX
            parsing_time = round(random.uniform(0.2, 3), 4)
            memory_usage = round(file_size_mb * 0.8, 2)
        elif best_parser == 3:  # ElementTree
            parsing_time = round(random.uniform(0.1, 2), 4)
            memory_usage = round(file_size_mb * 1.3, 2)
        else:  # lxml
            parsing_time = round(random.uniform(0.05, 1.5), 4)
            memory_usage = round(file_size_mb * 1.1, 2)
        
        efficiency_score = round(100 / (parsing_time + memory_usage/10 + 0.1), 2)
        
        data.append({
            'file_size_mb': file_size_mb,
            'total_elements': total_elements,
            'max_depth': max_depth,
            'processor_cores': processor_cores,
            'best_parser': best_parser,
            'parsing_time': parsing_time,
            'memory_usage': memory_usage,
            'efficiency_score': efficiency_score
        })
    
    df = pd.DataFrame(data)
    
    # Verify all parsers are represented
    parser_counts = df['best_parser'].value_counts().sort_index()
    print("\nParser distribution before balancing:")
    print(parser_counts)
    
    # Balance dataset if any parser is underrepresented
    min_samples = 50
    for parser_id in range(5):
        count = len(df[df['best_parser'] == parser_id])
        if count < min_samples:
            # Add more samples for this parser
            needed = min_samples - count
            print(f"\nAdding {needed} samples for parser {parser_id}")
            for _ in range(needed):
                # Generate targeted samples for this parser
                if parser_id == 0:  # DOM
                    sample = {
                        'file_size_mb': round(random.uniform(0.1, 5), 2),
                        'total_elements': random.randint(10, 1000),
                        'max_depth': random.randint(2, 8),
                        'processor_cores': random.choice([2, 4, 6, 8]),
                        'best_parser': 0,
                        'parsing_time': round(random.uniform(0.01, 0.5), 4),
                        'memory_usage': round(random.uniform(0.5, 10), 2),
                        'efficiency_score': round(random.uniform(5, 15), 2)
                    }
                elif parser_id == 1:  # SAX
                    sample = {
                        'file_size_mb': round(random.uniform(50, 500), 2),
                        'total_elements': random.randint(50000, 100000),
                        'max_depth': random.randint(10, 50),
                        'processor_cores': random.choice([4, 8, 12, 16]),
                        'best_parser': 1,
                        'parsing_time': round(random.uniform(0.5, 3), 4),
                        'memory_usage': round(random.uniform(10, 50), 2),
                        'efficiency_score': round(random.uniform(3, 10), 2)
                    }
                elif parser_id == 2:  # StAX
                    sample = {
                        'file_size_mb': round(random.uniform(20, 200), 2),
                        'total_elements': random.randint(10000, 80000),
                        'max_depth': random.randint(15, 40),
                        'processor_cores': random.choice([4, 6, 8, 12]),
                        'best_parser': 2,
                        'parsing_time': round(random.uniform(0.3, 4), 4),
                        'memory_usage': round(random.uniform(15, 80), 2),
                        'efficiency_score': round(random.uniform(2, 8), 2)
                    }
                elif parser_id == 3:  # ElementTree
                    sample = {
                        'file_size_mb': round(random.uniform(1, 50), 2),
                        'total_elements': random.randint(500, 30000),
                        'max_depth': random.randint(5, 20),
                        'processor_cores': random.choice([2, 4, 6, 8]),
                        'best_parser': 3,
                        'parsing_time': round(random.uniform(0.1, 2), 4),
                        'memory_usage': round(random.uniform(5, 50), 2),
                        'efficiency_score': round(random.uniform(4, 12), 2)
                    }
                else:  # lxml
                    sample = {
                        'file_size_mb': round(random.uniform(10, 300), 2),
                        'total_elements': random.randint(5000, 90000),
                        'max_depth': random.randint(10, 45),
                        'processor_cores': random.choice([6, 8, 12, 16]),
                        'best_parser': 4,
                        'parsing_time': round(random.uniform(0.05, 2), 4),
                        'memory_usage': round(random.uniform(10, 100), 2),
                        'efficiency_score': round(random.uniform(5, 15), 2)
                    }
                data.append(sample)
    
    # Recreate dataframe with balanced data
    df = pd.DataFrame(data)
    
    # Save to CSV
    df.to_csv('datasets/parser_performance.csv', index=False)
    print(f"\n✅ Generated {len(df)} records and saved to datasets/parser_performance.csv")
    print(f"\nDataset Info:")
    print(df.info())
    print(f"\nFirst 5 rows:")
    print(df.head())
    print(f"\nParser distribution (final):")
    parser_dist = df['best_parser'].value_counts().sort_index()
    for parser_id, count in parser_dist.items():
        parser_names = {0: 'DOM', 1: 'SAX', 2: 'StAX', 3: 'ElementTree', 4: 'lxml'}
        print(f"  {parser_names[parser_id]}: {count} samples ({count/len(df)*100:.1f}%)")
    
    return df

if __name__ == "__main__":
    # Create datasets directory if it doesn't exist
    import os
    os.makedirs('datasets', exist_ok=True)
    
    # Generate dataset
    generate_parser_performance_dataset(1000)
