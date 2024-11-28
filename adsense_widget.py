from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont, QKeyEvent
import sys
from adsense_data import AdSenseDataManager, DashboardData
from datetime import datetime

class AdSenseWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.data_manager = AdSenseDataManager()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.initUI()
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_data)
        self.timer.start(600000)  # 10분
        
        self.update_data()

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key_Escape or event.key() == Qt.Key_Q:
            self.close()
            QApplication.quit()

    def initUI(self):
        self.setFixedSize(400, 100)  # 높이를 늘림
        self.setStyleSheet("""
            QWidget {
                background-color: #0066CC;
                color: white;
                font-family: Arial;
            }
            QLabel {
                padding: 2px;
            }
        """)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(10, 5, 10, 5)
        main_layout.setSpacing(5)

        data_layout = QHBoxLayout()
        data_layout.setSpacing(15)

        self.columns = []
        titles = ["오늘 현재까지", "어제", "지난 7일", "이번 달"]
        for title in titles:
            column = self.create_column(title)
            data_layout.addLayout(column)
            self.columns.append(column)

        main_layout.addLayout(data_layout)

        # 업데이트 시간 표시 레이블
        self.update_time_label = QLabel()
        self.update_time_label.setFont(QFont("Arial", 8))
        self.update_time_label.setStyleSheet("color: rgba(255, 255, 255, 0.7);")
        self.update_time_label.setAlignment(Qt.AlignRight)
        main_layout.addWidget(self.update_time_label)

        self.setLayout(main_layout)

    def create_column(self, title):
        layout = QVBoxLayout()
        layout.setSpacing(2)
        
        title_label = QLabel(title)
        title_label.setFont(QFont("Arial", 8))
        title_label.setStyleSheet("color: rgba(255, 255, 255, 0.7);")
        
        amount_label = QLabel("US$0.00")
        amount_label.setFont(QFont("Arial", 12, QFont.Bold))
        
        comparison_label = QLabel("")
        comparison_label.setFont(QFont("Arial", 8))
        comparison_label.setStyleSheet("color: rgba(255, 255, 255, 0.7);")
        
        layout.addWidget(title_label)
        layout.addWidget(amount_label)
        layout.addWidget(comparison_label)
        
        return layout

    def update_data(self):
        data = self.data_manager.get_dashboard_data()
        
        earnings_data = [
            (data.today, True),
            (data.yesterday, True),
            (data.last_7_days, False),
            (data.this_month, True)
        ]
        
        for column, (earnings, has_comparison) in zip(self.columns, earnings_data):
            amount_label = column.itemAt(1).widget()
            amount_label.setText(f"US${earnings.amount:.2f}")
            
            comparison_label = column.itemAt(2).widget()
            if has_comparison and earnings.comparison:
                percentage = earnings.comparison.percentage
                if percentage is not None:
                    sign = "▲" if percentage > 0 else "▼"
                    comparison_label.setText(f"{sign} {abs(percentage):.1f}%")
                    color = "#00FF00" if percentage > 0 else "#FF4444"
                    comparison_label.setStyleSheet(f"color: {color}")
            else:
                comparison_label.setText("")

        # 업데이트 시간 갱신
        current_time = datetime.now().strftime("updated %Y-%m-%d %H:%M")
        self.update_time_label.setText(current_time)