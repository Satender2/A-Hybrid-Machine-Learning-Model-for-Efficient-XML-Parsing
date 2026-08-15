# Advanced lxml Parser with Multi-Level XML Optimization
from lxml import etree
from typing import Optional
import time
import os
import re
import json


class LxmlOptimizer:
    '''lxml-based XML optimizer with multiple optimization levels'''
    
    def __init__(self):
        self.tag_mapping = {}
        self.attr_mapping = {}
        self.tag_counter = 0
        self.attr_counter = 0
    
    def optimize(self, input_file: str, output_base: str, level: str = 'medium'):
        '''Optimize XML file using lxml'''
        parser = etree.XMLParser(remove_blank_text=True)
        tree = etree.parse(input_file, parser)
        root = tree.getroot()
        
        if level == 'light':
            self._optimize_light(root)
        elif level == 'medium':
            self._optimize_medium(root)
        elif level == 'heavy':
            self._optimize_heavy(root)
        
        output_file = f"{output_base}_optimized_{level}.xml"
        tree.write(output_file, encoding='utf-8', xml_declaration=True, 
                   pretty_print=False)
        
        if level in ['medium', 'heavy']:
            self._save_mapping(f"{output_base}_optimized_{level}_mapping.json")
        
        return output_file
    
    def _optimize_light(self, elem):
        '''Remove whitespace'''
        if elem.text:
            elem.text = elem.text.strip() if elem.text.strip() else None
        if elem.tail:
            elem.tail = elem.tail.strip() if elem.tail.strip() else None
        for child in elem:
            self._optimize_light(child)
    
    def _optimize_medium(self, elem):
        '''Compress tags and attributes'''
        original_tag = elem.tag
        if original_tag not in self.tag_mapping:
            self.tag_mapping[original_tag] = f"t{self.tag_counter}"
            self.tag_counter += 1
        elem.tag = self.tag_mapping[original_tag]
        
        new_attrib = {}
        for key, value in elem.attrib.items():
            if key not in self.attr_mapping:
                self.attr_mapping[key] = f"a{self.attr_counter}"
                self.attr_counter += 1
            new_attrib[self.attr_mapping[key]] = value
        elem.attrib.clear()
        elem.attrib.update(new_attrib)
        
        if elem.text:
            elem.text = elem.text.strip() if elem.text.strip() else None
        if elem.tail:
            elem.tail = elem.tail.strip() if elem.tail.strip() else None
        
        for child in elem:
            self._optimize_medium(child)
    
    def _optimize_heavy(self, elem):
        '''Full optimization'''
        self._optimize_medium(elem)
        
        if elem.text:
            elem.text = self._compress_text(elem.text)
        
        for key in list(elem.attrib.keys()):
            elem.attrib[key] = self._compress_text(elem.attrib[key])
    
    def _compress_text(self, text):
        '''Compress text'''
        if not text:
            return text
        
        text = re.sub(r'\s+', ' ', text).strip()
        
        abbreviations = {
            'description': 'desc',
            'information': 'info',
            'application': 'app',
            'development': 'dev',
            'management': 'mgmt',
        }
        
        for word, abbr in abbreviations.items():
            text = re.sub(r'\b' + word + r'\b', abbr, text, flags=re.IGNORECASE)
        
        return text
    
    def _save_mapping(self, mapping_file):
        '''Save mapping'''
        mapping = {
            'tags': {v: k for k, v in self.tag_mapping.items()},
            'attributes': {v: k for k, v in self.attr_mapping.items()}
        }
        with open(mapping_file, 'w', encoding='utf-8') as f:
            json.dump(mapping, f, indent=2)


def parse_and_optimize_xml(input_file: str):
    '''
    Parse and optimize XML with lxml
    Complexity: Simple
    Total Elements: 22
    '''
    base_name = os.path.splitext(input_file)[0]
    
    print("=" * 60)
    print("ADVANCED XML OPTIMIZER - lxml")
    print("=" * 60)
    print(f"Input: {input_file}")
    print("=" * 60)
    
    optimizer = LxmlOptimizer()
    
    for level in ['light', 'medium', 'heavy']:
        print(f"\n{'-'*60}")
        print(f"[OPT] Processing {level.upper()} optimization...")
        print(f"{'-'*60}")
        
        start_time = time.time()
        
        try:
            output_file = optimizer.optimize(input_file, base_name, level)
            elapsed = time.time() - start_time
            
            original_size = os.path.getsize(input_file)
            optimized_size = os.path.getsize(output_file)
            reduction = ((original_size - optimized_size) / original_size) * 100
            
            print(f"[OK] Completed in {elapsed:.4f} seconds")
            print(f"[SIZE] Original: {original_size:,} bytes ({original_size/1024:.2f} KB)")
            print(f"[SIZE] Optimized: {optimized_size:,} bytes ({optimized_size/1024:.2f} KB)")
            print(f"[STATS] Reduction: {reduction:.2f}%")
            print(f"[SUCCESS] Saved to: {output_file}")
            
        except Exception as e:
            print(f"[ERROR] Failed: {e}")
    
    print(f"\n{'='*60}")
    print("[SUCCESS] All optimizations completed!")
    print(f"{'='*60}")


if __name__ == "__main__":
    input_file = "D:/projects/projects new/A Hybrid Machine Learning Model for Efficient XML Parsing/xml_optimizer/media/xml_files/sample_test_3G8ZdHk.xml"
    parse_and_optimize_xml(input_file)
