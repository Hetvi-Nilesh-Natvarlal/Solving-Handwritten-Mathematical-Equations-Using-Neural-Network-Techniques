#import import_ipynb
import segmentation
import ImageViewer
import HistoryWindow
import logging
import re
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
import keras
import numpy as np
from ImageViewer import ImageLabel
from HistoryWindow import HistoryWindow
import solver

#Creating the User window
class MainWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("SOLVING HANDWRITTEN MATHEMATICAL EQUATIONS USING NEURAL NETWORK TECHNIQUES")
        self.showMaximized()
        # self.setMinimumSize(1280, 720)

        # define instance variables
        self.lbl_image = None
        self.txt_answer_field = None
        self.main_layout = None
        self.splitter = None
        self.wgt_left_sidebar = None
        self.lyt_left_sidebar = None
        self.wgt_right_sidebar = None
        self.lyt_right_sidebar = None
        self.btn_open_image = None
        self.btn_clear_image = None
        self.btn_solve = None
        self.btn_history = None
        self.cb_select_equation_type = None
        self.lbl_info = None
        self.db = None
        self.history_window = None

        self.create_widgets()
        self.create_layouts()
        self.create_connections()
        self.configure_database()

#Creating the buttons/widgets
    def create_widgets(self):
        self.wgt_left_sidebar = QWidget() #to create window inside which other QWidgets are placed
        self.wgt_right_sidebar = QWidget() #QWidget class is base class of all user interface objects

        self.lbl_image = ImageLabel() # renders a rectangle, like Frame does, with an image
        self.lbl_image.setText("DRAG AND DROP AN IMAGE HERE OR USE THE 'OPEN' BUTTON TO UPLOAD AN IMAGE")
        self.lbl_image.setAlignment(Qt.AlignCenter)

        self.btn_open_image = QPushButton("OPEN FOLDER") #is a simple button in PyQt, when clicked by a user some associated action gets performed
        self.btn_clear_image = QPushButton("CLEAR DISPLAY")
        self.btn_solve = QPushButton("SOLVE EQUATION")
        self.btn_history = QPushButton("HISTORY")

        self.cb_select_equation_type = QComboBox() #is widget in PyQt5 which is used to choose options from a list
        self.cb_select_equation_type.insertItem(0, "EXPRESSION")
        self.cb_select_equation_type.insertItem(1, "QUADRATIC EQUATION")
        self.cb_select_equation_type.insertItem(2, "CUBIC EQUATION")
        self.cb_select_equation_type.insertItem(3, "LINEAR SYSTEM")
        self.cb_select_equation_type.insertItem(4, "DIFFERENTIATION")
       

        self.lbl_info = QLabel("\nSolves expressions such as 5 + 2, 27 x 2 etc."
                               "\n\nDivision is not supported.") #QLabel acts as placeholder to display non-editable text or image

        self.txt_answer_field = QTextEdit() #is a mult-line text box control that diaplays mutliple lines of text,with multiple vertical scrolls when the text is outside the control's display range
        self.txt_answer_field.setReadOnly(True) #to make the field ready only if true
        self.txt_answer_field.setFixedHeight(150) #to set fix length of height of window
        self.txt_answer_field.setStyleSheet("font: 40px")

        self.history_window = HistoryWindow()

    def create_layouts(self):
        # initialize layouts
        self.main_layout = QVBoxLayout() # are basic layout class that line up widgets horizontally and vertically
        self.lyt_left_sidebar = QVBoxLayout()
        self.lyt_right_sidebar = QVBoxLayout()

        # create splitter and set splitter properties
        self.splitter = QSplitter(Qt.Horizontal) #lets the user control the size of child widgets by dragging the boundary between them
        self.splitter.addWidget(self.wgt_left_sidebar)
        self.splitter.addWidget(self.lbl_image)
        self.splitter.addWidget(self.wgt_right_sidebar)
        self.splitter.setSizes([80, 300, 80])
        self.splitter.setCollapsible(0, False)

        # set layouts
        self.wgt_left_sidebar.setLayout(self.lyt_left_sidebar) #applies layout to widgets
        self.lyt_left_sidebar.addWidget(self.btn_open_image)
        self.lyt_left_sidebar.addWidget(self.btn_clear_image)
        self.lyt_left_sidebar.addWidget(self.btn_solve)
        self.lyt_left_sidebar.addStretch(1)
        self.lyt_left_sidebar.addWidget(self.btn_history)
        self.wgt_right_sidebar.setLayout(self.lyt_right_sidebar)
        self.lyt_right_sidebar.addWidget(self.cb_select_equation_type)
        self.lyt_right_sidebar.addWidget(self.lbl_info)
        self.lyt_right_sidebar.addStretch(1) #creates an empty strectchable box

        self.main_layout.addWidget(self.splitter)
        self.main_layout.addWidget(self.txt_answer_field)

        self.setLayout(self.main_layout)

