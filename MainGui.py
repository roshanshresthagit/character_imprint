from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog, QLabel, QLineEdit
from PyQt5.QtGui import QPixmap
import os
import cv2

class Ui_MainWindow(object):
        def setupUi(self, MainWindow):
                MainWindow.setObjectName("MainWindow")
                MainWindow.resize(1116, 843)
                self.centralwidget = QtWidgets.QWidget(MainWindow)
                self.centralwidget.setObjectName("centralwidget")

                self.pushButton = QtWidgets.QPushButton(self.centralwidget)
                self.pushButton.setGeometry(QtCore.QRect(10, 60, 200, 50))
                self.pushButton.setObjectName("pushButton")

                self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
                self.pushButton_2.setGeometry(QtCore.QRect(10, 390, 200, 50))
                self.pushButton_2.setObjectName("pushButton_2")

                self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
                self.pushButton_3.setGeometry(QtCore.QRect(10, 720, 200, 50))
                self.pushButton_3.setObjectName("pushButton_3")

                self.reference_image_frame = QtWidgets.QFrame(self.centralwidget)
                self.reference_image_frame.setGeometry(QtCore.QRect(230, 40, 801, 311))
                self.reference_image_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
                self.reference_image_frame.setFrameShadow(QtWidgets.QFrame.Raised)
                self.reference_image_frame.setObjectName("reference_image_frame")

                self.test_image_frame = QtWidgets.QFrame(self.centralwidget)
                self.test_image_frame.setGeometry(QtCore.QRect(230, 380, 801, 301))
                self.test_image_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
                self.test_image_frame.setFrameShadow(QtWidgets.QFrame.Raised)
                self.test_image_frame.setObjectName("test_image_frame")

                self.avg_area_textbox = QLineEdit(self.centralwidget)
                self.avg_area_textbox.setGeometry(QtCore.QRect(260, 720, 300, 50))
                self.avg_area_textbox.setObjectName("avg_area_textbox")
                self.avg_area_textbox.setAlignment(QtCore.Qt.AlignCenter)
                self.avg_area_textbox.setReadOnly(True)

                self.result_textbox = QLineEdit(self.centralwidget)
                self.result_textbox.setGeometry(QtCore.QRect(530, 720, 150, 50))
                self.result_textbox.setObjectName("result_textbox")
                self.result_textbox.setAlignment(QtCore.Qt.AlignCenter)
                self.result_textbox.setReadOnly(True)

                MainWindow.setCentralWidget(self.centralwidget)
                self.menubar = QtWidgets.QMenuBar(MainWindow)
                self.menubar.setGeometry(QtCore.QRect(0, 0, 1116, 26))
                self.menubar.setObjectName("menubar")
                MainWindow.setMenuBar(self.menubar)
                self.statusbar = QtWidgets.QStatusBar(MainWindow)
                self.statusbar.setObjectName("statusbar")
                MainWindow.setStatusBar(self.statusbar)

                self.retranslateUi(MainWindow)
                QtCore.QMetaObject.connectSlotsByName(MainWindow)

                # Custom setup
                self.reference_image_label = QLabel(self.reference_image_frame)
                self.reference_image_label.setGeometry(0, 0, 801, 311)
                self.reference_image_label.setAlignment(QtCore.Qt.AlignCenter)
                
                self.test_image_label = QLabel(self.test_image_frame)
                self.test_image_label.setGeometry(0, 0, 801, 301)
                self.test_image_label.setAlignment(QtCore.Qt.AlignCenter)
                
                self.pushButton.clicked.connect(self.upload_reference_image)
                self.pushButton_2.clicked.connect(self.load_test_images)
                self.pushButton_3.clicked.connect(self.test_image)

                self.image_files = []
                self.current_image_index = -1
                self.reference_image_path = None

                # Connect key press event
                MainWindow.keyPressEvent = self.keyPressEvent

                # Apply styles
                self.apply_styles()

        def retranslateUi(self, MainWindow):
                _translate = QtCore.QCoreApplication.translate
                MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
                self.pushButton.setText(_translate("MainWindow", "Upload Reference Image"))
                self.pushButton_2.setText(_translate("MainWindow", "Load Test Image"))
                self.pushButton_3.setText(_translate("MainWindow", "Test"))
                self.avg_area_textbox.setPlaceholderText(_translate("MainWindow", "Average Area"))
                self.result_textbox.setPlaceholderText(_translate("MainWindow", "Result"))

        def apply_styles(self):
                button_style = """
                QPushButton {
                        background-color: #3498db;
                        color: white;
                        border-radius: 10px;
                        font-size: 16px;
                        padding: 10px;
                }
                QPushButton:hover {
                        background-color: #2980b9;
                }
                QPushButton:pressed {
                        background-color: #1abc9c;
                }
                """
                self.pushButton.setStyleSheet(button_style)
                self.pushButton_2.setStyleSheet(button_style)
                self.pushButton_3.setStyleSheet(button_style)

                frame_style = """
                QFrame {
                        background-color: #ecf0f1;
                        border: 2px solid #bdc3c7;
                        border-radius: 15px;
                }
                """
                self.reference_image_frame.setStyleSheet(frame_style)
                self.test_image_frame.setStyleSheet(frame_style)

        def upload_reference_image(self):
                options = QFileDialog.Options()
                fileName, _ = QFileDialog.getOpenFileName(None, "Select Reference Image", "", "Images (*.png *.jpg *.jpeg *.bmp *.gif)", options=options)
                if fileName:
                        self.reference_image_path = fileName
                        pixmap = QPixmap(fileName)
                        self.reference_image_label.setPixmap(pixmap.scaled(self.reference_image_label.size(), QtCore.Qt.KeepAspectRatio))
                self.perform_analysis()

        def load_test_images(self):
                options = QFileDialog.Options()
                directory = QFileDialog.getExistingDirectory(None, "Select Directory with Test Images", "", options=options)
                if directory:
                        self.image_files = [os.path.join(directory, f) for f in os.listdir(directory) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif'))]
                        self.current_image_index = -1
                        if self.image_files:
                                self.show_next_image()

        def show_next_image(self):
                self.current_image_index = (self.current_image_index + 1) % len(self.image_files)
                pixmap = QPixmap(self.image_files[self.current_image_index])
                self.test_image_label.setPixmap(pixmap.scaled(self.test_image_label.size(), QtCore.Qt.KeepAspectRatio))
                

        def keyPressEvent(self, event):
                if event.key() == QtCore.Qt.Key_D and self.image_files:
                        self.show_next_image()

        def perform_analysis(self):
                if not self.reference_image_path:
                        self.avg_area_textbox.setText("No reference image uploaded.")
                        return

                image = cv2.imread(self.reference_image_path)
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

                # Apply connected component analysis to the thresholded image
                connectivity = 2
                output = cv2.connectedComponentsWithStats(thresh, connectivity, cv2.CV_32S)
                (numLabel, labels, stats, centroids) = output

                self.area_t = 0
                self.l = numLabel-1
                self.labe=0
                for i in range(1, numLabel):  
                        area = stats[i, cv2.CC_STAT_AREA]
                        if area > 34:
                                self.area_t+=area
                                self.labe+=1
                                


                avg_area = self.area_t / (self.labe) if numLabel > 1 else 0
                self.avg_area_textbox.setText(f"Average Area: {avg_area:.2f}")

        def test_image(self):
                if not self.image_files:
                        self.avg_area_textbox.setText("No test images loaded.")
                        return


                image_file = self.image_files[self.current_image_index]
                print("image file",image_file)
                test_image = cv2.imread(image_file)
                gray = cv2.cvtColor(test_image, cv2.COLOR_BGR2GRAY)
                thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

                output = cv2.connectedComponentsWithStats(thresh, 2, cv2.CV_32S)
                (num_labels, labels, stats, centroids) = output

                num_labels_match = 0
                for i in range(1, num_labels):
                        w = stats[i, cv2.CC_STAT_WIDTH]
                        h = stats[i, cv2.CC_STAT_HEIGHT]
                        area = stats[i, cv2.CC_STAT_AREA]

                        keep_width = w > 2 and w < 50
                        keep_height = h > 10 and h < 65
                        keep_area = area > 34 and area < 200

                        if all((keep_width, keep_height, keep_area)):
                                num_labels_match += 1
                                # print(num_labels_match)

                # print(self.labe, num_labels_match)
                # print(self.l,num_labels-1)
                if self.l==(num_labels-1) and num_labels_match == self.labe:
                        self.result_textbox.clear() 
                        self.result_textbox.setText("True")
                        print("good") 
                else:
                        self.result_textbox.clear() 
                        self.result_textbox.setText("False")  
                        print("bad")
                        

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
