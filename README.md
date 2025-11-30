# Real Estate Analysis Chatbot

A full-stack web application for analyzing real estate data with a conversational chatbot interface. Built with Django REST Framework (backend) and React + Vite (frontend).

## 🎯 Features

- **Natural Language Queries**: Ask questions about real estate data in plain English
- **Single Locality Analysis**: Get detailed analysis for any locality (Wakad, Aundh, Akurdi, Ambegaon Budruk)
- **Comparison Mode**: Compare multiple localities side-by-side
- **Interactive Charts**: Visualize price and demand trends using Chart.js
- **Data Tables**: View detailed tabular data with filtering
- **AI-Powered Summaries**: OpenAI integration for intelligent summaries (with fallback)
- **Download Data**: Export analysis data as CSV or JSON
- **Auto-scroll Chat**: Automatically scrolls to show latest messages

## 📁 Project Structure

```
.
├── backend/                 # Django REST API
│   ├── api/                # API app
│   │   ├── views.py       # API endpoints
│   │   ├── urls.py        # URL routing
│   │   ├── utils.py       # Query parsing & data processing
│   │   └── apps.py        # App config (loads Excel on startup)
│   ├── backend/           # Django project settings
│   ├── data/              # Excel data file
│   │   └── realestate.xlsx
│   ├── manage.py
│   ├── requirements.txt
│   ├── Procfile           # For Render deployment
│   └── runtime.txt        # Python version
│
└── frontend/              # React + Vite app
    ├── src/
    │   ├── App.jsx        # Main app component
    │   ├── api.js         # API client
    │   └── components/
    │       ├── ChatInput.jsx
    │       ├── ChatMessage.jsx
    │       ├── ChartResult.jsx
    │       └── TableResult.jsx
    ├── package.json
    ├── vite.config.js
    └── vercel.json        # For Vercel deployment
```

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+
- npm or yarn

### Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create Excel data file:**
   ```bash
   python create_dataset.py
   ```
   This will create `data/realestate.xlsx` with the real estate data.

5. **Run migrations:**
   ```bash
   python manage.py migrate
   ```

6. **Start development server:**
   ```bash
   python manage.py runserver
   ```
   Backend will run on `http://localhost:8000`

### Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Create environment file:**
   ```bash
   cp .env.example .env
   ```
   Edit `.env` and set `VITE_API_URL=http://localhost:8000`

4. **Start development server:**
   ```bash
   npm run dev
   ```
   Frontend will run on `http://localhost:5173`

## 📡 API Endpoints

### POST `/api/query/`
Process a natural language query and return analysis.

**Request:**
```json
{
  "query": "Analyze Wakad"
}
```

**Response:**
```json
{
  "summary": "📊 Analysis of Wakad...",
  "chartData": {
    "years": [2020, 2021, 2022, 2023, 2024],
    "prices": [9116.95, 9289.04, ...],
    "demand": [3244, 4548, ...]
  },
  "tableData": [...],
  "localities": ["Wakad"],
  "metrics": ["price", "demand"],
  "type": "single"
}
```

### GET `/api/localities/`
Get list of all available localities.

**Response:**
```json
{
  "localities": ["Akurdi", "Ambegaon Budruk", "Aundh", "Wakad"],
  "count": 4
}
```

### POST `/api/download/`
Download analysis data in CSV or JSON format.

**Request:**
```json
{
  "tableData": [...],
  "format": "csv"
}
```

**Response:** File download (CSV or JSON)

## 🎨 Query Examples

The chatbot supports various query formats:

- **Single Analysis:**
  - "Analyze Wakad"
  - "Give me analysis of Wakad"
  - "Show price growth for Akurdi over the last 3 years"

- **Comparison:**
  - "Compare Ambegaon Budruk and Aundh demand trends"
  - "Compare Wakad and Aundh prices"

- **Specific Metrics:**
  - "Show price trends for Wakad"
  - "Show demand trends for Aundh"

## 🚢 Deployment

### Quick Start

**📖 See `DEPLOYMENT_STEPS.md` for detailed step-by-step instructions!**

### Quick Overview

**Backend (Render):**
1. Create account at [render.com](https://render.com)
2. Create Web Service → Connect GitHub
3. Set Root Directory: `backend`
4. Add environment variables (SECRET_KEY, DEBUG, etc.)
5. Deploy!

**Frontend (Vercel):**
1. Create account at [vercel.com](https://vercel.com)
2. Import GitHub repository
3. Set Root Directory: `frontend`
4. Add `VITE_API_URL` environment variable
5. Deploy!

**Full guide:** See `DEPLOYMENT_STEPS.md` for complete instructions with screenshots and troubleshooting.

## 🔧 Configuration

### Backend Environment Variables

```bash
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=your-domain.onrender.com
CORS_ALLOWED_ORIGINS=https://your-frontend.vercel.app
OPENAI_API_KEY=sk-...  # Optional: For AI-powered summaries
```

### Frontend Environment Variables

```bash
VITE_API_URL=https://your-backend.onrender.com
```

## 🎁 Bonus Features

### OpenAI Integration (Optional)
- Set `OPENAI_API_KEY` environment variable to enable AI-powered summaries
- Automatically falls back to mock summaries if not configured
- **📖 See `OPENAI_SETUP.md` for complete setup guide**
- **💰 Free $5 credits for new users!**
- See `BONUS_FEATURES.md` for details

### Download Data
- Click 📥 CSV or 📥 JSON buttons on bot messages to download data
- Exports all table data from the analysis
- Ready to use in Excel, Google Sheets, or other tools

## 📊 Data Format

The Excel file (`data/realestate.xlsx`) contains the following columns:

- `final location`: Locality name
- `year`: Year of data
- `city`: City name
- `total_sales - igr`: Total sales value
- `flat_sold - igr`: Number of flats sold
- `flat - weighted average rate`: Average price per sqft
- And more...

## 🛠️ Technologies Used

**Backend:**
- Django 4.2.7
- Django REST Framework 3.14.0
- pandas 2.1.3
- openpyxl 3.1.2
- gunicorn 21.2.0
- django-cors-headers 4.3.1

**Frontend:**
- React 18.2.0
- Vite 5.0.8
- Chart.js 4.4.0
- react-chartjs-2 5.2.0
- Bootstrap 5.3.2
- Axios 1.6.2

## 📝 Development Notes

- The Excel file is loaded once on Django startup (in `apps.py`)
- Query parsing uses simple keyword matching (no real LLM)
- Chart type is auto-detected based on query keywords
- All data is pre-loaded in memory for fast lookups

## 🐛 Troubleshooting

**Backend not loading data:**
- Check that `data/realestate.xlsx` exists
- Check Django startup logs for errors

**CORS errors:**
- Ensure `CORS_ALLOWED_ORIGINS` includes your frontend URL
- In development, `CORS_ALLOW_ALL_ORIGINS` is enabled

**Chart not displaying:**
- Check browser console for errors
- Ensure Chart.js is properly imported

## 📄 License

This project is created for the SigmaValue Full Stack Developer Assignment.

## 👤 Author

Built as part of the SigmaValue Full Stack Developer Assignment.
