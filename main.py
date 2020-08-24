####################################################
# You may only change the initial board here       #
# Any change other than board may result in crash  #
####################################################

from gui import App
from PyQt5.QtWidgets import QApplication
import sys
import chess

if __name__ == '__main__':
	app = QApplication(sys.argv)
	board = chess.Board("2k2R2/1b1p4/3B2r1/8/4q3/6P1/PPP5/1K1R4 b - - 0 1") #initial board is created here
	ex = App(board)
	app.exec_()
