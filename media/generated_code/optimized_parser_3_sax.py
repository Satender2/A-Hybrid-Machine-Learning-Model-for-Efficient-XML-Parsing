# Optimized SAX Parser
import xml.sax
import time

class XMLHandler(xml.sax.ContentHandler):
    '''
    SAX Event Handler for streaming XML parsing
    Complexity: Simple
    Expected Elements: 22
    Best for: Large files with memory constraints
    '''
    
    def __init__(self):
        self.element_count = 0
        self.current_element = None
        self.current_data = ""
        self.data_store = []
        
    def startDocument(self):
        print("Starting SAX parsing...")
        self.start_time = time.time()
        
    def endDocument(self):
        elapsed = time.time() - self.start_time
        print(f"SAX parsing completed in {elapsed:.4f} seconds")
        print(f"Total elements processed: {self.element_count:,}")
        
    def startElement(self, tag, attributes):
        self.element_count += 1
        self.current_element = tag
        self.current_data = ""
        
        # Process element start
        if attributes:
            attr_dict = dict(attributes.items())
            # Process attributes
            pass
        
    def endElement(self, tag):
        # Process complete element
        if self.current_data.strip():
            element_data = {
                'tag': tag,
                'content': self.current_data.strip()
            }
            self.data_store.append(element_data)
        
        self.current_element = None
        self.current_data = ""
            
    def characters(self, content):
        if self.current_element:
            self.current_data += content

def parse_xml(file_path: str) -> bool:
    '''SAX-based XML parser for large files'''
    try:
        handler = XMLHandler()
        parser = xml.sax.make_parser()
        parser.setContentHandler(handler)
        
        print(f"Parsing file: {file_path}")
        parser.parse(file_path)
        
        print(f"\nExtracted {len(handler.data_store)} data elements")
        return True
        
    except xml.sax.SAXException as e:
        print(f"SAX Error: {e}")
        return False
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    file_path = "E:\projects new\A Hybrid Machine Learning\xml_optimizer\media\xml_files\sample_test_A0RSkxM.xml"
    
    success = parse_xml(file_path)
    
    if success:
        print("\nSUCCESS: SAX parsing completed successfully!")
    else:
        print("\nERROR: Failed to parse XML")
