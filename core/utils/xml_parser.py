import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom
import xml.sax
from lxml import etree
import time
import psutil
import os

class XMLProfiler:
    """Profile XML files to extract characteristics"""
    
    def __init__(self, file_path):
        self.file_path = file_path
        self.file_size = os.path.getsize(file_path)
        
    def profile(self):
        """Extract XML file characteristics"""
        try:
            tree = ET.parse(self.file_path)
            root = tree.getroot()
            
            total_elements = len(list(root.iter()))
            max_depth = self._get_max_depth(root)
            total_attributes = sum(len(elem.attrib) for elem in root.iter())
            
            # Determine complexity
            complexity = self._determine_complexity(total_elements, max_depth)
            
            return {
                'file_size': self.file_size,
                'file_size_mb': round(self.file_size / (1024 * 1024), 2),
                'total_elements': total_elements,
                'max_depth': max_depth,
                'total_attributes': total_attributes,
                'complexity': complexity
            }
        except Exception as e:
            return {'error': str(e)}
    
    def _get_max_depth(self, element, current_depth=0):
        """Calculate maximum depth of XML tree"""
        if len(element) == 0:
            return current_depth
        return max(self._get_max_depth(child, current_depth + 1) for child in element)
    
    def _determine_complexity(self, elements, depth):
        """Determine XML complexity level"""
        if elements < 100 and depth < 5:
            return 'Simple'
        elif elements < 1000 and depth < 10:
            return 'Medium'
        else:
            return 'Complex'


class XMLParserBenchmark:
    """Benchmark different XML parsers"""
    
    def __init__(self, file_path):
        self.file_path = file_path
        self.process = psutil.Process(os.getpid())
        
    def benchmark_dom(self):
        """Benchmark DOM parser"""
        start_mem = self.process.memory_info().rss / 1024 / 1024
        start_time = time.time()
        
        try:
            dom = minidom.parse(self.file_path)
            elements = dom.getElementsByTagName('*')
            
            end_time = time.time()
            end_mem = self.process.memory_info().rss / 1024 / 1024
            
            return {
                'parser': 'DOM',
                'time': round(end_time - start_time, 4),
                'memory': round(end_mem - start_mem, 2),
                'success': True
            }
        except Exception as e:
            return {'parser': 'DOM', 'success': False, 'error': str(e)}
    
    def benchmark_etree(self):
        """Benchmark ElementTree parser"""
        start_mem = self.process.memory_info().rss / 1024 / 1024
        start_time = time.time()
        
        try:
            tree = ET.parse(self.file_path)
            root = tree.getroot()
            elements = list(root.iter())
            
            end_time = time.time()
            end_mem = self.process.memory_info().rss / 1024 / 1024
            
            return {
                'parser': 'ElementTree',
                'time': round(end_time - start_time, 4),
                'memory': round(end_mem - start_mem, 2),
                'success': True
            }
        except Exception as e:
            return {'parser': 'ElementTree', 'success': False, 'error': str(e)}
    
    def benchmark_lxml(self):
        """Benchmark lxml parser"""
        start_mem = self.process.memory_info().rss / 1024 / 1024
        start_time = time.time()
        
        try:
            tree = etree.parse(self.file_path)
            root = tree.getroot()
            elements = list(root.iter())
            
            end_time = time.time()
            end_mem = self.process.memory_info().rss / 1024 / 1024
            
            return {
                'parser': 'lxml',
                'time': round(end_time - start_time, 4),
                'memory': round(end_mem - start_mem, 2),
                'success': True
            }
        except Exception as e:
            return {'parser': 'lxml', 'success': False, 'error': str(e)}
    
    def benchmark_all(self):
        """Run all benchmarks"""
        results = []
        results.append(self.benchmark_dom())
        results.append(self.benchmark_etree())
        results.append(self.benchmark_lxml())
        return results
