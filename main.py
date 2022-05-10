import re
from cgitb import enable
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtGui import *
from pyqt5_plugins import *
from PySide6.QtCharts import *
from PySide6.QtCore import *
from PySide6.QtUiTools import loadUiType
from PySide6.QtWidgets import *
from PyQt5.QtGui import QPainter
import pandas as pd
import os
import json
import threading

from camera_connection import Collector
import detection
from calibrationCal.SteelSurfaceInspection import SSI
import create_folder

from PySide6.QtGui import QImage as sQImage    # should change
from PySide6.QtGui import QPixmap as sQPixmap 

import cv2


ui, _ = loadUiType("main.ui")
os.environ["QT_FONT_DPI"] = "96"  # FIX Problem for High DPI and Scale above 100%

camera_list = ['23683752','23699030']


class UI_main_window(QMainWindow, ui):
    global widgets
    widgets = ui
    x = 0

    def __init__(self):

        super(UI_main_window, self).__init__()

        self.setupUi(self)
        # flags = Qt.WindowFlags(Qt.FramelessWindowHint)
        self.pos_ = self.pos()
        self.capture_flag = False
        self.camera_connect_flag = False
        self.plate_entered_flag = False
        self.image_itr = 0
        self.perfect_itr = 0
        self.defect_itr = 0
        self.save_path_manual = 'save_path_manual'
        self.save_path_auto = 'save_path_auto'
        self.SSI_file = 'SSI_params.txt'
        self.SSI_params = []
        self.auto_detection = False
        # self.setWindowFlags(flags)
        # self.activate_()

        self.connect_btn.clicked.connect(self.connect_func)
        self.start_btn.clicked.connect(self.start_capturing)
        self.stop_btn.clicked.connect(self.stop_capturing)
        self.defect_detection_algo.stateChanged.connect(self.detection_algorithm)

        self.load_SSI_params()
        #print('ssi', self.SSI_params)

    



    def connect_func(self):

        if not self.camera_connect_flag:

            self.cameras=[]

            # for i in range(len(camera_list)):

            #print('connect')

            try:

                self.cameras.append(Collector(camera_list[0],exposure=200, gain=250, trigger=False, delay_packet=16256,\
                packet_size=9000,frame_transmission_delay=0,height=1212,width=1800,offet_x=136,offset_y=0,manual=True,list_devices_mode=False))

                #print(collector.serialnumber())
                self.cameras[0].start_grabbing()
                #print('connect')
                self.cameras.append(Collector(camera_list[1],exposure=200, gain=250, trigger=False, delay_packet=16230,\
                packet_size=9000,frame_transmission_delay=9018,height=1200,width=1900,offet_x=0,offset_y=0,manual=True,list_devices_mode=False))

                #print(collector.serialnumber())
                self.cameras[1].start_grabbing()

                # make get picture button available
                self.start_btn.setEnabled(True)
                # change camera-connect button text
                self.connect_btn.setText('Disconnect Camera')
                # change flag
                self.camera_connect_flag = True

                self.show_mesagges(self.msg_label, text='Camera(s) Connected', color='green')
                self.camera_connect_label.setStyleSheet('background-color: green;')

            except:
                self.show_mesagges(self.msg_label, text='Camera Connection Failed', color='red')

        # dissconnect camera
        else:
            self.stop_capturing()
            
            self.camera_connect_flag = False
            # make get picture button unavailable
            self.start_btn.setEnabled(False)
            self.stop_btn.setEnabled(False)
            # change camera-connect button text
            self.connect_btn.setText('Connect Camera')

            # dissconnect camera
            self.cameras[0].stop_grabbing()
            self.cameras[1].stop_grabbing()

            self.show_mesagges(self.msg_label, text='Camera(s) Disconnected', color='green')
            self.camera_connect_label.setStyleSheet('background-color: red;')
            
        




    def start_capturing(self):
        self.capture_flag = True
        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        self.get_picture()


    def get_picture(self):

        #print('asd')
        

        while True and self.capture_flag:
            
            img0 = self.cameras[0].getPictures()
            img1 = self.cameras[1].getPictures()

            self.set_image_label(self.cam1,img0)
            self.set_image_label(self.cam2,img1)



            if detection.check_crossing( img0, mode = detection.SHEET):

                if not self.plate_entered_flag:
                    self.plate_entered_flag = True
                    self.update_plate_detected_label(detected=True)
                    self.image_itr = 0
                    self.defect_itr = 0
                    self.perfect_itr = 0
        
                    if self.defect_detection_algo.isChecked():
                        self.auto_detection = True
                        perfect_folder_path, defect_folder_path = create_folder.get_last_floder_name(dir_name=self.save_path_auto, folder_name = 'plate', defect_deteection_algo=True)
                    else:
                        self.auto_detection = False
                        folder_path = create_folder.get_last_floder_name(dir_name=self.save_path_manual, folder_name = 'plate', defect_deteection_algo=False)


                #print('*'*50)
                
                if self.auto_detection:
                    # defect detection
                    if len(self.SSI_params) != 0:
                        output_img0,defect_flag0, defects_dict0 = SSI(img=img0, block_size=self.SSI_params[0], defect_th=int(self.SSI_params[1]), noise_th=int(self.SSI_params[2]), noise=self.SSI_params[3], heatmap=False)
                        output_img1,defect_flag1, defects_dict1 = SSI(img=img1, block_size=self.SSI_params[0], defect_th=int(self.SSI_params[1]), noise_th=int(self.SSI_params[2]), noise=self.SSI_params[3], heatmap=False)
                    else:
                        output_img0,defect_flag0, defects_dict0 = SSI(img=img0, block_size='Small', defect_th=0, noise_th=7, noise=True, heatmap=False)
                        output_img1,defect_flag1, defects_dict1 = SSI(img=img1, block_size='Small', defect_th=0, noise_th=7, noise=True, heatmap=False)
                    # save as defect
                    if defect_flag0:
                        self.set_image_label(self.cam1_defect,output_img0)
                        # save image and json
                        # image 1
                        #print(os.path.join(folder_path, 'image_%s.jpg' % self.image_itr))
                        cv2.imwrite(os.path.join(defect_folder_path, 'image_%s.jpg' % self.defect_itr), img0)
                        cv2.imwrite(os.path.join(defect_folder_path, 'imageres_%s.jpg' % self.defect_itr), output_img0)
                        with open(os.path.join(defect_folder_path, 'labels_%s.json' % self.defect_itr), 'w') as file:
                            json.dump(defects_dict0, file)
                        # image 2
                        self.defect_itr += 1
                    else:
                        # save image and json
                        # image 1
                        #print(os.path.join(folder_path, 'image_%s.jpg' % self.image_itr))
                        cv2.imwrite(os.path.join(perfect_folder_path, 'image_%s.jpg' % self.perfect_itr), img0)
                        # image 2
                        self.perfect_itr += 1
                    #
                    if defect_flag1:
                        self.set_image_label(self.cam2_defect,output_img1)
                        cv2.imwrite(os.path.join(defect_folder_path, 'image_%s.jpg' % self.defect_itr), img1)
                        cv2.imwrite(os.path.join(defect_folder_path, 'imageres_%s.jpg' % self.defect_itr), output_img1)
                        with open(os.path.join(defect_folder_path, 'labels_%s.json' % self.defect_itr), 'w') as file:
                            json.dump(defects_dict1, file)
                        self.defect_itr += 1
                    else:
                        cv2.imwrite(os.path.join(perfect_folder_path, 'image_%s.jpg' % self.perfect_itr), img1)
                        self.perfect_itr += 1
                

                else:
                    # save as defect
                    cv2.imwrite(os.path.join(folder_path, 'image_%s.jpg' % self.image_itr), img0)
                    # image 2
                    self.image_itr += 1
                    #
                    cv2.imwrite(os.path.join(folder_path, 'image_%s.jpg' % self.image_itr), img1)
                    self.image_itr += 1
                


            

            # palte exit
            else:
                self.plate_entered_flag = False
                self.update_plate_detected_label(detected=False)
                self.image_itr = 0
                self.perfect_itr = 0
                self.defect_itr = 0


            cv2.waitKey(100)
    


    def stop_capturing(self):
            self.capture_flag = False
            self.plate_entered_flag = False
            self.update_plate_detected_label(detected=False)
            self.start_btn.setEnabled(True)
            self.stop_btn.setEnabled(False)


    

    def update_plate_detected_label(self, detected = False):
        if detected:
            self.plate_detect_label.setStyleSheet('background-color: green;')
        else:
            self.plate_detect_label.setStyleSheet('background-color: red;')

    
    def show_mesagges(self, label_name, text, color='green'):
        
        name=label_name

        if text!=None:


            label_name.setText(text)
            label_name.setStyleSheet("color:{}".format(color))       

            threading.Timer(2,self.show_mesagges,args=(name,None)).start()

        else:
            label_name.setText('')



                


    def set_image_label(self,label_name, img):
        h, w, ch = img.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = sQImage(img.data, w, h, bytes_per_line, sQImage.Format_RGB888)


        label_name.setPixmap(sQPixmap.fromImage(convert_to_Qt_format))


    def detection_algorithm(self):
        if self.defect_detection_algo.isChecked():
            self.defect_detecttion_label.setStyleSheet('background-color: green;')
        else:
            self.defect_detecttion_label.setStyleSheet('background-color: red;')



    def load_SSI_params(self):
        lines = []
        if os.path.exists(self.SSI_file):
            with open(self.SSI_file) as file_in:
                lines = file_in.read().splitlines()
            file_in.close()
            lines[3] = True if lines[3] == 'True' else False
            self.SSI_params = lines
            return True, lines
        else:
            return False, lines
        
        








if __name__ == "__main__":
    app = QApplication()
    win = UI_main_window()
    win.show()
    sys.exit(app.exec())
