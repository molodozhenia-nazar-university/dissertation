TRAFFIC_ANALYSIS_STYLES = """

    QLabel#traffic_analysis_title {
        padding: 40px 20px 20px 20px;
        font-size: 32px;
        font-weight: bold;
        color: #2c3e50;
    }

    QPushButton#button_open_file,
    QPushButton#button_live_analysis {
        width: 750px;
        padding: 25px 30px;
        font-size: 24px;
        font-weight: bold;
        color: #ffffff;
        border: none;
        border-radius: 10px;
    }

    QPushButton#button_open_file {
        background-color: #3498db;
    }

    QPushButton#button_live_analysis {
        background-color: #27ae60;
    }

    QPushButton#button_open_file:hover {
        background-color: #2980b9;
    }

    QPushButton#button_live_analysis:hover {
        background-color: #219653;
    }

    QPushButton#button_back {
        min-width: 250px;
        padding: 10px 15px;
        font-size: 20px;
        font-weight: bold;
        color: #ffffff;
        border: none;
        border-radius: 5px;
        background-color: #3498db;
    }

"""

TRAFFIC_ANALYSIS_ADD_STYLES = """

    QWidget#interface_widget_file {
        background-color: transparent;
    }

    QWidget#file_widget {
        padding: 5px 10px;
        background-color: #ecf0f1;
        border: 1px solid #d0d3d4;
        border-radius: 5px;
    }

    QPushButton#button_browse {
        padding: 5px 10px;
        background-color: #ffffff;
        border: 1px solid #bdc3c7;
        border-radius: 5px;
        font-size: 16px;
        font-weight: normal;
        color: #000000;
    }

    QPushButton#button_browse:hover {
        background-color: #dfe4ea;
    }

    QLabel#file_label {
        padding-left: 25px;
        font-size: 16px;
        color: #000000;
    }

    QWidget#control_widget {
        background-color: transparent;
    }

    QPushButton#button_control {
        padding: 10px 15px;
        font-size: 16px;
        font-weight: bold;
        color: #ffffff;
        background-color: #3498db;
        border-radius: 5px;
    }

    QPushButton#button_control:hover {
        background-color: #2980b9;
    }

    QTextEdit#result_text_file {
        padding: 10px;
        background-color: #ffffff;
        border: 1px solid #d0d3d4;
        border-radius: 5px;
        font-size: 18px;
        color: #000000;
    }

    QPushButton#button_information {
        margin-top: 5px;
        padding: 10px 15px;
        background-color: #ecf0f1;
        border-radius: 5px;
        border: 1px solid #bdc3c7;
        font-size: 16px;
        font-weight: normal;
        color: #000000;
    }

    QPushButton#button_information:hover {
        background-color: #e0e6ea;
    }

    /* OTHER INTERFACE */

    QWidget#interface_widget_live {
        background-color: transparent;
    }

    QGroupBox#settings_group {
        margin-bottom: 10px;
        background-color: #ecf0f1;
        border: 1px solid #d0d3d4;
        border-radius: 5px;
    }

    QGroupBox#settings_group::title {
        subcontrol-origin: padding;
        subcontrol-position: top left;
        left: 25px;
        font-size: 18px;
        font-weight: normal;
        color: #000000;
    }

    QGroupBox#settings_group QLabel {
        font-size: 16px;
        color: #000000;
    }

    QComboBox#network_interface_combo,
    QSpinBox#duration_spin,
    QSpinBox#buffer_spin {
        padding: 10px 15px;
        font-size: 16px;
        border-radius: 5px;
    }

    QComboBox#network_interface_combo:focus,
    QSpinBox#duration_spin:focus,
    QSpinBox#buffer_spin:focus {
        border: 1px solid #000000;
    }

    /* ARROWS START */

    QComboBox#network_interface_combo::drop-down {
        width: 25px;
        background: #ffffff;
    }

    QComboBox#network_interface_combo::drop-down:focus {
        border-left: 1px solid #000000;
    }
    
    QComboBox#network_interface_combo::down-arrow {
        image: url("ui/icons/arrow_down.svg");
        width: 25px;
        height: 25px;
    }

    QSpinBox#duration_spin::up-button,
    QSpinBox#buffer_spin::up-button {
        image: url("ui/icons/arrow_up.svg");
        margin: 0px;
        padding: 0px;
        width: 25px;
        height: 25px;
    }

    QSpinBox#duration_spin::down-button,
    QSpinBox#buffer_spin::down-button {
        image: url("ui/icons/arrow_down.svg");
        margin: 0px;
        padding: 0px;
        width: 25px;
        height: 25px;
    }

    /* ARROWS END */

    QCheckBox#use_duration_checkbox {
        margin-left: 25px;
        font-size: 16px;
        font-weight: normal;
        color: #000000;
    }

    QCheckBox#use_duration_checkbox::indicator {
        width: 20px;
        height: 20px;
        border: 1px solid #2c3e50;
        border-radius: 5px;
        background: #ffffff;
    }

    QCheckBox#use_duration_checkbox::indicator:checked {
        background: #2ecc71;
        border: 1px solid #27ae60;
    }

    QPushButton#button_control_start,
    QPushButton#button_control_stop {
        padding: 10px 15px;
        border-radius: 5px;
        border: none;
        font-size: 16px;
        font-weight: bold;
        color: #ffffff;
    }

    QPushButton#button_control_start {
        background-color: #27ae60;
    }

    QPushButton#button_control_start:hover:enabled {
        background-color: #219653;
    }

    QPushButton#button_control_start:disabled {
        background-color: #95a5a6;
    }

    QPushButton#button_control_stop {
        background-color: #e74c3c;
    }

    QPushButton#button_control_stop:hover:enabled {
        background-color: #c0392b;
    }

    QPushButton#button_control_stop:disabled {
        background-color: #bdc3c7;
    }

    QGroupBox#result_group {
        margin-top: 10px;
        background-color: #ecf0f1;
        border: 1px solid #d0d3d4;
        border-radius: 5px;
    }

    QGroupBox#result_group::title {
        subcontrol-origin: padding;
        subcontrol-position: top left;
        left: 25px;
        font-size: 18px;
        font-weight: normal;
        color: #000000;
    }

    QTextEdit#result_text_live {
        padding: 10px;
        background-color: #ffffff;
        border: 1px solid #d0d3d4;
        border-radius: 5px;
        font-size: 18px;
        color: #000000;
    }

"""
