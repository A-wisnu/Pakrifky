# 🚀 Setup Guide - Masjid AI Ultimate

## 📁 File JSON Workflow

**File utama:** `masjid_ai_ultimate.json`

## ⚡ Quick Setup (5 Menit)

### 1. Import ke n8n Cloud
```
1. Login ke https://cloud.n8n.io
2. Create New Workflow
3. Klik icon ⚙️ → Import from JSON
4. Copy seluruh isi masjid_ai_ultimate.json
5. Paste & Import
6. Save workflow
```

### 2. Update WhatsApp API Key
```
Node: 📤 Ultimate Sender
Update: Authorization header
Value: YOUR_WHATSAPP_API_KEY

Contoh:
- Fonnte: "YOUR_FONNTE_TOKEN"
- Woowa: "Bearer YOUR_WOOWA_TOKEN"
```

### 3. Setup Database (Optional)
```sql
CREATE TABLE ultimate_analytics (
  id SERIAL PRIMARY KEY,
  user_phone TEXT,
  intent TEXT,
  confidence FLOAT,
  response_type TEXT,
  ai_model TEXT,
  ai_tokens INTEGER,
  processing_time INTEGER,
  timestamp TIMESTAMPTZ,
  day_name TEXT,
  is_friday BOOLEAN,
  success BOOLEAN,
  created_at TIMESTAMPTZ DEFAULT NOW()
);
```

### 4. Activate & Test
```
1. Activate workflow di n8n
2. Copy webhook URL
3. Test dengan: "assalamualaikum"
4. Verify response
```

## 🧪 Test Commands

### Quick Tests:
```
"assalamualaikum" → Menu lengkap
"jadwal shalat" → Prayer schedule  
"kiblat" → Qiblat direction
"donasi" → Payment methods
"tanya ustadz" → Consultation
"info masjid" → Mosque details
```

### AI Tests:
```
"bagaimana cara wudhu?" → Step guide
"apa itu tauhid?" → Islamic education
"saya sedang sedih" → Counseling
```

## 🎯 Features Ready

### ✅ 15+ Services:
- Jadwal shalat dengan countdown
- Arah kiblat 294° 
- Doa & dzikir harian
- Ayat Quran & hadits
- Kajian & pengajian
- TPQ & tahfidz
- Konsultasi syariah
- Donasi & zakat
- Info masjid lengkap
- AI Islamic chat

### ✅ Multi-Provider WhatsApp:
- Meta WhatsApp Business
- Fonnte API
- Woowa API  
- Generic format

### ✅ AI Powered:
- OpenRouter integration
- Islamic knowledge base
- Context-aware responses
- Fallback mechanisms

### ✅ Analytics:
- Supabase logging
- Performance tracking
- Intent analysis
- Usage metrics

## 🔧 Webhook URL Format

```
https://your-n8n-instance.cloud.n8n.io/webhook/webhook-masjid-ultimate
```

## 📞 Support

**File issues:** 
- Check console logs in n8n
- Verify API keys
- Test webhook manually

**Contact:**
- Admin: +62-812-3456-7890
- Technical: Ready for production!

---

**🎉 Ready to serve the Ummah! Deploy dan test sekarang.**