from PySide6.QtWidgets import QApplication
from adsense_widget import AdSenseWidget
import sys

def main():
    app = QApplication(sys.argv)
    widget = AdSenseWidget()
    
    # 화면 우상단에 위젯 배치
    screen = app.primaryScreen().geometry()
    widget.move(screen.width() - widget.width() - 20, 20)
    
    widget.show()
    return app.exec()

if __name__ == '__main__':
    sys.exit(main())