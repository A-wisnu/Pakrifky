import json
import logging
import re
import time
from datetime import datetime
from typing import Dict, List, Any, Optional
import requests
from dataclasses import dataclass
from enum import Enum
import sqlite3
import os

# Setup logging
logger = logging.getLogger(__name__)

class NodeType(Enum):
    PROCESSOR = "processor"
    AI_CLASSIFIER = "ai_classifier"
    DATA_PROCESSOR = "data_processor"
    DATABASE_QUERY = "database_query"
    PAYMENT_PROCESSOR = "payment_processor"
    CALENDAR_PROCESSOR = "calendar_processor"
    STATIC_RESPONDER = "static_responder"
    FORM_PROCESSOR = "form_processor"
    AI_RESPONDER = "ai_responder"
    FORMATTER = "formatter"
    API_SENDER = "api_sender"
    LOGGER = "logger"

@dataclass
class WorkflowContext:
    """Context data yang diteruskan antar node"""
    user_phone: str
    message_text: str
    timestamp: str
    message_type: str
    message_id: str
    contact_name: str
    intent: Optional[str] = None
    confidence: Optional[float] = None
    response_data: Any = None
    formatted_response: Optional[str] = None
    processing_time: float = 0.0
    error: Optional[str] = None

class WorkflowEngine:
    def __init__(self, config: Dict):
        self.config = config
        self.workflow_config = config['workflow']
        self.nodes = self.workflow_config['nodes']
        self.environment = self.workflow_config.get('environment', {})
        self.statistics = {
            'total_executions': 0,
            'successful_executions': 0,
            'failed_executions': 0,
            'average_processing_time': 0.0,
            'intent_distribution': {}
        }
        
        # Initialize database if needed
        self._init_database()
        
    def _init_database(self):
        """Initialize SQLite database untuk development"""
        env = os.getenv('ENVIRONMENT', 'development')
        if env == 'development':
            db_path = 'masjid_dev.db'
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Create tables
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS kajian_schedule (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    tanggal TEXT,
                    waktu TEXT,
                    ustadz TEXT,
                    tema TEXT,
                    lokasi TEXT,
                    active BOOLEAN DEFAULT 1
                )
            ''')
            
            # Insert sample data
            sample_kajian = [
                ('2024-01-15', '19:30', 'Ahmad Dahlan', 'Akhlak dalam Islam', 'Aula Masjid'),
                ('2024-01-22', '20:00', 'Muhammad Ridwan', 'Fiqh Muamalah', 'Aula Masjid'),
                ('2024-01-29', '19:30', 'Abdullah Syukur', 'Tafsir Al-Quran', 'Aula Masjid')
            ]
            
            cursor.executemany('''
                INSERT OR IGNORE INTO kajian_schedule (tanggal, waktu, ustadz, tema, lokasi)
                VALUES (?, ?, ?, ?, ?)
            ''', sample_kajian)
            
            conn.commit()
            conn.close()
    
    def execute_workflow(self, input_data: Dict) -> Dict:
        """Execute workflow utama"""
        start_time = time.time()
        
        try:
            # Create workflow context
            context = WorkflowContext(
                user_phone=input_data.get('phone_number', ''),
                message_text=input_data.get('message_text', ''),
                timestamp=input_data.get('timestamp', ''),
                message_type=input_data.get('message_type', ''),
                message_id=input_data.get('message_id', ''),
                contact_name=input_data.get('contact_name', '')
            )
            
            # Start dengan input processor
            current_node = 'input_processor'
            
            while current_node:
                logger.info(f"Executing node: {current_node}")
                
                # Execute current node
                result = self._execute_node(current_node, context)
                
                if not result['success']:
                    context.error = result.get('error')
                    break
                
                # Get next node
                next_nodes = result.get('next_nodes', [])
                if not next_nodes:
                    break
                    
                current_node = next_nodes[0] if isinstance(next_nodes, list) else next_nodes
            
            # Calculate processing time
            context.processing_time = time.time() - start_time
            
            # Update statistics
            self._update_statistics(context)
            
            # Log hasil
            self._log_execution(context)
            
            return {
                'success': context.error is None,
                'context': context.__dict__,
                'processing_time': context.processing_time,
                'error': context.error
            }
            
        except Exception as e:
            logger.error(f"Workflow execution error: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'processing_time': time.time() - start_time
            }
    
    def _execute_node(self, node_name: str, context: WorkflowContext) -> Dict:
        """Execute individual node"""
        try:
            node_config = self.nodes.get(node_name)
            if not node_config:
                return {'success': False, 'error': f"Node {node_name} not found"}
            
            node_type = NodeType(node_config['type'])
            
            # Route ke handler yang sesuai
            if node_type == NodeType.PROCESSOR:
                return self._execute_processor(node_config, context)
            elif node_type == NodeType.AI_CLASSIFIER:
                return self._execute_ai_classifier(node_config, context)
            elif node_type == NodeType.DATA_PROCESSOR:
                return self._execute_data_processor(node_config, context)
            elif node_type == NodeType.DATABASE_QUERY:
                return self._execute_database_query(node_config, context)
            elif node_type == NodeType.PAYMENT_PROCESSOR:
                return self._execute_payment_processor(node_config, context)
            elif node_type == NodeType.CALENDAR_PROCESSOR:
                return self._execute_calendar_processor(node_config, context)
            elif node_type == NodeType.STATIC_RESPONDER:
                return self._execute_static_responder(node_config, context)
            elif node_type == NodeType.FORM_PROCESSOR:
                return self._execute_form_processor(node_config, context)
            elif node_type == NodeType.AI_RESPONDER:
                return self._execute_ai_responder(node_config, context)
            elif node_type == NodeType.FORMATTER:
                return self._execute_formatter(node_config, context)
            elif node_type == NodeType.API_SENDER:
                return self._execute_api_sender(node_config, context)
            elif node_type == NodeType.LOGGER:
                return self._execute_logger(node_config, context)
            else:
                return {'success': False, 'error': f"Unknown node type: {node_type}"}
                
        except Exception as e:
            logger.error(f"Node execution error in {node_name}: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def _execute_processor(self, node_config: Dict, context: WorkflowContext) -> Dict:
        """Execute processor node (input validation)"""
        config = node_config['config']
        
        # Validation
        required_fields = config.get('validation', {}).get('required', [])
        for field in required_fields:
            if field == 'phone_number' and not context.user_phone:
                return {'success': False, 'error': 'Phone number required'}
            if field == 'message_text' and not context.message_text:
                return {'success': False, 'error': 'Message text required'}
        
        # Phone format validation
        phone_format = config.get('validation', {}).get('phone_format')
        if phone_format and context.user_phone:
            if not re.match(phone_format, context.user_phone):
                return {'success': False, 'error': 'Invalid phone format'}
        
        return {'success': True, 'next_nodes': node_config['next_nodes']}
    
    def _execute_ai_classifier(self, node_config: Dict, context: WorkflowContext) -> Dict:
        """Execute AI classifier untuk intent detection"""
        config = node_config['config']
        intents = config['intents']
        
        message_lower = context.message_text.lower()
        best_intent = None
        best_score = 0.0
        
        # Simple keyword dan pattern matching
        for intent_name, intent_config in intents.items():
            score = 0.0
            
            # Check keywords
            keywords = intent_config.get('keywords', [])
            for keyword in keywords:
                if keyword.lower() in message_lower:
                    score += 1.0
            
            # Check patterns
            patterns = intent_config.get('patterns', [])
            for pattern in patterns:
                if re.search(pattern, message_lower):
                    score += 1.5
            
            # Normalize score
            total_checks = len(keywords) + len(patterns)
            if total_checks > 0:
                score = score / total_checks
            
            if score > best_score:
                best_score = score
                best_intent = intent_name
        
        # Check confidence threshold
        threshold = config.get('confidence_threshold', 0.7)
        if best_score < threshold:
            best_intent = config.get('default_intent', 'informasi_umum')
        
        context.intent = best_intent
        context.confidence = best_score
        
        # Get next node based on intent
        next_nodes_map = node_config['next_nodes']
        next_node = next_nodes_map.get(best_intent, next_nodes_map.get('default', []))
        
        return {'success': True, 'next_nodes': next_node}
    
    def _execute_data_processor(self, node_config: Dict, context: WorkflowContext) -> Dict:
        """Execute data processor (contoh: prayer times)"""
        config = node_config['config']
        
        # Mock prayer times data (dalam implementasi nyata, panggil API)
        prayer_times = {
            'fajr': '04:30',
            'dhuhr': '12:15',
            'asr': '15:30',
            'maghrib': '18:45',
            'isha': '20:00'
        }
        
        # Format response
        template = config['response_template']
        response = template.format(**prayer_times)
        
        context.response_data = prayer_times
        context.formatted_response = response
        
        return {'success': True, 'next_nodes': node_config['next_nodes']}
    
    def _execute_database_query(self, node_config: Dict, context: WorkflowContext) -> Dict:
        """Execute database query untuk kajian schedule"""
        config = node_config['config']
        
        try:
            # Connect ke database
            env = os.getenv('ENVIRONMENT', 'development')
            if env == 'development':
                conn = sqlite3.connect('masjid_dev.db')
                cursor = conn.cursor()
                
                # Query kajian
                cursor.execute('''
                    SELECT tanggal, waktu, ustadz, tema, lokasi 
                    FROM kajian_schedule 
                    WHERE active = 1 
                    ORDER BY tanggal
                ''')
                
                results = cursor.fetchall()
                conn.close()
                
                # Format data
                kajian_list = []
                for row in results:
                    kajian_list.append({
                        'tanggal': row[0],
                        'waktu': row[1],
                        'ustadz': row[2],
                        'tema': row[3],
                        'lokasi': row[4]
                    })
                
                # Generate response
                template = config['response_template']
                if kajian_list:
                    response_text = "📚 *Jadwal Kajian Masjid*\n\n"
                    for kajian in kajian_list:
                        response_text += f"📅 {kajian['tanggal']}\n"
                        response_text += f"🕐 {kajian['waktu']}\n"
                        response_text += f"👨‍🏫 Ustadz {kajian['ustadz']}\n"
                        response_text += f"📖 Tema: {kajian['tema']}\n"
                        response_text += f"📍 {kajian['lokasi']}\n\n"
                    response_text += "Barakallahu fiikum! 🤲"
                else:
                    response_text = "Belum ada jadwal kajian yang tersedia saat ini. Silakan hubungi takmir masjid untuk informasi lebih lanjut."
                
                context.response_data = kajian_list
                context.formatted_response = response_text
                
                return {'success': True, 'next_nodes': node_config['next_nodes']}
            
        except Exception as e:
            logger.error(f"Database query error: {str(e)}")
            return {'success': False, 'error': f"Database error: {str(e)}"}
    
    def _execute_payment_processor(self, node_config: Dict, context: WorkflowContext) -> Dict:
        """Execute payment processor untuk donasi"""
        config = node_config['config']
        
        # Format bank accounts info
        template = config['response_template']
        bank_accounts = config['bank_accounts']
        qris_code = config.get('qris_code', 'QRIS_PLACEHOLDER')
        admin_phone = os.getenv('ADMIN_PHONE', '+62-812-3456-7890')
        
        response_text = "💰 *Donasi & Infaq Masjid*\n\n🏦 *Transfer Bank:*\n"
        for bank in bank_accounts:
            response_text += f"🏧 {bank['bank']}: {bank['account_number']}\n"
            response_text += f"a.n {bank['account_name']}\n\n"
        
        response_text += f"📱 *QRIS:*\n{qris_code}\n\n"
        response_text += f"Jazakallahu khairan atas kebaikan Anda! 🤲\n\n"
        response_text += f"Konfirmasi donasi ke: {admin_phone}"
        
        context.response_data = {'bank_accounts': bank_accounts, 'qris': qris_code}
        context.formatted_response = response_text
        
        return {'success': True, 'next_nodes': node_config['next_nodes']}
    
    def _execute_calendar_processor(self, node_config: Dict, context: WorkflowContext) -> Dict:
        """Execute calendar processor untuk events"""
        config = node_config['config']
        
        # Mock event data
        events = [
            {
                'nama_acara': 'Kajian Mingguan',
                'tanggal': '2024-01-15',
                'waktu': '19:30 WIB',
                'tempat': 'Aula Masjid',
                'peserta': 'Umum',
                'biaya': 'Gratis'
            },
            {
                'nama_acara': 'Bakti Sosial',
                'tanggal': '2024-01-20',
                'waktu': '08:00 WIB',
                'tempat': 'Lapangan Masjid',
                'peserta': 'Jamaah',
                'biaya': 'Gratis'
            }
        ]
        
        response_text = "📅 *Agenda Kegiatan Masjid*\n\n"
        for event in events:
            response_text += f"📋 {event['nama_acara']}\n"
            response_text += f"📅 {event['tanggal']}\n"
            response_text += f"🕐 {event['waktu']}\n"
            response_text += f"📍 {event['tempat']}\n"
            response_text += f"👥 {event['peserta']}\n"
            response_text += f"💵 {event['biaya']}\n\n"
        
        response_text += "Daftarkan diri Anda! 📝"
        
        context.response_data = events
        context.formatted_response = response_text
        
        return {'success': True, 'next_nodes': node_config['next_nodes']}
    
    def _execute_static_responder(self, node_config: Dict, context: WorkflowContext) -> Dict:
        """Execute static responder untuk info umum"""
        config = node_config['config']
        masjid_info = config['masjid_info']
        
        response_text = f"🕌 *Masjid {masjid_info['nama']}*\n\n"
        response_text += f"📍 Alamat: {masjid_info['alamat']}\n"
        response_text += f"☎️ Telepon: {masjid_info['telefon']}\n"
        response_text += f"📧 Email: {masjid_info['email']}\n"
        response_text += f"🕐 Jam Buka: {masjid_info['jam_buka']}\n\n"
        response_text += "🏢 *Fasilitas:*\n"
        
        for fasilitas in masjid_info['fasilitas']:
            response_text += f"✅ {fasilitas}\n"
        
        response_text += f"\n👨‍💼 Takmir: {masjid_info['takmir']}\n"
        response_text += f"📱 Kontak: {masjid_info['kontak_takmir']}\n\n"
        response_text += "Selamat datang di masjid kami! 🤲"
        
        context.response_data = masjid_info
        context.formatted_response = response_text
        
        return {'success': True, 'next_nodes': node_config['next_nodes']}
    
    def _execute_form_processor(self, node_config: Dict, context: WorkflowContext) -> Dict:
        """Execute form processor untuk pendaftaran nikah"""
        config = node_config['config']
        
        response_text = "💒 *Pendaftaran Nikah - Masjid Al-Ikhlas*\n\n"
        response_text += "📋 *Dokumen yang diperlukan:*\n"
        
        for doc in config['required_documents']:
            response_text += f"📄 {doc}\n"
        
        response_text += "\n📝 *Tahapan Proses:*\n"
        for i, step in enumerate(config['process_steps'], 1):
            response_text += f"{i}. {step}\n"
        
        response_text += f"\n👨‍🏫 Narahubung: {config['contact_person']}\n\n"
        response_text += "Semoga Allah mudahkan urusan Anda! 🤲"
        
        context.response_data = {
            'documents': config['required_documents'],
            'steps': config['process_steps']
        }
        context.formatted_response = response_text
        
        return {'success': True, 'next_nodes': node_config['next_nodes']}
    
    def _execute_ai_responder(self, node_config: Dict, context: WorkflowContext) -> Dict:
        """Execute AI responder untuk fallback"""
        config = node_config['config']
        
        # Untuk demo, gunakan fallback response
        fallback_responses = config.get('fallback_responses', [])
        if fallback_responses:
            response = fallback_responses[0]
        else:
            response = "Maaf, saya belum bisa memahami pertanyaan Anda. Silakan coba lagi atau hubungi admin."
        
        context.formatted_response = response
        
        return {'success': True, 'next_nodes': node_config['next_nodes']}
    
    def _execute_formatter(self, node_config: Dict, context: WorkflowContext) -> Dict:
        """Execute formatter untuk format final response"""
        config = node_config['config']
        
        response = context.formatted_response or "No response generated"
        
        # Add signature if configured
        if config.get('add_signature', False):
            signature = config.get('signature_text', '')
            response += signature
        
        # Check max length
        max_length = config.get('max_length', 4000)
        if len(response) > max_length:
            response = response[:max_length-3] + "..."
        
        context.formatted_response = response
        
        return {'success': True, 'next_nodes': node_config['next_nodes']}
    
    def _execute_api_sender(self, node_config: Dict, context: WorkflowContext) -> Dict:
        """Execute API sender untuk kirim ke WhatsApp"""
        config = node_config['config']
        
        # Dalam demo mode, hanya log response
        env = os.getenv('ENVIRONMENT', 'development')
        if env == 'development':
            logger.info(f"[DEMO] Would send WhatsApp message to {context.user_phone}:")
            logger.info(f"[DEMO] Message: {context.formatted_response}")
            return {'success': True, 'next_nodes': node_config['next_nodes']}
        
        # Untuk production, kirim actual API call
        try:
            api_url = config['api_endpoint']
            headers = config['headers']
            payload = {
                'phone': context.user_phone,
                'message': context.formatted_response,
                'type': 'text'
            }
            
            # Replace placeholders
            for key, value in headers.items():
                if isinstance(value, str) and '{{' in value:
                    headers[key] = value.replace('{{WHATSAPP_TOKEN}}', os.getenv('WHATSAPP_TOKEN', ''))
            
            response = requests.post(api_url, json=payload, headers=headers, timeout=30)
            
            if response.status_code == 200:
                return {'success': True, 'next_nodes': node_config['next_nodes']}
            else:
                return {'success': False, 'error': f"API call failed: {response.status_code}"}
                
        except Exception as e:
            return {'success': False, 'error': f"API sender error: {str(e)}"}
    
    def _execute_logger(self, node_config: Dict, context: WorkflowContext) -> Dict:
        """Execute logger untuk mencatat aktivitas"""
        config = node_config['config']
        
        log_data = {
            'timestamp': datetime.now().isoformat(),
            'user_phone': context.user_phone,
            'intent': context.intent,
            'response_status': 'success' if not context.error else 'error',
            'processing_time': context.processing_time
        }
        
        # Log to file
        log_file = config.get('log_file', 'logs/masjid_workflow.log')
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(f"{json.dumps(log_data, ensure_ascii=False)}\n")
        
        return {'success': True, 'next_nodes': []}
    
    def _update_statistics(self, context: WorkflowContext):
        """Update execution statistics"""
        self.statistics['total_executions'] += 1
        
        if context.error:
            self.statistics['failed_executions'] += 1
        else:
            self.statistics['successful_executions'] += 1
        
        # Update average processing time
        total_time = (self.statistics['average_processing_time'] * 
                     (self.statistics['total_executions'] - 1) + context.processing_time)
        self.statistics['average_processing_time'] = total_time / self.statistics['total_executions']
        
        # Update intent distribution
        if context.intent:
            if context.intent not in self.statistics['intent_distribution']:
                self.statistics['intent_distribution'][context.intent] = 0
            self.statistics['intent_distribution'][context.intent] += 1
    
    def _log_execution(self, context: WorkflowContext):
        """Log workflow execution"""
        status = "SUCCESS" if not context.error else "ERROR"
        logger.info(f"Workflow {status} - Phone: {context.user_phone}, "
                   f"Intent: {context.intent}, Time: {context.processing_time:.2f}s")
        
        if context.error:
            logger.error(f"Workflow error: {context.error}")
    
    def get_statistics(self) -> Dict:
        """Get workflow statistics"""
        return self.statistics.copy()