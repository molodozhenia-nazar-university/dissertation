import os

from PyQt6.QtWidgets import (
    QWidget,
    QFrame,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QTextEdit,
    QPushButton,
    QStackedWidget,
    QFileDialog,
    QGroupBox,
    QComboBox,
    QSpinBox,
    QProgressBar,  # need use
)
from PyQt6.QtCore import Qt, QTimer


from ui.windows.traffic_analysis_information_window import (
    TrafficAnalysisInformationWindow,
)

from core.wavelet_analysis import wavelet_analysis
from core.capture import get_interfaces
from core.capture import start_capture


def create_traffic_analysis_tab(main_window):

    traffic_analysis_widget = QWidget()
    traffic_analysis_layout = QVBoxLayout(traffic_analysis_widget)

    traffic_analysis_title = QLabel("Аналіз мережевого трафіку")
    traffic_analysis_title.setObjectName("traffic_analysis_title")
    traffic_analysis_title.setAlignment(Qt.AlignmentFlag.AlignCenter)

    buttons_container = QFrame()
    buttons_layout = QVBoxLayout(buttons_container)
    buttons_layout.setSpacing(30)
    buttons_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

    # Button Open File for Analysis
    button_open_file = QPushButton("📁 Аналіз файлу трафіку мережі")
    button_open_file.setObjectName("button_open_file")
    button_open_file.clicked.connect(lambda: show_analysis_interface("file"))

    # Button Live Analysis
    button_live_analysis = QPushButton(
        "🌐 Аналіз трафіку мережі в режимі реального часу"
    )
    button_live_analysis.setObjectName("button_live_analysis")
    button_live_analysis.clicked.connect(lambda: show_analysis_interface("live"))

    # Add objects to a buttons layout
    buttons_layout.addWidget(button_open_file)
    buttons_layout.addWidget(button_live_analysis)

    # STACKED WIDGET FOR DIFFERENT INTERFACES
    traffic_analysis_stacked_widget = QStackedWidget()

    # STRETCH
    stretch_page = QWidget()
    stretch_layout = QVBoxLayout(stretch_page)
    stretch_layout.addStretch()

    # Add STRETCH to STACKED and set index for STRETCH
    traffic_analysis_stacked_widget.insertWidget(0, stretch_page)
    traffic_analysis_stacked_widget.setCurrentIndex(0)

    # => Open File Interface
    file_analysis_widget = create_file_analysis_interface(main_window)
    traffic_analysis_stacked_widget.addWidget(file_analysis_widget)

    # => Live Analysis Interface
    live_analysis_widget = create_live_analysis_interface(main_window)
    traffic_analysis_stacked_widget.addWidget(live_analysis_widget)

    # BUTTON BACK
    button_back = QPushButton("Назад")
    button_back.setObjectName("button_back")
    button_back.clicked.connect(
        lambda: traffic_analysis_stacked_widget.setCurrentIndex(0)
    )

    # BUTTON BACK - status HIDE
    button_back.hide()

    # Add objects to a traffic analysis layout
    traffic_analysis_layout.addWidget(traffic_analysis_title)
    traffic_analysis_layout.addWidget(buttons_container)
    traffic_analysis_layout.addWidget(button_back)
    traffic_analysis_layout.addWidget(traffic_analysis_stacked_widget)

    def show_analysis_interface(type_analysis):
        if type_analysis == "file":
            traffic_analysis_stacked_widget.setCurrentIndex(1)
        elif type_analysis == "live":
            traffic_analysis_stacked_widget.setCurrentIndex(2)

        # BUTTON BACK - status SHOW
        button_back.show()
        # BUTTONS CONTAINER - status HIDE
        buttons_container.hide()

    def back_to_choice():
        traffic_analysis_stacked_widget.setCurrentIndex(0)
        # BUTTON BACK - status HIDE
        button_back.hide()
        # BUTTONS CONTAINER - status SHOW
        buttons_container.show()

    # BUTTON BACK - function
    button_back.clicked.connect(back_to_choice)

    main_window.stacked_widget.addWidget(traffic_analysis_widget)

    return traffic_analysis_widget


