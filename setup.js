#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

console.log('🚀 Setting up Masjid AI for Replit...\n');

// Check if workflow file exists
const workflowFile = 'n8n_masjid_workflow_replit.json';
if (!fs.existsSync(workflowFile)) {
  console.error('❌ Workflow file not found:', workflowFile);
  process.exit(1);
}

console.log('✅ Workflow file found');

// Create n8n config directory
const configDir = path.join(process.env.HOME || '/home/runner', '.n8n');
if (!fs.existsSync(configDir)) {
  fs.mkdirSync(configDir, { recursive: true });
  console.log('✅ Created n8n config directory');
}

// Instructions for user
console.log('\n📋 SETUP INSTRUCTIONS:');
console.log('\n1️⃣ Run this Replit project');
console.log('2️⃣ Open the n8n interface (it will open automatically)');
console.log('3️⃣ Import the workflow:');
console.log('   • Click "+" → Import from JSON');
console.log('   • Copy content from n8n_masjid_workflow_replit.json');
console.log('   • Paste and click Import');
console.log('\n4️⃣ Configure WhatsApp API:');
console.log('   • Go to "WhatsApp Sender" node');
console.log('   • Update Authorization header with your API key');
console.log('\n5️⃣ Activate workflow and get webhook URL');
console.log('\n🎯 Your webhook URL will be:');
console.log(`   https://${process.env.REPL_SLUG || 'your-repl'}.${process.env.REPL_OWNER || 'username'}.repl.co/webhook/webhook-masjid`);

console.log('\n📱 WHATSAPP PROVIDERS SUPPORTED:');
console.log('   • Fonnte API');
console.log('   • Woowa API');
console.log('   • WhatsApp Business API');
console.log('   • Generic APIs');

console.log('\n🤖 AI & DATABASE:');
console.log('   ✅ OpenRouter API key: Included');
console.log('   ✅ Supabase integration: Ready');
console.log('   ✅ Multi-provider WhatsApp: Ready');

console.log('\n🎊 Ready to serve your masjid community!');
console.log('\n📚 Services Available:');
console.log('   🕌 14 Islamic services (Health services removed)');
console.log('   🤖 AI Chat with Islamic knowledge');
console.log('   📊 Analytics logging to Supabase');
console.log('   🌐 Multi-provider WhatsApp support');

// Create a simple README for Replit
const readmeContent = `# 🕌 Masjid AI Assistant - Replit Ready

This project runs n8n with a pre-configured Islamic AI assistant workflow.

## 🚀 Quick Start

1. The project will auto-start n8n
2. Import the workflow from \`n8n_masjid_workflow_replit.json\`
3. Update WhatsApp API key in "WhatsApp Sender" node
4. Activate workflow
5. Use webhook URL in your WhatsApp provider

## 📱 Webhook URL
\`\`\`
https://${process.env.REPL_SLUG || 'your-repl'}.${process.env.REPL_OWNER || 'username'}.repl.co/webhook/webhook-masjid
\`\`\`

## 🎯 Features
- 14 Islamic services (no health services)
- AI chat with OpenRouter
- Supabase analytics
- Multi-provider WhatsApp support

## 🔧 Configuration
All API keys are pre-configured in the workflow JSON file.
Only WhatsApp API key needs to be updated.
`;

fs.writeFileSync('README.md', readmeContent);
console.log('\n✅ Created README.md for Replit');

console.log('\n🔧 Setup completed! Run "npm start" to begin.');