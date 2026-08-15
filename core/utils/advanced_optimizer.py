"""
Advanced XML Optimization Module
Provides multiple optimization levels for XML files
"""

import xml.etree.ElementTree as ET
import re
import json
import os


class AdvancedXMLOptimizer:
    """
    Advanced XML optimization with multiple strategies
    """
    
    def __init__(self):
        self.tag_mapping = {}
        self.attr_mapping = {}
        self.value_mapping = {}
        self.tag_counter = 0
        self.attr_counter = 0
        self.value_counter = 0
    
    def optimize(self, input_file, output_file, optimization_level='medium'):
        """
        Optimize XML with different levels:
        - light: Remove whitespace only (~10-20% reduction)
        - medium: Remove whitespace + compress tags (~30-40% reduction)
        - heavy: Full optimization with data compression (~50-70% reduction)
        """
        tree = ET.parse(input_file)
        root = tree.getroot()
        
        print(f"[OPT] Starting {optimization_level.upper()} optimization...")
        
        if optimization_level == 'light':
            self._optimize_light(root)
        elif optimization_level == 'medium':
            self._optimize_medium(root)
        elif optimization_level == 'heavy':
            self._optimize_heavy(root)
        
        # Write optimized XML
        tree.write(output_file, encoding='utf-8', xml_declaration=True)
        
        # Create mapping file for decoding
        if optimization_level in ['medium', 'heavy']:
            mapping_file = output_file.replace('.xml', '_mapping.json')
            self._save_mapping(mapping_file)
            print(f"[INFO] Mapping saved to: {mapping_file}")
        
        return tree
    
    def _optimize_light(self, elem):
        """Remove only whitespace"""
        if elem.text:
            elem.text = elem.text.strip() if elem.text.strip() else None
        if elem.tail:
            elem.tail = elem.tail.strip() if elem.tail.strip() else None
        for child in elem:
            self._optimize_light(child)
    
    def _optimize_medium(self, elem):
        """Compress tag names and remove whitespace"""
        # Shorten tag names
        original_tag = elem.tag
        if original_tag not in self.tag_mapping:
            short_tag = f"t{self.tag_counter}"
            self.tag_mapping[original_tag] = short_tag
            self.tag_counter += 1
        elem.tag = self.tag_mapping[original_tag]
        
        # Shorten attribute names
        new_attrib = {}
        for key, value in elem.attrib.items():
            if key not in self.attr_mapping:
                short_attr = f"a{self.attr_counter}"
                self.attr_mapping[key] = short_attr
                self.attr_counter += 1
            new_attrib[self.attr_mapping[key]] = value
        elem.attrib = new_attrib
        
        # Remove whitespace
        if elem.text:
            elem.text = elem.text.strip() if elem.text.strip() else None
        if elem.tail:
            elem.tail = elem.tail.strip() if elem.tail.strip() else None
        
        for child in elem:
            self._optimize_medium(child)
    
    def _optimize_heavy(self, elem):
        """Full optimization with data compression"""
        self._optimize_medium(elem)
        
        # Compress text content
        if elem.text:
            elem.text = self._compress_text(elem.text)
        
        # Compress attribute values
        for key in elem.attrib:
            elem.attrib[key] = self._compress_text(elem.attrib[key])
    
    def _compress_text(self, text):
        """Advanced text compression"""
        if not text:
            return text
        
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
    
    def _save_mapping(self, mapping_file):
        """Save tag/attribute mapping for decoding"""
        mapping = {
            'tags': {v: k for k, v in self.tag_mapping.items()},
            'attributes': {v: k for k, v in self.attr_mapping.items()},
            'info': {
                'total_tags': len(self.tag_mapping),
                'total_attributes': len(self.attr_mapping)
            }
        }
        with open(mapping_file, 'w', encoding='utf-8') as f:
            json.dump(mapping, f, indent=2)
    
    def decode(self, input_file, mapping_file, output_file):
        """Decode optimized XML back to original using mapping"""
        # Load mapping
        with open(mapping_file, 'r', encoding='utf-8') as f:
            mapping = json.load(f)
        
        tree = ET.parse(input_file)
        root = tree.getroot()
        
        self._decode_element(root, mapping)
        
        # Write decoded XML
        self._indent(root)
        tree.write(output_file, encoding='utf-8', xml_declaration=True)
        
        print(f"[SUCCESS] Decoded XML saved to: {output_file}")
    
    def _decode_element(self, elem, mapping):
        """Recursively decode element"""
        # Decode tag name
        if elem.tag in mapping['tags']:
            elem.tag = mapping['tags'][elem.tag]
        
        # Decode attributes
        new_attrib = {}
        for key, value in elem.attrib.items():
            new_key = mapping['attributes'].get(key, key)
            new_attrib[new_key] = value
        elem.attrib = new_attrib
        
        # Decode children
        for child in elem:
            self._decode_element(child, mapping)
    
    def _indent(self, elem, level=0):
        """Add pretty printing indentation"""
        i = "\n" + level * "  "
        if len(elem):
            if not elem.text or not elem.text.strip():
                elem.text = i + "  "
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
            for child in elem:
                self._indent(child, level+1)
            if not child.tail or not child.tail.strip():
                child.tail = i
        else:
            if level and (not elem.tail or not elem.tail.strip()):
                elem.tail = i