def create_file_analysis_interface(main_window):

    # VARIABLE
    selected_file_path = ""

    interface_widget = QWidget()
    interface_layout = QVBoxLayout(interface_widget)

    # FILE
    file_widget = QWidget()
    file_layout = QHBoxLayout(file_widget)

    button_browse = QPushButton("📂 Обрати файл")
    button_browse.setObjectName("button_browse")
    file_layout.addWidget(button_browse)

    file_label = QLabel("Файл не обрано")
    file_label.setObjectName("file_label")
    file_layout.addWidget(file_label)

    # Button Control Analysis
    control_widget = QWidget()
    control_layout = QHBoxLayout(control_widget)

    button_control = QPushButton("🔍 Почати аналіз")
    button_control.setObjectName("button_control")
    control_layout.addWidget(button_control)

    # RESULT
    result_text = QTextEdit()
    result_text.setPlaceholderText("Тут будуть результати аналізу...")

    # ASSEMBLE FILE ANALYSIS INTERFACE
    interface_layout.addWidget(file_widget)
    interface_layout.addWidget(control_widget)
    interface_layout.addWidget(result_text)

    # Button Information
    button_information = QPushButton("📄 Додаткова інформація")
    interface_layout.addWidget(button_information)

    def open_traffic_analysis_information_window(main_window):
        if main_window.traffic_analysis_information.isVisible():
            return
        else:
            main_window.traffic_analysis_information.show()
            main_window.traffic_analysis_information.raise_()

    button_information.clicked.connect(
        lambda: open_traffic_analysis_information_window(main_window)
    )

    button_information.setEnabled(False)

    # METHODS

    def browse_file():
        nonlocal selected_file_path
        file_path, _ = QFileDialog.getOpenFileName(
            None,
            "Оберіть файл трафіку мережі",
            "D:\\",
            "Файли трафіку (*.cap *.pcap *.pcapng);;Усі файли (*)",
        )
        if file_path:
            selected_file_path = file_path
            file_label.setText(os.path.basename(file_path))
            button_information.setEnabled(False)

    def analyze_file():
        if not selected_file_path:
            result_text.setText("❌ Будь ласка, оберіть файл для аналізу")
            return

        button_control.setEnabled(False)
        result_text.setText("⏳ Виконується вейвлет-аналіз...")

        complete_analysis()

    # NEED CHANGE
    def complete_analysis():

        # MAYBE NEED OTHER PLACE
        button_control.setEnabled(True)

        # RESULTS
        results = wavelet_analysis(selected_file_path, "db4", 6)

        if "error" in results:
            result_text.setText(f"❌ Помилка: {results['error']}")
            return

        # Форматування результатів
        result_string = f"""✅ Аналіз завершено!

📊 ЗАГАЛЬНА СТАТИСТИКА:
• Пакетів проаналізовано: {results['summary']['total_packets']}
• Тривалість аналізу: {results['summary']['analysis_duration']}
• Вейвлет: {results['summary']['wavelet_type']} (рівень {results['summary']['wavelet_level']})

🚨 ВИЯВЛЕНІ АНОМАЛІЇ:
• Спайків трафіку: {results['detected_anomalies']['volume_anomalies']}
• Аномалій пакетів: {results['detected_anomalies']['packet_anomalies']} 
• Протокольних аномалій: {results['detected_anomalies']['protocol_anomalies']}
• Змін тренду: {results['detected_anomalies']['trend_changes']}

📈 РОЗПОДІЛ ПРОТОКОЛІВ:
"""

        for protocol, count in results["protocol_distribution"].items():
            result_string += f"• {protocol}: {count} пакетів\n"

        result_string += "💡 РЕКОМЕНДАЦІЇ:\n"
        for recommendation in results["recommendations"]:
            result_string += f"• {recommendation}\n"

        result_text.setText(result_string)

        # TRAFFIC ANALYSIS INFORMATION
        main_window.traffic_analysis_information = TrafficAnalysisInformationWindow(
            selected_file_path
        )

        button_information.setEnabled(True)

    button_browse.clicked.connect(browse_file)
    button_control.clicked.connect(analyze_file)

    return interface_widget


