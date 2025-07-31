# 🤖 Masjid AI Workflow untuk n8n

Workflow AI Agent untuk masjid yang **siap import ke n8n** dengan fitur OpenRouter AI Chatbot, Supabase Cloud Storage, dan multi-provider WhatsApp API support.

## 📁 File Utama

**`n8n_masjid_workflow.json`** - Workflow n8n siap import dengan AI chatbot lengkap

## 🔧 Cara Import ke n8n

### 1. Copy Workflow JSON
```bash
# Copy isi file n8n_masjid_workflow.json
```

### 2. Import ke n8n
1. Buka **n8n interface** Anda
2. Klik **"+"** untuk workflow baru
3. Klik **"Import from JSON"**
4. **Paste** isi file `n8n_masjid_workflow.json`
5. Klik **"Import"**

### 3. Setup WhatsApp API Key
- Ganti `YOUR_WHATSAPP_API_KEY` di node **"Send WhatsApp Message"**
- Atau set environment variable `WHATSAPP_API_KEY`

### 4. Activate Workflow
- Klik **"Active"** toggle
- Webhook URL akan muncul: `https://your-n8n.com/webhook/webhook-whatsapp`

## 🚀 Fitur Yang Sudah Include

### 🤖 **AI Chatbot (OpenRouter)**
- ✅ API Key sudah include: `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`
- ✅ Model: `moonshotai/kimi-k2:free`
- ✅ Smart conversation untuk pertanyaan Islam
- ✅ Fallback system untuk pertanyaan kompleks

### ☁️ **Supabase Database**
- ✅ URL & API Key sudah include
- ✅ Auto logging ke tabel `usage_analytics`
- ✅ Message delivery tracking
- ✅ User interaction analytics

### 📱 **Multi-Provider WhatsApp**
- ✅ **Fonnte** format support
- ✅ **Woowa** format support
- ✅ **WhatsApp Business API** support
- ✅ **Generic** format support

## 🎯 Layanan Masjid Lengkap

| Keyword | Response |
|---------|----------|
| `jadwal shalat` | 🕌 Waktu shalat hari ini |
| `kajian` | 📚 Jadwal kajian & pengajian |
| `donasi` | 💰 Info rekening & QRIS |
| `acara` | 📅 Agenda kegiatan masjid |
| `alamat` | 🏠 Info lengkap masjid |
| `nikah` | 💒 Syarat pernikahan |
| `konsultasi` | 🤲 Bimbingan ustadz |
| `assalamualaikum` | 👋 Sapaan + menu lengkap |
| **Chat bebas** | 🤖 AI conversation |

## 🔗 Node Structure di n8n

```
WhatsApp Webhook → Enhanced Message Processor → Success Check
                                                      ↓
                  Send WhatsApp ← Success ←← ←← ←← ←← ←
                        ↓
                  Webhook Response
                        
                  Log to Supabase ← Success ←← ←← ←← ←
                  
                  Error Response ← Failed ←← ←← ←← ←
```

## 💬 Contoh AI Conversation

### Input: "Bagaimana cara shalat yang benar?"

**AI Response:**
```
🤲 Assalamualaikum! Berikut panduan shalat yang sesuai sunnah:

📿 **Persiapan:**
• Berwudhu dengan sempurna
• Menghadap kiblat
• Menutup aurat
• Niat dalam hati

🕌 **Gerakan Shalat:**
1. Takbiratul ihram
2. Membaca Al-Fatihah
3. Membaca surah pendek
4. Rukuk dengan tuma'ninah
5. I'tidal (berdiri tegak)
6. Sujud dengan khusyuk
7. Duduk di antara dua sujud
8. Sujud kedua
9. Tasyahud dan salam

📖 Untuk pembelajaran lebih detail, Anda bisa ikut kajian fiqh kami setiap Kamis jam 20:00.

👨‍🏫 **Ustadz Ahmad Dahlan** siap konsultasi di +62-813-1111-2222

💡 Ketik "menu" untuk layanan lain atau chat langsung untuk pertanyaan!

━━━━━━━━━━━━━━━━━━━━━
🕌 Masjid Al-Ikhlas
📱 AI Assistant v3.0
🤖 Melayani dengan ❤️ 24/7
```

