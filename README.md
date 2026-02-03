# Equipment Visualizer

A modern hybrid web and desktop application for analyzing chemical equipment parameters. Upload CSV data to get instant analytics, interactive visualizations, and PDF reports.

## ✨ Features

- **Dual Platform**: Web app (React) and Desktop app (PyQt5) share the same backend
- **CSV Upload**: Drag-and-drop CSV upload for both web and desktop
- **Real-time Analytics**: Instant summary statistics and calculations
- **Interactive Charts**: Bar, pie, and trend charts powered by Chart.js (web) and Matplotlib (desktop)
- **Equipment Data Table**: Sortable, searchable equipment list
- **PDF Reports**: Generate professional PDF reports for any dataset
- **Dataset History**: Store and access last 5 uploaded datasets
- **Minimal Design**: Clean, modern UI with custom Inter font and lucide-react icons
- **Cross-platform**: Windows, Mac, and Linux support

## 🏗️ Architecture

The application follows a **client-server architecture**:

```
┌──────────────────────────┐    ┌──────────────────────────┐
│  React Web Frontend      │    │ PyQt5 Desktop App        │
│ (localhost:3000)         │    │                          │
└────────────┬─────────────┘    └────────────┬─────────────┘
             │                               │
             └──────────────┬────────────────┘
                            │
                  ┌─────────▼────────┐
                  │ Django REST API  │
                  │ (localhost:8000) │
                  └─────────┬────────┘
                            │
                  ┌─────────▼────────┐
                  │ SQLite Database  │
                  │ (Last 5 datasets)│
                  └──────────────────┘
```

## 🛠️ Tech Stack

### Backend
- **Framework**: Django 3.2+ with Django REST Framework
- **Database**: SQLite (configurable to PostgreSQL)
- **Data Processing**: Pandas (CSV parsing, analytics)
- **Reports**: ReportLab (PDF generation)

### Web Frontend
- **Framework**: React 18.2
- **Charts**: Chart.js 4.4
- **Icons**: lucide-react
- **HTTP**: Axios
- **Typography**: Inter font (Google Fonts)
- **Styling**: CSS3 with minimal design principles

### Desktop Frontend
- **GUI**: PyQt5
- **Charts**: Matplotlib
- **HTTP**: Requests library
- **Data**: Pandas

## 📋 Requirements

- Python 3.8 or higher
- Node.js 14 or higher
- Git

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 14+
- Git

### 1️⃣ Backend Setup (3 minutes)

```bash
cd backend
python -m venv venv
venv\Scripts\activate      # Windows
# source venv/bin/activate  # Mac/Linux

pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Backend runs on `http://localhost:8000`

### 2️⃣ Web Frontend Setup (2 minutes)

```bash
cd frontend
npm install
npm start
```

Frontend runs on `http://localhost:3000`

**Local development uses `.env.local`** (created automatically):
```
REACT_APP_API_URL=http://localhost:8000
```

### 3️⃣ Desktop App Setup (1 minute)

```bash
cd desktop
pip install -r requirements.txt
python main.py
```

The desktop app automatically connects to `http://localhost:8000`

## 🧪 Testing with Sample Data

Use `sample_equipment_data.csv` to test all features:
1. Start backend and frontend
2. Open web app at `http://localhost:3000`
3. Upload the CSV file
4. View charts, tables, and download PDF report
5. Try the desktop app too - it connects to the same backend

## ❌ No Authentication Required

- **Demo mode**: All endpoints work without login
- **Fallback user**: Requests use "demo" user automatically
- **CSRF disabled**: For development simplicity
- **CORS enabled**: Frontend and desktop communicate freely with backend

## 📁 Project Structure

```
.
├── backend/                    # Django REST API
│   ├── equipment_api/         # Main app (models, views, serializers)
│   ├── manage.py
│   └── requirements.txt
│
├── frontend/                   # React web application
│   ├── src/
│   │   ├── components/        # React components
│   │   ├── App.js
│   │   └── App.css
│   └── package.json
│
├── desktop/                    # PyQt5 desktop application
│   ├── main.py               # Main application file
│   └── requirements.txt
│
├── sample_equipment_data.csv   # Test data
├── README.md                   # This file
├── DOCUMENTATION.md            # Complete technical documentation
└── QUICKSTART.md              # Quick reference guide
```

