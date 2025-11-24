# Deployment Guide - Intelligent Voice Bot

## Prerequisites

### System Requirements
- Python 3.11+
- Node.js 18+ and npm
- FFmpeg (for audio processing)
- PostgreSQL database (or SQLite for development)

### API Keys Required
Set these in your `.env` file:
- `GEMINI_API_KEY` - Google Gemini API for response generation
- `AWS_ACCESS_KEY_ID` & `AWS_SECRET_ACCESS_KEY` - Amazon Polly for text-to-speech
- `DATABASE_URL` - PostgreSQL connection string (or use SQLite)

---

## Local Development Setup

### 1. Backend Setup
```bash
# Install Python dependencies
pip install -r requirements.txt

# Initialize database
python init_db.py

# Run backend server
python dashboard/app.py
```
Backend runs on: `http://localhost:5000`

### 2. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```
Frontend runs on: `http://localhost:5173` (or next available port)

---

## Production Deployment

### Option 1: Traditional Server Deployment

#### Backend (Flask API)
1. **Use a production WSGI server** (Gunicorn or Waitress):
```bash
# Install Gunicorn
pip install gunicorn

# Run with Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 dashboard.app:app
```

2. **Set up reverse proxy** (Nginx):
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location /api {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location / {
        root /var/www/frontend/dist;
        try_files $uri /index.html;
    }
}
```

3. **Environment Variables**:
   - Set all API keys in production environment
   - Use PostgreSQL for production database
   - Set `DATABASE_TYPE=postgresql` in `.env`

#### Frontend (React)
1. **Build for production**:
```bash
cd frontend
npm run build
```

2. **Deploy the `dist` folder** to:
   - Static hosting (Netlify, Vercel, Cloudflare Pages)
   - Or serve via Nginx (as shown above)

3. **Update API endpoint**:
   - Change `http://localhost:5000` to your production API URL in:
     - `frontend/src/context/AuthContext.jsx`
     - `frontend/src/pages/Home.jsx`
     - `frontend/src/pages/Dashboard.jsx`

---

### Option 2: Docker Deployment


```dockerfile
FROM python:3.11-slim

# Install FFmpeg
RUN apt-get update && apt-get install -y ffmpeg

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "dashboard.app:app"]
```

Create `docker-compose.yml`:
```yaml
version: '3.8'
services:
  backend:
    build: .
    ports:
      - "5000:5000"
    environment:
      - GEMINI_API_KEY=${GEMINI_API_KEY}
      - AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID}
      - AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY}
      - DATABASE_URL=postgresql://user:pass@db:5432/voicebot
    depends_on:
      - db
  
  db:
    image: postgres:15
    environment:
      - POSTGRES_DB=voicebot
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
    volumes:
      - postgres_data:/var/lib/postgresql/data

  frontend:
    image: node:18
    working_dir: /app
    volumes:
      - ./frontend:/app
    command: npm run build
    
volumes:
  postgres_data:
```

---

### Option 3: Cloud Platform Deployment

#### **Vercel (Frontend) + Railway/Render (Backend)**

**Frontend on Vercel:**
1. Push code to GitHub
2. Import project in Vercel
3. Set build command: `cd frontend && npm run build`
4. Set output directory: `frontend/dist`
5. Add environment variable: `VITE_API_URL=https://your-backend.railway.app`

**Backend on Railway/Render:**
1. Connect GitHub repository
2. Set start command: `gunicorn -w 4 -b 0.0.0.0:$PORT dashboard.app:app`
3. Add environment variables (API keys, DATABASE_URL)
4. Railway will auto-provision PostgreSQL

---

## Security Checklist

- [ ] Change `JWT_SECRET_KEY` in production (use strong random string)
- [ ] Enable HTTPS (use Let's Encrypt or cloud provider SSL)
- [ ] Set CORS origins to specific domains (not `*`)
- [ ] Use environment variables for all secrets
- [ ] Enable rate limiting on API endpoints
- [ ] Set up database backups
- [ ] Use secure password hashing (already implemented with Werkzeug)

---

## Monitoring & Maintenance

### Logs
- Backend logs: Check Flask/Gunicorn output
- Database logs: Monitor PostgreSQL logs
- Frontend errors: Use browser console or error tracking (Sentry)

### Performance
- Monitor API response times in Dashboard
- Check database query performance
- Monitor Whisper transcription times (can be slow on CPU)

### Scaling
- **Backend**: Add more Gunicorn workers or use multiple instances
- **Database**: Use connection pooling, read replicas
- **Whisper**: Consider GPU instances for faster transcription
- **CDN**: Use CloudFlare or similar for frontend assets

---

## Troubleshooting

### Common Issues

1. **FFmpeg not found**:
   - Ensure FFmpeg is in PATH
   - On Docker: Install in Dockerfile
   - On cloud: Use buildpacks or install in startup script

2. **Database connection failed**:
   - Check DATABASE_URL format
   - Verify PostgreSQL is running
   - Check firewall/security group settings

3. **CORS errors**:
   - Update CORS settings in `dashboard/app.py`
   - Add frontend domain to allowed origins

4. **Whisper slow/crashes**:
   - Use smaller model (tiny/base instead of small)
   - Increase server memory
   - Consider using GPU instances

---

## Quick Deploy Commands

```bash
# Backend
pip install -r requirements.txt
python init_db.py
gunicorn -w 4 -b 0.0.0.0:5000 dashboard.app:app

# Frontend
cd frontend
npm install
npm run build
# Serve dist/ folder with any static server
```

---

## Support

For issues or questions:
- Check logs in `logs/` directory
- Review analytics in Dashboard
- Check database connection with `python init_db.py`
