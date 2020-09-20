# Rodrigo Custodio

from PyQt5.QtWidgets import QApplication
from training import Trainer

import argparse
import os

def main():
    parser = argparse.ArgumentParser(description="Sketch identifier")
    parser.add_argument("-train", action="store_true", help="Train the CNN")
    parser.add_argument("-dir", type=str,
                        help="File directory for training samples")
    args = parser.parse_args()
    if not args.train:
        if __debug__:
            os.system("pyuic5 sketch/canvas.ui > sketch/ui.py")
        from sketch.main_window import MainWindow
        app = QApplication([])
        window = MainWindow()
        app.exec_()
    else:
        trainer = Trainer()
        trainer.train()


if __name__ == "__main__":
    main()