## 🔌 API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/upload/` | POST | Upload and analyze CSV file |
| `/api/history/` | GET | Get last 5 uploaded datasets |
| `/api/summary/{id}/` | GET | Get full details for a dataset |
| `/api/report/{id}/` | GET | Generate and download PDF report |

### Example Upload Request

```bash
curl -X POST http://localhost:8000/api/upload/ \
  -F "file=@sample_equipment_data.csv"
```

Response includes:
- Dataset metadata (name, upload timestamp, owner)
- Summary statistics (total count, averages)
- Equipment type distribution
- Full equipment list with parameters

## 🎨 Design System

### Color Palette
- **Primary**: #2563eb (Modern Blue)
- **Primary Dark**: #1e40af
- **Secondary**: #64748b (Slate Gray)
- **Success**: #059669 (Teal)
- **Text Primary**: #0f172a (Dark Slate)
- **Background**: #f8fafc (Off-white)

### Typography
- **Font Family**: Inter (Google Fonts)
- **Weights**: 300, 400, 500, 600, 700
- **Minimal design** with subtle shadows and clean whitespace

### Icons
- **Web**: lucide-react (professional, consistent icon set)
- **Desktop**: Text labels (simple, clean)

## 🔄 Data Flow

### CSV Upload Process

```
1. User uploads CSV file
   ↓
2. Backend validates file format and required columns
   ↓
3. Pandas reads CSV and calculates statistics:
   - Total equipment count
   - Average flowrate, pressure, temperature
   - Equipment type distribution
   ↓
4. Data stored in SQLite:
   - One Dataset record (summary)
   - Multiple EquipmentData records (details)
   ↓
5. Previous datasets maintained (max 5 per user)
   ↓
6. JSON response sent to frontend
   ↓
7. Frontend displays:
   - Summary statistics
   - Interactive charts
   - Equipment data table
```

## 🧪 Testing

### Test the Full Workflow

1. **Start all services** (backend, frontend, desktop)
2. **Upload sample data** via web interface
3. **View analytics** in Summary and Charts tabs
4. **Check data table** for equipment details
5. **Select from history** to view previous uploads
6. **Generate PDF report** and verify content

### Manual API Testing

```bash
# Upload CSV
curl -X POST http://localhost:8000/api/upload/ \
  -F "file=@sample_equipment_data.csv"

# Get history
curl http://localhost:8000/api/history/

# Get summary
curl http://localhost:8000/api/summary/1/

# Download PDF
curl http://localhost:8000/api/report/1/ -o report.pdf
```

## 🐛 Troubleshooting

| Problem | Solution |
|---------|----------|
| Backend won't start | Check Python 3.8+, verify venv activated |
| CORS errors | Ensure backend at :8000, frontend at :3000 |
| CSV upload fails | Check columns: Equipment Name, Type, Flowrate, Pressure, Temperature |
| Charts not showing | Verify Chart.js/Matplotlib installed, check browser console |
| Desktop won't launch | Ensure PyQt5 installed, run `pip install PyQt5` |

## 📝 CSV File Format

Your CSV must have these columns (exact names required):

```csv
Equipment Name,Type,Flowrate,Pressure,Temperature
Pump-A1,Pump,50.0,110.0,70.0
Tank-B1,Tank,30.0,105.0,65.0
Reactor-C1,Reactor,75.5,125.0,80.5
...
```

## 🚀 Deployment

For production deployment:

1. **Backend**: Use Gunicorn + Nginx
2. **Frontend**: Build with `npm run build`, serve with static server
3. **Database**: Replace SQLite with PostgreSQL
4. **Environment**: Set `DEBUG=False`, configure `ALLOWED_HOSTS`

## 📄 License

This project is provided as-is for educational purposes.

## 👥 Contributing

Pull requests welcome! Please ensure:
- Code follows existing style conventions
- Comments explain business logic
- Both web and desktop functionality tested
- README updated if features added

## 💡 Future Enhancements

- [ ] Multi-user collaboration with permissions
- [ ] Real-time data streaming
- [ ] Advanced filtering and search
- [ ] Custom chart creation
- [ ] Data export formats (Excel, JSON)
- [ ] Equipment comparison tools
- [ ] Trend analysis and forecasting
- [ ] Mobile app version

---

**Version**: 1.0  
**Last Updated**: February 2026  
**Status**: Production Ready ✅
