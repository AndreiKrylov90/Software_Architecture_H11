import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem
from PyQt5.QtCore import Qt
import sqlite3
from PyQt5.QtWidgets import QInputDialog


class Repository:
    def __init__(self):
        self.conn = sqlite3.connect('vet_clinic.db')
        self.create_tables()

    def create_tables(self):
        # Создание таблиц, если они не существуют
        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS Clients(
                    ClientId INTEGER PRIMARY KEY,
                    Document TEXT,
                    SurName TEXT,
                    FirstName TEXT,
                    Patronymic TEXT,
                    Birthday INTEGER
                )
            ''')
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS Pets(
                    PetId INTEGER PRIMARY KEY,
                    ClientId INTEGER,
                    Name TEXT,
                    Birthday INTEGER
                )
            ''')
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS Consultations(
                    ConsultationId INTEGER PRIMARY KEY,
                    ClientId INTEGER,
                    PetId INTEGER,
                    ConsultationDate INTEGER,
                    Description TEXT
                )
            ''')

    def add_client(self, document, surname, firstname, patronymic, birthday):
        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute('''
                INSERT INTO Clients (Document, SurName, FirstName, Patronymic, Birthday)
                VALUES (?, ?, ?, ?, ?)
            ''', (document, surname, firstname, patronymic, birthday))

    def get_clients(self):
        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute('SELECT * FROM Clients')
            return cursor.fetchall()

    def remove_client(self, client_id):
        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute('DELETE FROM Clients WHERE ClientId = ?', (client_id,))


class VetClinicApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.repository = Repository()

        self.init_ui()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()

        label = QLabel("Vet Clinic App")
        layout.addWidget(label)

        add_client_button = QPushButton("Add Client")
        add_client_button.clicked.connect(self.show_add_client_dialog)
        layout.addWidget(add_client_button)

        remove_client_button = QPushButton("Remove Client")
        remove_client_button.clicked.connect(self.remove_client)
        layout.addWidget(remove_client_button)

        clients_table_label = QLabel("Clients:")
        layout.addWidget(clients_table_label)

        self.clients_table = QTableWidget(self)
        self.clients_table.setColumnCount(6)
        self.clients_table.setHorizontalHeaderLabels(["ClientId", "Document", "Surname", "Firstname", "Patronymic", "Birthday"])
        layout.addWidget(self.clients_table)

        central_widget.setLayout(layout)

        self.update_clients_table()

        self.setWindowTitle("Vet Clinic App")
        self.setGeometry(100, 100, 800, 600)

    def add_client(self):
        # Добавление нового клиента
        # Вы можете расширить этот метод для добавления остальных данных
        self.repository.add_client("123456789", "Doe", "John", "Smith", "19900101")
        self.update_clients_table()

    def update_clients_table(self):
        # Обновление таблицы клиентов
        clients = self.repository.get_clients()
        self.clients_table.setRowCount(len(clients))
        for row, client in enumerate(clients):
            for col, value in enumerate(client):
                item = QTableWidgetItem(str(value))
                item.setFlags(item.flags() ^ Qt.ItemIsEditable)
                self.clients_table.setItem(row, col, item)

    def remove_client(self):
        selected_row = self.clients_table.currentRow()
        if selected_row >= 0:
            client_id_item = self.clients_table.item(selected_row, 0)
            client_id = int(client_id_item.text())
            # Вызываем метод удаления клиента из репозитория
            self.repository.remove_client(client_id)
            self.update_clients_table()

    def show_add_client_dialog(self):
        document, ok = QInputDialog.getText(self, 'Add Client', 'Enter Document:')
        if ok:
            surname, ok = QInputDialog.getText(self, 'Add Client', 'Enter Surname:')
            if ok:
                firstname, ok = QInputDialog.getText(self, 'Add Client', 'Enter Firstname:')
                if ok:
                    patronymic, ok = QInputDialog.getText(self, 'Add Client', 'Enter Patronymic:')
                    if ok:
                        birthday, ok = QInputDialog.getText(self, 'Add Client', 'Enter Birthday (YYYYMMDD):')
                        if ok and birthday.isdigit() and len(birthday) == 8:
                            # Вызываем метод добавления клиента в репозиторий
                            self.repository.add_client(document, surname, firstname, patronymic, birthday)
                            self.update_clients_table()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = VetClinicApp()
    window.show()
    sys.exit(app.exec_())
