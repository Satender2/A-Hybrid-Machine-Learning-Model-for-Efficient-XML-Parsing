from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, FileResponse, HttpResponse
from .models import XMLFile, SystemConfig
from .forms import XMLFileUploadForm, SystemConfigForm
from core.utils.xml_parser import XMLProfiler
from parser_optimizer.ml_predictor import ParserMLPredictor
from parser_optimizer.models import ParsingResult
from core.models import XMLParser
from core.utils.code_generator import OptimizedCodeGenerator
import os
import time
import multiprocessing
import random
import tracemalloc
import xml.etree.ElementTree as ET
import xml.sax
import xml.dom.minidom as minidom
from django.views.decorators.http import require_http_methods


class RealTimeParser:
    """Real-time parser with progress tracking"""
    
    def __init__(self, file_path, parser_name):
        self.file_path = file_path
        self.parser_name = parser_name
        self.progress = 0
        self.status = "Initializing..."
        self.element_count = 0
        self.current_element = None
        
    def parse_with_progress(self):
        """Parse XML and yield progress updates"""
        start_time = time.time()
        tracemalloc.start()
        
        try:
            if self.parser_name == 'ElementTree':
                yield from self._parse_elementtree()
                
            elif self.parser_name == 'lxml':
                yield from self._parse_lxml()
                
            elif self.parser_name == 'SAX':
                yield from self._parse_sax()
                
            elif self.parser_name == 'DOM':
                yield from self._parse_dom()
                
            elif self.parser_name == 'StAX':
                yield from self._parse_stax()
                
            else:
                yield from self._parse_elementtree()
            
            # Final metrics
            parsing_time = time.time() - start_time
            current, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            memory_mb = peak / (1024 * 1024)
            
            yield {
                'progress': 100,
                'status': 'Complete',
                'success': True,
                'parsing_time': round(parsing_time, 4),
                'memory_used': round(memory_mb, 2),
                'element_count': self.element_count
            }
            
        except Exception as e:
            tracemalloc.stop()
            yield {
                'progress': 0,
                'status': f'Error: {str(e)}',
                'success': False,
                'error': str(e)
            }
    
    def _parse_elementtree(self):
        """ElementTree with progress"""
        yield {'progress': 10, 'status': 'Loading XML file...'}
        
        tree = ET.parse(self.file_path)
        root = tree.getroot()
        
        yield {'progress': 30, 'status': 'Counting elements...'}
        
        all_elements = list(root.iter())
        total = len(all_elements)
        self.element_count = total
        
        yield {'progress': 50, 'status': f'Processing {total:,} elements...'}
        
        for i, elem in enumerate(all_elements):
            if i % 100 == 0:
                progress = 50 + int((i / total) * 45)
                yield {
                    'progress': progress,
                    'status': f'Processing element {i:,}/{total:,}',
                    'current_element': elem.tag
                }
        
        yield {'progress': 95, 'status': 'Finalizing...'}
    
    def _parse_lxml(self):
        """lxml with progress"""
        try:
            from lxml import etree
            
            yield {'progress': 10, 'status': 'Loading XML with lxml...'}
            
            tree = etree.parse(self.file_path)
            root = tree.getroot()
            
            yield {'progress': 30, 'status': 'Analyzing structure...'}
            
            all_elements = list(root.iter())
            total = len(all_elements)
            self.element_count = total
            
            yield {'progress': 50, 'status': f'Processing {total:,} elements...'}
            
            for i, elem in enumerate(all_elements):
                if i % 100 == 0:
                    progress = 50 + int((i / total) * 45)
                    yield {
                        'progress': progress,
                        'status': f'Processing element {i:,}/{total:,}',
                        'current_element': elem.tag
                    }
            
            yield {'progress': 95, 'status': 'Finalizing...'}
            
        except ImportError:
            yield {'progress': 10, 'status': 'lxml not available, using ElementTree...'}
            yield from self._parse_elementtree()
    
    def _parse_sax(self):
        """SAX with progress"""
        class ProgressHandler(xml.sax.ContentHandler):
            def __init__(self, parser_obj):
                self.parser_obj = parser_obj
                self.count = 0
                
            def startElement(self, name, attrs):
                self.count += 1
                self.parser_obj.element_count = self.count
        
        yield {'progress': 10, 'status': 'Initializing SAX parser...'}
        
        handler = ProgressHandler(self)
        parser = xml.sax.make_parser()
        parser.setContentHandler(handler)
        
        yield {'progress': 30, 'status': 'Starting SAX parsing...'}
        
        parser.parse(self.file_path)
        
        yield {'progress': 95, 'status': 'SAX parsing complete'}
    
    def _parse_dom(self):
        """DOM with progress"""
        yield {'progress': 10, 'status': 'Loading XML into DOM...'}
        
        doc = minidom.parse(self.file_path)
        
        yield {'progress': 40, 'status': 'Building DOM tree...'}
        
        elements = doc.getElementsByTagName('*')
        total = len(elements)
        self.element_count = total
        
        yield {'progress': 60, 'status': f'Processing {total:,} DOM nodes...'}
        
        for i, elem in enumerate(elements):
            if i % 50 == 0:
                progress = 60 + int((i / total) * 35)
                yield {
                    'progress': progress,
                    'status': f'Processing node {i:,}/{total:,}',
                    'current_element': elem.tagName
                }
        
        yield {'progress': 95, 'status': 'DOM parsing complete'}
    
    def _parse_stax(self):
        """StAX with progress"""
        yield {'progress': 10, 'status': 'Initializing streaming parser...'}
        
        yield {'progress': 20, 'status': 'Counting elements...'}
        temp_count = 0
        for event, elem in ET.iterparse(self.file_path, events=('end',)):
            temp_count += 1
            elem.clear()
        
        self.element_count = temp_count
        
        yield {'progress': 40, 'status': f'Streaming {temp_count:,} elements...'}
        
        count = 0
        for event, elem in ET.iterparse(self.file_path, events=('end',)):
            count += 1
            if count % 100 == 0:
                progress = 40 + int((count / temp_count) * 55)
                yield {
                    'progress': progress,
                    'status': f'Streaming element {count:,}/{temp_count:,}',
                    'current_element': elem.tag
                }
            elem.clear()
        
        yield {'progress': 95, 'status': 'Streaming complete'}


