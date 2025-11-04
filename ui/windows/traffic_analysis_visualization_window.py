from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QStyle
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas

from core.traffic_analysis_visualization import create_plot


class TrafficAnalysisVisualization(QWidget):

    def __init__(self, file_path, visualization_type):
        super().__init__()
        self.file_path = file_path
        self.visualization_type = visualization_type
        self.setWindowTitle(f"Візуалізація: {visualization_type}")
        self.setWindowIcon(
            self.style().standardIcon(QStyle.StandardPixmap.SP_ComputerIcon)
        )
        self.setMinimumSize(800, 600)
        self.showMaximized()

        layout = QVBoxLayout(self)
        label = QLabel(f"<b>{visualization_type}</b>")
        layout.addWidget(label)

        # Create figure
        figure = create_plot(file_path, visualization_type)
        canvas = FigureCanvas(figure)
        layout.addWidget(canvas)
