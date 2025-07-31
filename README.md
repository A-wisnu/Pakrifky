# 🚀 Masjid AI Advanced Workflow - Rich Features

**Sistem AI Cerdas untuk Masjid Modern dengan 20+ Layanan Lengkap**

## 🌟 Overview

Workflow n8n advanced dengan **10 node cerdas**, **20+ layanan**, **AI chat**, dan **analytics lengkap**. Sistem praktis untuk masjid yang ingin memberikan layanan digital terbaik kepada jamaah.

## 📁 Files

- **`n8n_masjid_workflow_advanced.json`** - Advanced workflow (10 nodes, 1500+ lines)
- **`README.md`** - Dokumentasi lengkap

## 🎯 Key Features

### 🧠 **Smart Classification** 
20+ intent categories dengan scoring cerdas:
- **Core Religious:** Jadwal shalat, Kiblat, Doa, Ayat Quran, Hadits
- **Educational:** Kajian, TPQ/Tahfidz, Bahasa Arab, Konsultasi Syariah
- **Community:** Donasi, Program Sosial, Layanan Jenazah, Ambulans
- **Health:** Klinik Kesehatan, Ruqyah/Thibbun Nabawi
- **Modern:** Cuaca Jakarta, Live Streaming, AI Chat
- **Administrative:** Info Masjid, Sewa Gedung, Daftar Nikah

### 🤖 **AI Chat Engine**
- **OpenRouter Integration** dengan model `moonshotai/kimi-k2:free`
- **Islamic Knowledge Base** terintegrasi
- **Context-Aware Responses** dengan informasi masjid
- **Fallback System** untuk high availability

### 📊 **Rich Service Templates**
Setiap layanan memiliki response template yang sangat detail:

#### 🕌 **Jadwal Shalat Dynamic**
```
🕌 JADWAL SHALAT HARI INI
📅 Kamis, 30 Januari 2025
📍 Masjid Al-Ikhlas

🌅 Subuh: 04:30 WIB ⏰
☀️ Dzuhur: 12:15 WIB ✅
...
⏰ Shalat Selanjutnya: Ashar
⏳ Countdown: 2h 15m
```

#### 🤲 **Konsultasi Syariah Comprehensive**
- **3 Ustadz Spesialis** dengan jadwal lengkap
- **6 Kategori Konsultasi** (Pernikahan, Ekonomi, Parenting, dll)
- **4 Metode Konsultasi** (Tatap muka, Phone, Video, Email)
- **Contact Details** langsung

#### 💰 **Donasi & Zakat Complete**
- **Multiple Payment Methods** (3 Bank + 4 E-wallet + QRIS)
- **4 Kategori Donasi** dengan target tracking
- **Zakat Calculator** built-in
- **Transparent Reporting** system

### 🌐 **Multi-Provider WhatsApp Support**
- ✅ **WhatsApp Business API** (Meta Official)
- ✅ **Fonnte API**
- ✅ **Woowa API**  
- ✅ **Generic Format** (Custom APIs)

### 📈 **Advanced Analytics**
- **Real-time Tracking** via Supabase
- **Intent Distribution** analysis
- **Response Time** monitoring
- **User Engagement** metrics
- **AI Performance** tracking

## 🏗️ Workflow Architecture

### **10 Smart Nodes:**
```
📱 WhatsApp Gateway
    ↓
🧠 Smart Classifier (20+ intents)
    ↓
🤖 Need AI? ←→ 🕌 Prayer Service?
    ↓              ↓
🤖 AI Engine   🕌 Prayer Gen  🎯 Service Handler
    ↓              ↓              ↓
📤 WhatsApp Sender ←←←←←←←←←←←←←←←
    ↓
📊 Analytics Logger
    ↓
✅ Success Response
```

### **Flow Logic:**
1. **Message Reception** via multi-provider webhook
2. **Smart Classification** dengan 20+ intent categories
3. **Intelligent Routing** ke AI Engine, Prayer Service, atau Service Handler
4. **Response Generation** dengan template atau AI
5. **Message Sending** via WhatsApp
6. **Analytics Logging** ke Supabase
7. **Success Response** JSON format