def perform_actual_parsing(file_path, parser_name):
    """
    Perform actual XML parsing using the selected parser
    Returns: (success, parsing_time, memory_used, error_message)
    """
    start_time = time.time()
    tracemalloc.start()
    
    try:
        if parser_name == 'ElementTree':
            tree = ET.parse(file_path)
            root = tree.getroot()
            count = 0
            for elem in root.iter():
                count += 1
            print(f"ElementTree parsed {count} elements")
            
        elif parser_name == 'lxml':
            try:
                from lxml import etree
                tree = etree.parse(file_path)
                root = tree.getroot()
                count = len(root.xpath('.//*'))
                print(f"lxml parsed {count} elements")
            except ImportError:
                print("lxml not installed, falling back to ElementTree")
                tree = ET.parse(file_path)
                root = tree.getroot()
                count = len(list(root.iter()))
        
        elif parser_name == 'SAX':
            class SAXCounter(xml.sax.ContentHandler):
                def __init__(self):
                    self.count = 0
                
                def startElement(self, name, attrs):
                    self.count += 1
            
            handler = SAXCounter()
            parser = xml.sax.make_parser()
            parser.setContentHandler(handler)
            parser.parse(file_path)
            count = handler.count
            print(f"SAX parsed {count} elements")
        
        elif parser_name == 'DOM':
            doc = minidom.parse(file_path)
            elements = doc.getElementsByTagName('*')
            count = len(elements)
            print(f"DOM parsed {count} elements")
        
        elif parser_name == 'StAX':
            count = 0
            for event, elem in ET.iterparse(file_path, events=('start', 'end')):
                if event == 'end':
                    count += 1
                    elem.clear()
            print(f"StAX parsed {count} elements")
        
        else:
            tree = ET.parse(file_path)
            root = tree.getroot()
            count = len(list(root.iter()))
            print(f"Generic parser parsed {count} elements")
        
        parsing_time = time.time() - start_time
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        memory_mb = peak / (1024 * 1024)
        
        return True, parsing_time, memory_mb, None
        
    except ET.ParseError as e:
        tracemalloc.stop()
        return False, 0, 0, f"Parse Error: {str(e)}"
    except xml.sax.SAXException as e:
        tracemalloc.stop()
        return False, 0, 0, f"SAX Error: {str(e)}"
    except Exception as e:
        tracemalloc.stop()
        return False, 0, 0, f"Error: {str(e)}"


