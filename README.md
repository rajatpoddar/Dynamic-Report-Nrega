# 📊 Schemes & Works Dynamic Dashboard

A professional, interactive dashboard for visualizing and analyzing MGNREGA (Mahatma Gandhi National Rural Employment Guarantee Act) schemes and works data. Upload your Excel or CSV reports to generate dynamic insights instantly.

## Features

✨ **Key Features:**
- 📤 **Easy File Upload** - Upload Excel (.xlsx) or CSV files with a single click
- 📈 **Interactive Charts** - Dynamic Plotly visualizations including pie charts and distribution graphs
- 🔍 **Advanced Filtering** - Filter data by Panchayat and Scheme Type
- 📊 **KPI Metrics** - Real-time Key Performance Indicators including:
  - Total Works Count
  - Zero Paid Works Tracking
  - Critical Progress (<10%) Detection
  - Near Completion Works (>85%)
- 📋 **Detailed Data Tables** - Organized data with comprehensive columns including work code, sanctioned amounts, wages paid, and progress percentage
- 🎨 **Modern UI** - Clean, professional interface with custom styling
- 🐳 **Docker Support** - Easy containerized deployment

## Data Fields Tracked

The dashboard extracts and analyzes the following metrics from your reports:
- **Work Code** - Unique identifier for each work
- **Panchayat** - Administrative division
- **Work Name** - Description of the work
- **Work Type** - Category/Scheme type
- **Financial Year** - Fiscal year of the scheme
- **Work Status** - Current status of the work
- **Sanctioned Amount** - Approved budget
- **Wages Paid** - Wages disbursed
- **Material Paid** - Material costs disbursed
- **Total Paid** - Combined wages and material payments
- **Progress %** - Percentage of completion based on payments

## Technologies Used

- **Streamlit** - Web application framework for Python
- **Pandas** - Data manipulation and analysis
- **Plotly Express** - Interactive data visualization
- **OpenPyXL** - Excel file handling
- **Python 3.10** - Programming language
- **Docker** - Containerization

## Installation

### Prerequisites
- Python 3.10 or higher
- pip package manager
- (Optional) Docker and Docker Compose

### Local Setup

1. **Clone or download the project**
   ```bash
   cd dynamic_report
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   source venv/Scripts/activate  # On Windows
   # or
   source venv/bin/activate      # On macOS/Linux
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Running Locally

1. **Start the Streamlit application**
   ```bash
   streamlit run app.py
   ```

2. **Access the dashboard**
   - Open your browser and navigate to `http://localhost:8501`

3. **Upload your data**
   - Click on "Drop your Excel or CSV file here"
   - Select your MGNREGA report file (Excel or CSV format)
   - The dashboard will automatically process and display your data

4. **Apply Filters**
   - Use the sidebar to filter by Panchayat
   - Filter by Scheme Type to focus on specific work categories
   - View updated metrics and charts in real-time

### Running with Docker

1. **Build and run the Docker container**
   ```bash
   docker-compose up --build
   ```

2. **Access the dashboard**
   - Open your browser and navigate to `http://localhost:3737`

3. **Stop the container**
   ```bash
   docker-compose down
   ```

## File Structure

```
dynamic_report/
├── app.py                    # Main Streamlit application
├── requirements.txt          # Python dependencies
├── Dockerfile               # Docker image configuration
├── docker-compose.yml       # Docker Compose configuration
└── README.md               # This file
```

## Requirements

See `requirements.txt` for the complete list of dependencies:
- streamlit - Web application framework
- pandas - Data processing
- plotly - Visualization library
- openpyxl - Excel file support

## Performance & Health

- **Default Port (Local):** 8501
- **Docker Port:** 3737
- **Health Check:** Container includes automated health checks

## Data Format Requirements

The application expects MGNREGA reports with a specific structure:
- The first 3 rows are treated as headers/metadata and are skipped
- Specific columns are extracted by index (column positions)
- Numeric values are automatically converted with error handling
- Missing or invalid data is handled gracefully with default values

## Tips for Best Results

1. **Data Quality** - Ensure your Excel/CSV file follows the standard MGNREGA format
2. **File Size** - For optimal performance, work with files containing up to 10,000+ rows
3. **Columns** - Verify that all required columns are present in your source file
4. **Encoding** - Use UTF-8 encoding for CSV files with special characters

## Known Limitations

- File size is limited by Streamlit's default upload limits (200MB)
- Very large datasets may take a few seconds to process
- The dashboard is designed for MGNREGA report format specifically

## Troubleshooting

**Issue: "Import Error" when running the app**
- Solution: Ensure all dependencies are installed with `pip install -r requirements.txt`

**Issue: File upload not working**
- Solution: Verify the file is in Excel (.xlsx) or CSV format and follows the expected structure

**Issue: Empty charts or no data displayed**
- Solution: Check that the uploaded file contains the required columns in the expected positions

## Docker Troubleshooting

**Issue: Port 3737 already in use**
- Solution: Modify the port mapping in `docker-compose.yml` or stop the conflicting service

**Issue: Container exits immediately**
- Solution: Check logs with `docker-compose logs` to identify the issue

## Future Enhancements

- [ ] Support for additional report formats
- [ ] Export to PDF/Excel functionality
- [ ] Data caching for improved performance
- [ ] Custom date range filtering
- [ ] Advanced analytics and forecasting
- [ ] User authentication
- [ ] Multi-file batch processing

## Support & Contribution

For issues, suggestions, or contributions, please reach out or create an issue in the repository.

## License

This project is provided as-is for internal use.

---

**Last Updated:** 2026  
**Version:** 1.0.0  
**Status:** Active Development
