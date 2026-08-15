# Optimized SAX Parser with XML Output
import xml.sax
from xml.sax.saxutils import XMLGenerator
import time
import os

class OptimizingXMLHandler(xml.sax.ContentHandler):
    '''
    SAX Handler for streaming XML parsing and optimization
    Complexity: Simple
    Expected Elements: 22
    '''
    
    def __init__(self, output_file):
        self.element_count = 0
        self.output_file = output_file
        self.generator = XMLGenerator(output_file, encoding='utf-8')
        
    def startDocument(self):
        print("[INIT] Starting SAX parsing...")
        self.start_time = time.time()
        self.generator.startDocument()
        
    def endDocument(self):
        self.generator.endDocument()
        elapsed = time.time() - self.start_time
        print(f"[OK] SAX parsing completed in {elapsed:.4f} seconds")
        print(f"[OK] Total elements processed: {self.element_count:,}")
        
    def startElement(self, tag, attributes):
        self.element_count += 1
        self.generator.startElement(tag, attributes)
        
    def endElement(self, tag):
        self.generator.endElement(tag)
            
    def characters(self, content):
        stripped = content.strip()
        if stripped:
            self.generator.characters(stripped)

def parse_and_optimize_xml(input_file: str, output_file: str = None):
    '''SAX-based XML parser and optimizer'''
    
    if output_file is None:
        base_name = os.path.splitext(input_file)[0]
        output_file = f"{base_name}_optimized.xml"
    
    try:
        print(f"[SAVE] Creating optimized XML: {output_file}")
        
        with open(output_file, 'w', encoding='utf-8') as out_file:
            handler = OptimizingXMLHandler(out_file)
            parser = xml.sax.make_parser()
            parser.setContentHandler(handler)
            
            print(f"[LOAD] Parsing: {input_file}")
            parser.parse(input_file)
        
        original_size = os.path.getsize(input_file) / 1024
        optimized_size = os.path.getsize(output_file) / 1024
        reduction = ((original_size - optimized_size) / original_size) * 100
        
        print(f"\n{'='*60}")
        print(f"[SUCCESS] OPTIMIZATION COMPLETE")
        print(f"{'='*60}")
        print(f"[SIZE] Original Size: {original_size:.2f} KB")
        print(f"[SIZE] Optimized Size: {optimized_size:.2f} KB")
        print(f"[STATS] Size Reduction: {reduction:.2f}%")
        print(f"{'='*60}")
        
        return True
        
    except xml.sax.SAXException as e:
        print(f"[ERROR] SAX Error: {e}")
        return False
    except Exception as e:
        print(f"[ERROR] Error: {e}")
        return False

if __name__ == "__main__":
    input_file = "E:/projects new/A Hybrid Machine Learning/xml_optimizer/media/xml_files/sample_test_tRZZ49a.xml"
    
    print("=" * 60)
    print("XML PARSER & OPTIMIZER - SAX")
    print("=" * 60)
    
    success = parse_and_optimize_xml(input_file)
    
    if success:
        print("\n[SUCCESS] XML optimized successfully!")
    else:
        print("\n[ERROR] Failed to optimize XML")
