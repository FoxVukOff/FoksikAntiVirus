import os
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog, QTextBrowser, QProgressBar, QMessageBox, QLabel
from PyQt5.QtCore import Qt

class AntivirusApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Простой антивирус")
        self.setGeometry(100, 100, 500, 400)

        self.scan_button = QPushButton("Сканировать", self)
        self.scan_button.setGeometry(50, 50, 150, 50)
        self.scan_button.clicked.connect(self.scan_directory)

        self.result_browser = QTextBrowser(self)
        self.result_browser.setGeometry(50, 120, 400, 150)

        self.progress_bar = QProgressBar(self)
        self.progress_bar.setGeometry(50, 300, 400, 30)

        self.status_label = QLabel("Готов к сканированию", self)
        self.status_label.setGeometry(50, 350, 400, 20)

    def load_databases(self):
        self.good_programs = set()
        self.bad_programs = set()

        try:
            with open("databases/notevil.txt", "r") as file:
                self.good_programs.update(file.read().splitlines())
        except FileNotFoundError:
            QMessageBox.critical(self, "Ошибка", "Файл notevil.txt не найден.")
        
        try:
            with open("databases/evil.txt", "r") as file:
                self.bad_programs.update(file.read().splitlines())
                print("Содержимое файла evil.txt:", self.bad_programs)
        except FileNotFoundError:
            QMessageBox.critical(self, "Ошибка", "Файл evil.txt не найден.")

    def scan_directory(self):
        self.load_databases()
        directory = QFileDialog.getExistingDirectory(self, "Выберите директорию для сканирования")
        if directory:
            self.scan_button.setEnabled(False)
            self.result_browser.clear()
            self.progress_bar.setValue(0)
            self.progress_bar.setMaximum(0)
            self.status_label.setText("Загрузка...")
            self.scan_directory_helper(directory)
            self.ask_reload()

    def scan_directory_helper(self, directory):
        suspicious_files = []
        total_files = sum(len(files) for _, _, files in os.walk(directory))
        self.progress_bar.setMaximum(total_files)
        scanned_files = 0

        for root, dirs, files in os.walk(directory):
            for file in files:
                full_path = os.path.join(root, file)
                if full_path.lower() in self.bad_programs:
                    suspicious_files.append(full_path)
                scanned_files += 1
                progress_percent = int((scanned_files / total_files) * 100)
                self.progress_bar.setValue(scanned_files)
                self.status_label.setText(f"Сканирование... {progress_percent}% завершено")
                QApplication.processEvents()

        self.scan_button.setEnabled(True)
        self.progress_bar.setValue(total_files)
        self.status_label.setText("Сканирование завершено")
        
        if suspicious_files:
            self.result_browser.append("Обнаружены подозрительные файлы:")
            for file in suspicious_files:
                self.result_browser.append(file)
        else:
            self.result_browser.append("Подозрительных файлов не обнаружено.")

    def ask_reload(self):
        reply = QMessageBox.question(self, 'Перезагрузка', 'Желаете ли перезагрузить компьютер?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            os.system("shutdown /r /t 1")
            QApplication.quit()

def main():
    app = QApplication(sys.argv)
    window = AntivirusApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