## 🎨 Rich Services Available

### 🕌 **Spiritual Services**
1. **Jadwal Shalat** - Dynamic dengan countdown
2. **Arah Kiblat** - 294° dengan panduan lengkap
3. **Doa Harian** - Pagi, sore, dzikir, istighfar
4. **Ayat Quran** - Ayat Kursi, Al-Ikhlas, Mu'awwidzatain
5. **Hadits Nabi** - Akhlak, ilmu, sedekah

### 📚 **Educational Services**
6. **Kajian Pengajian** - 5 kajian rutin mingguan
7. **TPQ Tahfidz** - Anak & dewasa dengan target jelas
8. **Bahasa Arab** - Nahwu, sharaf, conversation
9. **Konsultasi Syariah** - 3 ustadz berpengalaman

### 🤝 **Community Services**
10. **Donasi Zakat** - Multi payment dengan calculator
11. **Program Sosial** - Yatim, lansia, beasiswa, kesehatan
12. **Layanan Jenazah** - 24/7 dengan tim lengkap
13. **Ambulans Emergency** - 2 unit siaga

### 🏥 **Health Services**
14. **Klinik Kesehatan** - 3 dokter spesialis
15. **Ruqyah Thibbun** - Pengobatan Islam

### ℹ️ **Information Services**
16. **Info Masjid** - Alamat, fasilitas, visi misi
17. **Cuaca Jakarta** - Real-time dengan tips jamaah
18. **Live Streaming** - YouTube, Facebook, Instagram
19. **AI Chat** - Conversational Islamic AI
20. **Salam Greeting** - Welcome dengan menu lengkap

## 🚀 Quick Setup

### **1. Import ke n8n**
```bash
1. Copy isi file n8n_masjid_workflow_advanced.json
2. Buka n8n → New Workflow
3. Import from JSON → Paste
4. Save workflow
```

### **2. Konfigurasi Required**
```javascript
// Update di node "WhatsApp Sender":
Authorization: "YOUR_WHATSAPP_API_KEY"

// API Keys sudah embedded di workflow:
OpenRouter: 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
Supabase: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### **3. Setup Supabase Table**
```sql
CREATE TABLE chat_analytics (
  id SERIAL PRIMARY KEY,
  user_phone TEXT,
  intent TEXT,
  confidence FLOAT,
  response_type TEXT,
  message_type TEXT,
  processing_time INTEGER,
  timestamp TIMESTAMPTZ,
  day_name TEXT,
  is_friday BOOLEAN,
  is_prayer_time BOOLEAN,
  ai_model TEXT,
  ai_tokens INTEGER,
  created_at TIMESTAMPTZ DEFAULT NOW()
);
```

### **4. Activate & Test**
```bash
1. Activate workflow di n8n
2. Test dengan webhook URL
3. Kirim pesan "assalamualaikum"
4. Cek response & analytics
```

## 💬 Example Conversations

### **Prayer Time Request**
```
User: "jadwal shalat"

Bot: 🕌 JADWAL SHALAT HARI INI
📅 Kamis, 30 Januari 2025
📍 Masjid Al-Ikhlas

🌅 Subuh: 04:30 WIB ✅
🌄 Terbit: 05:45 WIB
☀️ Dzuhur: 12:15 WIB ⏰
🌤️ Ashar: 15:30 WIB ⏰
🌅 Magrib: 18:45 WIB ⏰
🌙 Isya: 20:00 WIB ⏰

⏰ Shalat Selanjutnya: Dzuhur
🕐 Waktu: 12:15 WIB
⏳ Countdown: 2h 15m

🕋 Info Kiblat: 294° dari Utara
📱 Reminder: Ketik "reminder on" untuk notifikasi
📍 Lokasi Masjid: Jl. Raya Masjid No. 123, Jakarta Selatan 12345

🤲 "Aqiimu ash-shalata li dhikrii"
"Dirikanlah shalat untuk mengingat-Ku" (QS. Thaha: 14)

💡 Menu Cepat:
• Ketik "kiblat" untuk arah kiblat
• Ketik "doa" untuk dzikir setelah shalat
• Ketik "kajian" untuk jadwal pengajian
• Ketik "ustadz" untuk konsultasi
```

### **AI Islamic Chat**
```
User: "Bagaimana cara mendekatkan diri kepada Allah?"

