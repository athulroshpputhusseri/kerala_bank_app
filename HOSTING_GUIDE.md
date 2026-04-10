# Kerala Bank Application - Hosting Guide

## 🚀 Quick Hosting Options

### **Option 1: Local Network Hosting (Recommended)**
- **Cost**: Free
- **Setup**: 5 minutes
- **Best for**: Testing, internal use

### **Option 2: Cloud Hosting**
- **Cost**: $5-20/month
- **Setup**: 15 minutes
- **Best for**: Production, external access

---

## 📋 Option 1: Local Network Hosting

### **Step 1: Find Your IP Address**
```bash
# Windows
ipconfig

# Linux/Mac
ifconfig
```

### **Step 2: Update Configuration**
Edit `.env` file:
```env
# Change localhost to your IP
DATABASE_URL=postgresql://user:password@YOUR_IP:5432/kerala_bank
```

### **Step 3: Start Backend**
```bash
cd backend
python -m uvicorn main:app --host 0.0.0.0 --port 8000
```

### **Step 4: Build Frontend**
```bash
# Build APK for Android
python -m pyinstaller main11.py

# Or create executable for Windows
python -m pyinstaller --onefile main11.py
```

### **Step 5: Test Access**
- **Backend**: `http://YOUR_IP:8000`
- **Frontend**: Install APK on Android devices
- **Desktop**: Run executable on Windows

---

## 🌐 Option 2: Cloud Hosting Services

### **Recommended Platforms**

#### **1. PythonAnywhere**
- **Pricing**: Free tier available
- **Setup**: Upload files directly
- **URL**: `https://yourapp.pythonanywhere.com`

#### **2. Heroku**
- **Pricing**: Free tier available
- **Setup**: Git deployment
- **URL**: `https://yourapp.herokuapp.com`

#### **3. Vercel**
- **Pricing**: Free tier available
- **Setup**: Git deployment
- **URL**: `https://yourapp.vercel.app`

#### **4. AWS EC2**
- **Pricing**: Free tier (12 months)
- **Setup**: Full server control
- **URL**: Your custom domain

---

## 🔧 Production Setup Checklist

### **✅ Security**
- [ ] Change default passwords
- [ ] Enable HTTPS (SSL certificate)
- [ ] Set up firewall rules
- [ ] Configure database backups

### **✅ Performance**
- [ ] Optimize database queries
- [ ] Enable caching
- [ ] Set up CDN for static files
- [ ] Monitor application performance

### **✅ Domain**
- [ ] Register custom domain name
- [ ] Configure DNS settings
- [ ] Set up email addresses

---

## 📱 Mobile App Distribution

### **Android APK**
```bash
# Build APK
python -m pyinstaller main11.py --name "Kerala Bank"

# Distribute via:
# - Google Play Store
# - Direct APK download
# - WhatsApp sharing
```

### **iOS App**
```bash
# Requires Mac/Xcode for iOS build
# Consider React Native for cross-platform
```

---

## 🛠️ Deployment Commands

### **Start Backend Service**
```bash
# Production mode
cd backend
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4

# With systemd (Linux)
sudo systemctl start kerala-bank
```

### **Database Setup**
```bash
# PostgreSQL production
createdb kerala_bank_prod
createuser kerala_bank_user

# Update .env for production
DATABASE_URL=postgresql://kerala_bank_user:password@localhost:5432/kerala_bank_prod
```

---

## 📊 Monitoring & Maintenance

### **Log Monitoring**
```bash
# Backend logs
tail -f backend.log

# Application logs
python -c "import logging; logging.basicConfig(level=logging.INFO)"
```

### **Backup Strategy**
```bash
# Database backup
pg_dump kerala_bank_prod > backup_$(date +%Y%m%d).sql

# File backup
tar -czf kerala_bank_backup_$(date +%Y%m%d).tar.gz .
```

---

## 🚨 Troubleshooting

### **Common Issues**
1. **Port already in use**: Change port or kill process
2. **Database connection**: Check credentials and firewall
3. **CORS errors**: Configure allowed origins
4. **Static files not loading**: Check file paths

### **Help Commands**
```bash
# Kill process on port 8000
netstat -tulpn | grep :8000
kill -9 PID

# Check firewall status
sudo ufw status

# Test database connection
python -c "import psycopg2; print('Connected')"
```

---

## 📞 Support

For hosting issues, contact:
- **Documentation**: Check this guide
- **Community**: GitHub Issues
- **Professional**: Consider managed hosting services

---

## ✅ Quick Start Summary

1. **Choose hosting option** (Local vs Cloud)
2. **Follow setup steps** for your choice
3. **Test thoroughly** before going live
4. **Monitor performance** after deployment
5. **Keep backups** of data and configuration

Your Kerala Bank application is ready for hosting! 🎉
