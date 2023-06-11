from __future__         import print_function, division
from obj_classes.texture_editor import TextureEditor
from PIL                import Image, ImageEnhance, ImageQt
from PyQt5.QtCore import center
from PyQt5.QtGui import QIcon, QPixmap
from obj_classes.vector import Vector
from PyQt5              import QtWidgets, QtGui, QtCore
import sys

# app = QtWidgets.QApplication(sys.argv)
# ex = TextureEditor()
# app.exec()

# Set up window
app = QtWidgets.QApplication(sys.argv)
win = QtWidgets.QWidget()
winWidth = 1104
winHeight = 662
win.setGeometry(100, 100, winWidth, winHeight)
win.setWindowTitle("Texturize Me Cap'n!")


# Define the image to use here
input = "./inputs/soil2.jpg"
output= "./outputs/soil2.jpg"

# Define how many levels of color we want (less levels = more bit-like)
levels = 4

# This just divides max range for RGB by # of levels
step = 256 / max(1, (levels - 1))

# Open the image we defined above
img = Image.open(input)
img = img.resize((256,256))

# Create preview Box
previewLabel = QtWidgets.QLabel(win)
previewLabel.setText("Original")
previewLabel.setGeometry(10,10,256,60)
previewLabel.setAlignment(QtCore.Qt.AlignCenter)
previewLabel.setFont(QtGui.QFont("Arial", 12))
preview = QtWidgets.QLabel(win)
preview.setGeometry(10,70,256,256)
preview.setPixmap(
    QtGui.QPixmap.fromImage(
        ImageQt.ImageQt(
            img.resize((256,256))
        ).copy()
    )
)

# Create Adjusted Box
enhancer = ImageEnhance.Contrast(img)
adj = enhancer.enhance(1.5)
adjustedLabel = QtWidgets.QLabel(win)
adjustedLabel.setText("Adjusted")
adjustedLabel.setGeometry(286,10,256,60)
adjustedLabel.setAlignment(QtCore.Qt.AlignCenter)
adjustedLabel.setFont(QtGui.QFont("Arial", 12))
adjusted = QtWidgets.QLabel(win)
adjusted.setGeometry(286,70,256,256)
adjusted.setPixmap(
    QtGui.QPixmap.fromImage(
        ImageQt.ImageQt(
            adj.resize((256,256))
        ).copy()
    )
)

# Create Greyscale Box
gs = adj.copy()

# Pull out the pixel data
gsdata = gs.load()

# Want to loop over the entire image
for i in range(0,256):
    for j in range(0,256):
        # Define minDist to be something huge here (anything > 255 will work)
        minDist = 100000.0

        # Save the pixel value here (need to keep this for modifying)
        pix = gsdata[i,j]

        # Going to loop through our levels here i.e. clamp each pixel to the
        # nearest level
        for k in range(0,levels):
            # So find our current level value (clamp at RGB max)
            shade = int(min(255, step*k))
            # Find the distance between the pixel and our level
            dist = Vector(*pix).dist(Vector(shade,shade,shade))
            # If the distance is smaller than anything we've seen, update the
            # Color
            if dist < minDist:
                minDist = dist
                gsdata[i,j] = (shade,shade,shade)
greyscaleLabel = QtWidgets.QLabel(win)
greyscaleLabel.setText("Greyscale")
greyscaleLabel.setGeometry(562,10,256,60)
greyscaleLabel.setAlignment(QtCore.Qt.AlignCenter)
greyscaleLabel.setFont(QtGui.QFont("Arial", 12))
greyscale = QtWidgets.QLabel(win)
greyscale.setGeometry(562,70,256,256)
greyscale.setPixmap(
    QtGui.QPixmap.fromImage(
        ImageQt.ImageQt(
            gs.resize((256,256))
        ).copy()
    )
)

textureLabel = QtWidgets.QLabel(win)
textureLabel.setText("Texture")
textureLabel.setGeometry(838,10,256,60)
textureLabel.setAlignment(QtCore.Qt.AlignCenter)
textureLabel.setFont(QtGui.QFont("Arial", 12))
texture = QtWidgets.QLabel(win)
texture.setGeometry(838,70,256,256)
texture.setAlignment(QtCore.Qt.AlignCenter)
texture.setPixmap(
    QtGui.QPixmap.fromImage(
        ImageQt.ImageQt(
            gs.resize((32,32), resample=0).resize((256,256))
        ).copy()
    )
)

def saveCallback():
    global gs
    global output
    tex = gs.resize((32,32), resample=0)
    tex.save(output)

# Adjustment group

def enhanceSliderUpdate():
    return

enhanceSlider = QtWidgets.QSlider(win)
enhanceSlider.setMinimum(1.0)
enhanceSlider.setMaximum(20.0)
enhanceSlider.setOrientation(1)
enhanceSlider.setGeometry(10,406,winWidth-100, 40)
enhanceSlider.valueChanged.connect(enhanceSliderUpdate)
enhanceSliderLabel = QtWidgets.QLabel(win)
enhanceSliderLabel.setText("Enhancement")
enhanceSliderLabel.setGeometry(10,346,winWidth-40, 40)
enhanceSliderLabel.setFont(QtGui.QFont("Arial", 12))
enhanceSliderValueLabel = QtWidgets.QLabel(win)
enhanceSliderValueLabel.setFont(QtGui.QFont("Arial", 12))
enhanceSliderValueLabel.setText(str(enhanceSlider.value()))
enhanceSliderValueLabel.setGeometry(winWidth-80,406,60, 40)



# Save Button
saveBtn = QtWidgets.QPushButton(win)
saveBtn.setGeometry(10,386,256,60)
saveBtn.setText("Save Texture")
saveBtn.clicked.connect(saveCallback)


# Show Window
win.show()
sys.exit(app.exec_())