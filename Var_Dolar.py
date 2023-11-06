import sys
import requests
import json
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QColor, QPalette
from PyQt5.QtGui import QFont

import datetime

import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Variaciones del Dólar")
        self.setGeometry(200, 200, 640, 400)
        self.setMinimumSize(640,400)
        
        # Crear una instancia de QFont con el tipo y tamaño de letra deseado
        qtfont = QFont("Bebas Neue", 18, QFont.Bold)
        #qtfont = QFont("Roboto", 20, QFont.Bold)
        #qtfont = QFont("Ubuntu", 20, QFont.Bold)
        
        # Aplicar el tipo y tamaño de letra a la ventana principal y a los widgets deseados
        self.setFont(qtfont)
        
        self.setAutoFillBackground(True)
        # Configurar el estilo Fusion con un esquema oscuro
        self.set_style()
        #configurar color del grafico
        self.set_colorgraf()

        self.figure = Figure(facecolor="black")
        self.canvas = FigureCanvas(self.figure)
        self.setCentralWidget(self.canvas)

        self.labeltime = QLabel(self)
        self.labeltime.move(100, 35)
        self.labeltime.resize(640, 25)

        self.titulo = QLabel(self)
        self.titulo.move(50, 5)
        self.titulo.resize(640, 25)
        self.titulo.setText("Hola Aquí Tienes la Cotización del Dolar Ultima Hora...")

        self.timer = QTimer(self)
        self.timer.setInterval(3600000)  # Intervalo de una hora (3600000 ms)
        self.timer.timeout.connect(self.update_chart)
        self.timer.start()

        self.update_chart()

    def set_style(self):
        # Obtener el estilo Fusion y configurar el esquema oscuro
        app.setStyle("Fusion")
        palette = QPalette()
        palette.setColor(QPalette.WindowText, QColor(255, 255, 255))
        palette.setColor(QPalette.Text, QColor(255, 255, 255))
        palette.setColor(QPalette.Foreground, QColor(255, 255, 255))
        palette.setColor(QPalette.ToolTipBase, QColor(255, 255, 255))
        palette.setColor(QPalette.ToolTipText, QColor(255, 255, 255))
        palette.setColor(QPalette.Button, QColor(53, 53, 53))
        palette.setColor(QPalette.ButtonText, QColor(255, 255, 255))
        palette.setColor(QPalette.BrightText, QColor(255, 0, 0))
        palette.setColor(QPalette.Link, QColor(42, 130, 218))
        palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        palette.setColor(QPalette.HighlightedText, QColor(0, 0, 0))
        palette.setColor(QPalette.Window, QColor(53, 53, 53))
        palette.setColor(QPalette.Base, QColor(25, 25, 25))
        palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        palette.setColor(QPalette.Background, QColor(25, 25, 25))
        app.setPalette(palette)

    def set_colorgraf(self):
        # Configurar colores específicos para el gráfico
        matplotlib.rcParams['font.family'] = 'Ubuntu'
        matplotlib.rcParams['font.weight'] = 'bold'
        matplotlib.rcParams['font.size'] = 14
        matplotlib.rcParams['text.color'] = 'black'
        matplotlib.rcParams['axes.labelcolor'] = 'grey'
        matplotlib.rcParams['xtick.color'] = 'grey'
        matplotlib.rcParams['ytick.color'] = 'lightgrey'
        matplotlib.rcParams['axes.facecolor'] = 'black'

    def update_chart(self):
        response = requests.get("https://criptoya.com/api/dolar")
        data = json.loads(response.text)
        print(data)
        usd_values = {key: value for key, value in data.items() if key in ['blue', 'mep', 'ccl', 'ccb']}
        types = list(usd_values.keys())
        values = list(usd_values.values())

        self.figure.clear()
        ax = self.figure.add_subplot(111)
        colors = ['blue', '#FFFF00', '#00FF00', '#FF0000']  # azul, amarillo, verde, rojo
        bars= ax.barh(types, values, color=colors) # Utilizamos barh en lugar de bar

        for i, bar in enumerate(bars):
            x = bar.get_width()
            y = bar.get_y() + bar.get_height() / 2
            ax.text((x-250), y, str(values[i]), ha='left', va='center', weight='bold', size=18)

        self.canvas.draw()

        self.labeltime.setText(f"Última actualización: {datetime.datetime.utcfromtimestamp(data['time'] - 10800)}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
