import sys
import os
import django

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'xml_optimizer.settings')
django.setup()

from core.models import XMLParser

def populate_parsers():
    parsers = [
        {
            'name': 'DOM',
            'description': 'Document Object Model parser - loads entire XML into memory as tree structure',
            'best_for': 'Small to medium XML files (< 10MB), Random access needed, Multiple traversals',
            'memory_efficient': False,
            'speed_efficient': False,
            'is_active': True
        },
        {
            'name': 'SAX',
            'description': 'Simple API for XML - event-driven streaming parser',
            'best_for': 'Large XML files, Sequential processing, Memory constraints',
            'memory_efficient': True,
            'speed_efficient': True,
            'is_active': True
        },
        {
            'name': 'StAX',
            'description': 'Streaming API for XML - pull parsing model',
            'best_for': 'Large files with selective parsing, Bidirectional navigation needed',
            'memory_efficient': True,
            'speed_efficient': True,
            'is_active': True
        },
        {
            'name': 'ElementTree',
            'description': 'Python built-in XML parser - lightweight and efficient',
            'best_for': 'General purpose parsing, Medium complexity documents, Python-native solution',
            'memory_efficient': True,
            'speed_efficient': True,
            'is_active': True
        },
        {
            'name': 'lxml',
            'description': 'High-performance XML parser based on libxml2 and libxslt',
            'best_for': 'Large files, Complex XPath queries, High performance requirements',
            'memory_efficient': True,
            'speed_efficient': True,
            'is_active': True
        }
    ]
    
    for parser_data in parsers:
        parser, created = XMLParser.objects.get_or_create(
            name=parser_data['name'],
            defaults=parser_data
        )
        if created:
            print(f"✓ Created parser: {parser.name}")
        else:
            print(f"- Parser already exists: {parser.name}")
    
    print(f"\nTotal parsers in database: {XMLParser.objects.count()}")

if __name__ == "__main__":
    print("Populating XML Parsers...")
    print("=" * 50)
    populate_parsers()
    print("=" * 50)
    print("Done!")
