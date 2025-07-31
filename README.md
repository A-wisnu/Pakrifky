# 🕌 Workflow Agent AI Masjid

Sistem workflow agent AI untuk layanan masjid dengan integrasi WhatsApp Business API. Sistem ini menggunakan konfigurasi JSON untuk menghubungkan semua node workflow dan memberikan respons otomatis untuk berbagai layanan masjid.

## 📋 Fitur Utama

### 🔄 Workflow Engine
- **Trigger**: Webhook WhatsApp Business API
- **Intent Classification**: AI-powered classification untuk mengenali maksud pesan
- **Multi-Node Processing**: 12 node berbeda untuk berbagai layanan
- **Error Handling**: Robust error handling dengan retry mechanism
- **Monitoring**: Built-in statistics dan logging

### 🎯 Layanan Masjid
1. **📅 Jadwal Shalat** - Informasi waktu shalat harian
2. **📚 Info Kajian** - Jadwal kajian dan pengajian
3. **💰 Donasi & Infaq** - Informasi rekening dan QRIS
4. **📅 Acara Masjid** - Agenda kegiatan dan event
5. **ℹ️ Info Umum** - Informasi masjid, alamat, kontak
6. **💒 Daftar Nikah** - Syarat dan prosedur pernikahan

## 🏗️ Arsitektur Sistem

```
WhatsApp → Webhook → Input Processor → Intent Classifier → Service Handlers → Response Formatter → WhatsApp Sender
```

### 📊 Node Workflow
| Node ID | Type | Fungsi |
|---------|------|--------|
| node_001 | processor | Validasi input pesan WhatsApp |
| node_002 | ai_classifier | Klasifikasi intent pesan |
| node_003 | data_processor | Handler jadwal shalat |
| node_004 | database_query | Handler info kajian |
| node_005 | payment_processor | Handler donasi |
| node_006 | calendar_processor | Handler acara masjid |
| node_007 | static_responder | Handler info umum |
| node_008 | form_processor | Handler daftar nikah |
| node_009 | ai_responder | Fallback handler |
| node_010 | formatter | Format response |
| node_011 | api_sender | Kirim ke WhatsApp |
| node_012 | logger | Log aktivitas |

## 🚀 Setup dan Instalasi

### 1. Clone Repository
```bash
git clone <repository-url>
cd masjid-ai-workflow
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Environment Configuration
```bash
cp .env.example .env
# Edit .env dengan konfigurasi Anda
```

### 4. Setup Database (Development)
```bash
# Database SQLite akan dibuat otomatis saat pertama kali run
python app.py
```

## ⚙️ Konfigurasi

### Environment Variables
- `ENVIRONMENT`: development/production
- `WHATSAPP_TOKEN`: Token WhatsApp Business API
- `WHATSAPP_VERIFY_TOKEN`: Token verifikasi webhook
- `WEBHOOK_SECRET`: Secret key untuk signature verification
- `ADMIN_PHONE`: Nomor admin untuk notifikasi

### Workflow Configuration
Seluruh konfigurasi workflow ada di `masjid_workflow.json`:
- **Trigger**: Konfigurasi webhook endpoint
- **Nodes**: Definisi semua node dan koneksinya
- **Environment**: Setting development dan production
- **Error Handling**: Policy retry dan fallback
- **Security**: Rate limiting dan input validation

## 🔧 API Endpoints

### Webhook WhatsApp
```
POST /webhook/whatsapp
GET /webhook/whatsapp (verification)
```

### Testing & Monitoring
```
POST /webhook/test        # Test workflow dengan data dummy
GET /health              # Health check
GET /workflow/status     # Status dan statistik workflow
```

## 📱 Format Pesan WhatsApp

### Contoh Input User:
- "jadwal shalat"
- "info kajian"
- "mau donasi"
- "acara apa minggu ini"
- "alamat masjid"
- "syarat nikah"

### Contoh Response:
```
🕌 *Jadwal Shalat Hari Ini*

🌅 Subuh: 04:30
☀️ Dzuhur: 12:15
🌤️ Ashar: 15:30
🌅 Magrib: 18:45
🌙 Isya: 20:00

Semoga bermanfaat! 🤲

---
🕌 *Masjid Al-Ikhlas*
📱 Bot Assistant v1.0
```

## 🔒 Keamanan

- **Webhook Verification**: HMAC signature validation
- **Rate Limiting**: 30 requests/minute per user
- **Input Sanitization**: Validasi dan filtering input
- **Environment Separation**: Konfigurasi terpisah dev/prod

## 📊 Monitoring & Logging

### Statistics Tracking:
- Total executions
- Success/error rate
- Average processing time
- Intent distribution

### Log Files:
- `logs/masjid_webhook.log` - Webhook activities
- `logs/masjid_workflow.log` - Workflow executions

## 🛠️ Development

### Running Development Server
```bash
export ENVIRONMENT=development
python app.py
```

### Testing Workflow
```bash
curl -X POST http://localhost:5000/webhook/test \
  -H "Content-Type: application/json" \
  -d '{"message": "jadwal shalat"}'
```

### Adding New Intent
1. Tambah intent di `masjid_workflow.json` > `intent_classifier` > `intents`
2. Buat handler node baru
3. Update routing di `next_nodes`

### Custom Node Types
Extend `workflow_engine.py` untuk node type baru:
1. Tambah enum di `NodeType`
2. Implementasi handler di `_execute_node()`
3. Update workflow JSON

## 📱 WhatsApp Business API Setup

### 1. Facebook Business Account
- Daftar WhatsApp Business API
- Dapatkan access token
- Setup webhook URL

### 2. Webhook Configuration
```
URL: https://your-domain.com/webhook/whatsapp
Verify Token: your_verify_token
```

### 3. Message Template (Optional)
Untuk broadcast message atau notifikasi proaktif

## 🔄 Production Deployment

### 1. Environment Setup
```bash
export ENVIRONMENT=production
export WHATSAPP_TOKEN=your_production_token
export DATABASE_URL=postgresql://user:pass@host/db
```

### 2. Database Migration
```bash
# Setup PostgreSQL untuk production
# Update connection string di environment
```

### 3. Process Manager
```bash
# Gunakan gunicorn untuk production
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## 📈 Scaling Considerations

- **Database**: Migrate ke PostgreSQL untuk production
- **Caching**: Redis untuk response caching
- **Queue**: Celery untuk async processing
- **Load Balancer**: Nginx untuk multiple instances

## 🤝 Contributing

1. Fork repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Create Pull Request

## 📄 License

MIT License - see LICENSE file for details

## 🆘 Support

- **Documentation**: Lihat README dan komentar kode
- **Issues**: Gunakan GitHub Issues
- **WhatsApp**: Hubungi admin di nomor yang terkonfigurasi

---

**Dibuat dengan ❤️ untuk kemudahan layanan masjid** 🕌