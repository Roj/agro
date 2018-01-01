#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
import sys
import os
from PyQt4.QtGui import *
from PyQt4.QtCore import *

class QProgBar(QProgressBar):
 
    value = 0
 
    @pyqtSlot()
    def increaseValue(progressBar):
        progressBar.setValue(progressBar.value)
        progressBar.value = progressBar.value+1
 

class GUI:
    def __init__(self):
        # Create an PyQT4 application object.
        self.a = QApplication(sys.argv)
         
        # The QWidget widget is the base class of all user interface objects in PyQt4.
        self.window = QWidget()

        # Set window size.
        self.window.resize(640/2,480/4)

        # Set window title
        self.window.setWindowTitle("Detección de eventos de incendio")
        self.macrolayout = QVBoxLayout(self.window)
        self.addIntroBlock()
        self.addFirstStageBlock()
        self.addSecondStageBlock()
        self.addThirdStageBlock()

    def addIntroBlock(self):
        label = QLabel("Detectar eventos de incendio")
        label.setAlignment(Qt.AlignCenter)
        self.macrolayout.addWidget(label)

    def addFirstStageBlock(self):
        # First stage: join_fires.py
        topgridlayout = QGridLayout()
        self.macrolayout.addLayout(topgridlayout)

        textbox = QLineEdit()
        textbox.setPlaceholderText("archivo csv")

        def openFileDialog():
            filename = QFileDialog.getOpenFileName(
                self.window, 
                'Abrir CSV', 
                os.getcwd()
            )
            textbox.setText(filename)

        btn = QPushButton('Cargar archivo de entrada')
        btn.clicked.connect(openFileDialog)
        btn.resize(btn.sizeHint())
        btn.move(100, 80)

        topgridlayout.addWidget(textbox,0,0)
        topgridlayout.addWidget(btn, 0,1)
        
        firstStageLayout = QGridLayout()
        self.macrolayout.addLayout(firstStageLayout)
        formato_fecha_label = QLabel("Formato de la fecha")
        formato_fecha_box = QLineEdit()
        formato_fecha_box.setPlaceholderText("%d (dia) %m (mes) %Y (año)")
        formato_fecha_ayuda = QLabel("e.g. %d/%m/%Y")
        firstStageLayout.addWidget(formato_fecha_label, 2,0)
        firstStageLayout.addWidget(formato_fecha_box, 2,1)
        firstStageLayout.addWidget(formato_fecha_ayuda, 2,2)

        separador_label = QLabel("Separador:")
        separador_radio_1 = QRadioButton(";")
        separador_radio_2 = QRadioButton(",")
        #separador_radio_group = QButtonGroup()
        #separador_radio_group.addButton(separador_radio_1)
        #separador_radio_group.addButton(separador_radio_2)
        firstStageLayout.addWidget(separador_label,3,0)
        firstStageLayout.addWidget(separador_radio_1,3,1)
        firstStageLayout.addWidget(separador_radio_2,3,2)

        pdecimal_label = QLabel("Punto decimal:")
        pdecimal_radio_1 = QRadioButton(",")
        pdecimal_radio_2 = QRadioButton(".")
        #pdecimal_radio_group = QButtonGroup()
        #pdecimal_radio_group.addButton(pdecimal_radio_1)
        #pdecimal_radio_group.addButton(pdecimal_radio_2)
        firstStageLayout.addWidget(pdecimal_label,4,0)
        firstStageLayout.addWidget(pdecimal_radio_1,4,1)
        firstStageLayout.addWidget(pdecimal_radio_2,4,2)

        def procesar_join_fires():
            bar = QProgBar()
            self.macrolayout.insertWidget(3,bar)

            
        procesar_1 = QPushButton('Procesar')
        procesar_1.clicked.connect(procesar_join_fires)
        firstStageLayout.addWidget(procesar_1, 5,0)
        self.macrolayout.addSpacing(10)

    def addSecondStageBlock(self):
        secondStageLayout = QGridLayout()
        self.macrolayout.addLayout(secondStageLayout)

        def procesar_agrupar():
            bar = QProgBar()
            # It may look like it should be 5, but after a bar
            # is inserted in the first stage it shuold be 6.
            self.macrolayout.insertWidget(6,bar)

        secondStageTitle = QLabel("Agrupar focos de incendio")
        secondStageTitle.setAlignment(Qt.AlignCenter)
        secondStageFileOut = QLabel(
            "Archivo de salida:"
            + os.getcwd() + "/datos/focos_salida_agrupados.csv"
        )
        secondStageFileOut.setAlignment(Qt.AlignLeft)
        secondStageButton = QPushButton("Procesar")
        secondStageButton.clicked.connect(procesar_agrupar)
        secondStageLayout.addWidget(secondStageTitle)
        secondStageLayout.addWidget(secondStageFileOut)
        secondStageLayout.addWidget(secondStageButton)
    def addThirdStageBlock(self):
        thirdStageLayout = QGridLayout()
        self.macrolayout.addLayout(thirdStageLayout)

        def procesar_agrupar():
            bar = QProgBar()
            self.macrolayout.addWidget(bar)

        thirdStageTitle = QLabel("Asignar celdas de grillas")
        thirdStageTitle.setAlignment(Qt.AlignCenter)
        thirdStageFileOut = QLabel(
            "Archivo de salida:"
            + os.getcwd() + "/datos/incendios_con_celdas.csv"
        )
        thirdStageFileOut.setAlignment(Qt.AlignLeft)
        thirdStageButton = QPushButton("Procesar")
        thirdStageButton.clicked.connect(procesar_agrupar)
        thirdStageLayout.addWidget(thirdStageTitle)
        thirdStageLayout.addWidget(thirdStageFileOut)
        thirdStageLayout.addWidget(thirdStageButton)


    def run(self):
        
        self.window.show()
         
        sys.exit(self.a.exec_())


g = GUI()
g.run()

# Parte 2

# Show window