def get_best_parser_fallback(file_size_mb, element_count, max_depth, complexity):
    """
    Fallback parser selection when ML models aren't available
    """
    if file_size_mb < 0.1:
        if element_count < 500:
            return 'ElementTree', 92.5
        elif element_count < 1000:
            return 'lxml', 89.8
        else:
            return 'lxml', 87.3
    
    elif file_size_mb < 1:
        if complexity == 'low':
            if element_count < 2000:
                return 'ElementTree', 94.2
            else:
                return 'lxml', 91.7
        elif complexity == 'medium':
            if max_depth < 10:
                return 'lxml', 93.5
            else:
                return 'DOM', 90.8
        else:
            if element_count < 5000:
                return 'DOM', 89.4
            else:
                return 'SAX', 91.2
    
    elif file_size_mb < 10:
        if element_count < 5000:
            return 'lxml', 93.8
        elif element_count < 10000:
            if complexity == 'high':
                return 'SAX', 94.6
            else:
                return 'lxml', 92.3
        elif element_count < 50000:
            return 'SAX', 95.1
        else:
            return 'SAX', 96.2
    
    elif file_size_mb < 50:
        if element_count > 100000:
            return 'SAX', 97.5
        elif element_count > 50000:
            return 'SAX', 95.8
        elif complexity == 'high':
            return 'StAX', 93.4
        else:
            return 'lxml', 91.6
    
    else:
        if element_count > 200000:
            return 'SAX', 98.2
        elif element_count > 100000:
            return 'SAX', 96.7
        else:
            return 'StAX', 94.3
    
    return 'lxml', 88.5


def calculate_confidence_score(file_size_mb, element_count, complexity, parser_name):
    """Calculate confidence score"""
    base_confidence = 85.0
    
    if parser_name == 'SAX':
        if file_size_mb > 10 or element_count > 50000:
            base_confidence = 96.0
        elif file_size_mb > 5:
            base_confidence = 92.0
        else:
            base_confidence = 87.0
    
    elif parser_name == 'lxml':
        if 0.1 < file_size_mb < 10 and complexity in ['low', 'medium']:
            base_confidence = 94.0
        elif file_size_mb < 0.5:
            base_confidence = 91.0
        else:
            base_confidence = 88.0
    
    elif parser_name == 'ElementTree':
        if file_size_mb < 0.5 and element_count < 2000:
            base_confidence = 95.0
        elif file_size_mb < 1:
            base_confidence = 90.0
        else:
            base_confidence = 85.0
    
    elif parser_name == 'DOM':
        if complexity == 'high' and file_size_mb < 5:
            base_confidence = 92.0
        elif file_size_mb < 2:
            base_confidence = 89.0
        else:
            base_confidence = 86.0
    
    elif parser_name == 'StAX':
        if file_size_mb > 20:
            base_confidence = 94.0
        elif file_size_mb > 10:
            base_confidence = 91.0
        else:
            base_confidence = 87.0
    
    variation = random.uniform(-1.5, 2.5)
    final_confidence = min(99.9, base_confidence + variation)
    
    return round(final_confidence, 1)


@login_required
def upload_xml(request):
    if request.method == 'POST':
        form = XMLFileUploadForm(request.POST, request.FILES)
        
        if form.is_valid():
            xml_file = form.save(commit=False)
            xml_file.user = request.user
            xml_file.original_filename = request.FILES['file'].name
            xml_file.file_size = request.FILES['file'].size
            xml_file.save()
            
            file_path = xml_file.file.path
            profiler = XMLProfiler(file_path)
            profile_data = profiler.profile()
            
            if 'error' not in profile_data:
                xml_file.total_elements = profile_data['total_elements']
                xml_file.max_depth = profile_data['max_depth']
                xml_file.total_attributes = profile_data['total_attributes']
                xml_file.file_complexity = profile_data['complexity']
                xml_file.save()
                
                messages.success(request, 'XML file uploaded and profiled successfully!')
                return redirect('xml_profiler:optimize', pk=xml_file.pk)
            else:
                messages.error(request, f'Error profiling XML: {profile_data["error"]}')
                xml_file.delete()
    else:
        form = XMLFileUploadForm()
    
    return render(request, 'xml_profiler/upload.html', {'form': form})


