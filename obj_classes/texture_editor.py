from __future__         import print_function, division
from PIL                import Image, ImageEnhance, ImageQt
from PyQt5.QtCore import center
from PyQt5.QtGui import QIcon, QPixmap
from obj_classes.vector import Vector
from PyQt5              import QtWidgets, QtGui, QtCore
import sys

class TextureEditor(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        winWidth = 1104
        winHeight = 662
        gutterSize = 10
        texSize = 256
        labelHeight = 60

        # Init window
        self.setGeometry(100, 100, winWidth, winHeight)
        self.setWindowTitle("Texturize Me Cap'n!")

        # Define the image to use here
        input = "./inputs/soil2.jpg"
        output= "./outputs/soil2.jpg"

        # Define how many levels of color we want (less levels = more bit-like)
        self.levels = 4

        # This just divides max range for RGB by # of levels
        step = 256 / max(1, (self.levels - 1))

        # Open the image we defined above
        self.img = Image.open(input)
        self.img = self.img.resize((256,256))

        # Create preview Box
        previewLabel = QtWidgets.QLabel(self)
        previewLabel.setText("Original")
        previewLabel.setGeometry(gutterSize,gutterSize, texSize, labelHeight)
        previewLabel.setAlignment(QtCore.Qt.AlignCenter)
        previewLabel.setFont(QtGui.QFont("Arial", 12))
        preview = QtWidgets.QLabel(self)
        preview.setGeometry(gutterSize,previewLabel.height()+gutterSize,texSize,texSize)
        preview.setPixmap(
            QtGui.QPixmap.fromImage(
                ImageQt.ImageQt(
                    self.img.resize((texSize,texSize))
                ).copy()
            )
        )

        # Create Adjusted Box
        enhancer = ImageEnhance.Contrast(self.img)
        self.adj = enhancer.enhance(1.5)
        adjustedLabel = QtWidgets.QLabel(self)
        adjustedLabel.setText("Adjusted")
        adjustedLabel.setGeometry(texSize+3*gutterSize,gutterSize,texSize,labelHeight)
        adjustedLabel.setAlignment(QtCore.Qt.AlignCenter)
        adjustedLabel.setFont(QtGui.QFont("Arial", 12))
        adjusted = QtWidgets.QLabel(self)
        adjusted.setGeometry(texSize+3*gutterSize,gutterSize+labelHeight,texSize,texSize)
        adjusted.setPixmap(
            QtGui.QPixmap.fromImage(
                ImageQt.ImageQt(
                    self.adj.resize((texSize,texSize))
                ).copy()
            )
        )

        # Create Greyscale Box
        self.gs = self.adj.copy()

        # Pull out the pixel data
        gsdata = self.gs.load()

        # Want to loop over the entire image
        for i in range(0,256):
            for j in range(0,256):
                # Define minDist to be something huge here (anything > 255 will work)
                minDist = 100000.0

                # Save the pixel value here (need to keep this for modifying)
                pix = gsdata[i,j]

                # Going to loop through our levels here i.e. clamp each pixel to the
                # nearest level
                for k in range(0,self.levels):
                    # So find our current level value (clamp at RGB max)
                    shade = int(min(255, step*k))
                    # Find the distance between the pixel and our level
                    dist = Vector(*pix).dist(Vector(shade,shade,shade))
                    # If the distance is smaller than anything we've seen, update the
                    # Color
                    if dist < minDist:
                        minDist = dist
                        gsdata[i,j] = (shade,shade,shade)

        greyscaleLabel = QtWidgets.QLabel(self)
        greyscaleLabel.setText("Greyscale")
        greyscaleLabel.setGeometry(2*texSize + 5*gutterSize,gutterSize,texSize,labelHeight)
        greyscaleLabel.setAlignment(QtCore.Qt.AlignCenter)
        greyscaleLabel.setFont(QtGui.QFont("Arial", 12))
        greyscale = QtWidgets.QLabel(self)
        greyscale.setGeometry(2*texSize + 5*gutterSize,gutterSize + labelHeight,texSize,texSize)
        greyscale.setPixmap(
            QtGui.QPixmap.fromImage(
                ImageQt.ImageQt(
                    self.gs.resize((texSize,texSize))
                ).copy()
            )
        )

        self.show()