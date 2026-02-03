import sys
import requests
import pandas as pd
from io import StringIO
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, QLineEdit, 
                             QFileDialog, QTableWidget, QTableWidgetItem, 
                             QMessageBox, QTabWidget, QComboBox, QTextEdit,
                             QDialog, QProgressBar, QScrollArea, QFrame,
                             QGridLayout, QSpinBox, QDoubleSpinBox)
from PyQt5.QtCore import Qt, QSize, QTimer
from PyQt5.QtGui import QIcon, QFont, QColor, QPixmap
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib import pyplot as plt
import matplotlib.patches as mpatches

# QSS stylesheet - defines the visual appearance of all PyQt5 widgets
# Uses minimal, elegant design with modern blue color scheme
# All colors match the web frontend for consistency
MODERN_STYLE = """
    QMainWindow {
        background-color: #f8fafc;
    }
    
    QWidget {
        background-color: #f8fafc;
    }
    
    QPushButton {
        background-color: #2563eb;
        color: white;
        border: none;
        border-radius: 6px;
        padding: 10px 20px;
        font-weight: 500;
        font-size: 11pt;
        font-family: 'Inter', 'Segoe UI', sans-serif;
    }
    
    QPushButton:hover {
        background-color: #1e40af;
    }
    
    QPushButton:pressed {
        background-color: #1e3a8a;
        padding: 11px 19px;
    }
    
    QLabel {
        color: #0f172a;
        font-size: 11pt;
        font-family: 'Inter', 'Segoe UI', sans-serif;
    }
    
    QLineEdit {
        border: 1px solid #e2e8f0;
        border-radius: 6px;
        padding: 8px;
        background-color: white;
        color: #0f172a;
        font-family: 'Inter', 'Segoe UI', sans-serif;
    }
    
    QLineEdit:focus {
        border: 2px solid #2563eb;
        padding: 7px;
        background-color: white;
    }
    
    QComboBox {
        border: 1px solid #e2e8f0;
        border-radius: 6px;
        padding: 6px;
        background-color: white;
        color: #0f172a;
        font-family: 'Inter', 'Segoe UI', sans-serif;
    }
    
    QComboBox:focus {
        border: 2px solid #2563eb;
        padding: 5px;
    }
    
    QTabWidget::pane {
        border: 1px solid #e2e8f0;
        border-radius: 6px;
    }
    
    QTabBar::tab {
        background-color: #f1f5f9;
        color: #64748b;
        padding: 8px 20px;
        margin-right: 2px;
        border-radius: 6px 6px 0px 0px;
        font-weight: 500;
        font-family: 'Inter', 'Segoe UI', sans-serif;
        border: 1px solid #e2e8f0;
    }
    
    QTabBar::tab:selected {
        background-color: #2563eb;
        color: white;
        border: 1px solid #2563eb;
    }
    
    QTableWidget {
        border: 1px solid #e2e8f0;
        border-radius: 6px;
        gridline-color: #e2e8f0;
        background-color: white;
        alternate-background-color: #f8fafc;
    }
    
    QTableWidget::item {
        padding: 8px;
        color: #0f172a;
        font-family: 'Inter', 'Segoe UI', sans-serif;
    }
    
    QHeaderView::section {
        background-color: #2563eb;
        color: white;
        padding: 8px;
        border: none;
        font-weight: 600;
        font-family: 'Inter', 'Segoe UI', sans-serif;
    }
    
    QTextEdit {
        border: 1px solid #e2e8f0;
        border-radius: 6px;
        background-color: white;
        color: #0f172a;
        font-family: 'Inter', 'Courier New', monospace;
        font-size: 10pt;
    }
    
    QProgressBar {
        border: 1px solid #e2e8f0;
        border-radius: 6px;
        background-color: white;
        text-align: center;
        color: white;
        font-weight: 500;
    }
    
    QProgressBar::chunk {
        background-color: #2563eb;
    }
"""

