from msilib.schema import CheckBox
from PySide2 import QtWidgets
from PySide2.QtWidgets import QMessageBox,QLabel,QVBoxLayout,QDialog,QFileDialog,QApplication, QMainWindow, QPushButton,  QPlainTextEdit,QGraphicsScene
from PySide2.QtCore import *
from PySide2.QtGui import QPixmap,QPalette,QIcon
from Ui_uart_teat_1_0 import Ui_MainWindow  # 串口UI文件
from ast import Num
from itertools import takewhile
import sys
import matplotlib
import matplotlib.pyplot as plt
from numpy import append, uint
import serial
import serial.tools.list_ports
import webbrowser
import time
from threading import Thread 
import math
import numpy as np
import palettable
import seaborn as sns
from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from scipy.fftpack import fft,fftshift

##from PyQt5.QtCore import *
##from PyQt5.QtGui import *
##from PyQt5.QtWidgets import *



matplotlib.use("Qt5Agg") 
class MyFigureCanvas(FigureCanvas):
  '''
  通过继承FigureCanvas类，使得该类既是一个PyQt5的Qwidget，又是一个matplotlib的FigureCanvas，这是连接pyqt5与matplotlib的关键
  '''
  def __init__(self, parent=None, width=10, height=5, xlim=(0, 2500), ylim=(-2, 2), dpi=100):
    # 创建一个Figure
    fig = plt.Figure(figsize=(width, height), dpi=dpi, tight_layout=True) # tight_layout: 用于去除画图时两边的空白
  
    FigureCanvas.__init__(self, fig) # 初始化父类
    self.setParent(parent)
  
    self.axes = fig.add_subplot(111) # 添加子图
    self.axes.spines['top'].set_visible(False) # 去掉绘图时上面的横线
    self.axes.spines['right'].set_visible(False) # 去掉绘图时右面的横线
    self.axes.set_xlim(xlim)
    self.axes.set_ylim(ylim)

class MySignals(QObject):
    text_print = Signal(bytes)  
    text_data = Signal(str)

@Slot(bytes)
def write_text(bytes):
    num = len(bytes)
    if num > 0:
        # HEX显示数据
        if myshow.checkBox.checkState():
            out_s = ''
            for i in range(0, len(bytes)):
                out_s = out_s + '{:02X}'.format(bytes[i]) + ' '
            myshow.textEdit_2.setPlainText(out_s)
        # ASCII显示数据
        else:
            myshow.textEdit_2.setPlainText(bytes.decode('utf-8'))
        # 接收换行              
        #if self.Checkbox6.isChecked():
        #    self.textEdit_2.insertPlainText('\r\n')
        # 获取到text光标
        textCursor = myshow.textEdit_2.textCursor()
        # 滚动到底部
        textCursor.movePosition(textCursor.End)
        # 设置光标到text中去
        myshow.textEdit_2.setTextCursor(textCursor)
    else:
        pass 
    
