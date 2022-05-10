# import os
# import PySide6

# dirname = os.path.dirname(PySide6.__file__)
# plugin_path = os.path.join(dirname, 'plugins', 'platforms')
# os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = plugin_path

# from PySide6.QtWidgets import *

import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 
from PyQt5.QtGui import *
from matplotlib import image
from pyparsing import col
from pyqt5_plugins import *
from PySide6.QtCharts import *
from PySide6.QtCore import *
from PySide6.QtUiTools import loadUiType
from PySide6.QtWidgets import *
from PyQt5.QtGui import QPainter
from PyQt5.QtCore import QSize, QRegExp
import numpy as np
import threading
import time
from PyQt5.QtGui import QPainter
import os
import setting_api
import cv2
from qt_material import apply_stylesheet
from app_settings import Settings
from functools import partial

import numpy as np

from backend import camera_funcs, user_login_logout_funcs, colors_pallete, chart_funcs
import resources


from PySide6.QtGui import QImage as sQImage    # should change
from PySide6.QtGui import QPixmap as sQPixmap   # should change
from PySide6.QtCharts import QChart as sQChart
from PySide6.QtCharts import QChartView as sQChartView
from PySide6.QtCharts import QLineSeries as sQLineSeries
from PySide6.QtCharts import QScatterSeries as sQScatterSeries
from PySide6.QtCharts import QSplineSeries as sQSplineSeries
from PySide6.QtCharts import QValueAxis as sQValueAxis
from PySide6.QtCore import QPointF as sQPointF
from PySide6.QtWidgets import QHBoxLayout as sQHBoxLayout
from PySide6.QtWidgets import QVBoxLayout as sQVBoxLayout
from PySide6.QtWidgets import QScrollBar as sQScrollBar
from PySide6.QtWidgets import QAbstractSlider as sQAbstractSlider
from PySide6.QtWidgets import QSlider as sQSlider
from PySide6.QtWidgets import QLabel as sQLabel
from PySide6 import QtCore as sQtCore
from PySide6.QtGui import QColor as sQColor
from PySide6.QtGui import QBrush as sQBrush
from PySide6.QtGui import QPen as sQPen
from PySide6.QtGui import QPainter as sQPainter
from PySide6.QtGui import QCursor as sQCursor


ui, _ = loadUiType("main_window_Copy.ui")


