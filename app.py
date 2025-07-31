from flask import Flask, request, jsonify
import json
import logging
import os
from datetime import datetime
import hashlib
import hmac
from workflow_engine import WorkflowEngine

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/masjid_webhook.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Load workflow configuration
with open('masjid_workflow.json', 'r', encoding='utf-8') as f:
    workflow_config = json.load(f)

# Initialize workflow engine
workflow_engine = WorkflowEngine(workflow_config)

# Environment configuration
ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')
WEBHOOK_SECRET = os.getenv('WEBHOOK_SECRET', 'your-webhook-secret')
WHATSAPP_VERIFY_TOKEN = os.getenv('WHATSAPP_VERIFY_TOKEN', 'your-verify-token')

def verify_webhook_signature(payload, signature):
    """Verifikasi signature webhook untuk keamanan"""
    if not signature:
        return False
    
    expected_signature = hmac.new(
        WEBHOOK_SECRET.encode('utf-8'),
        payload,
        hashlib.sha256
    ).hexdigest()
    
    return hmac.compare_digest(f"sha256={expected_signature}", signature)

@app.route('/webhook/whatsapp', methods=['GET', 'POST'])
def whatsapp_webhook():
    """Endpoint utama untuk menerima webhook dari WhatsApp"""
    
    if request.method == 'GET':
        # Webhook verification untuk setup awal
        verify_token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')
        
        if verify_token == WHATSAPP_VERIFY_TOKEN:
            logger.info("Webhook verification successful")
            return challenge
        else:
            logger.warning("Webhook verification failed")
            return "Verification failed", 403
    
    elif request.method == 'POST':
        # Proses pesan masuk
        try:
            # Verifikasi signature (opsional, tergantung provider)
            signature = request.headers.get('X-Hub-Signature-256')
            if workflow_config['workflow']['security']['webhook_verification']:
                if not verify_webhook_signature(request.data, signature):
                    logger.warning("Invalid webhook signature")
                    return "Invalid signature", 403
            
            # Parse payload
            payload = request.get_json()
            logger.info(f"Received webhook payload: {json.dumps(payload, indent=2)}")
            
            # Extract message data berdasarkan format WhatsApp Business API
            if 'entry' in payload and payload['entry']:
                for entry in payload['entry']:
                    if 'changes' in entry:
                        for change in entry['changes']:
                            if change.get('field') == 'messages':
                                value = change.get('value', {})
                                messages = value.get('messages', [])
                                
                                for message in messages:
                                    # Process each message
                                    process_message(message, value.get('contacts', []))
            
            return jsonify({"status": "success"}), 200
            
        except Exception as e:
            logger.error(f"Error processing webhook: {str(e)}")
            return jsonify({"error": "Internal server error"}), 500

def process_message(message, contacts):
    """Memproses pesan individual melalui workflow engine"""
    try:
        # Extract contact info
        contact_info = {}
        if contacts:
            contact_info = contacts[0]  # Ambil kontak pertama
        
        # Prepare input data untuk workflow
        input_data = {
            "phone_number": message.get('from'),
            "message_text": extract_message_text(message),
            "timestamp": message.get('timestamp'),
            "message_type": message.get('type'),
            "message_id": message.get('id'),
            "contact_name": contact_info.get('profile', {}).get('name', ''),
            "contact_wa_id": contact_info.get('wa_id', '')
        }
        
        logger.info(f"Processing message from {input_data['phone_number']}: {input_data['message_text']}")
        
        # Jalankan workflow
        result = workflow_engine.execute_workflow(input_data)
        
        if result['success']:
            logger.info(f"Workflow executed successfully for {input_data['phone_number']}")
        else:
            logger.error(f"Workflow execution failed: {result.get('error')}")
            
    except Exception as e:
        logger.error(f"Error processing message: {str(e)}")

def extract_message_text(message):
    """Extract text dari berbagai tipe pesan WhatsApp"""
    message_type = message.get('type')
    
    if message_type == 'text':
        return message.get('text', {}).get('body', '')
    elif message_type == 'button':
        return message.get('button', {}).get('text', '')
    elif message_type == 'interactive':
        interactive = message.get('interactive', {})
        if interactive.get('type') == 'button_reply':
            return interactive.get('button_reply', {}).get('title', '')
        elif interactive.get('type') == 'list_reply':
            return interactive.get('list_reply', {}).get('title', '')
    
    return f"[{message_type} message]"

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "environment": ENVIRONMENT,
        "workflow_version": workflow_config['workflow']['version']
    })

@app.route('/workflow/status', methods=['GET'])
def workflow_status():
    """Status workflow engine"""
    stats = workflow_engine.get_statistics()
    return jsonify({
        "workflow_name": workflow_config['workflow']['name'],
        "total_nodes": len(workflow_config['workflow']['nodes']),
        "statistics": stats
    })

@app.route('/webhook/test', methods=['POST'])
def test_webhook():
    """Endpoint untuk testing workflow dengan data dummy"""
    test_data = {
        "phone_number": "+62812345678",
        "message_text": request.json.get('message', 'jadwal shalat'),
        "timestamp": str(int(datetime.now().timestamp())),
        "message_type": "text",
        "message_id": "test_" + str(int(datetime.now().timestamp())),
        "contact_name": "Test User",
        "contact_wa_id": "62812345678"
    }
    
    logger.info(f"Test workflow with data: {test_data}")
    result = workflow_engine.execute_workflow(test_data)
    
    return jsonify(result)

if __name__ == '__main__':
    # Pastikan direktori logs ada
    os.makedirs('logs', exist_ok=True)
    
    # Run aplikasi
    port = int(os.getenv('PORT', 5000))
    debug = ENVIRONMENT == 'development'
    
    logger.info(f"Starting Masjid AI Workflow App on port {port}")
    logger.info(f"Environment: {ENVIRONMENT}")
    logger.info(f"Workflow: {workflow_config['workflow']['name']} v{workflow_config['workflow']['version']}")
    
    app.run(host='0.0.0.0', port=port, debug=debug)