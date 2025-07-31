#!/usr/bin/env python3
"""
Script testing untuk memvalidasi Workflow Engine Masjid AI
"""

import json
import sys
import os
from datetime import datetime

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from workflow_engine import WorkflowEngine

def load_workflow_config():
    """Load workflow configuration"""
    with open('masjid_workflow.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def test_workflow_scenarios():
    """Test berbagai skenario workflow"""
    
    print("🕌 Testing Masjid AI Workflow Engine")
    print("="*50)
    
    # Load config dan initialize engine
    config = load_workflow_config()
    engine = WorkflowEngine(config)
    
    # Test scenarios
    test_cases = [
        {
            "name": "Jadwal Shalat",
            "message": "jadwal shalat hari ini",
            "expected_intent": "jadwal_shalat"
        },
        {
            "name": "Info Kajian",
            "message": "ada kajian apa minggu ini?",
            "expected_intent": "kajian_info"
        },
        {
            "name": "Donasi",
            "message": "mau donasi ke masjid",
            "expected_intent": "donasi"
        },
        {
            "name": "Acara Masjid",
            "message": "ada acara apa bulan ini?",
            "expected_intent": "acara_masjid"
        },
        {
            "name": "Info Umum",
            "message": "alamat masjid dimana?",
            "expected_intent": "informasi_umum"
        },
        {
            "name": "Daftar Nikah",
            "message": "syarat nikah apa saja?",
            "expected_intent": "daftar_nikah"
        },
        {
            "name": "Fallback",
            "message": "halo apa kabar?",
            "expected_intent": "informasi_umum"  # fallback to default
        }
    ]
    
    success_count = 0
    total_tests = len(test_cases)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📝 Test {i}: {test_case['name']}")
        print(f"Input: '{test_case['message']}'")
        
        # Prepare input data
        input_data = {
            "phone_number": "+62812345678",
            "message_text": test_case['message'],
            "timestamp": str(int(datetime.now().timestamp())),
            "message_type": "text",
            "message_id": f"test_{i}_{int(datetime.now().timestamp())}",
            "contact_name": "Test User"
        }
        
        try:
            # Execute workflow
            result = engine.execute_workflow(input_data)
            
            if result['success']:
                context = result['context']
                detected_intent = context.get('intent')
                response = context.get('formatted_response', 'No response')
                processing_time = result.get('processing_time', 0)
                
                print(f"✅ Success")
                print(f"   Intent: {detected_intent}")
                print(f"   Processing Time: {processing_time:.3f}s")
                print(f"   Response Preview: {response[:100]}...")
                
                # Check if intent matches expectation
                if detected_intent == test_case['expected_intent']:
                    print(f"   ✅ Intent match: Expected {test_case['expected_intent']}")
                    success_count += 1
                else:
                    print(f"   ⚠️  Intent mismatch: Expected {test_case['expected_intent']}, got {detected_intent}")
                    
            else:
                print(f"❌ Failed: {result.get('error')}")
                
        except Exception as e:
            print(f"❌ Exception: {str(e)}")
    
    # Summary
    print(f"\n{'='*50}")
    print(f"📊 Test Summary:")
    print(f"   Total Tests: {total_tests}")
    print(f"   Successful: {success_count}")
    print(f"   Failed: {total_tests - success_count}")
    print(f"   Success Rate: {(success_count/total_tests)*100:.1f}%")
    
    # Engine statistics
    stats = engine.get_statistics()
    print(f"\n📈 Engine Statistics:")
    print(f"   Total Executions: {stats['total_executions']}")
    print(f"   Successful Executions: {stats['successful_executions']}")
    print(f"   Failed Executions: {stats['failed_executions']}")
    print(f"   Average Processing Time: {stats['average_processing_time']:.3f}s")
    print(f"   Intent Distribution: {stats['intent_distribution']}")
    
    return success_count == total_tests

def test_workflow_config_validation():
    """Test validasi konfigurasi workflow"""
    
    print(f"\n🔍 Testing Workflow Configuration Validation")
    print("-" * 40)
    
    try:
        config = load_workflow_config()
        workflow = config['workflow']
        
        # Check required sections
        required_sections = ['name', 'version', 'trigger', 'nodes', 'environment']
        for section in required_sections:
            if section in workflow:
                print(f"✅ {section}: Found")
            else:
                print(f"❌ {section}: Missing")
                return False
        
        # Check nodes
        nodes = workflow['nodes']
        print(f"✅ Total Nodes: {len(nodes)}")
        
        # Check node connections
        all_node_names = set(nodes.keys())
        referenced_nodes = set()
        
        for node_name, node_config in nodes.items():
            next_nodes = node_config.get('next_nodes', [])
            if isinstance(next_nodes, dict):
                # For intent classifier with conditional routing
                for intent, target_nodes in next_nodes.items():
                    if isinstance(target_nodes, list):
                        referenced_nodes.update(target_nodes)
                    else:
                        referenced_nodes.add(target_nodes)
            elif isinstance(next_nodes, list):
                referenced_nodes.update(next_nodes)
        
        # Remove empty references
        referenced_nodes.discard('')
        
        # Check for dangling references
        dangling = referenced_nodes - all_node_names
        if dangling:
            print(f"⚠️  Dangling node references: {dangling}")
        else:
            print(f"✅ All node references are valid")
        
        return True
        
    except Exception as e:
        print(f"❌ Configuration validation failed: {str(e)}")
        return False

def main():
    """Main testing function"""
    
    print("🚀 Starting Masjid AI Workflow Tests")
    print("="*60)
    
    # Test 1: Configuration validation
    config_valid = test_workflow_config_validation()
    
    if not config_valid:
        print("\n❌ Configuration validation failed. Aborting tests.")
        return False
    
    # Test 2: Workflow scenarios
    workflow_tests_passed = test_workflow_scenarios()
    
    # Final result
    print(f"\n{'='*60}")
    if config_valid and workflow_tests_passed:
        print("🎉 All tests passed! Workflow engine is ready to use.")
        return True
    else:
        print("❌ Some tests failed. Please check the issues above.")
        return False

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)