class MainWindow(QMainWindow):
    # Main application window - orchestrates the desktop UI
    # Manages file upload, API communication, and visualization
    def __init__(self, session, api_url, username):
        super().__init__()
        self.session = session  # HTTP session for API calls
        self.api_url = api_url  # Backend API base URL
        self.username = username  # Current user (hardcoded as 'admin')
        self.current_dataset = None  # Currently loaded dataset
        self.setStyleSheet(MODERN_STYLE)
        
        self.initUI()
    
    def initUI(self):
        # Build the UI layout - header, upload controls, tabs, download button
        self.setWindowTitle(f'Equipment Visualizer - {self.username}')
        self.setGeometry(50, 50, 1400, 900)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Header with user info
        header_widget = QFrame()
        header_widget.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 10px;
                border: 1px solid #e2e8f0;
            }
        """)
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(20, 15, 20, 15)
        
        title_label = QLabel('Equipment Visualizer Dashboard')
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title_font.setFamily('Inter')
        title_label.setFont(title_font)
        title_label.setStyleSheet('color: #2563eb;')
        header_layout.addWidget(title_label)
        
        header_layout.addStretch()
        
        user_label = QLabel(f'{self.username}')
        user_font = QFont()
        user_font.setPointSize(10)
        user_font.setFamily('Inter')
        user_label.setFont(user_font)
        user_label.setStyleSheet('color: #64748b;')
        header_layout.addWidget(user_label)
        
        header_widget.setLayout(header_layout)
        main_layout.addWidget(header_widget)
        
        # Upload and History Section
        controls_widget = QFrame()
        controls_widget.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 10px;
                border: 1px solid #e2e8f0;
            }
        """)
        controls_layout = QVBoxLayout()
        controls_layout.setContentsMargins(20, 15, 20, 15)
        controls_layout.setSpacing(10)
        
        # File upload section
        upload_title = QLabel('Upload & Analyze')
        upload_title.setStyleSheet('font-weight: 600; font-size: 12pt; color: #0f172a; font-family: Inter;')
        controls_layout.addWidget(upload_title)
        
        upload_row = QHBoxLayout()
        upload_row.setSpacing(10)
        
        self.file_path_label = QLabel('No file selected')
        self.file_path_label.setStyleSheet('color: #64748b; padding: 8px; font-family: Inter;')
        upload_row.addWidget(self.file_path_label, 1)
        
        browse_btn = QPushButton('Browse')
        browse_btn.setMinimumWidth(120)
        browse_btn.clicked.connect(self.browse_file)
        upload_row.addWidget(browse_btn)
        
        upload_btn = QPushButton('Upload & Analyze')
        upload_btn.setMinimumWidth(150)
        upload_btn.clicked.connect(self.upload_file)
        upload_row.addWidget(upload_btn)
        
        controls_layout.addLayout(upload_row)
        
        # History section
        history_row = QHBoxLayout()
        history_row.setSpacing(10)
        
        history_label = QLabel('Recent Datasets:')
        history_label.setStyleSheet('font-weight: 600; color: #0f172a; font-family: Inter;')
        history_row.addWidget(history_label)
        
        self.history_combo = QComboBox()
        self.history_combo.setMinimumWidth(250)
        self.history_combo.currentIndexChanged.connect(self.load_dataset)
        history_row.addWidget(self.history_combo)
        
        refresh_btn = QPushButton('Refresh')
        refresh_btn.setMinimumWidth(100)
        refresh_btn.clicked.connect(self.load_history)
        history_row.addWidget(refresh_btn)
        
        history_row.addStretch()
        controls_layout.addLayout(history_row)
        
        controls_widget.setLayout(controls_layout)
        main_layout.addWidget(controls_widget)
        
        # Tabs
        self.tabs = QTabWidget()
        
        # Summary tab
        self.summary_tab = QTextEdit()
        self.summary_tab.setReadOnly(True)
        self.summary_tab.setStyleSheet("""
            QTextEdit {
                background-color: white;
                border: 1px solid #e2e8f0;
                border-radius: 6px;
                padding: 15px;
                font-family: 'Inter', 'Courier New', monospace;
                font-size: 10pt;
                line-height: 1.6;
                color: #0f172a;
            }
        """)
        self.tabs.addTab(self.summary_tab, "Summary")
        
        # Charts tab
        self.charts_tab = QWidget()
        self.charts_layout = QVBoxLayout()
        self.charts_tab.setLayout(self.charts_layout)
        self.tabs.addTab(self.charts_tab, "Charts")
        
        # Data table tab
        self.table_widget = QTableWidget()
        self.table_widget.setStyleSheet("""
            QTableWidget {
                background-color: white;
                border: 1px solid #e2e8f0;
                border-radius: 6px;
            }
            QTableWidget::item:selected {
                background-color: #e0e7ff;
                color: #0f172a;
            }
        """)
        self.tabs.addTab(self.table_widget, "Data Table")
        
        main_layout.addWidget(self.tabs)
        
        # Download button
        pdf_btn = QPushButton('Download PDF Report')
        pdf_btn.setMinimumHeight(45)
        pdf_btn.clicked.connect(self.download_pdf)
        pdf_btn_font = QFont('Inter', 11, QFont.Bold)
        pdf_btn.setFont(pdf_btn_font)
        main_layout.addWidget(pdf_btn)
        
        central_widget.setLayout(main_layout)
        
        # Load initial history
        self.load_history()
    
    def browse_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, 
            "Select CSV File", 
            "", 
            "CSV Files (*.csv)"
        )
        if file_path:
            self.file_path = file_path
            self.file_path_label.setText(f"{file_path.split('/')[-1]}")
            self.file_path_label.setStyleSheet('color: #059669; padding: 8px; font-weight: 500; font-family: Inter;')
    
    def upload_file(self):
        # Handle CSV file upload - validates file, sends to backend, updates UI
        if not hasattr(self, 'file_path'):
            QMessageBox.warning(self, 'Error', 'Please select a file first')
            return
        
        try:
            with open(self.file_path, 'rb') as f:
                files = {'file': f}
                response = self.session.post(
                    f'{self.api_url}/upload/',
                    files=files
                )
            
            # API returns 201 on success with full dataset JSON
            if response.status_code == 201:
                data = response.json()
                self.current_dataset = data.get('data')
                self.display_summary()
                self.display_charts()
                self.display_table()
                self.load_history()
                QMessageBox.information(self, 'Success', 'File uploaded and analyzed successfully!')
            else:
                QMessageBox.warning(self, 'Error', response.json().get('error', 'Upload failed'))
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Upload failed: {str(e)}')
    
    def load_history(self):
        # Fetch and populate the dataset history dropdown
        # Displays last 5 uploaded datasets with item count in label
        try:
            response = self.session.get(f'{self.api_url}/history/')
            if response.status_code == 200:
                history = response.json()
                self.history_combo.clear()
                self.history_combo.addItem("-- Select a dataset --", None)
                for item in history:
                    display_text = f"{item['name']} ({item['total_count']} items)"
                    self.history_combo.addItem(display_text, item['id'])
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Failed to load history: {str(e)}')
    
    def load_dataset(self):
        # Load previously uploaded dataset when user selects from history
        # Makes API call to get full dataset details
        dataset_id = self.history_combo.currentData()
        if dataset_id is None:
            return
        
        try:
            response = self.session.get(f'{self.api_url}/summary/{dataset_id}/')
            if response.status_code == 200:
                self.current_dataset = response.json()
                self.display_summary()
                self.display_charts()
                self.display_table()
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Failed to load dataset: {str(e)}')
    
    def display_summary(self):
        if not self.current_dataset:
            return
        
        summary_text = f"""
Equipment Visualizer - Summary Statistics
─────────────────────────────────────────────

Dataset:              {self.current_dataset['name']}
Uploaded:             {self.current_dataset['uploaded_at']}
Uploaded By:          {self.current_dataset['uploaded_by_username']}

KEY METRICS
─────────────────────────────────────────────

Total Equipment       {self.current_dataset['total_count']}
Average Flowrate      {self.current_dataset['avg_flowrate']:.2f}
Average Pressure      {self.current_dataset['avg_pressure']:.2f}
Average Temperature   {self.current_dataset['avg_temperature']:.2f}

EQUIPMENT TYPE DISTRIBUTION
─────────────────────────────────────────────

"""
        
        for equipment_type, count in self.current_dataset['type_distribution'].items():
            percentage = (count / self.current_dataset['total_count']) * 100
            bar_length = int(percentage / 5)
            bar = '█' * bar_length + '░' * (20 - bar_length)
            summary_text += f"  {equipment_type:<20} {bar} {count:>3} ({percentage:>5.1f}%)\n"
        
        self.summary_tab.setText(summary_text)
    
    def display_charts(self):
        if not self.current_dataset:
            return
        
        # Clear previous charts
        for i in reversed(range(self.charts_layout.count())): 
            self.charts_layout.itemAt(i).widget().setParent(None)
        
        # Create a figure with subplots
        fig = Figure(figsize=(12, 8), dpi=100, facecolor='white')
        
        # Pie chart for type distribution
        ax1 = fig.add_subplot(2, 2, 1)
        types = list(self.current_dataset['type_distribution'].keys())
        counts = list(self.current_dataset['type_distribution'].values())
        colors = ['#2563eb', '#1e40af', '#3b82f6', '#0ea5e9', '#06b6d4', '#10b981'][:len(types)]
        ax1.pie(counts, labels=types, autopct='%1.1f%%', colors=colors, startangle=90)
        ax1.set_title('Equipment Type Distribution', fontweight='bold', fontsize=12, color='#0f172a')
        
        # Bar chart for average parameters
        ax2 = fig.add_subplot(2, 2, 2)
        parameters = ['Flowrate', 'Pressure', 'Temperature']
        values = [
            self.current_dataset['avg_flowrate'],
            self.current_dataset['avg_pressure'],
            self.current_dataset['avg_temperature']
        ]
        bars = ax2.bar(parameters, values, color=['#2563eb', '#3b82f6', '#0ea5e9'])
        ax2.set_title('Average Parameter Values', fontweight='bold', fontsize=12, color='#0f172a')
        ax2.set_ylabel('Value', fontweight='bold', color='#0f172a')
        ax2.tick_params(colors='#0f172a')
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.2f}', ha='center', va='bottom', fontweight='bold', color='#0f172a')
        
        # Equipment count stats
        ax3 = fig.add_subplot(2, 2, 3)
        type_names = list(self.current_dataset['type_distribution'].keys())[:10]
        type_counts = list(self.current_dataset['type_distribution'].values())[:10]
        bars = ax3.barh(type_names, type_counts, color=['#2563eb', '#1e40af', '#3b82f6', '#0ea5e9', '#06b6d4', '#10b981', '#059669', '#14b8a6', '#06b6d4', '#0284c7'][:len(type_names)])
        ax3.set_title('Equipment Count by Type', fontweight='bold', fontsize=12, color='#0f172a')
        ax3.set_xlabel('Count', fontweight='bold', color='#0f172a')
        ax3.tick_params(colors='#0f172a')
        
        # Add count labels
        for i, (name, count) in enumerate(zip(type_names, type_counts)):
            ax3.text(count, i, f' {count}', va='center', fontweight='bold', color='#0f172a')
        
        # Summary text
        ax4 = fig.add_subplot(2, 2, 4)
        ax4.axis('off')
        summary_info = f"""
Dataset: {self.current_dataset['name']}
Total Equipment: {self.current_dataset['total_count']}

Key Metrics:
• Avg Flowrate: {self.current_dataset['avg_flowrate']:.2f}
• Avg Pressure: {self.current_dataset['avg_pressure']:.2f}
• Avg Temperature: {self.current_dataset['avg_temperature']:.2f}

Equipment Types: {len(self.current_dataset['type_distribution'])}
        """
        ax4.text(0.1, 0.5, summary_info, fontsize=11, verticalalignment='center',
                family='monospace', color='#0f172a', bbox=dict(boxstyle='round', facecolor='#f8fafc', alpha=0.8, edgecolor='#e2e8f0'))
        
        fig.tight_layout()
        canvas = FigureCanvas(fig)
        self.charts_layout.addWidget(canvas)
    
    def display_table(self):
        if not self.current_dataset or 'equipment' not in self.current_dataset:
            return
        
        equipment = self.current_dataset['equipment']
        
        # Set up table
        self.table_widget.setRowCount(len(equipment))
        self.table_widget.setColumnCount(5)
        self.table_widget.setHorizontalHeaderLabels([
            'Equipment Name', 'Type', 'Flowrate', 'Pressure', 'Temperature'
        ])
        
        # Populate table
        for row, item in enumerate(equipment):
            items = [
                item['equipment_name'],
                item['equipment_type'],
                f"{item['flowrate']:.2f}",
                f"{item['pressure']:.2f}",
                f"{item['temperature']:.2f}"
            ]
            
            for col, text in enumerate(items):
                table_item = QTableWidgetItem(text)
                if col == 1:  # Type column - add styling
                    table_item.setForeground(QColor('#2563eb'))
                self.table_widget.setItem(row, col, table_item)
        
        # Resize columns
        self.table_widget.resizeColumnsToContents()
        header = self.table_widget.horizontalHeader()
        header.setStretchLastSection(True)
    
    def download_pdf(self):
        # Generate and download PDF report for current dataset
        # Opens save dialog, makes API request, saves to user's filesystem
        if not self.current_dataset:
            QMessageBox.warning(self, 'Error', 'No dataset loaded. Please load a dataset first.')
            return
        
        try:
            file_path, _ = QFileDialog.getSaveFileName(
                self,
                "Save PDF Report",
                f"equipment_report_{self.current_dataset['id']}.pdf",
                "PDF Files (*.pdf)"
            )
            
            if not file_path:
                return
            
            # Fetch PDF from backend
            response = self.session.get(
                f'{self.api_url}/report/{self.current_dataset["id"]}/',
                timeout=30
            )
            
            if response.status_code == 200:
                with open(file_path, 'wb') as f:
                    f.write(response.content)
                QMessageBox.information(self, 'Success', f'PDF report saved to:\n{file_path}')
            else:
                QMessageBox.warning(self, 'Error', 'Failed to generate PDF report')
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Failed to download PDF: {str(e)}')


def main():
    # Application entry point - creates and runs the PyQt5 app
    app = QApplication(sys.argv)
    
    # Create HTTP session for API communication
    session = requests.Session()
    api_url = "http://localhost:8000/api"
    
    # Hardcoded as admin (authentication removed for simplified access)
    main_window = MainWindow(session, api_url, "admin")
    main_window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

