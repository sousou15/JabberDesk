import sys
import requests
from PyQt5.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget, QLineEdit, QPushButton, QApplication, QStackedWidget

class MainWindow(QMainWindow):
    def __init__(self, username):
        super().__init__()
        self.setWindowTitle('Main Window')
        self.setGeometry(300, 300, 400, 200)

        # QStackedWidget para alternar entre visualización y edición
        self.stacked_widget = QStackedWidget(self)
        self.setCentralWidget(self.stacked_widget)

        # Widget para visualización de perfil
        self.profile_widget = QWidget()
        self.stacked_widget.addWidget(self.profile_widget)

        self.setup_profile_view(username)
        self.setup_edit_mode()

    def setup_profile_view(self, username):
        # Obtener datos del perfil del usuario desde la API
        profile_data = self.get_user_profile(username)
        
        # Mostrar los datos del perfil del usuario
        if profile_data:
            self.username_label = QLabel(f'<h1>{profile_data["username"]}</h1>')
            self.email_label = QLabel(f'Email: {profile_data["email"]}')
            self.location_label = QLabel(f'Location: {profile_data["location"]}')
            self.languages_label = QLabel(f'Languages: {profile_data["languages"]}')

            layout = QVBoxLayout(self.profile_widget)
            layout.addWidget(self.username_label)
            layout.addWidget(self.email_label)
            layout.addWidget(self.location_label)
            layout.addWidget(self.languages_label)
            layout.addStretch()

            # Botón para activar el modo de edición
            edit_button = QPushButton('Edit Profile', self.profile_widget)
            edit_button.clicked.connect(self.enable_edit_mode)
            layout.addWidget(edit_button)

    def setup_edit_mode(self):
        # Crear widgets para el modo de edición
        self.email_text = QLineEdit()
        self.location_text = QLineEdit()
        self.languages_text = QLineEdit()

        # Crear layout para el modo de edición
        edit_layout = QVBoxLayout()
        edit_layout.addWidget(QLabel('Email:'))
        edit_layout.addWidget(self.email_text)
        edit_layout.addWidget(QLabel('Location:'))
        edit_layout.addWidget(self.location_text)
        edit_layout.addWidget(QLabel('Languages:'))
        edit_layout.addWidget(self.languages_text)

        edit_widget = QWidget()
        edit_widget.setLayout(edit_layout)
        self.stacked_widget.addWidget(edit_widget)

        # Botón para guardar cambios en el perfil
        save_button = QPushButton('Save', edit_widget)
        save_button.clicked.connect(self.save_profile_changes)
        edit_layout.addWidget(save_button)

    def enable_edit_mode(self):
        self.stacked_widget.setCurrentIndex(1)  # Cambiar al widget de edición

        # Prellenar los campos de edición con los datos actuales
        self.email_text.setText(self.email_label.text().split(': ')[1])
        self.location_text.setText(self.location_label.text().split(': ')[1])
        self.languages_text.setText(self.languages_label.text().split(': ')[1])

    def save_profile_changes(self):
        # Obtener el nombre de usuario actual
        username = self.username_label.text().strip('<h1>').strip('</h1>')

        # Obtener los nuevos valores desde los campos de texto de edición
        new_email = self.email_text.text()
        new_location = self.location_text.text()
        new_languages = self.languages_text.text()

        # Construir los datos a enviar al backend
        data = {
            'email': new_email,
            'location': new_location,
            'languages': new_languages
        }

        # Realizar la solicitud POST al endpoint de actualización de perfil
        url = f'http://localhost:5000/api/profile/{username}'
        try:
            response = requests.post(url, json=data)
            if response.status_code == 200:
                # Actualizar los labels con los nuevos datos
                self.email_label.setText(f'Email: {new_email}')
                self.location_label.setText(f'Location: {new_location}')
                self.languages_label.setText(f'Languages: {new_languages}')

                # Cambiar de vuelta al widget de visualización después de guardar
                self.stacked_widget.setCurrentIndex(0)
            else:
                print(f'Error: Failed to update profile - {response.status_code}')
        except requests.exceptions.RequestException as e:
            print(f'Error: {e}')
            
    def get_user_profile(self, username):
        # Función para obtener datos del perfil del usuario desde la API
        url = f'http://localhost:5000/api/profile/{username}'
        try:
            response = requests.get(url)
            if response.status_code == 200:
                return response.json()
            else:
                print(f'Error: Failed to fetch user profile - {response.status_code}')
                return None
        except requests.exceptions.RequestException as e:
            print(f'Error: {e}')
            return None
