import sys
import os
import logging
from datetime import datetime
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt
from adsense_widget import AdSenseWidget

def setup_logging():
    """로깅 설정"""
    # 실행 파일 위치에 로그 디렉토리 생성
    log_dir = 'logs'
    if getattr(sys, 'frozen', False):
        log_dir = os.path.join(os.path.dirname(sys.executable), 'logs')

    os.makedirs(log_dir, exist_ok=True)

    # 로그 파일명에 날짜/시간 포함
    log_file = os.path.join(log_dir, f'app_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log')

    # 로깅 설정
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s [%(levelname)s] %(message)s',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler(sys.stdout)  # 콘솔에도 출력
        ]
    )

    return logging.getLogger(__name__)

def resource_path(relative_path):
    """Get absolute path to resource for PyInstaller"""
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def main():
    # 로거 설정
    logger = setup_logging()
    logger.info("애플리케이션 시작")
    
    try:
        # QApplication 생성 전에 DLL 디렉토리 설정
        if getattr(sys, 'frozen', False):
            dll_dir = os.path.join(sys._MEIPASS, "PySide6", "plugins")
            if os.path.exists(dll_dir):
                os.environ["QT_PLUGIN_PATH"] = dll_dir
                logger.info(f"QT_PLUGIN_PATH 설정: {dll_dir}")
            else:
                logger.warning(f"DLL 디렉토리를 찾을 수 없음: {dll_dir}")

        # High DPI 지원 설정
        QApplication.setHighDpiScaleFactorRoundingPolicy(
            Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
        )

        logger.info("QApplication 초기화")
        app = QApplication(sys.argv)

        logger.info("AdSenseWidget 생성")
        widget = AdSenseWidget()

        # 화면 우상단에 위젯 배치
        screen = app.primaryScreen()
        screen_geometry = screen.availableGeometry()

        x = min(screen_geometry.width() - widget.width() - 20, screen_geometry.width() - 20)
        y = max(20, screen_geometry.top() + 20)

        widget.move(x, y)
        logger.info(f"위젯 위치 설정: x={x}, y={y}")

        # 항상 위에 표시
        widget.setWindowFlags(widget.windowFlags() | Qt.WindowStaysOnTopHint)

        widget.show()
        logger.info("위젯 표시")

        return app.exec()

    except Exception as e:
        logger.exception("애플리케이션 실행 중 오류 발생")
        raise

if __name__ == '__main__':
    try:
        sys.exit(main())
    except Exception as e:
        logging.error(f"치명적 오류 발생: {str(e)}")
        sys.exit(1)