#!/usr/bin/env python3
"""
Script untuk menjalankan Masjid AI Workflow Server
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

def main():
    """Main function untuk menjalankan server"""
    
    # Import app setelah path setup
    from app import app, logger
    
    # Environment setup
    environment = os.getenv('ENVIRONMENT', 'development')
    port = int(os.getenv('PORT', 5000))
    debug = environment == 'development'
    
    # Pastikan direktori logs ada
    os.makedirs('logs', exist_ok=True)
    
    # Log startup information
    logger.info("="*50)
    logger.info("🕌 MASJID AI WORKFLOW SERVER")
    logger.info("="*50)
    logger.info(f"Environment: {environment}")
    logger.info(f"Port: {port}")
    logger.info(f"Debug Mode: {debug}")
    logger.info(f"WhatsApp Webhook: /webhook/whatsapp")
    logger.info(f"Test Endpoint: /webhook/test")
    logger.info(f"Health Check: /health")
    logger.info(f"Workflow Status: /workflow/status")
    logger.info("="*50)
    
    # Jalankan server
    try:
        app.run(
            host='0.0.0.0',
            port=port,
            debug=debug,
            threaded=True
        )
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.error(f"Server error: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main()