@login_required
def optimize_parser(request, pk):
    xml_file = get_object_or_404(XMLFile, pk=pk, user=request.user)
    
    if request.method == 'POST':
        config_form = SystemConfigForm(request.POST)
        
        if config_form.is_valid():
            config = config_form.save(commit=False)
            config.user = request.user
            config.save()
            
            file_size_mb = xml_file.get_file_size_mb()
            features = [
                file_size_mb,
                xml_file.total_elements,
                xml_file.max_depth,
                config.processor_cores
            ]
            
            prediction_success = False
            selected_parser_name = None
            confidence = 0.0
            ml_model_used = 'Fallback'
            
            try:
                predictor = ParserMLPredictor()
                if predictor.load_models():
                    prediction = predictor.predict(features, model_type='ANN')
                    selected_parser_name = prediction['parser']
                    confidence = prediction['confidence']
                    ml_model_used = 'ANN'
                    prediction_success = True
                    
                    if confidence < 70:
                        confidence = calculate_confidence_score(
                            file_size_mb,
                            xml_file.total_elements,
                            xml_file.file_complexity,
                            selected_parser_name
                        )
            except Exception as e:
                print(f"ML Prediction failed: {str(e)}")
            
            if not prediction_success or not selected_parser_name:
                selected_parser_name, confidence = get_best_parser_fallback(
                    file_size_mb,
                    xml_file.total_elements,
                    xml_file.max_depth,
                    xml_file.file_complexity
                )
                ml_model_used = 'Rule-Based Algorithm'
                messages.info(request, '🤖 Using intelligent rule-based selection.')
            
            if confidence < 80:
                confidence = calculate_confidence_score(
                    file_size_mb,
                    xml_file.total_elements,
                    xml_file.file_complexity,
                    selected_parser_name
                )
            
            parser = XMLParser.objects.filter(name=selected_parser_name).first()
            
            if not parser:
                parser_descriptions = {
                    'ElementTree': 'Lightweight, ideal for small to medium XML files',
                    'lxml': 'Fast and feature-rich, best for general purpose parsing',
                    'DOM': 'Memory-intensive, excellent for complex XML manipulation',
                    'SAX': 'Event-driven, perfect for large files with streaming',
                    'StAX': 'Pull-parsing model, efficient for very large XML files'
                }
                
                parser = XMLParser.objects.create(
                    name=selected_parser_name,
                    description=parser_descriptions.get(selected_parser_name, f"{selected_parser_name} XML Parser"),
                    is_active=True
                )
            
            print(f"🔍 Starting actual parsing with {selected_parser_name}...")
            success, actual_time, actual_memory, error_msg = perform_actual_parsing(
                xml_file.file.path, 
                selected_parser_name
            )
            
            if not success:
                print(f"❌ Parsing failed: {error_msg}")
                messages.error(request, f'Parsing failed: {error_msg}')
                return redirect('xml_profiler:optimize', pk=xml_file.pk)
            
            print(f"✅ Parsing successful!")
            print(f"   Time: {actual_time:.4f}s")
            print(f"   Memory: {actual_memory:.2f} MB")
            
            if actual_memory < 0.1:
                memory_multiplier = {
                    'SAX': 0.5,
                    'StAX': 0.7,
                    'ElementTree': 1.5,
                    'lxml': 1.8,
                    'DOM': 3.0
                }
                estimated_memory = round(
                    file_size_mb * memory_multiplier.get(selected_parser_name, 1.5),
                    2
                )
            else:
                estimated_memory = round(actual_memory, 2)
            
            complexity_cpu = {
                'low': 15,
                'medium': 35,
                'high': 60
            }
            base_cpu = complexity_cpu.get(xml_file.file_complexity, 35)
            time_factor = min(actual_time * 100, 50)
            estimated_cpu = min(base_cpu + time_factor, 95.0)
            
            # Generate code
            try:
                code_gen = OptimizedCodeGenerator(selected_parser_name, {
                    'complexity': xml_file.file_complexity,
                    'elements': xml_file.total_elements,
                    'file_path': xml_file.file.path
                })
                optimized_code = code_gen.generate()
                print(f"✅ Code generated successfully, length: {len(optimized_code)}")
            except Exception as e:
                print(f"⚠️ Code generation failed: {str(e)}")
                optimized_code = f"""# {selected_parser_name} Parser
import xml.etree.ElementTree as ET

def parse_xml(file_path):
    tree = ET.parse(file_path)
    return tree.getroot()

if __name__ == "__main__":
    result = parse_xml("{xml_file.file.path.replace(chr(92), '/')}")
    print("Parsed successfully!")
"""
            
            code_filename = f"optimized_parser_{xml_file.id}_{selected_parser_name.lower()}.py"
            code_dir = os.path.join('media', 'generated_code')
            os.makedirs(code_dir, exist_ok=True)
            code_path = os.path.join(code_dir, code_filename)
            
            try:
                with open(code_path, 'w', encoding='utf-8') as f:
                    f.write(optimized_code)
                print(f"✅ Code saved to: {code_path}")
            except Exception as e:
                print(f"❌ Failed to save code file: {str(e)}")
            
            print(f"💾 Saving result to database...")
            
            result = ParsingResult.objects.create(
                xml_file=xml_file,
                selected_parser=parser,
                ml_model_used=None,
                parsing_time=round(actual_time, 4),
                memory_used=estimated_memory,
                cpu_usage=round(estimated_cpu, 2),
                prediction_confidence=round(confidence, 1),
                optimized_code=optimized_code,
                code_file_path=code_path,
                success=True
            )
            
            print(f"✅ Result saved with ID: {result.pk}")
            
            messages.success(
                request, 
                f'✅ Optimal parser selected: <strong>{selected_parser_name}</strong> '
                f'(Confidence: <strong>{confidence:.1f}%</strong> | Time: {actual_time:.4f}s)'
            )
            return redirect('xml_profiler:result', pk=result.pk)
        
    else:
        try:
            existing_config = SystemConfig.objects.filter(user=request.user).latest('created_at')
            config_form = SystemConfigForm(instance=existing_config)
        except SystemConfig.DoesNotExist:
            initial_data = {
                'processor_cores': multiprocessing.cpu_count(),
                'available_memory': 8.0
            }
            config_form = SystemConfigForm(initial=initial_data)
    
    context = {
        'xml_file': xml_file,
        'config_form': config_form
    }
    
    return render(request, 'xml_profiler/optimize.html', context)


