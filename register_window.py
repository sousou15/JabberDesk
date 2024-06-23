import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox, QSizePolicy

class RegisterWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Register')
        self.setGeometry(200, 200, 300, 200)  # Ajusta las dimensiones según tus necesidades
        self.setStyleSheet(open('login_styles.css').read())  # Aplica estilos desde archivo CSS

        self.username_input = QLineEdit(self)
        self.email_input = QLineEdit(self)
        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.Password)

        # Conectar la señal returnPressed a handle_register para todos los QLineEdit
        self.username_input.returnPressed.connect(self.handle_register)
        self.email_input.returnPressed.connect(self.handle_register)
        self.password_input.returnPressed.connect(self.handle_register)

        self.register_button = QPushButton('Register', self)
        self.register_button.clicked.connect(self.handle_register)

        # Layout para organizar los widgets verticalmente
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel('Username:', self))
        layout.addWidget(self.username_input)
        layout.addWidget(QLabel('Email:', self))
        layout.addWidget(self.email_input)
        layout.addWidget(QLabel('Password:', self))
        layout.addWidget(self.password_input)
        layout.addWidget(self.register_button)

    def handle_register(self):
        # Implementación de handle_register aquí
        # Aquí puedes realizar la lógica para registrar al usuario
        # Por ahora, simplemente mostramos un mensaje de registro exitoso
        QMessageBox.information(self, 'Registration Successful', 'Registration successful.')
        self.close()  # Cerrar la ventana de registro después de registrar al usuario

if __name__ == '__main__':
    app = QApplication(sys.argv)
    register_window = RegisterWindow()
    register_window.show()

    # También abrimos la ventana de login al presionar "Intro"
    def handle_return_pressed():
        login_window = LoginWindow()
        login_window.show()
        register_window.close()

    register_window.username_input.returnPressed.connect(handle_return_pressed)
    register_window.email_input.returnPressed.connect(handle_return_pressed)
    register_window.password_input.returnPressed.connect(handle_return_pressed)

    sys.exit(app.exec_())