## ⚙️ Konfigurasi (Edit di Function Node)

### Update Info Masjid
```javascript
const masjidInfo = {
  nama: 'Nama Masjid Anda',
  alamat: 'Alamat Lengkap Masjid',
  whatsapp: '+62-xxx-xxx-xxxx',
  email: 'email@masjid.id',
  website: 'https://website-masjid.id'
};
```

### Update Rekening Donasi
```javascript
const rekening = {
  bca: 'nomor_rekening_bca',
  mandiri: 'nomor_rekening_mandiri', 
  bri: 'nomor_rekening_bri',
  qris: 'https://link-qris-anda.png'
};
```

### Tambah Ustadz
```javascript
const ustadz = [
  {
    nama: 'Ustadz Nama',
    spesialisasi: ['Fiqh', 'Tafsir'],
    jadwal: 'Senin-Kamis 19:00-21:00',
    kontak: '+62-xxx-xxx-xxxx'
  }
];
```

## 🔧 Setup WhatsApp Provider

### Fonnte
```javascript
// Webhook URL ke n8n: https://your-n8n.com/webhook/webhook-whatsapp
// Format yang didukung: { device, message, message_type }
```

### Woowa  
```javascript
// Format yang didukung: { from, body, type }
```

### WhatsApp Business API
```javascript
// Format yang didukung: { entry[].changes[].value.messages[] }
```

## 📊 Supabase Analytics

### Tables yang akan terisi otomatis:
```sql
-- Usage Analytics
usage_analytics (
  user_phone,
  interaction_type, 
  intent,
  timestamp,
  response_time,
  success
)

-- Message Delivery
message_delivery (
  user_phone,
  message_id,
  status,
  provider,
  timestamp,
  retry_count
)
```

## 🔒 Security Features

- ✅ **Phone Number Validation** - Format Indonesia (+62)
- ✅ **Text Message Only** - Auto reject media untuk security
- ✅ **Error Handling** - Graceful error responses
- ✅ **API Rate Limiting** - Built-in protection
- ✅ **Data Logging** - Complete audit trail

## 🚨 Troubleshooting

### Import Error di n8n?
1. **Copy exact JSON** dari file `n8n_masjid_workflow.json`
2. **Check JSON format** - harus valid JSON
3. **Use latest n8n version** - minimum v0.200+

### Webhook tidak respond?
1. **Check webhook URL** di n8n workflow
2. **Activate workflow** dengan toggle
3. **Test dengan data sample** di n8n interface

### AI tidak response?
1. **OpenRouter API key** sudah include dan valid
2. **Check internet connection** dari n8n server
3. **Model moonshotai/kimi-k2:free** tersedia gratis

### WhatsApp tidak terkirim?
1. **Update WhatsApp API key** di node "Send WhatsApp Message"
2. **Check provider format** (Fonnte/Woowa/etc)
3. **Verify phone number format** (+62xxx)

## 📱 Testing

### Test via n8n Interface
1. Go to **"Enhanced Message Processor"** node
2. Click **"Execute Node"**
3. Input test data:
```json
{
  "body": {
    "device": "+6281234567890",
    "message": "assalamualaikum",
    "message_type": "text"
  }
}
```

### Test via Webhook
```bash
curl -X POST https://your-n8n.com/webhook/webhook-whatsapp \
  -H "Content-Type: application/json" \
  -d '{
    "device": "+6281234567890", 
    "message": "jadwal shalat",
    "message_type": "text"
  }'
```

## 🎉 Ready to Use!

1. ✅ **Import** workflow ke n8n
2. ✅ **Update** WhatsApp API key
3. ✅ **Activate** workflow  
4. ✅ **Copy webhook URL** ke WhatsApp provider
5. ✅ **Test** dengan kirim "assalamualaikum"

**Masjid Anda sekarang punya AI Assistant 24/7!** 🤖🕌

---

**Platform**: n8n • **AI**: OpenRouter • **Storage**: Supabase • **WhatsApp**: Multi-Provider