@Slot(str)
def plot_data(str):
    global Num
    global filenames_f
    Num = Num + 1
    raw_list = []
    cir_data_r = []
    cir_data_i = []
    cir_data_s_f = []
    cir_data_r_int32_f = []
    cir_data_i_int32_f = []
    cir_fft = []
    cir_fft_s = []
    cir_data_r_int32_f = np.array(cir_data_r_int32_f)
    cir_data_i_int32_f = np.array(cir_data_i_int32_f)
    cir_data_r_int32_fp = []
    cir_data_i_int32_fp = []
    cir_data_r_int32_fp = np.array(cir_data_r_int32_fp)
    cir_data_i_int32_fp = np.array(cir_data_i_int32_fp)
    cir_data_s_fp = []
    cir_data_s_fp = np.array(cir_data_s_fp)
    cir_data_s_f = np.array(cir_data_s_f)
    l = len(str)
    if l >= 144000:
        print(l)
        for i in range(0,l,3):
            raw_data = int(str[i:i+2],16)
            raw_list.append(raw_data)
        cir_len = len(raw_list)
        cir_len_f = cir_len // 3600
        cir_len_f = cir_len_f * 3600
        for i in range(0,cir_len_f,6):
            cir_data_r_s = raw_list[i] 
            i += 1
            cir_data_r_s = cir_data_r_s | (raw_list[i]<<8)
            i += 1
            cir_data_r_s = cir_data_r_s | ((raw_list[i]&0x03)<<16)
            if cir_data_r_s & 0x020000:
                cir_data_r_s = cir_data_r_s | 0xfffc0000
            cir_data_r.append(cir_data_r_s)
            i += 1
            cir_data_i_s = raw_list[i] 
            i += 1
            cir_data_i_s = cir_data_i_s | (raw_list[i]<<8) 
            i += 1
            cir_data_i_s = cir_data_i_s | ((raw_list[i]&0x03)<<16)
            if cir_data_i_s & 0x020000:
                cir_data_i_s = cir_data_i_s | 0xfffc0000
            cir_data_i.append(cir_data_i_s)
        cir_data_r_int32 = np.array(cir_data_r)
        cir_data_r_int32 = cir_data_r_int32.astype(np.int32)
        cir_data_i_int32 = np.array(cir_data_i)
        cir_data_i_int32 = cir_data_i_int32.astype(np.int32)
        double_cir = cir_data_r_int32*cir_data_r_int32+cir_data_i_int32*cir_data_i_int32
        double_cir = np.array(double_cir)
        double_cir = double_cir.astype(np.double)
        cir_data_s = np.sqrt(double_cir)
        
        #for i in range(cir_im_s.shape[0]):
        #    cir_fft = fft(cir_im_s[i])


        #for i in range(0,len(cir_data_r_int32),1022):
        #    cir_data_r_int32_fp = np.append(cir_data_r_int32_fp,cir_data_r_int32[i:i+6])
        #    cir_data_r_int32_fp = np.append(cir_data_r_int32_fp,cir_data_r_int32[i:i+6])
        #    cir_data_s_fp = np.append(cir_data_s_fp,cir_data_s[i:i+6])
        #    cir_data_r_int32_f = np.append(cir_data_r_int32_f,cir_data_r_int32[i+6:i+1022])
        #    cir_data_i_int32_f = np.append(cir_data_i_int32_f,cir_data_i_int32[i+6:i+1022])
        #    cir_data_s_f = np.append(cir_data_s_f,cir_data_s[i+6:i+1022])
        #cir_data_s_n = np.array(cir_data_s_f)
        #cir_data_s_m = cir_data_s_n.reshape(-1,1016)
        #cir_data_s_m = cir_data_s_m[:,730:830]
        cir_data_s_m = cir_data_s.reshape(-1,100)
        c_max = np.max(cir_data_s_m)
        c_min = np.min(cir_data_s_m)
        norm = (cir_data_s_m-np.min(cir_data_s_m))/(np.max(cir_data_s_m)-np.min(cir_data_s_m))
        if myshow.checkBox_5.checkState():
            save_heatmap_path = filenames_f+'/'+format(Num)+'_heatmap'+'.jpg'
            save_cir_path=filenames_f+'/'+format(Num)+'_cir'+'.jpg'
            save_cir_l_path=filenames_f+'/'+format(Num)+'_cir_l'+'.jpg'
            save_cir_phase_path=filenames_f+'/'+format(Num)+'_cir_phase'+'.jpg'
            save_path_txt = filenames_f+'/'+format(Num)+'.txt'
            save_heatmap_w_path = filenames_f+'/'+format(Num)+'_heatmap_w'+'.txt'
        else:
            save_cir_l_path=''
            save_cir_path=''
            save_cir_phase_path=''
            save_heatmap_path=''
            save_path_txt = ''
            save_heatmap_w_path = ''

        if save_path_txt != '':
            with open(file = save_path_txt, mode='w', encoding='utf-8') as file:
                file.write(str)

        ##开始绘制图像
        plt.ion()
        x = range(1,101)
        y = np.array(x)
        myshow.cir_data_content.axes.set_title('cir')
        myshow.cir_data_content.axes.clear()
        for i in range(norm.shape[0]):
            myshow.cir_data_content.axes.plot(y, norm[i])
        myshow.cir_data_content.draw()
        if save_cir_path !='':
            myshow.cir_data_content.print_figure(save_cir_path)
        myshow.cir_phase_data_content.axes.set_title('cir_phase')
        myshow.cir_phase_data_content.axes.clear()
        myshow.cir_phase_data_content.axes.plot(cir_data_r_int32, cir_data_i_int32,'.')
        myshow.cir_phase_data_content.draw()
        if save_cir_phase_path != '':
            myshow.cir_phase_data_content.print_figure(save_cir_phase_path)
        myshow.cir_l_data_content.axes.set_title('cir_l')
        myshow.cir_l_data_content.axes.clear()
        for i in range(cir_data_s_m.shape[0]):
            myshow.cir_l_data_content.axes.plot(y, cir_data_s_m[i])
        myshow.cir_l_data_content.draw()
        if save_cir_l_path != '':
            myshow.cir_l_data_content.print_figure(save_cir_l_path)
        myshow.cir_heatmap_data_content.axes.set_title('heatmap')
        myshow.cir_heatmap_data_content.axes.clear()
        myshow.cir_heatmap_data_content.axes.imshow(norm,cmap = plt.cm.BuGn)
        myshow.cir_heatmap_data_content.draw()
        if save_heatmap_path != '':
            myshow.cir_heatmap_data_content.print_figure(save_heatmap_path) 
        #cmap = sns.cubehelix_palette(start = 1.5, rot = 3, gamma=0.8, as_cmap = True)
        #plt.figure("heatmap_w")
        #plt.clf()
        #fig=sns.heatmap(data = norm,
        #            cmap = cmap)
        #plt.draw()
        #plt.pause(0.5)
        #if save_heatmap_w_path != '':
        #    heatmap =fig.get_figure()
        #    heatmap.savefig(save_heatmap_w_path)
        plt.ioff()
        plt.show()       
        
    else:
        pass
    
