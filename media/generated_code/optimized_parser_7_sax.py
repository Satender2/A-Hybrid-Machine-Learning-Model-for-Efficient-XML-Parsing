# Advanced SAX Parser with Multi-Level XML Optimization
import xml.sax
from xml.sax.saxutils import XMLGenerator
import time
import os
import re
import json


class AdvancedOptimizingHandler(xml.sax.ContentHandler):
    '''
    Advanced SAX Handler with multiple optimization levels
    Complexity: Simple
    Expected Elements: 22
    '''
    
    def __init__(self, output_file, optimization_level='medium'):
        self.element_count = 0
        self.output_file = output_file
        self.generator = XMLGenerator(output_file, encoding='utf-8')
        self.optimization_level = optimization_level
        self.tag_mapping = {}
        self.attr_mapping = {}
        self.tag_counter = 0
        self.attr_counter = 0
        
    def startDocument(self):
        print(f"[INIT] Starting {self.optimization_level.upper()} optimization...")
        self.start_time = time.time()
        self.generator.startDocument()
        
    def endDocument(self):
        self.generator.endDocument()
        elapsed = time.time() - self.start_time
        print(f"[OK] Parsing completed in {elapsed:.4f} seconds")
        print(f"[OK] Elements processed: {self.element_count:,}")
        
        # Save mapping if needed
        if self.optimization_level in ['medium', 'heavy']:
            self._save_mapping()
        
    def startElement(self, tag, attributes):
        self.element_count += 1
        
        # Optimize tag name
        optimized_tag = tag
        if self.optimization_level in ['medium', 'heavy']:
            if tag not in self.tag_mapping:
                short_tag = f"t{self.tag_counter}"
                self.tag_mapping[tag] = short_tag
                self.tag_counter += 1
            optimized_tag = self.tag_mapping[tag]
        
        # Optimize attributes
        optimized_attrs = {}
        for key, value in attributes.items():
            optimized_key = key
            optimized_value = value
            
            if self.optimization_level in ['medium', 'heavy']:
                if key not in self.attr_mapping:
                    short_attr = f"a{self.attr_counter}"
                    self.attr_mapping[key] = short_attr
                    self.attr_counter += 1
                optimized_key = self.attr_mapping[key]
            
            if self.optimization_level == 'heavy':
                optimized_value = self._compress_text(value)
            
            optimized_attrs[optimized_key] = optimized_value
        
        self.generator.startElement(optimized_tag, optimized_attrs)
        
    def endElement(self, tag):
        # Use optimized tag name
        optimized_tag = tag
        if self.optimization_level in ['medium', 'heavy']:
            if tag in self.tag_mapping:
                optimized_tag = self.tag_mapping[tag]
        
        self.generator.endElement(optimized_tag)
            
    def characters(self, content):
        # Optimize content
        stripped = content.strip()
        if stripped:
            if self.optimization_level == 'heavy':
                # Advanced text compression
                stripped = self._compress_text(stripped)
            self.generator.characters(stripped)
    
    def _compress_text(self, text):
        '''Compress text for heavy optimization'''
        # Remove extra spaces
        text = re.sub(r'\s+', ' ', text).strip()
        
        # Abbreviate common words
        abbreviations = {
            'description': 'desc',
            'information': 'info',
            'application': 'app',
            'applications': 'apps',
            'development': 'dev',
            'developer': 'dev',
            'management': 'mgmt',
            'corporation': 'corp',
            'international': 'intl',
            'department': 'dept',
            'government': 'govt',
            'university': 'univ',
            'entertainment': 'ent',
            'technology': 'tech',
            'professional': 'prof',
            'architecture': 'arch',
            'infrastructure': 'infra',
        }
        
        for word, abbr in abbreviations.items():
            text = re.sub(r'\b' + word + r'\b', abbr, text, flags=re.IGNORECASE)
        
        return text
    
    def _save_mapping(self):
        '''Save tag and attribute mapping for decoding'''
        base_name = self.output_file.name.replace('.xml', '')
        mapping_file = f"{base_name}_mapping.json"
        
        mapping = {
            'tags': {v: k for k, v in self.tag_mapping.items()},
            'attributes': {v: k for k, v in self.attr_mapping.items()},
            'info': {
                'optimization_level': self.optimization_level,
                'total_tags': len(self.tag_mapping),
                'total_attributes': len(self.attr_mapping)
            }
        }
        
        with open(mapping_file, 'w', encoding='utf-8') as f:
            json.dump(mapping, f, indent=2)
        
        print(f"[INFO] Mapping saved to: {mapping_file}")


