from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QStyle
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas

from core.traffic_analysis.traffic_analysis_visualization import create_plot


class TrafficAnalysisVisualization(QWidget):

    def __init__(self, file_path, visualization_type):
        super().__init__()
        self.file_path = file_path
        self.visualization_type = visualization_type
        self.setWindowTitle(f"Візуалізація")
        self.setWindowIcon(
            self.style().standardIcon(QStyle.StandardPixmap.SP_ComputerIcon)
        )
        self.setMinimumSize(1280, 720)
        self.showMaximized()

        box = QVBoxLayout(self)

        # Create figure
        figure = create_plot(file_path, visualization_type)
        canvas = FigureCanvas(figure)
        canvas.setObjectName("canvas")
        box.addWidget(canvas)
