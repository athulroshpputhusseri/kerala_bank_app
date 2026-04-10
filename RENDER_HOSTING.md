# Kerala Bank Application - Render Hosting Guide

## **Render.com** is perfect for hosting your Kerala Bank application!

### **Why Choose Render?**
- **Free tier** available for web services
- **Auto-deployment** from GitHub
- **Built-in database** (PostgreSQL)
- **SSL certificates** automatically
- **Easy setup** - no complex configuration

---

## **Quick Setup: 15 Minutes**

### **Step 1: Prepare Your Code**

#### **A. Create GitHub Repository**
```bash
# Initialize Git
git init
git add .
git commit -m "Initial Kerala Bank app"

# Create repository on GitHub.com
git remote add origin https://github.com/yourusername/kerala-bank.git
git push -u origin main
```

#### **B. Create Render Configuration Files**

**1. `render.yaml`** (Root folder)
```yaml
services:
  # Backend API Service
  - type: web
    name: kerala-bank-api
    env: python
    plan: free
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn main:app --host 0.0.0.0 --port $PORT
    healthCheckPath: /health
    
  # PostgreSQL Database
  - type: pserv
    name: kerala-bank-db
    plan: free
    databaseName: kerala_bank
    databaseUser: kerala_bank_user
```

**2. `requirements.txt`** (Root folder)
```txt
fastapi==0.104.1
uvicorn==0.24.0
sqlalchemy==2.0.23
psycopg2-binary==2.9.9
python-multipart==0.0.6
python-dotenv==1.0.0
```

**3. `.env.production`** (Root folder)
```env
# Production environment variables
DATABASE_URL=postgresql://kerala_bank_user:password@kerala-bank-db:5432/kerala_bank
SECRET_KEY=your-secret-key-here
```

---

### **Step 2: Deploy to Render**

#### **A. Sign Up for Render**
1. Go to **render.com**
2. Sign up with **GitHub**
3. Authorize repository access

#### **B. Create Web Service**
1. Click **"New +"** button
2. Select **"Web Service"**
3. Connect your **GitHub repository**
4. Configure settings:
   - **Name**: `kerala-bank-api`
   - **Environment**: `Python`
   - **Region**: Choose nearest to you
   - **Branch**: `main`
   - **Root Directory**: `backend`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`

#### **C. Create Database**
1. Click **"New +"** button
2. Select **"PostgreSQL"**
3. Configure:
   - **Name**: `kerala-bank-db`
   - **Database Name**: `kerala_bank`
   - **User**: `kerala_bank_user`

---

### **Step 3: Configure Environment**

#### **A. Add Environment Variables**
In your web service settings, add:
```env
DATABASE_URL=postgresql://kerala_bank_user:password@kerala-bank-db:5432/kerala_bank
SECRET_KEY=your-secret-key-here
```

#### **B. Update Backend Code**
In `backend/main.py`, add health check:
```python
@app.get("/health")
def health_check():
    return {"status": "healthy"}
```

---

### **Step 4: Deploy Frontend**

#### **Option 1: Static Site (Recommended)**
1. Create **`static/`** folder
2. Add your frontend files
3. Configure as **Static Site** on Render

#### **Option 2: Build APK for Android**
```bash
# Build APK locally
python -m pyinstaller main11.py --name "Kerala Bank"

# Host APK file on Render static site
# Users download APK from your Render URL
```

---

## **Render URLs**

After deployment, you'll get:
- **Backend API**: `https://kerala-bank-api.onrender.com`
- **Database**: Internal connection
- **Frontend**: `https://kerala-bank.onrender.com`

---

## **Mobile App Setup**

### **Update Frontend Configuration**
In `main11.py`, update API URL:
```python
# Change from localhost to Render URL
API_BASE_URL = "https://kerala-bank-api.onrender.com"
```

### **Build and Distribute**
```bash
# Build APK
python -m pyinstaller main11.py --onefile --name "Kerala Bank"

# Upload APK to Render static site
# Share download link with users
```

---

## **Free Tier Limits**

### **What's Included:**
- **750 hours** of compute time/month
- **PostgreSQL database** (256MB)
- **SSL certificates**
- **Auto-deployment**
- **Custom domains**

### **Upgrade Options:**
- **Starter**: $7/month (more resources)
- **Standard**: $25/month (more performance)
- **Business**: $100/month (full features)

---

## **Monitoring & Maintenance**

### **View Logs**
```bash
# On Render dashboard
# Go to Service > Logs tab
```

### **Health Checks**
```bash
# Test your API
curl https://kerala-bank-api.onrender.com/health
```

### **Database Access**
```bash
# Connect to Render PostgreSQL
psql "postgresql://kerala_bank_user:password@kerala-bank-db:5432/kerala_bank"
```

---

## **Troubleshooting**

### **Common Issues**
1. **Build fails**: Check `requirements.txt`
2. **Database connection**: Verify environment variables
3. **CORS errors**: Update allowed origins
4. **Health check fails**: Add `/health` endpoint

### **Quick Fixes**
```python
# In backend/main.py
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## **Success Checklist**

### **Before Going Live:**
- [ ] **Test all API endpoints**
- [ ] **Verify database connection**
- [ ] **Check mobile app connectivity**
- [ ] **Test user authentication**
- [ ] **Verify loan actions functionality**
- [ ] **Test file uploads (if any)**

### **After Deployment:**
- [ ] **Monitor application logs**
- [ ] **Set up alerts** (if needed)
- [ ] **Regular database backups**
- [ ] **Performance monitoring**

---

## **Next Steps**

### **Production Enhancements:**
1. **Add custom domain** (keralabank.com)
2. **Set up monitoring** (Render has built-in)
3. **Configure email** for notifications
4. **Add analytics** (Google Analytics)
5. **Set up backups** (automatic on Render)

---

## **Support**

### **Render Documentation**
- **docs.render.com** - Official docs
- **Community forum** - User support
- **Email support** - Paid plans

### **Your Kerala Bank App**
- **Fully functional** on Render
- **Mobile ready** with APK distribution
- **Scalable** for multiple users
- **Professional** appearance

---

## **Quick Start Summary**

1. **Push code to GitHub**
2. **Create Render account**
3. **Deploy backend** (Web Service)
4. **Create database** (PostgreSQL)
5. **Configure environment**
6. **Deploy frontend** (Static Site)
7. **Build mobile app** (APK)
8. **Test everything**

**Your Kerala Bank application will be live on Render in minutes!** 

---

## **Render vs Other Options**

| Feature | Render | PythonAnywhere | Heroku |
|---------|--------|----------------|---------|
| **Free Tier** | Yes | Yes | Yes |
| **Database** | Built-in | Separate | Separate |
| **SSL** | Auto | Manual | Auto |
| **Deployment** | Git | Upload | Git |
| **Ease** | Very Easy | Easy | Medium |

**Render is the best choice for your Kerala Bank app!** 

---

## **Congratulations!** 

Your Kerala Bank application is ready for production hosting on Render! 

- **Professional URL**: `https://kerala-bank.onrender.com`
- **Mobile app**: APK download from your site
- **Database**: Managed PostgreSQL
- **SSL**: Automatic security
- **Backup**: Built-in reliability

**You're ready to serve users!** 

---

**Happy hosting!** 

---

## **Need Help?**

If you need assistance:
1. **Check this guide** first
2. **Visit render.com/docs**
3. **Ask in Render community**
4. **Contact their support**

Your Kerala Bank banking application is ready for the world! 

---

**Deploy now and start serving users!**