#Connecting each button to their functions 
    def create_connections(self):
        self.btn_open_image.clicked.connect(self.lbl_image.browse)
        self.btn_clear_image.clicked.connect(self.clear)
        self.btn_solve.clicked.connect(self.solve_equation)
        self.btn_history.clicked.connect(self.show_history)
        self.cb_select_equation_type.currentTextChanged.connect(self.display_info)

#The history displayed uses QSQLITE and hence creating a table and the respective queries to add and clear the history
    def configure_database(self):
        self.db = QSqlDatabase.addDatabase('QSQLITE')
        self.db.setDatabaseName('history.db')
        self.db.open()
        query = QSqlQuery(self.db) #QSqlQuery class provides a means of executing and manipulating SQL statements.
        query.exec_("""
            CREATE TABLE IF NOT EXISTS history(
                equation TEXT,
                solution TEXT
            )
        """)
        if query.isActive():
            print("Table created successfully!")
        else:
            print("Error creating table: ", query.lastError().text())

    def add_record(self, equation, solution):
        query = QSqlQuery()
        query.prepare("INSERT INTO history (equation, solution) VALUES (:equation, :solution)")
        query.bindValue(":equation", equation)
        query.bindValue(":solution", solution)
        query.exec_()
        if query.isActive():
            print("Record added successfully")
        else:
            print("Error adding record: ", query.lastError().text())

        self.history_window.load_data()

    def close_connection(self):
        self.db.close()

#Comparing if entered image matches the equation mode selected
    def solve_equation(self): #Pixmap class is an off screen image representation that can be used as paint device
        pixmap = self.lbl_image.pixmap()
        if pixmap:
            image = self.pixmap_to_numpy(pixmap)
            mode = self.cb_select_equation_type.currentText()
            if mode == 'EXPRESSION':
                self.process_expression(image)
            if mode == 'QUADRATIC EQUATION':
                self.process_quadratic_eq(image)
            if mode == 'CUBIC EQUATION':
                self.process_quadratic_eq(image)
            if mode == 'LINEAR SYSTEM':
                self.process_linear_system(image)
            if mode == 'DIFFERENTIATION':
                self.process_derivative(image)
        else:
            QMessageBox.critical(self, 'Error', 'Please input an image!')

#Solve the expression entered as image
    def process_expression(self, image):
        try:
            expression = solver.extract(image)
            solution = solver.solve_expression(expression)

            self.txt_answer_field.setText(solution)

            self.add_record(expression, solution)
        except (ValueError, SyntaxError):
            QMessageBox.critical(self, 'Error', 'Invalid Expression! Please open another image!')
        except Exception as e:
            logging.exception(e)

#Solve the quadratic equation entered as image
    def process_quadratic_eq(self, image):
        try:
            equation = solver.extract(image)
            equation, solution = solver.solve_linear_equation(equation)

            self.add_record(equation, solution)

            solution = self.pretty(solution)
            self.txt_answer_field.setHtml(solution)
        except (ValueError, SyntaxError):
            QMessageBox.critical(self, 'Error', 'Invalid Equation! Please open another image!')
        except Exception as e:
            logging.exception(e)