os.environ["QT_FONT_DPI"] = "96" # FIX Problem for High DPI and Scale above 100%
class UI_main_window(QMainWindow, ui):
    global widgets
    widgets = ui

    def __init__(self):

        super(UI_main_window, self).__init__()


        self.setupUi(self)
        flags = Qt.WindowFlags(Qt.FramelessWindowHint)
        self.pos_ = self.pos()
        self.setWindowFlags(flags)
        self.activate_()


        self.cam_num_old=1

        self.calibration_image = None


        self.login_flag = False
        self.camera_connect_flag = False

        # dashboard button ids
        self.dash_buttons = [self.camera_setting_btn,self.calibration_setting_btn, self.plc_setting_btn\
                            , self.defect_setting_btn, self.users_setting_btn, self.level2_setting_btn\
                            ,self.general_setting_btn, self.storage_setting_btn]
        # side-bar button ids
        self.side_buttons = [self.side_camera_setting_btn, self.side_calibration_setting_btn, self.side_plc_setting_btn\
                            , self.side_defect_setting_btn, self.side_users_setting_btn, self.side_level2_setting_btn\
                            ,self.side_general_setting_btn, self.side_storage_setting_btn, self.side_dashboard_btn]

        # camera variable parameters ids in the camera-settings section of the UI 
        self.camera_params = [self.gain_spinbox, self.expo_spinbox, self.width_spinbox\
                            , self.height_spinbox, self.offsetx_spinbox, self.offsety_spinbox\
                            ,self.trigger_combo, self.maxbuffer_spinbox, self.packetdelay_spinbox\
                                , self.packetsize_spinbox, self.transmissiondelay_spinbox, self.ip_lineedit, self.serial_number_combo, self.camera_setting_connect_btn]
        

        self.main_login_btn.setIcon(sQPixmap.fromImage(sQImage('images/login_white.png')))
        # APP NAME
        # ///////////////////////////////////////////////////////////////
        title = "SABA - settings"

        self.setWindowTitle(title)



        self.toogle_btn_1.clicked.connect(partial(self.leftmenu))
        self.toogle_btn_2.clicked.connect(partial(self.leftmenu))



        self.set_combo_boxes()
        self.set_sliders()
        self.set_checkboxes()

        # validator = ip_validator.IP4Validator()
        # self.ip_lineedit.setValidator(validator)

        # combobox.activated.connect(self.activated)

        

        


        self.camera_params = [self.gain_spinbox, self.expo_spinbox, self.width_spinbox\
                            , self.height_spinbox, self.offsetx_spinbox, self.offsety_spinbox\
                            ,self.trigger_combo, self.maxbuffer_spinbox, self.packetdelay_spinbox\
                                , self.packetsize_spinbox, self.transmissiondelay_spinbox, self.ip_lineedit, self.serial_number_combo, self.camera_setting_connect_btn]

        
        

        
        # SET LANGUAGE
        #//////////////////////////////////////////////
        # self.set_language()
        self.language = 'en'

        self._old_pos = None



        

        
       

        self.toogle_btn_1.clicked.connect(partial(self.leftmenu))
        self.toogle_btn_2.clicked.connect(partial(self.leftmenu))
        self.stackedWidget.currentChanged.connect(self.disable_camera_settings)

        
        # chart
        # chart ---------------------------------------------------------------------------------------------
        chart_funcs.create_train_chart_on_ui(ui_obj=self, frame_obj=self.frame_chart, hover_label_obj=self.label_chart, chart_postfix='accuracy', chart_title='chart', legend_train='legend1', legend_val='legend2',
                            axisX_title='epoch', axisY_title='Accuracy', checkbox_obj=self.checkBox)
        
        self.pushButton.clicked.connect(partial(lambda: chart_funcs.update_chart(ui_obj=self, chart_postfix='accuracy')))

        
        
        
          

        
        



    # def showPassword(self, show):
    #     echo=str(self.password.echoMode()).split(".", 4)[-1]


        

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self._old_pos = event.pos()

    def mouseReleaseEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self._old_pos = None

    def mouseMoveEvent(self, event):
        if not self._old_pos:
            return
        delta = event.pos() - self._old_pos
        self.move(self.pos() + delta)



    # Label Dorsa
        # ///////////////////////////////////////////////     

    #///////////////////// LANGUAGE
    # def set_language(self):
    #     print(detect_lenguage.language())
    #     if detect_lenguage.language()=='Persian(فارسی)':
    #         detect_lenguage.main_window(self)
    
 