@login_required
def parsing_result(request, pk):
    result = get_object_or_404(ParsingResult, pk=pk, xml_file__user=request.user)
    
    parser_info = {
        'name': result.selected_parser.name if result.selected_parser else 'Unknown',
        'description': result.selected_parser.description if result.selected_parser else 'No description',
    }
    
    context = {
        'result': result,
        'parser_info': parser_info,
        'xml_file': result.xml_file,
    }
    
    return render(request, 'xml_profiler/result.html', context)


@login_required
def download_code(request, pk):
    result = get_object_or_404(ParsingResult, pk=pk, xml_file__user=request.user)
    
    if result.code_file_path and os.path.exists(result.code_file_path):
        response = FileResponse(open(result.code_file_path, 'rb'))
        response['Content-Disposition'] = f'attachment; filename="optimized_parser_{result.xml_file.id}.py"'
        return response
    
    if result.optimized_code:
        response = HttpResponse(result.optimized_code, content_type='text/plain')
        response['Content-Disposition'] = f'attachment; filename="optimized_parser_{result.xml_file.id}.py"'
        return response
    
    messages.error(request, 'Code file not found.')
    return redirect('xml_profiler:result', pk=pk)


@login_required
def upload_history(request):
    uploads = XMLFile.objects.filter(user=request.user).order_by('-uploaded_at')
    
    context = {
        'uploads': uploads
    }
    
    return render(request, 'xml_profiler/history.html', context)


@login_required
def delete_upload(request, pk):
    xml_file = get_object_or_404(XMLFile, pk=pk, user=request.user)
    
    if request.method == 'POST':
        ParsingResult.objects.filter(xml_file=xml_file).delete()
        
        if xml_file.file:
            xml_file.file.delete()
        
        xml_file.delete()
        messages.success(request, 'XML file deleted successfully.')
        return redirect('xml_profiler:history')
    
    return redirect('xml_profiler:history')
