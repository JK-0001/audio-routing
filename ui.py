import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout,
                             QPushButton, QComboBox, QMessageBox)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from app import list_sink_inputs, list_sinks, move_sink_input_to_sink

class AudioRouterApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Modern Audio Router")
        self.setGeometry(100, 100, 600, 400)
        self.setStyleSheet("background-color: #2E3440; color: #ECEFF4;")
        
        self.sink_inputs_map = {}  # Store sink input IDs and names
        self.sinks_map = {}  # Store sink IDs and descriptions
        self.initUI()

    def initUI(self):
        # Layout setup
        layout = QVBoxLayout()
        layout.setSpacing(20)

        # Title Label
        title = QLabel("Audio Router")
        title.setFont(QFont("Arial", 18, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #88C0D0;")
        layout.addWidget(title)

        # Dropdown for Sink Inputs (Audio Streams)
        self.sink_input_dropdown = QComboBox(self)
        self.sink_input_dropdown.setStyleSheet(self.combo_box_style())
        layout.addWidget(self.create_label_dropdown("Select Application (Sink Input):", self.sink_input_dropdown))

        # Dropdown for Sinks (Audio Output Devices)
        self.sink_dropdown = QComboBox(self)
        self.sink_dropdown.setStyleSheet(self.combo_box_style())
        layout.addWidget(self.create_label_dropdown("Select Audio Output (Sink):", self.sink_dropdown))

        # Action Buttons
        btn_layout = QHBoxLayout()

        update_btn = QPushButton("Update Lists")
        update_btn.setStyleSheet(self.button_style())
        update_btn.clicked.connect(self.update_lists)
        btn_layout.addWidget(update_btn)

        move_audio_btn = QPushButton("Move Audio")
        move_audio_btn.setStyleSheet(self.button_style())
        move_audio_btn.clicked.connect(self.move_audio)
        btn_layout.addWidget(move_audio_btn)

        layout.addLayout(btn_layout)

        # Set main layout
        self.setLayout(layout)

    def create_label_dropdown(self, label_text, dropdown):
        """ Helper method to create a label and dropdown layout. """
        container = QWidget()
        layout = QVBoxLayout()
        
        label = QLabel(label_text)
        label.setFont(QFont("Arial", 14))
        layout.addWidget(label)
        layout.addWidget(dropdown)

        container.setLayout(layout)
        return container

    def combo_box_style(self):
        return """
        QComboBox {
            padding: 5px;
            border-radius: 5px;
            border: 2px solid #88C0D0;
            background-color: #4C566A;
            color: #ECEFF4;
        }
        QComboBox::drop-down {
            subcontrol-origin: padding;
            subcontrol-position: top right;
            width: 30px;
            border-left-width: 1px;
            border-left-color: #88C0D0;
            border-left-style: solid;
            border-top-right-radius: 5px;
            border-bottom-right-radius: 5px;
        }
        """

    def button_style(self):
        return """
        QPushButton {
            background-color: #5E81AC;
            color: #ECEFF4;
            padding: 10px;
            font-size: 14px;
            border-radius: 5px;
        }
        QPushButton:hover {
            background-color: #81A1C1;
        }
        """

    def update_lists(self):
        # Update available audio streams (sink inputs)
        self.sink_input_dropdown.clear()
        sink_inputs = list_sink_inputs()

        self.sink_inputs_map = sink_inputs  # Save the sink input ID to app name mapping
        self.sink_input_dropdown.addItems(sink_inputs.values())  # Show only app names in the dropdown

        # Update available audio output devices (sinks)
        self.sink_dropdown.clear()
        sinks = list_sinks()

        self.sinks_map = sinks  # Save the sink ID to sink description mapping
        self.sink_dropdown.addItems(sinks.values())  # Show only sink descriptions in the dropdown

        QMessageBox.information(self, "Updated", "Lists have been updated!")

    def move_audio(self):
        # Get the selected app name and sink description
        selected_app_name = self.sink_input_dropdown.currentText()
        selected_sink_name = self.sink_dropdown.currentText()

        # Get the corresponding IDs for the selected names
        sink_input_id = next(key for key, value in self.sink_inputs_map.items() if value == selected_app_name)
        sink_id = next(key for key, value in self.sinks_map.items() if value == selected_sink_name)

        if not sink_input_id or not sink_id:
            QMessageBox.warning(self, "Error", "Please select valid Sink Input and Sink")
            return

        move_sink_input_to_sink(sink_input_id, sink_id)
        QMessageBox.information(self, "Success", "Audio moved successfully!")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AudioRouterApp()
    window.show()
    sys.exit(app.exec_())
