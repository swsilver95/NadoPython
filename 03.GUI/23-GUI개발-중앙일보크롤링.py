from PyQt5.QtCore import QObject, QThread, pyqtSignal
from PyQt5.QtWidgets import *
import sys
from PyQt5 import uic
from bs4 import BeautifulSoup
import urllib.request as req
import urllib.parse as par

ui_file = "./joongang.ui"


class CrawlingWorker(QObject):

    crawling_result_signal = pyqtSignal(str)
    info_signal = pyqtSignal(str)
    finish_signal = pyqtSignal()

    def __init__(self):
        QObject.__init__(self, None)

    def crawling(self, keyword):
        # -----------------------------------
        # 크롤링 시작
        # -----------------------------------
        encoded = par.quote(keyword)  # 한글 -> 특수한 문자
        page_num = 1
        page_limit = 2
        crawling_num = 0
        while page_num <= page_limit:
            url = f"https://www.joongang.co.kr/_CP/496?keyword={encoded}&sort%20=&pageItemId=439&page={page_num}"
            code = req.urlopen(url)
            soup = BeautifulSoup(code, "html.parser")
            title = soup.select("h2.headline a")
            if len(title) == 0:  # 끝 페이지까지 크롤링 완료했으면?
                self.finish_signal.emit()
                break
            for i in title:
                self.crawling_result_signal.emit(f"제목 : {i.text.strip()}")
                self.crawling_result_signal.emit(f'링크 : {i.attrs["href"]}')
                code_news = req.urlopen(i.attrs["href"])
                soup_news = BeautifulSoup(code_news, "html.parser")
                content = soup_news.select_one("div#article_body")
                result = content.text.replace("\n", " ").strip()
                self.crawling_result_signal.emit(result + "\n")
                crawling_num += 1
                self.info_signal.emit(f"현재 수집 개수 : {crawling_num}개")
            page_num += 1
        # -----------------------------------
        # 크롤링 종료
        # -----------------------------------


class MainDialog(QDialog):
    
    # 시그널 객체 정의
    # 클래스 객체로 정의해야 정상 동작
    crawling_signal = pyqtSignal(str)

    def __init__(self):
        QDialog.__init__(self, None)
        uic.loadUi(ui_file, self)
        # -----------------------------------
        # 스레드 할당받기
        # -----------------------------------
        self.crawling_worker = CrawlingWorker()
        self.thread = QThread()
        self.crawling_worker.moveToThread(self.thread)
        self.thread.start()
        # -----------------------------------
        # 스레드 할당 완료
        # -----------------------------------
        
        # 연결관계 설정
        # 연결관계는 무조건 메인 다이얼로그에만 설정 가능
        self.searchButton.clicked.connect(self.crawling_start)
        self.crawling_signal.connect(self.crawling_worker.crawling)
        self.crawling_worker.crawling_result_signal.connect(self.outputBox.append)
        self.crawling_worker.info_signal.connect(self.info.setText)
        self.crawling_worker.finish_signal.connect(self.finish_crawling)

    def crawling_start(self):
        self.searchButton.setEnabled(False)
        keyword = self.inputBox.text()
        self.inputBox.clear()
        self.crawling_signal.emit(keyword)

    def finish_crawling(self):
        self.searchButton.setEnabled(True)
        msg = QMessageBox()
        msg.setWindowTitle("안내")
        msg.setText("크롤링이 완료되었습니다.")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()



QApplication.setStyle("fusion")
app = QApplication(sys.argv)
main_dialog = MainDialog()
main_dialog.show()
sys.exit(app.exec_())