# Label Dorsa
    # ///////////////////////////////////////////////     

    def leftmenu(self):


        width=self.leftMenuBg.width()
        # self.stackedWidget_defect.setCurrentWidget(self.page_no)
        # self.stackedWidget_defect.setMaximumHeight(60)
        # x=self.stackedWidget_defect.height()
        #print('height',height)
        if width ==0:
    
            # print('if')

            self.left_box = QPropertyAnimation(self.topMenu, b"maximumHeight")
            self.left_box.setDuration(Settings.TIME_ANIMATION)
            self.left_box.setStartValue(0)
            self.left_box.setEndValue(11111)
            self.left_box.setEasingCurve(QEasingCurve.InOutQuart) 

            self.left_box_2 = QPropertyAnimation(self.leftMenuBg, b"minimumWidth")
            self.left_box_2.setDuration(Settings.TIME_ANIMATION)
            self.left_box_2.setStartValue(0)
            self.left_box_2.setEndValue(60)
            self.left_box_2.setEasingCurve(QEasingCurve.InOutQuart) 
    
            self.left_box_5 = QPropertyAnimation(self.leftMenuBg, b"maximumWidth")
            self.left_box_5.setDuration(Settings.TIME_ANIMATION)
            self.left_box_5.setStartValue(0)
            self.left_box_5.setEndValue(60)
            self.left_box_5.setEasingCurve(QEasingCurve.InOutQuart) 

            self.left_box_3 = QPropertyAnimation(self.toogle_btn_1, b"minimumWidth")
            self.left_box_3.setDuration(Settings.TIME_ANIMATION)
            self.left_box_3.setStartValue(0)
            self.left_box_3.setEndValue(34)
            self.left_box_3.setEasingCurve(QEasingCurve.InOutQuart) 
 
            self.left_box_4 = QPropertyAnimation(self.toogle_btn_2, b"minimumWidth")
            self.left_box_4.setDuration(Settings.TIME_ANIMATION)
            self.left_box_4.setStartValue(34)
            self.left_box_4.setEndValue(0)
            self.left_box_4.setEasingCurve(QEasingCurve.InOutQuart) 


            self.group = QParallelAnimationGroup()
            self.group.addAnimation(self.left_box)
            self.group.addAnimation(self.left_box_2)
            self.group.addAnimation(self.left_box_3)
            self.group.addAnimation(self.left_box_4)
            self.group.addAnimation(self.left_box_5)
            # self.group.addAnimation(self.right_box)
            self.group.start()    
            #print('no ani')
        else :

            # print('else')

            self.left_box = QPropertyAnimation(self.topMenu, b"maximumHeight")
            self.left_box.setDuration(Settings.TIME_ANIMATION)
            self.left_box.setStartValue(width)
            self.left_box.setEndValue(0)
            self.left_box.setEasingCurve(QEasingCurve.InOutQuart) 

            self.left_box_2 = QPropertyAnimation(self.leftMenuBg, b"minimumWidth")
            self.left_box_2.setDuration(Settings.TIME_ANIMATION)
            self.left_box_2.setStartValue(60)
            self.left_box_2.setEndValue(0)
            self.left_box_2.setEasingCurve(QEasingCurve.InOutQuart)

            self.left_box_5 = QPropertyAnimation(self.leftMenuBg, b"maximumWidth")
            self.left_box_5.setDuration(Settings.TIME_ANIMATION)
            self.left_box_5.setStartValue(60)
            self.left_box_5.setEndValue(0)
            self.left_box_5.setEasingCurve(QEasingCurve.InOutQuart)            

            self.left_box_3 = QPropertyAnimation(self.toogle_btn_1, b"minimumWidth")
            self.left_box_3.setDuration(Settings.TIME_ANIMATION)
            self.left_box_3.setStartValue(34)
            self.left_box_3.setEndValue(0)
            self.left_box_3.setEasingCurve(QEasingCurve.InOutQuart) 


            self.left_box_4 = QPropertyAnimation(self.toogle_btn_2, b"minimumWidth")
            self.left_box_4.setDuration(Settings.TIME_ANIMATION)
            self.left_box_4.setStartValue(0)
            self.left_box_4.setEndValue(34)
            self.left_box_4.setEasingCurve(QEasingCurve.InOutQuart) 


            self.group = QParallelAnimationGroup()
            self.group.addAnimation(self.left_box)
            self.group.addAnimation(self.left_box_2)
            self.group.addAnimation(self.left_box_3)
            self.group.addAnimation(self.left_box_4)
            self.group.addAnimation(self.left_box_5)
            # self.group.addAnimation(self.right_box)
            self.group.start()    
            #print('no ani')
 


    def animation_move(self,label_name,lenght):

        width=label_name.width()
        # self.stackedWidget_defect.setCurrentWidget(self.page_no)
        # self.stackedWidget_defect.setMaximumHeight(60)
        # x=self.stackedWidget_defect.height()
        #print('height',height)
        if width ==0:


            self.animation_box = QPropertyAnimation(label_name, b"minimumWidth")
            self.animation_box.setDuration(Settings.TIME_ANIMATION)
            self.animation_box.setStartValue(0)
            self.animation_box.setEndValue(lenght)
            self.animation_box.setEasingCurve(QEasingCurve.InOutQuart) 


            self.group = QParallelAnimationGroup()
            self.group.addAnimation(self.animation_box)
            self.group.start() 

        else :
    
        
            self.animation_box = QPropertyAnimation(label_name, b"minimumWidth")
            self.animation_box.setDuration(Settings.TIME_ANIMATION)
            self.animation_box.setStartValue(lenght)
            self.animation_box.setEndValue(0)
            self.animation_box.setEasingCurve(QEasingCurve.InOutQuart)


            self.group = QParallelAnimationGroup()
            self.group.addAnimation(self.animation_box)
            self.group.start() 


    def activate_(self):
        self.closeButton.clicked.connect(self.close_win)
        self.miniButton.clicked.connect(self.minimize_win)
        self.maxiButton.clicked.connect(self.maxmize_minimize)

        self.camera_setting_btn.clicked.connect(self.buttonClick)
        self.side_camera_setting_btn.clicked.connect(self.buttonClick)
        self.side_dashboard_btn.clicked.connect(self.buttonClick)
        self.calibration_setting_btn.clicked.connect(self.buttonClick)
        self.side_calibration_setting_btn.clicked.connect(self.buttonClick)
        self.general_setting_btn.clicked.connect(self.buttonClick)
        self.side_general_setting_btn.clicked.connect(self.buttonClick)





        self.camera01_btn.clicked.connect(self.buttonClick)
        self.camera02_btn.clicked.connect(self.buttonClick)
        self.camera03_btn.clicked.connect(self.buttonClick)
        self.camera04_btn.clicked.connect(self.buttonClick)
        self.camera05_btn.clicked.connect(self.buttonClick)
        self.camera06_btn.clicked.connect(self.buttonClick)
        self.camera07_btn.clicked.connect(self.buttonClick)
        self.camera08_btn.clicked.connect(self.buttonClick)
        self.camera09_btn.clicked.connect(self.buttonClick)
        self.camera10_btn.clicked.connect(self.buttonClick)
        self.camera11_btn.clicked.connect(self.buttonClick)
        self.camera12_btn.clicked.connect(self.buttonClick)
        self.camera13_btn.clicked.connect(self.buttonClick)
        self.camera14_btn.clicked.connect(self.buttonClick)
        self.camera15_btn.clicked.connect(self.buttonClick)
        self.camera16_btn.clicked.connect(self.buttonClick)
        self.camera17_btn.clicked.connect(self.buttonClick)
        self.camera18_btn.clicked.connect(self.buttonClick)
        self.camera19_btn.clicked.connect(self.buttonClick)
        self.camera20_btn.clicked.connect(self.buttonClick)
        self.camera21_btn.clicked.connect(self.buttonClick)
        self.camera22_btn.clicked.connect(self.buttonClick)
        self.camera23_btn.clicked.connect(self.buttonClick)
        self.camera24_btn.clicked.connect(self.buttonClick)

        self.checkBox_top.clicked.connect(self.buttonClick)
        self.checkBox_bottom.clicked.connect(self.buttonClick)

        self.side_users_setting_btn.clicked.connect(self.buttonClick)
        self.users_setting_btn.clicked.connect(self.buttonClick)
        self.add_user_btn.clicked.connect(self.buttonClick)

        self.defect_setting_btn.clicked.connect(self.buttonClick)
        self.side_defect_setting_btn.clicked.connect(self.buttonClick)




    def close_win(self):
        self.close()
        sys.exit()

    def minimize_win(self):
        self.showMinimized()

    def maxmize_minimize(self):
        
        if self.isMaximized():
            self.showNormal()
            # self.sheet_view_down=data_grabber.sheetOverView(h=129,w=1084,nh=12,nw=30)
        else:
            self.showMaximized()



    def set_combo_boxes(self):

        x=["Operator", "Admin", "DORSA"]
        self.user_role.addItems(x)

        x=['Small','Medium','Large']
        self.block_image_proccessing={'Small':100,'Medium':200,'Large':300}
        self.comboBox_block_size.addItems(x)
        self.comboBox_block_size.currentTextChanged.connect(self.combo_image_preccess)

        cam_nums=[]

        for i in range(1,25):
            cam_nums.append(str(i))

        self.comboBox_cam_select_calibration.addItems(cam_nums)
        self.comboBox_cam_select_calibration.currentTextChanged.connect(self.selected_camera)




    def set_sliders(self):

        self.verticalSlider_noise.valueChanged[int].connect(self.show_value)
        self.verticalSlider_defect.valueChanged[int].connect(self.show_value)


    def set_checkboxes(self):

        # self.checkBox_noise.stateChanged.connect(lambda:self.btnstate(self.b1))
        self.checkBox_noise.setChecked(True)
        self.checkBox_noise.stateChanged.connect(lambda:self.check_box_state(self.checkBox_noise))

    def check_box_state(self,b):

            if b.isChecked() == True:
                b.setText('Enable')
            else:
                b.setText('Disable')
                    
            
    def show_value(self,value):
        print(value)
        btn = self.sender()
        btnName = btn.objectName()

        if btnName=='verticalSlider_noise':
            self.remaining_noise.setText(str(value))

        elif btnName=='verticalSlider_defect':
            self.remaining_defect.setText(str(value))



    def combo_image_preccess(self,s):

        # self.block_image_proccessi

        self.remaining_p_value.setText(str(self.block_image_proccessing[s]))

        self.set_default_image_proccess(s)


    



    def set_default_image_proccess(self,value):

        if value=='Small':
            self.verticalSlider_defect.setValue(1.5)
            self.verticalSlider_noise.setValue(42)

        if value=='Medium':
            self.verticalSlider_defect.setValue(3)
            self.verticalSlider_noise.setValue(35)

        if value=='Large':
            self.verticalSlider_defect.setValue(2)
            self.verticalSlider_noise.setValue(40)





    def selected_camera(self,s):
        

        for i in range(1,25):
            if i<13:
                eval('self.camera%s_btn_2'%i).setIcon(QIcon('images/camtop.png'))
            else:
                eval('self.camera%s_btn_2'%i).setIcon(QIcon('images/cambtm.png'))

        cam_num=s

        if int(s)<13:
            eval('self.camera%s_btn_2'%cam_num).setIcon(QIcon('images/camtop_actived.png'))

        else :
            eval('self.camera%s_btn_2'%cam_num).setIcon(QIcon('images/cambtm_actived.png'))





    # User Managment page --------------------------------

 

    def get_user_pass(self):
        self.user_name_value=self.user_name.text()
        self.password_value=self.password.text()

        return self.user_name_value,self.password_value


    def set_login_message(self,text,color):
        self.login_message.setText(text)
        self.login_message.setStyleSheet("color:#{}".format(color))



    

    



    



    def show_mesagges(self,label_name,text,color='green'):
        
        name=label_name

        if text!=None:


            label_name.setText(text)
            label_name.setStyleSheet("color:{}".format(color))       

            threading.Timer(2,self.show_mesagges,args=(name,None)).start()

        else:
            label_name.setText('')


    def clear_line_edits(self,line_edits):

        for i in range(len(line_edits)):
            line_edits[i].setText('')



    # Calibration Page-----------------------

    def get_image_proccessing_parms(self):

        combo=self.comboBox_block_size.currentText()
        defect=self.verticalSlider_defect.value()
        noise=self.verticalSlider_noise.value()
        noise_flag=self.checkBox_noise.isChecked()

        return {'block_size':combo,'defect':defect/10,'noise':noise,'noise_flag':noise_flag}

    def get_width_guage_parms(self):

        combo=self.comboBox_cam_select_calibration.currentText()

        # print(combo)

        return combo






    def buttonClick(self):
        # GET BUTTON CLICKED
        btn = self.sender()
        btnName = btn.objectName()


        
        if btnName =='camera_setting_btn' and self.stackedWidget.currentWidget()!=self.page_camera_setting:

            self.stackedWidget.setCurrentWidget(self.page_camera_setting)
            

        if btnName =='side_camera_setting_btn' and self.stackedWidget.currentWidget()!=self.page_camera_setting:

            self.stackedWidget.setCurrentWidget(self.page_camera_setting)
        
        if btnName =='side_dashboard_btn' and self.stackedWidget.currentWidget()!=self.page_dashboard:


            self.stackedWidget.setCurrentWidget(self.page_dashboard)
        
        if btnName =='users_setting_btn' :

            self.stackedWidget.setCurrentWidget(self.page_users_setting)
        
        if btnName =='side_users_setting_btn' :

            self.stackedWidget.setCurrentWidget(self.page_users_setting)
        
        if btnName =='add_user_btn' :

            self.animation_move(self.frame_add_user,300)

        
        if btnName =='defect_setting_btn' :

            self.stackedWidget.setCurrentWidget(self.page_defects)
        
        if btnName =='side_defect_setting_btn' :

            self.stackedWidget.setCurrentWidget(self.page_defects)

        
        
        if btnName =='calibration_setting_btn' :

            self.stackedWidget.setCurrentWidget(self.page_calibration_setting)

        
        if btnName =='side_calibration_setting_btn' :

            self.stackedWidget.setCurrentWidget(self.page_calibration_setting)
        
        if btnName =='general_setting_btn' :

            self.stackedWidget.setCurrentWidget(self.page_settings)

        
        if btnName =='side_general_setting_btn' :

            self.stackedWidget.setCurrentWidget(self.page_settings)

        
        







        # if btnName =='camera1_btn_11':
        if btnName[:6] == 'camera' and btnName != 'camera_setting_btn':
            camera_id = btnName[6:8]
            #self.left_bar_clear()
            #self.Data_auquzation_btn.setStyleSheet("background-image: url(:/icons/images/icons/graber.png);background-color: rgb(212, 212, 212);color:rgp(0,0,0);")
            if not self.camera_setting_apply_btn.isEnabled() or (self.cameraname_label.text()!='No Camera Selected' and self.cameraname_label.text()[-2:]!=camera_id):
                
                self.cameraname_label.setText('Cam%s' % camera_id)
                #self.change_camera_btn_icon(camera_id, active=True)
                self.camera_setting_apply_btn.setEnabled(True)
                self.camera_setting_connect_btn.setStyleSheet("background-color:{}; border:Transparent".format(colors_pallete.successfull_green))
                self.set_button_enable_or_disable(self.camera_params, enable=True)
            else:
                self.disable_camera_settings()
                #self.change_camera_btn_icon(camera_id, active=False)

        

        
        
                

        
    def disable_camera_settings(self):
        self.cameraname_label.setText('No Camera Selected')
        self.camera_setting_apply_btn.setEnabled(False)
        self.camera_setting_connect_btn.setStyleSheet("background-color:{}; border:Transparent".format(colors_pallete.disabled_btn))
        self.set_button_enable_or_disable(self.camera_params, enable=False)
        

    
    def set_button_enable_or_disable(self, names, enable=True):
        
        for name in names:
            name.setEnabled(enable)


    def set_label(self,label_name,msg):
    
        label_name.setText(msg)
 
    def get_label(self,label_name):

        return label_name.text()


    def set_image_label(self,label_name, img):
        h, w, ch = img.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = sQImage(img.data, w, h, bytes_per_line, sQImage.Format_RGB888)


        label_name.setPixmap(sQPixmap.fromImage(convert_to_Qt_format))






    def change_camera_btn_icon(self, camera_id, active=False):
        image_active_id = 'images/cambtm_actived.png' if int(camera_id)>12 else 'images/camtop_actived.png'    

        for cam_id in camera_funcs.all_camera_ids:
            image_deactive_id = 'images/cambtm.png' if int(cam_id)>12 else 'images/camtop.png'
            eval('self.camera%s_btn' % cam_id).setIcon(QIcon(image_deactive_id))
            
        if active:    
            eval('self.camera%s_btn' % camera_id).setIcon(QIcon(image_active_id))

    
    



    
        

            

    
    








if __name__ == "__main__":
    app = QApplication()
    win = UI_main_window()
    # apply_stylesheet(app,theme='dark_cyan.xml')
    api = setting_api.API(win)
    win.show()
    sys.exit(app.exec())
    