class Pyqt5_Serial(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(Pyqt5_Serial, self).__init__()
        #self.ui = Ui_MainWindow()
        #self.ui.setupUi(self)
        self.setupUi(self)
        
        self.init()
        
        self.ser = serial.Serial()
        self.cir_data_content=MyFigureCanvas(width=self.graphicsView.width() / 25,
                                                     height=self.graphicsView.height() /8,
                                                     xlim=(0, 100),
                                                     ylim=(0, 1))
        self.graphic_scene = QGraphicsScene()
        self.graphic_scene.addWidget(self.cir_data_content) 
        self.graphicsView.setScene(self.graphic_scene)     
        self.graphicsView.show() 
        self.cir_phase_data_content=MyFigureCanvas(width=self.graphicsView_2.width() / 25,
                                                     height=self.graphicsView_2.height() / 8,
                                                     )      
        self.graphic_scene = QGraphicsScene()
        self.graphic_scene.addWidget(self.cir_phase_data_content)       
        self.graphicsView_2.setScene(self.graphic_scene)     
        self.graphicsView_2.show() 
        self.cir_l_data_content=MyFigureCanvas(width=self.graphicsView_3.width() / 25,
                                                     height=self.graphicsView_3.height() / 8,
                                                     )      
        self.graphic_scene = QGraphicsScene()
        self.graphic_scene.addWidget(self.cir_l_data_content)       
        self.graphicsView_3.setScene(self.graphic_scene)     
        self.graphicsView_3.show()
        self.cir_heatmap_data_content=MyFigureCanvas(width=self.graphicsView_4.width() / 25,
                                                     height=self.graphicsView_4.height() /8,)      
        self.graphic_scene = QGraphicsScene()
        self.graphic_scene.addWidget(self.cir_heatmap_data_content)       
        self.graphicsView_4.setScene(self.graphic_scene)     
        self.graphicsView_4.show()                      
        self.port_check()
        
        self.global_ms = MySignals()

        #self.slot = MySlot()
        self.global_ms.text_print.connect(write_text)
        self.global_ms.text_data.connect(plot_data)
        
        # 设置Logo和标题
        self.setWindowTitle("串口调试助手")
        # 设置禁止拉伸窗口大小
        self.setFixedSize(self.width(), self.height())

        # 串口关闭按钮使能关闭
        self.pushButton_3.setEnabled(False)

        # 发送框、文本框清除
        self.textEdit.setText("")
        self.textEdit_2.setText("")
        
    # 建立控件信号与槽关系
    def init(self):
        # 串口检测
        self.pushButton_8.clicked.connect(self.port_check)
        # 串口打开按钮
        self.pushButton_2.clicked.connect(self.port_open)

        # 串口关闭按钮
        self.pushButton_3.clicked.connect(self.port_close)
        
        # 发送数据按钮
        self.pushButton_5.clicked.connect(self.data_send)

        # 加载日志
        self.pushButton.clicked.connect(self.savefiles)

        # 清除接收按钮
        self.pushButton_4.clicked.connect(self.receive_data_clear)
        
        #保存热力图
        self.pushButton_6.clicked.connect(self.save_heatmap)

    #串口检测
    def port_check(self):
        # 检测所有存在的串口，将信息存储在字典中
        self.Com_Dict = {}
        port_list = list(serial.tools.list_ports.comports())

        self.comboBox.clear()
        for port in port_list:
            self.Com_Dict["%s" % port[0]] = "%s" % port[1]
            self.comboBox.addItem(port[0])

        # 无串口判断
        if len(self.Com_Dict) == 0:
            self.comboBox.addItem("无串口")

    #串口打开
    def port_open(self):
        self.ser.port = self.comboBox.currentText()      # 串口号
        self.ser.baudrate = int(self.comboBox_4.currentText()) # 波特率
        flag_data = int(self.comboBox_6.currentText())  # 数据位
        if flag_data == 5:
            self.ser.bytesize = serial.FIVEBITS
        elif flag_data == 6:
            self.ser.bytesize = serial.SIXBITS
        elif flag_data == 7:
            self.ser.bytesize = serial.SEVENBITS
        else:
            self.ser.bytesize = serial.EIGHTBITS
        flag_data = self.comboBox_8.currentText()  # 校验位
        if flag_data == "None":
            self.ser.parity = serial.PARITY_NONE
        elif flag_data == "Odd":
            self.ser.parity = serial.PARITY_ODD
        else:
            self.ser.parity = serial.PARITY_EVEN
        flag_data = int(self.comboBox_7.currentText()) # 停止位
        if flag_data == 1:
            self.ser.stopbits = serial.STOPBITS_ONE
        else:
            self.ser.stopbits = serial.STOPBITS_TWO

        if self.checkBox_2.isChecked():
            self.ser.dsrdtr = True  #硬件流控 DTR
        if self.checkBox_3.isChecked():
            self.ser.rtscts = True  #硬件流控 RTS
            
        try:
            time.sleep(0.1)
            self.ser.open() 
        except:
            QMessageBox.critical(self, "串口异常", "此串口不能被打开！")
            return None

        # 串口打开后，切换开关串口按钮使能状态，防止失误操作        
        if self.ser.isOpen():
            self.pushButton_2.setEnabled(False)
            self.pushButton_3.setEnabled(True)
            self.groupBox.setTitle("串口状态（开启）")
        
        thread = Thread(target = self.data_receive)
        thread.start()
        
        
    def port_close(self):
        try:
            self.ser.close()
        except:
            QMessageBox.critical(self, '串口异常', '关闭串口失败，请重启程序！')
            return None
        self.pushButton_2.setEnabled(True)
        self.pushButton_3.setEnabled(False)
        #self.Lineedit1.setEnabled(True)
        self.groupBox.setTitle("串口状态（关闭）")

    def data_send(self):
        if self.ser.isOpen():
            input_s = self.textEdit.toPlainText()

            # 判断是否为非空字符串
            if input_s != "":
                if self.checkBox_4.isChecked():  
                    input_s = input_s.strip()
                    send_list = []
                    while input_s != '':
                        try:
                            num = int(input_s[0:2], 16)
                        except ValueError:
                            QMessageBox.critical(self, '串口异常', '请输入规范十六进制数据，以空格分开！')
                            return None
                        
                        input_s = input_s[2:].strip()
                        send_list.append(num)
                        
                    input_s = bytes(send_list)
                # ASCII发送
                else:  
                    input_s = (input_s).encode('utf-8')

                # 获取到Text光标
                textCursor = self.textEdit.textCursor()
                # 滚动到底部
                textCursor.movePosition(textCursor.End)
                # 设置光标到Text中去
                self.textEdit.setTextCursor(textCursor)
                self.ser.write(input_s)
        else:
            pass

    def savefiles(self):
        dlg = QFileDialog()
        global filenames
        filenames = dlg.getSaveFileName(None, "保存日志文件", None, "Txt files(*.txt)")

    def save_heatmap(self):
        dlg = QFileDialog()
        global filenames_f
        filenames_f = dlg.getExistingDirectory(None, "请选择文件夹路径")

    def data_receive(self):
        global timer
        global filenames
        n=0
        m=0
        data1 = ''
        status = True
        while True :
            try:
                num = self.ser.inWaiting()
                if num > 0:
                    status =True
                    time.sleep(0.001)
                    num = self.ser.inWaiting()  #延时，再读一次数据，确保数据完整性\
                else:
                    status = False
                if num>0:
                    n += 1
                    data = self.ser.read_all()
                    a=type(data)   
                    out_s = ''
                    for i in range(0, len(data)):
                        out_s = out_s + '{:02X}'.format(data[i]) + ' '
                    a = type(out_s)
                    data1 = data1 + out_s
                    s = len(data1)
                    print(s)
                    if self.checkBox_5.checkState():
                        if filenames != '':
                            with open(file = filenames[0], mode='a', encoding='utf-8') as file:
                                file.write(out_s)
                        #print(data1)
                    else:
                        if filenames != '':
                            with open(file = filenames[0], mode='a', encoding='utf-8') as file:
                                file.write(data.decode('utf-8'))
                    self.global_ms.text_print.emit(data)
                    #self.global_ms.text_data.emit(data1)
                
                    num_s = len(data1)
                    if num_s > 144000 :
                        num_l = num_s // 144000
                        num_a = num_l * 144000
                        data2 = data1[:num_a]
                        data1 = data1[num_a:]
                        self.global_ms.text_data.emit(data2)
                    print(num_s)
                    n = 0
                else:
                    data = ''
                    #filenames = ''
            except:
                QMessageBox.critical(self, '串口异常', '串口接收数据异常，请重新连接设备！')
                self.port_close()
                return None
            pass
        #self.thread.cancel()

    
    def receive_data_clear(self):
        self.textEdit_2.setText("")
    
if __name__ == '__main__':
    filenames = ''
    Num  = 0
    filenames_f = ''
    timer = QTimer()
    app = QtWidgets.QApplication(sys.argv)
    myshow = Pyqt5_Serial()
    myshow.show()
    sys.exit(app.exec_())
        
