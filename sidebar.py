import mysql.connector
from ui_sidebar import Ui_MainWindow
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, QVBoxLayout, QHBoxLayout, QMessageBox, QTableWidget, QTableWidgetItem, QDateTimeEdit
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, QVBoxLayout, QHBoxLayout, QMessageBox, QTableWidget, QTableWidgetItem,QLineEdit
import pandas as pd
import datetime




class MySideBar(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("SideBar Menu")
        
        #xulycombobox
        self.populate_combobox()
        
        #Lấy thời gian hiện tại
        now = datetime.datetime.now()

        # Thiết lập giá trị cho QDateTimeEdit
        

        self.dtime_tgian= now.strftime("%Y-%m-%d %H:%M:%S")
        # echpmode password
        n= QLineEdit.EchoMode.Password
        self.text_mk.setEchoMode(n)
        #xuly search
        self.pb_search.clicked.connect(self.search_data)
        
        self.cb_dichvu.currentIndexChanged.connect(self.combobox_current_index_changed)
        
        #xulystacktranghome
        
        self.pb_dichvu.clicked.connect(self.swich_to_dichvuPage)
        
        self.pb_hoadon.clicked.connect(self.swich_to_hoadonPage)
        
        self.pb_thongke.clicked.connect(self.swich_to_thongkePage)
        
        
        #xulytrangdn
        self.pb_dn.clicked.connect(self.dangnhap)             
        self.pb_dk.clicked.connect(self.swich_to_dkPage) 
        #xulytrangdk       
        self.pb_dn_pagedk.clicked.connect(self.swich_to_dnPage)
        self.pb_dk_pagedk.clicked.connect(self.dangky)
        #xulythoat
        self.pb_thoat.clicked.connect(self.swich_to_dnPage)


        #xulytranghome
        self.pb_themdv.clicked.connect(self.add_data)
        self.pb_rsdv.clicked.connect(self.load_data)
        self.pb_suadv.clicked.connect(self.update_data)
        self.pb_xoadv.clicked.connect(self.delete_data)
        self.pb_xuatdv.clicked.connect(self.call_data)
        #xulytrangdondat
        self.pb_themdon.clicked.connect(self.add_dondat)
        self.pb_rsdon.clicked.connect(self.load_dondat)
        self.pb_suadon.clicked.connect(self.update_dondat)
        self.pb_xoadon.clicked.connect(self.delete_dondat)
        self.pb_xuatdon.clicked.connect(self.call_dondat)
        
        #
        self.pb_tke1.clicked.connect(self.load_thongke1)
        
    
    def create_connection(self):
        self.mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="thucung"
        )
        return self.mydb
    
    
    #chuyển hướng stack trang chính
    def swich_to_dnPage(self):
        self.stackedWidget.setCurrentIndex(0)
    
    def swich_to_dkPage(self):
        self.stackedWidget.setCurrentIndex(1)
        
    def swich_to_homePage(self):
        self.stackedWidget.setCurrentIndex(2) 
     
      
    #chuyển hướng stack page_home
    def swich_to_dichvuPage(self):
        self.stackedWidget_3.setCurrentIndex(0)
    
    def swich_to_hoadonPage(self):
        self.stackedWidget_3.setCurrentIndex(1)
        
    def swich_to_thongkePage(self):
        self.stackedWidget_3.setCurrentIndex(2) 
        
    def insert_data(self):
        cursor= self.create_connection().cursor()
        self.dichvu=[
            ("tia mong","30000")
        ]
        cursor.executemany("insert into dichvu (tendv, giadv) values (%s,%s)", self.dichvu)
        self.mydb.commit()
        self.mydb.close()
    
    def load_data(self):
        self.text_search.clear()
        cursor= self.create_connection().cursor()
        sql= "select * from dichvu"
        self.tableWidget.setRowCount(len(sql))
        table_row=0
        
        cursor.execute(sql)
        records= cursor.fetchall()
        
        for i in records:
            self.tableWidget.setItem(table_row, 0, QTableWidgetItem(i[0]))
            self.tableWidget.setItem(table_row, 1, QTableWidgetItem(i[1]))
            table_row= table_row + 1
        self.mydb.commit()
        self.mydb.close()
        
    
    def add_data(self):
        cursor= self.create_connection().cursor()
        
        self.new_dichvu=[
            self.text_tendv.text(),
            self.text_giadv.text(),
        ]
        
        cursor.execute("insert into dichvu (tendv, giadv) values (%s,%s)", self.new_dichvu)
        self.mydb.commit()
        self.mydb.close()
    
    def call_data(self):
        current_row_index= self.tableWidget.currentRow()
        
        self.tendv_edit= str(self.tableWidget.item(current_row_index,0).text())
        self.giadv_edit= str(self.tableWidget.item(current_row_index,1).text())
        
        self.text_tendv.setText(self.tendv_edit)
        self.text_giadv.setText(self.giadv_edit)
        
    def update_data(self):
        cursor= self.create_connection().cursor()
        up_dichvu=(
            self.text_tendv.text(),
            self.text_giadv.text(),
            self.tendv_edit
        )
        cursor.execute("update dichvu set tendv=%s, giadv=%s where tendv=%s", up_dichvu)
        
        self.text_tendv.clear()
        self.text_giadv.clear()
        
        self.mydb.commit()
        self.mydb.close()
    
    def delete_data(self):
        cursor= self.create_connection().cursor()
        current_row_index= self.tableWidget.currentRow()
        name_item= str(self.tableWidget.item(current_row_index,0).text())
        if current_row_index <0:
            warning= QMessageBox.question(self,'waring','please selfect a record to delete')
        else:
            message= QMessageBox.question(self,'confirm','Are u sure to delete?', QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        
        if message == QMessageBox.StandardButton.Yes:
            sql="delete from dichvu where tendv=%s"
            cursor.execute(sql, (name_item,))
            
        self.mydb.commit()
        self.mydb.close()
        
    def search_data(self):
        self.tableWidget.clear()
        # Nhận giá trị tìm kiếm từ trường nhập liệu
        search_term = self.text_search.text()

        cursor= self.create_connection().cursor()

        sql = "SELECT * FROM dichvu WHERE tendv LIKE '%{}%'".format(search_term)
        cursor.execute(sql)
        records= cursor.fetchall()

        self.tableWidget.setRowCount(len(sql))
        table_row=0
           
        for i in records:
            self.tableWidget.setItem(table_row, 0, QTableWidgetItem(i[0]))
            self.tableWidget.setItem(table_row, 1, QTableWidgetItem(i[1]))
            table_row= table_row + 1
        self.mydb.commit()
        self.mydb.close()
        
                  
        
    #hàm dn
    def dangnhap(self):
        
        cursor= self.create_connection().cursor()
        
        tendn=self.text_tendn.text()
        mk=self.text_mk.text()
        
        cursor.execute("SELECT * FROM tk WHERE ten = %s AND pass = %s", (tendn, mk))
        user = cursor.fetchone()

        if user:
            # Đăng nhập thành công
            print("Login successful!")
            # ... (thực hiện các hành động sau đăng nhập)
            self.swich_to_homePage()
            
        else:
            # Đăng nhập thất bại
            QMessageBox.warning(self, "Error", "ten dang nhap hoac mat khau khong dung.")
     
    #hàm dk       
    def dangky(self):
        cursor= self.create_connection().cursor()
        
        tendk=self.text_tendk.text()
        sdt=self.text_sdtdk.text()
        mkk=self.text_mkdk.text()
         
        cursor.execute("SELECT * FROM tk WHERE ten = %s or sdt = %s", (tendk, sdt))
        user = cursor.fetchone()
        if user:
            # Đăng nhập thất bại
            QMessageBox.warning(self, "Error", "ten dang nhap hoac sdt ton tai.")
            
        else:
            cursor.execute("insert into tk (ten, sdt, pass) values (%s,%s,%s)", (tendk, sdt, mkk))
            self.mydb.commit()
            self.mydb.close()
            self.swich_to_dnPage()

     
    
     
    #hàm xử lý trang đơn đặt
    
    def load_dondat(self):
        cursor= self.create_connection().cursor()
        sql= "select * from dondat"
        self.tableWidget_4.setRowCount(len(sql))
        table_row=0
        
        cursor.execute(sql)
        records= cursor.fetchall()
        
        for i in records:
            self.tableWidget_4.setItem(table_row, 0, QTableWidgetItem(i[0]))
            self.tableWidget_4.setItem(table_row, 1, QTableWidgetItem(i[1]))
            self.tableWidget_4.setItem(table_row, 2, QTableWidgetItem(i[2]))
            self.tableWidget_4.setItem(table_row, 3, QTableWidgetItem(i[3]))
            self.tableWidget_4.setItem(table_row, 4, QTableWidgetItem(i[4]))
            
            table_row= table_row + 1
        self.mydb.commit()
        self.mydb.close()      
    
    def add_dondat(self):
        # Lấy tên sản phẩm được chọn
        # selected_product = self.cb_dichvu.currentText()
        #Lấy thời gian hiện tại
        
        cursor= self.create_connection().cursor()
      
        self.new_dondat=[
            self.text_tenkh.text(),
            self.text_sdt.text(),        
            self.cb_dichvu.currentText(),
            self.text_tongtien.text(),
            self.dtime_tgian,
        ]
        
        cursor.execute("insert into dondat (tenkh, sdtkh, dichvu, tongtien, tgian) values (%s,%s,%s,%s,%s)", self.new_dondat)
        self.mydb.commit()
        self.mydb.close()
    
    def call_dondat(self):
        current_row_index= self.tableWidget_4.currentRow()
        
        self.tenkh_edit= str(self.tableWidget_4.item(current_row_index,0).text())
        self.sdt_edit= str(self.tableWidget_4.item(current_row_index,1).text())
        self.cbdichvu_edit= str(self.tableWidget_4.item(current_row_index,2).text())
        self.tongtien_edit= str(self.tableWidget_4.item(current_row_index,3).text())
        self.dtime_edit= str(self.tableWidget_4.item(current_row_index,4).text())
        
        self.text_tenkh.setText(self.tenkh_edit)
        self.text_sdt.setText(self.sdt_edit)
        self.cb_dichvu.setCurrentText(self.cbdichvu_edit)
        self.text_tongtien.setText(self.tenkh_edit)
        self.dtime_tgian= self.dtime_edit
        
        
    def update_dondat(self):
        cursor= self.create_connection().cursor()
        up_dondat=(
            self.text_tenkh.text(),
            self.text_sdt.text(),
            self.cb_dichvu.currentText(),
            self.text_tongtien.text(),
            self.dtime_tgian.text(),
            self.tenkh_edit
        )
        cursor.execute("update dondat set tenkh=%s, sdtkh=%s, dichvu=%s where tenkh=%s", up_dondat)
        
        self.text_tenkh.clear()
        self.text_sdt.clear()
        
        self.mydb.commit()
        self.mydb.close()
    
    def delete_dondat(self):
        cursor= self.create_connection().cursor()
        current_row_index= self.tableWidget_4.currentRow()
        name_item= str(self.tableWidget_4.item(current_row_index,0).text())
        if current_row_index <0:
            warning= QMessageBox.question(self,'waring','please select a record to delete')
        else:
            message= QMessageBox.question(self,'confirm','Are u sure to delete?', QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        
        if message == QMessageBox.StandardButton.Yes:
            sql="delete from dondat where tenkh=%s"
            cursor.execute(sql, (name_item,))
            
        self.mydb.commit()
        self.mydb.close()
        
    def populate_combobox(self):
        cursor= self.create_connection().cursor()

        cursor.execute("SELECT * FROM dichvu") 
        services = cursor.fetchall()

        # Add services to combobox
        for service in services:
            self.cb_dichvu.addItems([service[0]])
        
        
        self.mydb.commit()
        self.mydb.close()
    def get_product_price(self, product_name):
        cursor= self.create_connection().cursor()

        sql = "SELECT giadv FROM dichvu WHERE tendv = %s"
        cursor.execute(sql, (product_name,))
        result = cursor.fetchone()

        if result:
            price = result[0]
        else:
            price = None

        self.mydb.close()
        return price
    def combobox_current_index_changed(self):
        product_name = self.cb_dichvu.currentText()
        product_price = self.get_product_price(product_name)
        if product_price:
            self.text_tongtien.setText(product_price)
        else:
            self.text_tongtien.setText("Giá không xác định")

   
            
    def load_thongke1(self):
        cursor= self.create_connection().cursor()
        cursor.execute("SELECT dichvu, COUNT(tenkh) AS total_sold FROM dondat GROUP BY dichvu") 
        data=cursor.fetchall()
        
    
        df = pd.DataFrame(data, columns=['dichvu', 'total_sold'])

        # Sort DataFrame by total_sold in descending order
        df = df.sort_values(by='total_sold', ascending=False)

        # Generate text representation of sales statistics
        result_text = "**Thống kê số lượng bán sản phẩm:**\n\n"
        for index, row in df.iterrows():
            dichvu = row['dichvu']
            total_sold = row['total_sold']
            result_text += f"{dichvu}: {total_sold}\n"

        # Display the text in the result_label
        self.label_plot.setText(result_text)


                

        

        

  
    
    