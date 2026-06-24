# 📊 MGNREGA Schemes & Works Dynamic Dashboard

A professional, interactive Streamlit dashboard for analyzing MGNREGA scheme data with advanced search, analytics, and Excel export capabilities.

## ✨ Features

### 🔍 Smart Search
- **Live search** by Work Name or Work Code (partial text supported)
- **Instant shortlisting** with color-coded progress indicators
- **Individual work analytics** with detailed insights

### 📈 Analytics & Visualizations
- **KPI Cards**: Total works, zero paid, critical & near-completion counts
- **Work Type Distribution**: Interactive pie charts
- **Financial Year Analysis**: Bar charts showing old vs new schemes
- **Panchayat-wise Breakdown**: Horizontal bar charts & comparisons
- **Progress Distribution**: Histogram showing work progress spread
- **Budget Utilisation**: Sanctioned vs Paid comparisons

### 🎯 Individual Work Analytics
When you search and select a specific work, you get:
- **Progress Gauge**: Visual indicator with color zones
- **Expenditure Breakdown**: Wages, Material, and Remaining budget pie chart
- **Panchayat Comparison**: How this work compares to panchayat average
- **Budget Utilisation**: Real-time utilisation percentage

### 📥 Professional Export
- **Formatted Excel Export** (not basic CSV!)
  - Styled headers with dark navy background
  - Alternating row colors for readability
  - Auto-formatted currency columns (₹ symbol, comma separators)
  - Percentage columns with % format
  - Frozen header row & auto-filter enabled
  - Column width optimization
- **Per-tab export** available on each report view

### 🔎 Advanced Filters
- Panchayat
- Work Type / Scheme
- Financial Year
- Work Status

### 📋 Detailed Reports (Tabs)
- **All Schemes**: Complete dataset
- **Zero Paid**: Works with no payment yet
- **Low Progress**: Works below 10% completion
- **High Progress**: Works above 85% completion
- **Old Schemes**: Historical financial years
- **Material Oriented**: Works with material expenditure

## 🚀 Quick Start

### Using Virtual Environment (Recommended)

1. **Clone the repository**
   ```bash
   git clone https://github.com/rajatpoddar/Dynamic-Report-Nrega.git
   cd Dynamic-Report-Nrega
   ```

2. **Create and activate virtual environment**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate
   
   # Linux/Mac
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the app**
   ```bash
   streamlit run app.py --server.port=3737
   ```

5. **Open in browser**
   ```
   http://localhost:3737
   ```

### Using Docker

1. **Build and run**
   ```bash
   docker-compose up --build
   ```

2. **Access**
   ```
   http://localhost:3737
   ```

## 📂 File Structure

```
.
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
├── Dockerfile          # Docker configuration
├── docker-compose.yml  # Docker Compose setup
├── .dockerignore       # Docker ignore rules
├── .gitignore          # Git ignore rules
└── README.md           # This file
```

## 📊 Expected Data Format

The app expects MGNREGA Excel/CSV files with:
- Header rows starting from row 4 (rows 1-3 skipped)
- Column 4: Panchayat
- Column 5: Financial Year
- Column 6: Work Status
- Column 7: Work Code
- Column 8: Work Name
- Column 12: Work Type
- Column 16: Sanctioned Amount
- Column 23: Wages Paid
- Column 24: Material Paid

## 🛠️ Technology Stack

- **Streamlit**: Web framework
- **Pandas**: Data manipulation
- **Plotly**: Interactive visualizations
- **XlsxWriter**: Professional Excel export
- **OpenPyxl**: Excel file reading

## 📝 Dependencies

```
streamlit
pandas
plotly
openpyxl
xlsxwriter
```

## 🎨 UI Features

- Modern, professional design with custom CSS
- Responsive layout
- Dark sidebar with light content area
- Color-coded metrics and progress indicators
- Gradient backgrounds for data tables
- Card-based layout for work details

## 🔧 Configuration

The app runs on port `3737` by default. To change:

```bash
streamlit run app.py --server.port=YOUR_PORT
```

## 📸 Screenshots

Upload your MGNREGA Excel/CSV file and get:
- ✅ Instant KPIs
- ✅ Interactive charts
- ✅ Smart search
- ✅ Individual work analytics
- ✅ Professional Excel reports

## 🤝 Contributing

Pull requests are welcome. For major changes, please open an issue first.

## 📜 License

MIT

## 👤 Author

**Rajat Poddar**
- GitHub: [@rajatpoddar](https://github.com/rajatpoddar)

---

**Made with ❤️ for MGNREGA data analysis**