def create_live_analysis_interface(main_window):

    # VARIABLE
    timer = QTimer()
    is_monitoring = False

    interface_widget = QWidget()
    interface_layout = QVBoxLayout(interface_widget)

    # SETTINGS MONITORING
    settings_group = QGroupBox("Налаштування моніторингу")
    settings_layout = QVBoxLayout(settings_group)

    # Network interface
    network_interface_layout = QHBoxLayout()

    network_interface_label = QLabel("Мережевий інтерфейс:")
    network_interface_layout.addWidget(network_interface_label)

    network_interface_combo = QComboBox()

    dictionary_network_interfaces = get_interfaces()
    network_interface_combo.addItems(dictionary_network_interfaces.keys())
    """
    network_interfaces = get_interfaces()
    network_interface_combo.addItems(network_interfaces)
    """
    network_interface_layout.addWidget(network_interface_combo)

    network_interface_layout.addStretch()

    # Capture duration
    duration_layout = QHBoxLayout()

    duration_label = QLabel("Тривалість захоплення трафіку мережі:")
    duration_layout.addWidget(duration_label)

    duration_spin = QSpinBox()

    duration_spin.setRange(30, 600)
    duration_spin.setValue(30)

    duration_spin.setSuffix(" сек")

    duration_layout.addWidget(duration_spin)

    duration_layout.addStretch()

    # Size buffer
    buffer_layout = QHBoxLayout()

    buffer_label = QLabel("Розмір буфера:")
    buffer_layout.addWidget(buffer_label)

    buffer_spin = QSpinBox()

    buffer_spin.setRange(1, 100)
    buffer_spin.setValue(50)

    buffer_spin.setSuffix(" МБ")

    buffer_layout.addWidget(buffer_spin)

    buffer_layout.addStretch()

    # Add objects to a settings layout
    settings_layout.addLayout(network_interface_layout)
    settings_layout.addLayout(duration_layout)
    settings_layout.addLayout(buffer_layout)

    # Button Control Monitoring

    control_layout = QHBoxLayout()
    button_control_start = QPushButton("▶️ Почати моніторинг")
    button_control_stop = QPushButton("⏹️ Зупинити моніторинг")
    button_control_stop.setEnabled(False)

    control_layout.addWidget(button_control_start)
    control_layout.addWidget(button_control_stop)

    control_layout.addStretch()

    # RESULT
    result_group = QGroupBox("Результати моніторингу в реальному часі")
    result_layout = QVBoxLayout(result_group)

    result_text = QTextEdit()
    result_text.setReadOnly(True)
    result_text.setPlaceholderText("Статус моніторингу: не активний")

    result_layout.addWidget(result_text)

    # Add objects to a interface layout
    interface_layout.addWidget(settings_group)
    interface_layout.addLayout(control_layout)
    interface_layout.addWidget(result_group)
    interface_layout.addStretch()

    # METHODS

    def update_status_result(text):
        result_text.append(text)

    def start_monitoring():

        nonlocal is_monitoring
        is_monitoring = True
        button_control_start.setEnabled(False)
        button_control_stop.setEnabled(True)

        # Change result
        result_text.clear()
        update_status_result("🟢 Моніторинг активний...\n")

        # Folder for save file
        os.makedirs("live_traffic", exist_ok=True)
        output_path = os.path.join("live_traffic", "live_traffic.pcap")

        # Interface for monitoring
        display_name_interface = network_interface_combo.currentText()
        system_name_interface = dictionary_network_interfaces[display_name_interface]

        # Duration for monitoring
        duration = duration_spin.value()

        # Change result
        update_status_result(f"📡 Захоплення трафіку з {display_name_interface}")
        update_status_result(f"🕒 Тривалість: {duration} сек")

        # CAPTURE
        start_capture(
            system_name_interface,
            duration,
            output_path,
            update_status_result,
        )

        # STOP TIME
        timer.singleShot(duration * 1000, stop_monitoring)

    def stop_monitoring():

        nonlocal is_monitoring

        if not is_monitoring:
            return

        is_monitoring = False
        button_control_start.setEnabled(True)
        button_control_stop.setEnabled(False)

        update_status_result("\n🔴 Моніторинг завершено.")
        update_status_result(
            f"📁 Результат збережено у: live_traffic/live_traffic.pcap"
        )

    button_control_start.clicked.connect(start_monitoring)
    button_control_stop.clicked.connect(stop_monitoring)

    return interface_widget
