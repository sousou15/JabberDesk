import sys
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox, QHBoxLayout, QSizePolicy
from main_window import MainWindow  # Importa la clase MainWindow
from register_window import RegisterWindow  # Importa la clase RegisterWindow

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Login')
        self.setGeometry(200, 200, 300, 150)

        self.setStyleSheet(open('login_styles.css').read())  # Aplica estilos desde archivo CSS

        self.username_input = QLineEdit(self)
        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.Password)

        # Conectar la señal returnPressed a handle_login para ambos QLineEdit
        self.username_input.returnPressed.connect(self.handle_login)
        self.password_input.returnPressed.connect(self.handle_login)

        self.login_button = QPushButton('Login', self)
        self.login_button.clicked.connect(self.handle_login)

        self.register_label = QLabel('Don\'t have an account yet? ', self)
        self.register_link = QLabel('<a href="register">Register</a>', self)
        self.register_link.setOpenExternalLinks(True)
        self.register_link.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.register_link.linkActivated.connect(self.open_register_window)  # Conectar evento de clic del enlace

        # Layout para organizar los widgets verticalmente
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel('Username:', self))
        layout.addWidget(self.username_input)
        layout.addWidget(QLabel('Password:', self))
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_button)

        # Layout horizontal para alinear el botón de registro con el botón de inicio de sesión
        register_layout = QHBoxLayout()
        register_layout.addWidget(self.register_label)
        register_layout.addWidget(self.register_link)
        layout.addLayout(register_layout)

    def handle_login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        # Enviar solicitud POST al endpoint de login en Flask
        url = 'http://localhost:5000/api/login'
        data = {'username': username, 'password': password}
        response = requests.post(url, json=data)

        if response.status_code == 200:
            QMessageBox.information(self, 'Login Successful', 'Login successful.')
            self.open_main_window(username)  # Abre la ventana principal con el nombre de usuario
        else:
            QMessageBox.warning(self, 'Login Failed', 'Incorrect username or password.')

    def open_main_window(self, username):
        self.main_window = MainWindow(username)  # Crea MainWindow con el nombre de usuario
        self.main_window.show()

    def open_register_window(self, url):
        self.register_window = RegisterWindow()  # Crea la ventana de registro
        self.register_window.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    login_window = LoginWindow()
    login_window.show()
    sys.exit(app.exec_())
