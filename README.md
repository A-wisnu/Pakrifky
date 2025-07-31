# 🕌 Masjid AI Assistant - Replit Ready

**Sistem AI Cerdas untuk Masjid Modern - Optimized untuk Replit Hosting**

## 🌟 Overview

Workflow n8n siap deploy di Replit dengan **8 smart nodes**, **14 layanan Islamic**, **AI chat**, dan **analytics**. Health services sudah dihapus untuk optimasi hosting.

## 📁 Files Replit Ready

- **`n8n_masjid_workflow_replit.json`** - Main workflow (8 nodes, optimized)
- **`package.json`** - Dependencies untuk Replit
- **`.replit`** - Konfigurasi Replit
- **`replit.nix`** - Environment setup
- **`setup.js`** - Auto setup script
- **`README.md`** - Dokumentasi

## 🎯 Features (Health Services Removed)

### 🕌 **Spiritual Services (5)**
1. **Jadwal Shalat** - Dynamic dengan countdown
2. **Arah Kiblat** - 294° dengan panduan
3. **Doa Harian** - Pagi, sore, dzikir
4. **Ayat Quran** - Ayat Kursi, Al-Ikhlas
5. **Hadits Nabi** - Akhlak, ilmu, sedekah

### 📚 **Educational Services (3)**
6. **Kajian Pengajian** - 5 kajian mingguan
7. **TPQ Tahfidz** - Anak & dewasa
8. **Konsultasi Syariah** - 3 ustadz

### 🤝 **Community Services (3)**
9. **Donasi Zakat** - Multi payment
10. **Program Sosial** - Yatim, lansia, beasiswa
11. **Layanan Jenazah** - 24/7 siaga

### ℹ️ **Information Services (3)**
12. **Info Masjid** - Alamat, fasilitas
13. **Live Streaming** - YouTube, Facebook
14. **AI Chat** - Islamic conversation

## 🚀 Quick Deploy ke Replit

### **1. Setup Replit Project**
```bash
1. Buat Replit baru (Node.js template)
2. Upload semua files ke Replit
3. Run setup: npm run setup
4. Start: npm start
```

### **2. Import Workflow ke n8n**
```bash
1. n8n akan terbuka otomatis di Replit
2. Klik "+" → Import from JSON
3. Copy isi n8n_masjid_workflow_replit.json
4. Paste dan Import
```

### **3. Update WhatsApp API Key**
```javascript
// Di node "WhatsApp Sender":
Authorization: "YOUR_WHATSAPP_API_KEY"

// API Keys lain sudah include:
OpenRouter: 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
Supabase: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### **4. Setup Supabase Table**
```sql
CREATE TABLE chat_logs (
  id SERIAL PRIMARY KEY,
  user_phone TEXT,
  intent TEXT,
  confidence FLOAT,
  response_type TEXT,
  processing_time INTEGER,
  timestamp TIMESTAMPTZ,
  day_name TEXT,
  ai_model TEXT,
  ai_tokens INTEGER,
  created_at TIMESTAMPTZ DEFAULT NOW()
);
```

### **5. Webhook URL**
```
https://your-repl.username.repl.co/webhook/webhook-masjid
```

## 🏗️ Workflow Architecture (8 Nodes)

```
📱 WhatsApp Gateway
    ↓
🧠 Smart Processor (14 intents, no health)
    ↓
🤖 Need AI?
    ↓        ↓
🤖 AI Engine    📋 Service Templates
    ↓               ↓
📤 WhatsApp Sender ←←
    ↓
📊 Supabase Logger
    ↓
✅ Success Response
```

## 💬 Example Usage

### **Prayer Time Request**
```
User: "jadwal shalat"

Bot: 🕌 JADWAL SHALAT HARI INI
📅 Kamis, 30 Januari 2025
📍 Masjid Al-Ikhlas

🌅 Subuh: 04:30 WIB
☀️ Dzuhur: 12:15 WIB
🌤️ Ashar: 15:30 WIB
🌅 Magrib: 18:45 WIB
🌙 Isya: 20:00 WIB

