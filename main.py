from PySide6.QtWidgets import QApplication
import sys
from sidebar import MySideBar
#
app = QApplication(sys.argv)

window = MySideBar()
window.show()

    
app.exec()