def parse_and_optimize_xml(input_file: str, output_base: str = None, level: str = 'medium'):
    '''
    SAX-based XML parser with advanced optimization
    
    Optimization Levels:
    - light: Remove whitespace only (~10-20% reduction)
    - medium: Compress tags + whitespace (~30-40% reduction)  
    - heavy: Full compression (~50-70% reduction)
    '''
    
    if output_base is None:
        output_base = os.path.splitext(input_file)[0]
    
    output_file = f"{output_base}_optimized_{level}.xml"
    
    try:
        print(f"[START] Creating {level} optimized XML: {output_file}")
        
        with open(output_file, 'w', encoding='utf-8') as out_file:
            handler = AdvancedOptimizingHandler(out_file, optimization_level=level)
            parser = xml.sax.make_parser()
            parser.setContentHandler(handler)
            
            print(f"[LOAD] Parsing: {input_file}")
            parser.parse(input_file)
        
        # Statistics
        original_size = os.path.getsize(input_file)
        optimized_size = os.path.getsize(output_file)
        reduction = ((original_size - optimized_size) / original_size) * 100
        
        print(f"\n{'='*60}")
        print(f"[SUCCESS] OPTIMIZATION COMPLETE - {level.upper()}")
        print(f"{'='*60}")
        print(f"[SIZE] Original: {original_size:,} bytes ({original_size/1024:.2f} KB)")
        print(f"[SIZE] Optimized: {optimized_size:,} bytes ({optimized_size/1024:.2f} KB)")
        print(f"[SIZE] Saved: {original_size - optimized_size:,} bytes")
        print(f"[STATS] Reduction: {reduction:.2f}%")
        print(f"{'='*60}")
        
        return True
        
    except xml.sax.SAXException as e:
        print(f"[ERROR] SAX Error: {e}")
        return False
    except Exception as e:
        print(f"[ERROR] Error: {e}")
        return False


if __name__ == "__main__":
    input_file = "E:/projects new/A Hybrid Machine Learning/xml_optimizer/media/xml_files/sample_test_optimized_WLW4THX.xml"
    base_name = os.path.splitext(input_file)[0]
    
    print("=" * 60)
    print("ADVANCED XML PARSER & OPTIMIZER - SAX")
    print("=" * 60)
    print(f"Input: {input_file}")
    print("=" * 60)
    
    # Generate all optimization levels
    results = {}
    for level in ['light', 'medium', 'heavy']:
        print(f"\n{'-'*60}")
        print(f"Processing {level.upper()} optimization")
        print(f"{'-'*60}")
        success = parse_and_optimize_xml(input_file, base_name, level=level)
        results[level] = success
        if not success:
            print(f"[ERROR] Failed at {level} level")
    
    # Summary
    print(f"\n{'='*60}")
    print("OPTIMIZATION SUMMARY")
    print(f"{'='*60}")
    for level, success in results.items():
        status = "[SUCCESS]" if success else "[FAILED]"
        print(f"{status} {level.upper()} optimization")
    print(f"{'='*60}")
    
    print("\n[INFO] Files generated:")
    print(f"  - {base_name}_optimized_light.xml")
    print(f"  - {base_name}_optimized_medium.xml")
    print(f"  - {base_name}_optimized_medium_mapping.json")
    print(f"  - {base_name}_optimized_heavy.xml")
    print(f"  - {base_name}_optimized_heavy_mapping.json")
    print("\n[SUCCESS] All optimizations completed!")