⏰ Shalat Selanjutnya: Dzuhur
🕐 Waktu: 12:15 WIB
⏳ Countdown: 2h 15m

🕋 Arah Kiblat: 294° dari Utara
📍 Lokasi: Jl. Raya Masjid No. 123

🤲 "Aqiimu ash-shalata li dhikrii"
"Dirikanlah shalat untuk mengingat-Ku" (QS. Thaha: 14)
```

### **AI Islamic Chat**
```
User: "Bagaimana cara mendekatkan diri kepada Allah?"

Bot: 🤲 Assalamualaikum! Berikut cara mendekatkan diri kepada Allah:

📿 DZIKIR & DOA
• Perbanyak istighfar
• Berdoa dengan khusyuk
• Baca Al-Quran setiap hari

🕌 IBADAH SUNNAH
• Shalat tahajud dan dhuha
• Puasa sunnah Senin-Kamis
• Umrah dan haji jika mampu

💡 Menu Lainnya:
• "jadwal shalat" - Waktu shalat
• "donasi" - Info rekening
• "kajian" - Jadwal pengajian
• "info" - Tentang masjid
```

## 🌐 Multi-Provider WhatsApp

### **Supported APIs:**
- ✅ **Fonnte API** 
- ✅ **Woowa API**
- ✅ **WhatsApp Business API** (Meta)
- ✅ **Generic Format** (Custom APIs)

### **Message Format Auto-Detection:**
```javascript
// Fonnte: { device, message, message_type }
// Woowa: { from, body, type }
// Meta: { entry[].changes[].value.messages[] }
// Generic: { phone, message, type }
```

## 📊 Analytics & Monitoring

### **Real-time Logging:**
- **User Interactions** per intent
- **Response Times** monitoring
- **AI Performance** tracking
- **Daily Activity** patterns

### **Supabase Dashboard:**
```sql
-- Top Services
SELECT intent, COUNT(*) as usage 
FROM chat_logs 
GROUP BY intent 
ORDER BY usage DESC;

-- Performance
SELECT AVG(processing_time) as avg_ms
FROM chat_logs 
WHERE DATE(created_at) = CURRENT_DATE;
```

## 🔧 Customization

### **Add New Service:**
```javascript
// Di node "Service Templates":
new_service: () => `🎯 *NEW SERVICE*
Your content here with:
• Bullet points
• Islamic guidance
• Contact info`
```

### **Update Masjid Info:**
```javascript
// Di node "Smart Processor":
const MASJID = {
  info: {
    nama: 'Your Masjid Name',
    alamat: 'Your Address',
    whatsapp: 'Your WhatsApp',
    // ... other details
  }
}
```

## 🎊 Ready for Replit!

### **Advantages:**
- ✅ **Optimized** untuk Replit hosting
- ✅ **Health Services Removed** - cleaner & focused
- ✅ **8 Nodes Only** - faster execution
- ✅ **14 Core Services** - essential for masjid
- ✅ **Auto Setup** - minimal configuration
- ✅ **All APIs Included** - just add WhatsApp key

### **Performance:**
- **Response Time:** < 1 second
- **Node Count:** 8 (streamlined)
- **Services:** 14 (focused on essentials)
- **Memory Usage:** Optimized for Replit
- **Hosting:** Free on Replit

## 📱 Quick Start Checklist

1. ✅ **Upload files** ke Replit
2. ✅ **Run setup**: `npm run setup`
3. ✅ **Start n8n**: `npm start`
4. ✅ **Import workflow** dari JSON file
5. ✅ **Update WhatsApp API** key
6. ✅ **Activate workflow**
7. ✅ **Setup webhook** di WhatsApp provider
8. ✅ **Test** dengan "assalamualaikum"

**Masjid Anda sekarang memiliki AI Assistant siap 24/7 di Replit! 🤖🕌**

---

**🔬 Tech Stack**: Replit • n8n • OpenRouter AI • Supabase • Multi-Provider WhatsApp

**🎯 Replit Edition** - Streamlined, optimized, and ready to deploy!