Bot: 🤲 Assalamualaikum! Pertanyaan yang sangat mulia, berikut beberapa cara mendekatkan diri kepada Allah SWT:

📿 DZIKIR & DOA
• Perbanyak istighfar dan tasbih
• Berdoa dengan khusyuk
• Baca Al-Quran setiap hari

🕌 IBADAH SUNNAH
• Shalat tahajud dan dhuha
• Puasa sunnah (Senin-Kamis)
• Umrah dan haji jika mampu

🤝 BERBUAT BAIK
• Sedekah dan membantu sesama
• Berbakti kepada orang tua
• Silaturahmi dengan saudara

📚 MENUNTUT ILMU
• Hadiri kajian dan pengajian
• Baca buku-buku Islam
• Berguru kepada ulama

💡 Saran Lainnya:
• Ketik "jadwal shalat" untuk waktu shalat
• Ketik "tanya ustadz" untuk konsultasi
• Ketik "doa" untuk dzikir harian
• Ketik "info masjid" untuk informasi lengkap
```

## 🎯 Advanced Features

### **Smart Context Awareness**
- **Time-based Priority** (Prayer time detection)
- **Day-based Scoring** (Friday = higher kajian priority)
- **Dynamic Prayer Calculation** dengan countdown
- **Weather Integration** untuk tips jamaah

### **Rich Content Templates**
- **Arabic Text** dengan transliterasi dan terjemahan
- **Structured Information** dengan emoji dan formatting
- **Interactive Suggestions** di setiap response
- **Contact Details** langsung tersedia

### **Multi-Modal Support**
- **Text Messages** - Full processing
- **Media Messages** - Type detection
- **Location Messages** - GPS coordinate support
- **Webhook Compatibility** dengan multiple providers

## 📊 Analytics & Monitoring

### **Real-time Metrics**
- **Message Volume** per hour/day
- **Intent Distribution** analytics
- **Response Time** monitoring
- **AI Performance** tracking
- **User Engagement** patterns

### **Supabase Dashboard**
```sql
-- Popular Intents
SELECT intent, COUNT(*) as count 
FROM chat_analytics 
GROUP BY intent 
ORDER BY count DESC;

-- Response Time Analytics
SELECT AVG(processing_time) as avg_ms,
       MIN(processing_time) as min_ms,
       MAX(processing_time) as max_ms
FROM chat_analytics;

-- Daily Activity
SELECT DATE(created_at) as date,
       COUNT(*) as messages
FROM chat_analytics 
GROUP BY DATE(created_at)
ORDER BY date DESC;
```

## 🔧 Customization Guide

### **Add New Intent**
```javascript
// In Smart Classifier node, add to intents object:
new_service: {
  keywords: ['keyword1', 'keyword2', 'keyword3'],
  score: 8
}
```

### **Add New Service Template**
```javascript
// In Service Handler node, add to serviceTemplates:
new_service: () => `🎯 *NEW SERVICE*
Your rich content here with:
• Bullet points
• Detailed information
• Contact details
• Interactive suggestions`
```

### **Update Masjid Information**
```javascript
// In Smart Classifier node, update MASJID object:
const MASJID = {
  info: {
    nama: 'Your Masjid Name',
    alamat: 'Your Address',
    // ... other details
  }
}
```

## 🎊 Ready to Deploy!

**Advanced workflow dengan 20+ layanan siap pakai!**

### **Quick Start:**
1. ✅ **Import** `n8n_masjid_workflow_advanced.json`
2. ✅ **Update** WhatsApp API key  
3. ✅ **Setup** Supabase table
4. ✅ **Activate** workflow
5. ✅ **Test** dengan "assalamualaikum"

**Masjid Anda sekarang memiliki AI Assistant dengan 20+ layanan lengkap! 🤖🕌**

---

**🔬 Tech Stack**: n8n • OpenRouter AI • Supabase • Advanced Classification • Rich Templates

**🎯 Advanced Edition** - Practical, feature-rich, and user-friendly.