#Solve the linear equation entered as image
    def process_linear_system(self, image):
        try:
            equations = solver.extract_linear_equations(image)
            solution = solver.solve_linear_system(equations)

            self.txt_answer_field.setText(solution)

            self.add_record(equations, solution)
        except (ValueError, SyntaxError):
            QMessageBox.critical(self, 'Error', 'Invalid system of linear equations! Please open another image!')
        except Exception as e:
            logging.exception(e)

#Solve the differentiation equation entered as image
    def process_derivative(self, image):
        try:
            equation = solver.extract(image)
            solution = solver.differentiate(equation)

            equation = re.sub(r"(\d)(x)", r"\1*\2", equation)
            equation = re.sub(r"(x)(\d)", r"\1**\2", equation)
            self.add_record(equation, "Derivative: " + solution)

            solution = self.pretty(solution)
            solution = solution.replace("*", "")

            self.txt_answer_field.setHtml(solution)
        except (ValueError, SyntaxError):
            QMessageBox.critical(self, 'Error', 'Could not differentiate the equation! Please open another image!')
        except Exception as e:
            logging.exception(e)

    def show_history(self):
        self.history_window.exec_()

    def clear(self):
        self.lbl_image.setPixmap(QPixmap())

    def display_info(self):
        mode = self.cb_select_equation_type.currentText()
        if mode == 'EXPRESSION':
            self.lbl_info.setText("<br>Solves expressions such as 5 + 2, 27 x 2 etc."
                                  "<br><br>Division is not supported.")
        if mode == 'QUADRATIC EQUATION':
            self.lbl_info.setText("<br>Solves quadratic equations such as 5x<sup>2</sup> + 1 = 0."
                                  "<br><br>Please enter an equation with the variable x only."
                                  "<br><br>Solutions may be complex numbers.")
        if mode == 'CUBIC EQUATION':
            self.lbl_info.setText("<br>Solves cubic equations such as 3x<sup>3</sup> + 2x<sup>2</sup> + 8x = 7."
                                  "<br><br>Please enter an equation with the variable x only."
                                  "<br><br>Solutions may be complex numbers.")
        if mode == 'LINEAR SYSTEM':
            self.lbl_info.setText("<br>Solves a linear system of equations such as:"
                                  "<br>x + 2y = 5"
                                  "<br>2x + 3y = 7"
                                  "<br><br>Please enter 2 equations with the variables x and y only.")
        if mode == 'DIFFERENTIATION':
            self.lbl_info.setText("<br>Finds the derivative of an expression such as 3x<sup>2</sup>"
                                  "<br><br>Do not prepend the expression with d/dx"
                                  "<br><br>Derivatives are calculated with respect to the variable x only")
    @staticmethod
    def pixmap_to_numpy(pixmap):
        image = pixmap.toImage()
        image = image.convertToFormat(QImage.Format_RGBA8888) #to convert an image into another format
        width, height = image.width(), image.height()
        ptr = image.bits()
        ptr.setsize(image.byteCount())
        image = np.array(ptr).reshape((height, width, 4))

        return image

    @staticmethod
    def pretty(text):
        text = text.replace("\n", "<br>")
        text = re.sub(r"sqrt\(([^)]+)\)", r"&radic;\1", text)

        text = re.sub(r"\*\*(\d)", r"<sup>\1</sup>", text)

        return text


def main():
    app = QApplication([]) #QApplication specializes QGuiApplication with some functionality needed for QWidget
    app.setStyle("Fusion")
    with open("style.css", 'r') as style:
        app.setStyleSheet(style.read())

    window = MainWindow() #for window management
    app.aboutToQuit.connect(window.close_connection)
    window.show()
    app.exec_()


if __name__ == "__main__":
    main()
