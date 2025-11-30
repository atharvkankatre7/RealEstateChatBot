# Setup Instructions

Complete step-by-step guide to set up the Real Estate Analysis Chatbot locally.

## 📋 Prerequisites

Before starting, ensure you have:

- **Python 3.11+** installed
  - Check: `python --version`
  - Download: [python.org](https://www.python.org/downloads/)

- **Node.js 18+** and npm installed
  - Check: `node --version` and `npm --version`
  - Download: [nodejs.org](https://nodejs.org/)

- **Git** (optional, for version control)
  - Check: `git --version`

## 🔧 Backend Setup

### Step 1: Navigate to Backend Directory

```bash
cd backend
```

### Step 2: Create Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` in your terminal prompt.

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- Django 4.2.7
- Django REST Framework
- pandas
- openpyxl
- gunicorn
- django-cors-headers
- whitenoise

### Step 4: Create Excel Data File

```bash
python create_dataset.py
```

This creates `data/realestate.xlsx` with the real estate data.

**Expected output:**
```
Created Excel file: data/realestate.xlsx
Total records: 20
Localities: Akurdi, Ambegaon Budruk, Aundh, Wakad
Years: 2020 - 2024
```

### Step 5: Run Database Migrations

```bash
python manage.py migrate
```

This sets up the database (SQLite by default).

### Step 6: Create Superuser (Optional)

```bash
python manage.py createsuperuser
```

This allows you to access Django admin at `/admin/`.

### Step 7: Start Development Server

```bash
python manage.py runserver
```

Backend will run on `http://localhost:8000`

**Verify it's working:**
- Visit: `http://localhost:8000/api/health/`
- Should return: `{"status": "ok", "data_loaded": true, "rows": 20}`

## 🎨 Frontend Setup

### Step 1: Open New Terminal

Keep backend running, open a new terminal window/tab.

### Step 2: Navigate to Frontend Directory

```bash
cd frontend
```

### Step 3: Install Dependencies

```bash
npm install
```

This installs:
- React 18.2.0
- Vite 5.0.8
- Chart.js
- Bootstrap
- Axios
- And more...

### Step 4: Create Environment File

**Windows:**
```bash
copy .env.example .env
```

**macOS/Linux:**
```bash
cp .env.example .env
```

### Step 5: Configure Environment Variables

Edit `.env` file and set:

```env
VITE_API_URL=http://localhost:8000
```

This tells the frontend where to find the backend API.

### Step 6: Start Development Server

```bash
npm run dev
```

Frontend will run on `http://localhost:5173`

**Verify it's working:**
- Browser should open automatically
- You should see the chatbot interface
- Try query: "Analyze Wakad"

## ✅ Verification

### Test Backend API

**Test localities endpoint:**
```bash
curl http://localhost:8000/api/localities/
```

**Test query endpoint:**
```bash
curl -X POST http://localhost:8000/api/query/ \
  -H "Content-Type: application/json" \
  -d "{\"query\": \"Analyze Wakad\"}"
```

### Test Frontend

1. Open `http://localhost:5173`
2. Try these queries:
   - "Analyze Wakad"
   - "Compare Aundh and Akurdi"
   - "Show price trends for Ambegaon Budruk"
   - "Compare Wakad and Aundh demand trends"

3. Verify:
   - ✅ Chat messages appear
   - ✅ Charts display correctly
   - ✅ Tables show data
   - ✅ Loading spinner works

## 🐛 Troubleshooting

### Backend Issues

**Issue: ModuleNotFoundError**
```bash
# Make sure virtual environment is activated
# Reinstall dependencies
pip install -r requirements.txt
```

**Issue: Excel file not found**
```bash
# Run the dataset creation script
python create_dataset.py

# Verify file exists
ls data/realestate.xlsx  # macOS/Linux
dir data\realestate.xlsx  # Windows
```

**Issue: Port 8000 already in use**
```bash
# Use a different port
python manage.py runserver 8001
# Then update frontend .env: VITE_API_URL=http://localhost:8001
```

**Issue: CORS errors**
- Check that `CORS_ALLOW_ALL_ORIGINS = True` in settings.py (for development)
- Verify frontend URL matches

### Frontend Issues

**Issue: npm install fails**
```bash
# Clear cache and retry
npm cache clean --force
npm install
```

**Issue: Module not found**
```bash
# Delete node_modules and reinstall
rm -rf node_modules  # macOS/Linux
rmdir /s node_modules  # Windows
npm install
```

**Issue: API calls failing**
- Verify backend is running on `http://localhost:8000`
- Check `.env` file has correct `VITE_API_URL`
- Check browser console for errors
- Verify CORS is enabled in backend

**Issue: Charts not displaying**
- Check browser console for errors
- Verify Chart.js is installed: `npm list chart.js`
- Check that data is being received from API

**Issue: Port 5173 already in use**
```bash
# Vite will automatically use next available port
# Or specify port in vite.config.js
```

## 📁 Project Structure Check

Verify your project structure:

```
.
├── backend/
│   ├── api/
│   │   ├── views.py
│   │   ├── urls.py
│   │   ├── utils.py
│   │   └── apps.py
│   ├── backend/
│   │   ├── settings.py
│   │   └── urls.py
│   ├── data/
│   │   └── realestate.xlsx  ← Must exist!
│   ├── manage.py
│   ├── requirements.txt
│   └── create_dataset.py
│
└── frontend/
    ├── src/
    │   ├── App.jsx
    │   ├── api.js
    │   └── components/
    │       ├── ChatInput.jsx
    │       ├── ChatMessage.jsx
    │       ├── ChartResult.jsx
    │       └── TableResult.jsx
    ├── package.json
    ├── vite.config.js
    └── .env  ← Must exist!
```

## 🚀 Next Steps

After successful setup:

1. **Explore the code:**
   - Backend: `backend/api/views.py` and `backend/api/utils.py`
   - Frontend: `frontend/src/App.jsx` and components

2. **Try different queries:**
   - Single locality analysis
   - Multi-locality comparison
   - Price-specific queries
   - Demand-specific queries

3. **Customize:**
   - Modify chart colors
   - Add new query patterns
   - Enhance summary generation

4. **Deploy:**
   - Follow `DEPLOYMENT.md` for production deployment

## 📚 Additional Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [React Documentation](https://react.dev/)
- [Vite Documentation](https://vitejs.dev/)
- [Chart.js Documentation](https://www.chartjs.org/)

## 💡 Tips

- Keep backend and frontend terminals open
- Use browser DevTools to debug
- Check terminal logs for errors
- Test API endpoints with curl or Postman
- Use React DevTools browser extension

## 🆘 Still Having Issues?

1. Check all prerequisites are installed
2. Verify file structure matches above
3. Check terminal error messages
4. Review logs in browser console
5. Ensure ports are not blocked by firewall

---

Happy coding! 🎉

