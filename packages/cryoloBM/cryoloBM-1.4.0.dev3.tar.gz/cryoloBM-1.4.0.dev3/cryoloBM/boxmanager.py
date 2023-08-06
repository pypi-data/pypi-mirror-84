import os
import sys
import matplotlib.pyplot as plt

from mrcfile import mmap as mrcfile_mmap        #it is not in the setup.py because it is already installed by cryolo
import numpy as np
import random
import time
try:
    QT = 4
    import PyQt4.QtGui as QtG
    import PyQt4.QtCore as QtCore
    from PyQt4.QtGui import QFontMetrics
    from PyQt4.QtCore import pyqtSlot
    import matplotlib.backends.backend_qt4agg as plt_qtbackend
except ImportError:
    QT = 5
    import PyQt5.QtWidgets as QtG
    from PyQt5.QtGui import QFontMetrics
    import PyQt5.QtCore as QtCore
    from PyQt5.QtCore import pyqtSlot
    import matplotlib.backends.backend_qt5agg as plt_qtbackend


from cryolo import imagereader, CoordsIO
from . import boxmanager_toolbar, MyRectangle, helper, helper_writer
import argparse

argparser = argparse.ArgumentParser(
    description="Train and validate crYOLO on any dataset",
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
)

argparser.add_argument("-i", "--image_dir", help="Path to image directory.")

argparser.add_argument("-b", "--box_dir", help="Path to box directory.")

argparser.add_argument("--wildcard", help="Wildcard for selecting specific images (e.g *_new_*.mrc)")

argparser.add_argument("-t", "--is_tomo_dir", action="store_true", help="Flag for specifying that the directory contains tomograms.")

DEFAULT_BOX_SIZE = 200

class MainWindow(QtG.QMainWindow):
    def __init__(self, font, images_path=None, boxes_path=None, wildcard=None, parent=None, is_tomo_dir=None):
        self.is_folder_3D_tomo = False
        self.is_3D_tomo=False
        self.index_3D_tomo=None
        self.im = None
        self.rectangles = []
        self.current_image3D_mmap = None

        # last* variables are used to clean the boxes when we switch between 3D tomo images in a list of images
        self.last_file_3D_tomo=None
        self.last_index_3D_tomo = None
        self.last_filename_in_tomo_folder = None

        super(MainWindow, self).__init__(parent)
        # SETUP QT
        self.font = font
        self.setWindowTitle("Box manager")
        central_widget = QtG.QWidget(self)

        self.setCentralWidget(central_widget)

        # Center on screen
        resolution = QtG.QDesktopWidget().screenGeometry()
        self.move(
            (resolution.width() / 2) - (self.frameSize().width() / 2),
            (resolution.height() / 2) - (self.frameSize().height() / 2),
        )

        # Setup Menu
        close_action = QtG.QAction("Close", self)
        close_action.setShortcut("Ctrl+Q")
        close_action.setStatusTip("Leave the app")
        close_action.triggered.connect(self.close_boxmanager)

        open_image_folder = QtG.QAction("Micrograph folder", self)
        open_image_folder.triggered.connect(self.open_image_folder)

        open_image_3D_folder = QtG.QAction("Folder", self)
        open_image_3D_folder.triggered.connect(self.open_image3D_folder)

        open_image3D_tomo = QtG.QAction("file", self)
        open_image3D_tomo.triggered.connect(self.open_image3D_tomo)

        import_box_folder = QtG.QAction("Import box files", self)
        import_box_folder.triggered.connect(self.load_box_files)

        save_data = QtG.QAction("Save", self)
        save_data.triggered.connect(self.write_all_type)

        self.show_confidence_histogram_action = QtG.QAction(
            "Confidence histogram", self
        )
        self.show_confidence_histogram_action.triggered.connect(
            self.show_confidence_histogram
        )
        self.show_confidence_histogram_action.setEnabled(False)

        self.show_size_distribution_action = QtG.QAction("Size distribution", self)
        self.show_size_distribution_action.triggered.connect(
            self.show_size_distribution
        )
        self.show_size_distribution_action.setEnabled(False)

        self.mainMenu = self.menuBar()
        self.fileMenu = self.mainMenu.addMenu("&File")
        openMenu = self.fileMenu.addMenu("&Open")
        openMenuSPA = openMenu.addMenu("&SPA")
        openMenuTomo = openMenu.addMenu("&Tomogram")
        openMenuSPA.addAction(open_image_folder)
        openMenuTomo.addAction(open_image_3D_folder)
        openMenuTomo.addAction(open_image3D_tomo)

        self.fileMenu.addAction(import_box_folder)
        self.fileMenu.addAction(save_data)

        self.fileMenu.addAction(close_action)
        self.image_folder = ""

        self.plotMenu = self.mainMenu.addMenu("&Plot")
        self.plotMenu.addAction(self.show_confidence_histogram_action)
        self.plotMenu.addAction(self.show_size_distribution_action)

        # Setup tree
        self.layout = QtG.QGridLayout(central_widget)
        self.setMenuBar(self.mainMenu)

        self.tree = QtG.QTreeWidget(self)
        self.tree.setHeaderHidden(True)
        self.layout.addWidget(self.tree, 0, 0, 1, 3)
        self.tree.currentItemChanged.connect(self._event_image_changed)
        line_counter = 1

        # Box size setup
        self.boxsize = DEFAULT_BOX_SIZE
        self.boxsize_label = QtG.QLabel()
        self.boxsize_label.setText("Box size: ")
        self.layout.addWidget(self.boxsize_label, line_counter, 0)

        self.boxsize_line = QtG.QLineEdit()
        self.boxsize_line.setText(str(self.boxsize))
        self.boxsize_line.returnPressed.connect(self.box_size_changed)
        self.layout.addWidget(self.boxsize_line, line_counter, 1)

        self.button_set_box_size = QtG.QPushButton("Set")
        self.button_set_box_size.clicked.connect(self.box_size_changed)
        self.layout.addWidget(self.button_set_box_size, line_counter, 2)
        line_counter = line_counter + 1

        # Show estimated size
        self.use_estimated_size_label = QtG.QLabel()
        self.use_estimated_size_label.setText("Use estimated size:")
        self.use_estimated_size_label.setEnabled(False)
        self.layout.addWidget(self.use_estimated_size_label, line_counter, 0)

        self.use_estimated_size_checkbox = QtG.QCheckBox()
        self.layout.addWidget(self.use_estimated_size_checkbox, line_counter, 1)
        self.use_estimated_size_checkbox.stateChanged.connect(
            self.use_estimated_size_changed
        )
        self.use_estimated_size_checkbox.setEnabled(False)
        line_counter = line_counter + 1

        # Lower size
        self.lower_size_thresh = 0
        self.lower_size_thresh_label = QtG.QLabel()
        self.lower_size_thresh_label.setText("Minimum size: ")
        self.layout.addWidget(self.lower_size_thresh_label, line_counter, 0)
        self.lower_size_thresh_label.setEnabled(False)
        self.lower_size_thresh_slide = QtG.QSlider(QtCore.Qt.Horizontal)
        self.lower_size_thresh_slide.setMinimum(0)
        self.lower_size_thresh_slide.setMaximum(500)
        self.lower_size_thresh_slide.setValue(0)
        self.lower_size_thresh_slide.valueChanged.connect(
            self.lower_size_thresh_changed
        )
        self.lower_size_thresh_slide.setTickPosition(QtG.QSlider.TicksBelow)
        self.lower_size_thresh_slide.setTickInterval(1)
        self.lower_size_thresh_slide.setEnabled(False)
        self.layout.addWidget(self.lower_size_thresh_slide, line_counter, 1)

        self.lower_size_thresh_line = QtG.QLineEdit()
        self.lower_size_thresh_line.setText("0")
        self.lower_size_thresh_line.textChanged.connect(self.lower_size_label_changed)
        self.lower_size_thresh_line.setEnabled(False)
        self.layout.addWidget(self.lower_size_thresh_line, line_counter, 2)

        line_counter = line_counter + 1

        # Upper size threshold
        self.upper_size_thresh = 99999
        self.upper_size_thresh_label = QtG.QLabel()
        self.upper_size_thresh_label.setText("Maximum size: ")
        self.layout.addWidget(self.upper_size_thresh_label, line_counter, 0)
        self.upper_size_thresh_label.setEnabled(False)
        self.upper_size_thresh_slide = QtG.QSlider(QtCore.Qt.Horizontal)
        self.upper_size_thresh_slide.setMinimum(0)
        self.upper_size_thresh_slide.setMaximum(99999)
        self.upper_size_thresh_slide.setValue(99999)
        self.upper_size_thresh_slide.valueChanged.connect(
            self.upper_size_thresh_changed
        )
        self.upper_size_thresh_slide.setTickPosition(QtG.QSlider.TicksBelow)
        self.upper_size_thresh_slide.setTickInterval(1)
        self.upper_size_thresh_slide.setEnabled(False)
        self.layout.addWidget(self.upper_size_thresh_slide, line_counter, 1)

        self.upper_size_thresh_line = QtG.QLineEdit()
        self.upper_size_thresh_line.setText("99999")
        self.upper_size_thresh_line.textChanged.connect(self.upper_size_label_changed)
        self.upper_size_thresh_line.setEnabled(False)
        self.layout.addWidget(self.upper_size_thresh_line, line_counter, 2)

        line_counter = line_counter + 1

        # Confidence threshold setup
        self.current_conf_thresh = 0.3
        self.conf_thresh_label = QtG.QLabel()
        self.conf_thresh_label.setText("Confidence threshold: ")
        self.layout.addWidget(self.conf_thresh_label, line_counter, 0)
        self.conf_thresh_label.setEnabled(False)
        self.conf_thresh_slide = QtG.QSlider(QtCore.Qt.Horizontal)
        self.conf_thresh_slide.setMinimum(0)
        self.conf_thresh_slide.setMaximum(100)
        self.conf_thresh_slide.setValue(30)
        self.conf_thresh_slide.valueChanged.connect(self.conf_thresh_changed)
        self.conf_thresh_slide.setTickPosition(QtG.QSlider.TicksBelow)
        self.conf_thresh_slide.setTickInterval(1)
        self.conf_thresh_slide.setEnabled(False)
        self.layout.addWidget(self.conf_thresh_slide, line_counter, 1)

        self.conf_thresh_line = QtG.QLineEdit()
        self.conf_thresh_line.setText("0.3")
        self.conf_thresh_line.textChanged.connect(self.conf_thresh_label_changed)
        self.conf_thresh_line.setEnabled(False)
        self.layout.addWidget(self.conf_thresh_line, line_counter, 2)

        line_counter = line_counter + 1

        # Low pass filter setup
        self.filter_freq = 0.1
        self.filter_label = QtG.QLabel()
        self.filter_label.setText("Low pass filter cut-off: ")
        self.layout.addWidget(self.filter_label, line_counter, 0)

        self.filter_line = QtG.QLineEdit()
        self.filter_line.setText(str(self.filter_freq))
        self.layout.addWidget(self.filter_line, line_counter, 1)

        self.button_apply_filter = QtG.QPushButton("Apply")
        self.button_apply_filter.clicked.connect(self.apply_filter)
        self.button_apply_filter.setEnabled(False)
        self.layout.addWidget(self.button_apply_filter, line_counter, 2)

        # self.button_set_conf_thresh = QtG.QPushButton("Set")
        # self.button_set_conf_thresh.clicked.connect(self.conf_thresh_changed)
        # self.layout.addWidget(self.button_set_conf_thresh, 2, 2)

        # Show image selection
        self.show()



        # in case of folder of tomo it will be a dict of Thorsten original self.box_dictionary .
        # k1=tomo_filename v1=dict (same as Thorsten original self.box_dictionary)
        self.box_dictionary = {}

        # k=tomo_filename v= item
        self.item_3D_filename = {}

        self.plot = None
        self.fig = None
        self.ax = None

        self.moving_box = None

        self.zoom_update = False
        self.doresizing = False
        self.current_image_path = None
        self.background_current = None
        self.unsaved_changes = False
        self.is_cbox = False
        self.toggle = False
        self.use_estimated_size = False
        self.wildcard = wildcard
        if images_path:
            if is_tomo_dir is True:
                img_loaded = self._open_image3D_folder(images_path)
                self.is_folder_3D_tomo = True
            else:
                img_loaded = self._open_image_folder(images_path)
            if img_loaded:
                self.button_apply_filter.setEnabled(True)
            if boxes_path:
                if is_tomo_dir is False:
                    self._import_boxes(box_dir=boxes_path, keep=False)
                else:
                    self._import_boxes_3D_tomo_folder(box_dir=boxes_path, keep=False)

    def close_boxmanager(self):
        if self.unsaved_changes:
            msg = "All loaded boxes are discarded. Are you sure?"
            reply = QtG.QMessageBox.question(
                self, "Message", msg, QtG.QMessageBox.Yes, QtG.QMessageBox.Cancel
            )

            if reply == QtG.QMessageBox.Cancel:
                return
        self.close()

    def _set_first_time_img(self,im):
        """
        Set the variable to show an image
        :param im: np array
        :return: none
        """
        # Create figure and axes
        self.fig, self.ax = plt.subplots(1)

        self.ax.xaxis.set_visible(False)
        self.ax.yaxis.set_visible(False)

        self.fig.tight_layout()
        self.fig.canvas.set_window_title(
            os.path.basename(self.current_image_path)
        )
        # Display the image
        self.im = self.ax.imshow(
            im, origin="lower", cmap="gray", interpolation="Hanning"
        )  #

        self.plot = QtG.QDialog(self)
        self.plot.canvas = plt_qtbackend.FigureCanvasQTAgg(self.fig)
        self.plot.canvas.mpl_connect("button_press_event", self.onclick)
        self.plot.canvas.mpl_connect("key_press_event", self.myKeyPressEvent)
        self.plot.canvas.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.plot.canvas.setFocus()
        self.plot.canvas.mpl_connect("button_release_event", self.onrelease)
        self.plot.canvas.mpl_connect("motion_notify_event", self.onmove)
        self.plot.canvas.mpl_connect("resize_event", self.onresize)
        self.plot.canvas.mpl_connect("draw_event", self.ondraw)
        self.plot.toolbar = boxmanager_toolbar.Boxmanager_Toolbar(
            self.plot.canvas, self.plot, self.fig, self.ax, self
        )  # plt_qtbackend.NavigationToolbar2QT(self.plot.canvas, self.plot)
        layout = QtG.QVBoxLayout()
        layout.addWidget(self.plot.toolbar)
        layout.addWidget(self.plot.canvas)
        self.plot.setLayout(layout)
        self.plot.canvas.draw()
        self.plot.show()
        self.background_current = self.fig.canvas.copy_from_bbox(self.ax.bbox)
        self.background_orig = self.fig.canvas.copy_from_bbox(self.ax.bbox)



    def _event_image_changed(self, root_tree_item):

            if (
                root_tree_item is not None
                and root_tree_item.childCount() == 0
                and self.current_image_path is not None
            ):
                if self.is_folder_3D_tomo is True:
                    self.current_image_path = os.path.join(self.image_folder,root_tree_item.parent().text(0))

                if self.is_3D_tomo is False:
                    self.current_tree_item = root_tree_item
                    filename = root_tree_item.text(0)
                    pure_filename = os.path.splitext(os.path.basename(self.current_image_path))[
                        0
                    ]

                    if pure_filename in self.box_dictionary:
                        self.rectangles = self.box_dictionary[pure_filename]
                        self.delete_all_patches(self.rectangles)
                    else:
                        self.rectangles = []
                    prev_size = imagereader.read_width_height(self.current_image_path)
                    self.current_image_path = os.path.join(self.image_folder, str(filename))
                    self.fig.canvas.set_window_title(os.path.basename(self.current_image_path))
                    img = helper.read_image(self.current_image_path)
                    prev_size = prev_size[::-1]
                    if prev_size == img.shape:
                        self.im.set_data(img)
                    else:
                        self.im = self.ax.imshow(
                            img, origin="lower", cmap="gray", interpolation="Hanning"
                        )


                    self.plot.setWindowTitle(os.path.basename(self.current_image_path))
                    self.fig.canvas.draw()
                    self.background_current = self.fig.canvas.copy_from_bbox(self.ax.bbox)
                    self.background_orig = self.fig.canvas.copy_from_bbox(self.ax.bbox)
                    self.update_boxes_on_current_image()
                else:
                    if self.is_folder_3D_tomo is True:
                        pure_filename = os.path.splitext(os.path.basename(self.current_image_path.split('/')[-1]))[0]

                        # allow to separate the boxes present in the 'index_3D_tomo' slice between different tomo
                        if self.last_filename_in_tomo_folder != pure_filename:
                            self.delete_all_patches(self.rectangles)
                            self.current_image3D_mmap= helper.read_image(self.current_image_path, use_mmap=True)
                            self.last_filename_in_tomo_folder=pure_filename

                        # load the boxes already selected in the 'index_3D_tomo' slice
                        if pure_filename in self.box_dictionary and self.index_3D_tomo in self.box_dictionary[pure_filename]:
                            self.rectangles = self.box_dictionary[pure_filename][self.index_3D_tomo]
                        self.last_file_3D_tomo = pure_filename
                        self.delete_all_patches(self.rectangles)
                    elif self.index_3D_tomo in self.box_dictionary :
                        self.rectangles = self.box_dictionary[self.index_3D_tomo]
                        self.delete_all_patches(self.rectangles)
                        self.last_index_3D_tomo = self.index_3D_tomo
                    else:
                        self.rectangles = []

                    #imgdata = self.read_image(self.current_image_path, use_mmap=True) #imagereader.image_read(self.current_image_path, use_mmap=True)
                    #with mrcfile_mmap(self.current_image_path, permissive=True,
                    #                      mode="r") as mrc:
                    self.index_3D_tomo = int(root_tree_item.text(0))
                    self.last_index_3D_tomo = self.index_3D_tomo

                    self.im.set_data(self.current_image3D_mmap[self.index_3D_tomo, :, :])                   # all the slice have the same size

                    title=os.path.basename(self.current_image_path)+"\tindex: "+str(self.index_3D_tomo)
                    self.plot.setWindowTitle(title)
                    self.fig.canvas.draw()
                    self.background_current = self.fig.canvas.copy_from_bbox(self.ax.bbox)
                    self.background_orig = self.fig.canvas.copy_from_bbox(self.ax.bbox)
                    self.update_boxes_on_current_image()
                    print("3D tomo implementing ... pressed index tomo: "+str(self.index_3D_tomo))

    def lower_size_label_changed(self):
        try:
            new_value = int(float(self.lower_size_thresh_line.text()))
            upper_value = self.upper_size_thresh_slide.value()
            if new_value >= upper_value:
                return
        except ValueError:
            return
        self.lower_size_thresh_slide.setValue(new_value)

    def upper_size_label_changed(self):
        try:
            new_value = int(float(self.upper_size_thresh_line.text()))
            lower_value = self.lower_size_thresh_slide.value()
            if new_value <= lower_value:
                return
        except ValueError:
            return
        self.upper_size_thresh_slide.setValue(new_value)

    @pyqtSlot()
    def conf_thresh_label_changed(self):
        try:
            new_value = float(self.conf_thresh_line.text())
            if new_value > 1.0 or new_value < 0:
                return
        except ValueError:
            return
        self.current_conf_thresh = new_value
        self.conf_thresh_slide.setValue(new_value * 100)

    @pyqtSlot()
    def conf_thresh_changed(self):
        try:
            self.current_conf_thresh = float(self.conf_thresh_slide.value()) / 100
        except ValueError:
            return
        try:
            if (
                np.abs(float(self.conf_thresh_line.text()) - self.current_conf_thresh)
                >= 0.01
            ):
                self.conf_thresh_line.setText("" + str(self.current_conf_thresh))
        except ValueError:
            self.conf_thresh_line.setText("" + str(self.current_conf_thresh))

        if self.is_3D_tomo:
            self.update_3D_counter()

        self.update_boxes_on_current_image()
        self.fig.canvas.restore_region(self.background_current)
        self._draw_all_boxes()
        self.unsaved_changes = True
        self.update_tree_boxsizes()

    def upper_size_thresh_changed(self):
        self.upper_size_thresh = int(float(self.upper_size_thresh_slide.value()))
        self.upper_size_thresh_line.setText("" + str(self.upper_size_thresh))
        if self.upper_size_thresh <= self.lower_size_thresh:
            self.lower_size_thresh_slide.setValue(self.upper_size_thresh - 1)
        self.update_boxes_on_current_image()
        self.fig.canvas.restore_region(self.background_current)
        self._draw_all_boxes()
        self.unsaved_changes = True
        self.update_tree_boxsizes()

    def lower_size_thresh_changed(self):
        self.lower_size_thresh = int(float(self.lower_size_thresh_slide.value()))
        self.lower_size_thresh_line.setText("" + str(self.lower_size_thresh))
        if self.lower_size_thresh >= self.upper_size_thresh:
            self.upper_size_thresh_slide.setValue(self.lower_size_thresh + 1)
        self.update_boxes_on_current_image()
        self.fig.canvas.restore_region(self.background_current)
        self._draw_all_boxes()
        self.unsaved_changes = True
        self.update_tree_boxsizes()

    def show_confidence_histogram(self):
        import matplotlib as mpl

        confidence = []
        for box in self.rectangles:
            confidence.append(box.confidence)
        fig = plt.figure()
        # mpl.rcParams["figure.dpi"] = 200
        # mpl.rcParams.update({"font.size": 7})
        width = max(10, int((np.max(confidence) - np.min(confidence)) / 0.05))
        plt.hist(confidence, bins=width)
        plt.title("Confidence distribution")
        bin_size_str = "{0:.2f}".format(
            ((np.max(confidence) - np.min(confidence)) / width)
        )
        plt.xlabel("Confidence (Bin size: " + bin_size_str + ")")
        plt.ylabel("Count")

        plot = QtG.QDialog(self)
        plot.canvas = plt_qtbackend.FigureCanvasQTAgg(fig)
        layout = QtG.QVBoxLayout()
        layout.addWidget(plot.canvas)
        plot.setLayout(layout)
        plot.setWindowTitle("Size distribution")
        plot.canvas.draw()
        plot.show()

    def show_size_distribution(self):
        import matplotlib as mpl

        estimated_size = []
        for ident in self.box_dictionary:
            for box in self.box_dictionary[ident]:
                estimated_size.append(box.est_size)
        fig = plt.figure()
        # mpl.rcParams["figure.dpi"] = 200
        # mpl.rcParams.update({"font.size": 7})
        width = max(10, int((np.max(estimated_size) - np.min(estimated_size)) / 10))
        plt.hist(estimated_size, bins=width)
        plt.title("Particle diameter distribution")
        plt.xlabel("Partilce diameter [px] (Bin size: " + str(width) + "px )")
        plt.ylabel("Count")

        plot = QtG.QDialog(self)
        plot.canvas = plt_qtbackend.FigureCanvasQTAgg(fig)
        layout = QtG.QVBoxLayout()
        layout.addWidget(plot.canvas)
        plot.setLayout(layout)
        plot.setWindowTitle("Size distribution")
        plot.canvas.draw()
        plot.show()

    def apply_filter(self):
        try:
            self.filter_freq = float(self.filter_line.text())
        except ValueError:
            return
        if self.filter_freq < 0.5 and self.filter_freq >= 0:
            import cryolo.lowpass as lp

            if self.is_3D_tomo is False:
                img = lp.filter_single_image(self.current_image_path, self.filter_freq)
                im_type = helper.get_file_type(self.current_image_path)
                img = helper.normalize_and_flip(img,im_type)
            else:
                img = helper.read_image(self.current_image_path,use_mmap=True)
                img = lp.filter_single_image_from_np_array(img[self.index_3D_tomo, :, :],self.filter_freq)
            img = np.squeeze(img)
            self.delete_all_patches(self.rectangles)
            self.im.set_data(img)
            self.fig.canvas.draw()
            self.background_current = self.fig.canvas.copy_from_bbox(self.ax.bbox)
            self.background_orig = self.fig.canvas.copy_from_bbox(self.ax.bbox)
            self.update_boxes_on_current_image()
        else:
            msg = "Frequency has to be between 0 and 0.5."
            QtG.QMessageBox.information(self, "Message", msg)


    def box_size_changed(self):
        try:
            self.boxsize = int(float(self.boxsize_line.text()))
        except ValueError:
            return
        if self.boxsize >= 0:
            #for _, rectangles in self.box_dictionary.items():
            #    QtCore.QCoreApplication.instance().processEvents()
            #for rect in self.rectangles:
            #    if self.use_estimated_size:
            #        self.resize_box(rect, rect.est_size)
            #    else:
            #        self.resize_box(rect, self.boxsize)

            if self.background_current:
                self.update_boxes_on_current_image()
                self.fig.canvas.restore_region(self.background_current)
                self._draw_all_boxes()
                self.unsaved_changes = True
            if self.is_3D_tomo:
                self.update_3D_counter()
                self.update_tree_boxsizes()


    @pyqtSlot()
    def use_estimated_size_changed(self):
        self.use_estimated_size = self.use_estimated_size_checkbox.isChecked()
        self.box_size_changed()
        self.button_set_box_size.setEnabled(not self.use_estimated_size)
        self.boxsize_line.setEnabled(not self.use_estimated_size)
        self.boxsize_label.setEnabled(not self.use_estimated_size)

        self.upper_size_thresh_line.setEnabled(self.use_estimated_size)
        self.upper_size_thresh_slide.setEnabled(self.use_estimated_size)

        self.lower_size_thresh_line.setEnabled(self.use_estimated_size)
        self.lower_size_thresh_slide.setEnabled(self.use_estimated_size)

    def delete_all_boxes(self):
        if self.is_folder_3D_tomo is True:
            for filename in self.box_dictionary.keys():
                for _, rectangles in self.box_dictionary[filename].items():
                    self.delete_all_patches(rectangles)
        else:
            for _, rectangles in self.box_dictionary.items():
                self.delete_all_patches(rectangles)

        self.rectangles = []

        self.clean_box_dictionary()

        self.update_boxes_on_current_image()
        if self.background_current is not None:
            self.fig.canvas.restore_region(self.background_current)

    def update_boxes_on_current_image(self):
        if self.current_image_path is None:
            return

        if self.is_folder_3D_tomo is True:
            pure_filename = os.path.splitext(os.path.basename(self.current_image_path.split('/')[-1]))[0]
            if pure_filename in self.box_dictionary and self.index_3D_tomo in self.box_dictionary[pure_filename]:
                self.rectangles = self.box_dictionary[pure_filename][self.index_3D_tomo]
                self.delete_all_patches(self.rectangles, update=True)
                self.draw_all_patches(self.rectangles)
                self._draw_all_boxes()
        else:
            # if it is a single 3D image tomo pure_filename identifies the slice of the tomo
            pure_filename = os.path.splitext(os.path.basename(self.current_image_path))[0] if self.is_3D_tomo is False else self.index_3D_tomo
            if pure_filename in self.box_dictionary:
                self.rectangles = self.box_dictionary[pure_filename]
                self.delete_all_patches(self.rectangles, update=True)
                self.draw_all_patches(self.rectangles)
                self._draw_all_boxes()

    def delete_all_patches(self, rects, update=False):
        state = self.get_filter_state()
        for box in rects:
            if helper.check_if_should_be_visible(box,self.current_conf_thresh, self.upper_size_thresh, self.lower_size_thresh)==False or update==False:
                rect = box.getRect()
                rect.set_visible(False)
                if rect.is_figure_set():
                    rect.remove()
            if not helper.filter_tuple_is_equal(self.get_filter_state(),state):
                break


    def write_all_type(self):
        box_dir = str(QtG.QFileDialog.getExistingDirectory(self, "Select Box Directory"))
        if box_dir == "":
            return

        # Remove untitled from path if untitled not exists
        if box_dir[-8] == "untitled" and os.path.isdir(box_dir):
            box_dir = box_dir[:-8]

        if box_dir == "":
            return

        for file_type in ["STAR", "CBOX", "BOX"]:
            file_name = self.current_image_path.split("/")[-1].split(".")[0]
            d = os.path.join(box_dir, file_type)

            file_ext, write_coords_ = helper_writer.prepare_vars_for_writing(box_dir, file_type, self.is_3D_tomo)

            pd = QtG.QProgressDialog("Write box files to " + box_dir, "Cancel", 0, 100, self)
            pd.show()
            if self.is_folder_3D_tomo is True:
                helper_writer.write_coordinates_3d_folder(pd, self.box_dictionary, self.is_folder_3D_tomo, self.is_cbox,
                                                          self.current_conf_thresh, self.upper_size_thresh,
                                                          self.lower_size_thresh, self.boxsize, write_coords_, file_ext,
                                                          d)
                continue

            helper_writer.write_coordinates(pd, self.box_dictionary, file_name, d, self.is_3D_tomo, file_ext,
                                            self.is_cbox, self.current_conf_thresh,
                                            self.upper_size_thresh, self.lower_size_thresh, self.boxsize, write_coords_)

        self.unsaved_changes = False


    def load_box_files(self):
        self.is_cbox = False
        keep = False
        if self.unsaved_changes:
            msg = "There are unsaved changes. Are you sure?"
            reply = QtG.QMessageBox.question(
                self, "Message", msg, QtG.QMessageBox.Yes, QtG.QMessageBox.Cancel
            )

            if reply == QtG.QMessageBox.Cancel:
                return

        # It considers the 3d single image or the 2D_images folder
        show_question_box = len(self.box_dictionary) > 0 and self.is_folder_3D_tomo is False


        if self.is_folder_3D_tomo is True:
            for f in self.box_dictionary.keys():
                if len(self.box_dictionary[f]) > 0:
                    show_question_box = True
                    break

        if show_question_box:
            msg = "Keep old boxes loaded and show the new ones in a different color?"
            reply = QtG.QMessageBox.question(
                self, "Message", msg, QtG.QMessageBox.Yes, QtG.QMessageBox.No
            )

            if reply == QtG.QMessageBox.Yes:
                keep = True

        if keep == False:
            self.delete_all_boxes()

        if self.plot is not None or self.is_folder_3D_tomo is True:
            box_dir = str(
                QtG.QFileDialog.getExistingDirectory(self, "Select Box Directory")
            )

            if box_dir == "":
                return
            if self.is_3D_tomo is False:
                self._import_boxes(box_dir, keep)
            elif self.is_folder_3D_tomo is True:
                self._import_boxes_3D_tomo_folder(box_dir, keep)
            else:
                self._import_boxes_3D_tomo(box_dir, keep)

            if self.is_3D_tomo:
                self.update_3D_counter()

        else:
            errmsg = QtG.QErrorMessage(self)
            errmsg.showMessage("Please open an image folder first")



    def _import_boxes_3D_tomo_folder(self, box_dir, keep=False):
        """
        It is the adaptation of '_import_boxes_3D_tomo' to work on the 'Open 3D image folder' case
        """
        import time as t

        t_start = t.time()

        all_image_filenames = helper.get_all_loaded_filesnames(self.tree.invisibleRootItem().child(0))

        onlyfiles = [
            f
            for f in os.listdir(box_dir)
            if os.path.isfile(os.path.join(box_dir, f))
            and not f.startswith(".")
            and os.path.splitext(f)[0] in all_image_filenames
            and (f.endswith(".box") or f.endswith(".star") or f.endswith(".cbox"))

        ]
        for fname in onlyfiles:
            path_3d_file = os.path.join(box_dir,fname)

            is_star_file = path_3d_file.split(".")[-1] =="star"
            is_cbox_file = path_3d_file.endswith(".cbox")

            fname=path_3d_file.split(".")[0].split("/")[-1]

            if keep is False:
                rand_color = "r"
            else:
                rand_color = random.choice(["b", "c", "m", "y", "k", "w"])

            self.setWindowTitle("Box manager (Showing: " + box_dir + ")")
            box_imported = 0

            if is_star_file:
                boxes = CoordsIO.read_star_file(path_3d_file,self.boxsize)
            elif is_cbox_file:
                boxes = CoordsIO.read_cbox_boxfile(path_3d_file)
                self.is_cbox = True
            else:
                boxes = CoordsIO.read_eman1_boxfile(path_3d_file)

            for box in boxes:
                rect = self.box_to_rectangle(box, rand_color)
                box_imported += 1
                if int(box.z) in self.box_dictionary[fname]:
                    self.box_dictionary[fname][int(box.z)].append(rect)
                else:
                    self.box_dictionary[fname][int(box.z)] = [rect]

            self.show_loaded_boxes(self.box_dictionary[fname])

            print("Total time", t.time() - t_start)
            print("Total imported particles: ", box_imported)


    def _import_boxes_3D_tomo(self, box_dir, keep=False):
        import time as t

        t_start = t.time()
        fname=self.current_image_path.split("/")[-1].split(".")[0]
        path_3d_file = os.path.join(box_dir,fname)

        if os.path.isfile(path_3d_file+".star") is True:
            boxes = CoordsIO.read_star_file(path_3d_file+".star",self.boxsize)
        elif os.path.isfile(path_3d_file+".box") is True:
            boxes = CoordsIO.read_eman1_boxfile(path_3d_file+".box")
        elif os.path.isfile(path_3d_file+".cbox") is True:
            boxes = CoordsIO.read_cbox_boxfile(path_3d_file+".cbox")
            #hm = 100
            #boxes = [box for box in boxes if
            #         box.x > (336 - hm) and box.x < (336 + hm) and box.y > (336 - hm) and box.y < (
            #                     336 + hm)]
            self.is_cbox = True
        else:
            errmsg = QtG.QErrorMessage(self)
            errmsg.showMessage("Error: no valid .star, .box or .cbox files found in directory '"+box_dir+"'")
            return

        if keep is False:
            rand_color = "r"
        else:
            rand_color = random.choice(["b", "c", "m", "y", "k", "w"])

        self.setWindowTitle("Box manager (Showing: " + box_dir + ")")
        box_imported = 0

        for  box in boxes:
            rect = self.box_to_rectangle(box, rand_color)
            box_imported += 1
            if box.z in self.box_dictionary:
                self.box_dictionary[int(box.z)].append(rect)
            else:
                self.box_dictionary[int(box.z)] = [rect]

        self.show_loaded_boxes(self.box_dictionary)

        print("Total time", t.time() - t_start)
        print("Total imported particles: ", box_imported)


    def _import_boxes(self, box_dir, keep=False):
        import time as t

        t_start = t.time()
        self.setWindowTitle("Box manager (Showing: " + box_dir + ")")
        box_imported = 0
        all_image_filenames = helper.get_all_loaded_filesnames(self.tree.invisibleRootItem().child(0))

        onlyfiles = [
            f
            for f in os.listdir(box_dir)
            if os.path.isfile(os.path.join(box_dir, f))
            and not f.startswith(".")
            and os.path.splitext(f)[0] in all_image_filenames
            and (
                f.endswith(".box")
                or f.endswith(".txt")
                or f.endswith(".star")
                or f.endswith(".cbox")
            )
            and os.stat(os.path.join(box_dir, f)).st_size != 0
        ]
        colors = ["b", "r", "c", "m", "y", "k", "w"]
        if keep == False:
            rand_color = "r"
        else:
            rand_color = random.choice(colors)
            while rand_color == "r":
                rand_color = random.choice(colors)
        star_dialog_was_shown = False
        filaments_imported = 0

        self.conf_thresh_line.setEnabled(False)
        self.conf_thresh_slide.setEnabled(False)
        self.conf_thresh_label.setEnabled(False)
        self.use_estimated_size_label.setEnabled(False)
        self.use_estimated_size_checkbox.setEnabled(False)
        self.show_confidence_histogram_action.setEnabled(False)
        self.show_size_distribution_action.setEnabled(False)


        if len(onlyfiles)>0:
            pd = QtG.QProgressDialog("Load box files...", "Cancel", 0, 100, self)
            pd.show()

        is_star_startend = False
        for file_index, file in enumerate(onlyfiles):
            if pd.wasCanceled():
                break
            else:
                pd.show()
                pd.setValue(int((file_index + 1) * 100 / len(onlyfiles)))
            QtCore.QCoreApplication.instance().processEvents()

            path = os.path.join(box_dir, file)
            is_eman1_startend = False


            is_helicon = CoordsIO.is_eman1_helicon(path)
            if not is_helicon:
                is_eman1_startend = CoordsIO.is_eman1_filament_start_end(path)

            if not is_helicon and not is_eman1_startend:
                if file.endswith(".star") and star_dialog_was_shown == False:
                    msg = "Are the star files containing filament coordinates (start/end)?"
                    reply = QtG.QMessageBox.question(
                        self, "Message", msg, QtG.QMessageBox.Yes, QtG.QMessageBox.No
                    )
                    if reply == QtG.QMessageBox.Yes:
                        is_star_startend = True
                    star_dialog_was_shown = True

            if is_helicon or is_eman1_startend or is_star_startend:
                rects = []
                identifier = file[:-4]
                if is_helicon:
                    filaments = CoordsIO.read_eman1_helicon(path)
                elif is_eman1_startend:
                    filaments = CoordsIO.read_eman1_filament_start_end(path)
                elif is_star_startend:
                    print("Read filaments", path)
                    filaments = CoordsIO.read_star_filament_file(
                        path=path, box_width=100
                    )
                    identifier = file[:-5]

                filaments_imported = filaments_imported + len(filaments)
                for fil in filaments:
                    rand_color = random.choice(colors)
                    rect = [self.box_to_rectangle(box, rand_color) for box in fil.boxes]
                    rects.extend(rect)
                    box_imported = box_imported + len(rects)
                self.box_dictionary[identifier] = rects
            else:
                self.is_cbox = False
                if path.endswith(".box"):
                    boxes = CoordsIO.read_eman1_boxfile(path)
                if path.endswith(".star"):
                    boxes = CoordsIO.read_star_file(path,self.boxsize)
                if path.endswith(".cbox"):
                    boxes = CoordsIO.read_cbox_boxfile(path)
                    self.is_cbox = True

                dict_entry_name = os.path.splitext(file)[0]

                rects = [self.box_to_rectangle(box, rand_color) for box in boxes]
                box_imported = box_imported + len(rects)

                if dict_entry_name in self.box_dictionary:
                    self.box_dictionary[dict_entry_name].extend(rects)
                else:
                    self.box_dictionary[dict_entry_name] = rects

        self.show_loaded_boxes(self.box_dictionary)

        print("Total time", t.time() - t_start)
        print("Total imported particles: ", box_imported)
        if filaments_imported > 0:
            print("Total imported filaments: ", filaments_imported)

    def show_loaded_boxes(self,box_dict):

        if self.is_cbox:
            self.conf_thresh_line.setEnabled(True)
            self.conf_thresh_slide.setEnabled(True)
            self.conf_thresh_label.setEnabled(True)
            self.use_estimated_size_label.setEnabled(True)
            self.use_estimated_size_checkbox.setEnabled(True)
            self.show_confidence_histogram_action.setEnabled(True)
            self.show_size_distribution_action.setEnabled(True)

        self.update_boxes_on_current_image()
        self.boxsize_line.setText(str(self.boxsize))

        # In case of cbox files, set the minimum and maximum
        if self.is_cbox:
            min_size = 99999
            max_size = -99999
            for _, rectangles in box_dict.items():
                for rect in rectangles:
                    if rect.est_size > max_size:
                        max_size = rect.est_size
                    if rect.est_size < min_size:
                        min_size = rect.est_size
            self.upper_size_thresh_slide.setMaximum(max_size)
            self.upper_size_thresh_slide.setMinimum(min_size)
            self.upper_size_thresh_slide.setValue(max_size)
            self.upper_size_thresh_line.setText("" + str(max_size))
            self.lower_size_thresh_slide.setMaximum(max_size)
            self.lower_size_thresh_slide.setMinimum(min_size)
            self.lower_size_thresh_slide.setValue(min_size)
            self.lower_size_thresh_line.setText("" + str(min_size))

        # Update particle numbers
        self.update_tree_boxsizes()

    def get_filter_state(self):
        lowersize = int(float(self.lower_size_thresh_line.text()))
        uppersize = int(float(self.lower_size_thresh_line.text()))
        conf = float(self.conf_thresh_slide.value())
        return (lowersize,uppersize,conf)

    def update_tree_boxsizes(self, update_current=False):
        state = self.get_filter_state()

        def update(boxes, item):

            res = [helper.check_if_should_be_visible(box,self.current_conf_thresh, self.upper_size_thresh, self.lower_size_thresh) for box in boxes]

            num_box_vis = int(np.sum(res))
            item.setText(1, "{0:> 4d}  / {1:> 4d}".format(num_box_vis, len(res)))

        if update_current:
            item = self.tree.currentItem()
            filename = os.path.splitext(item.text(0))[0]

            if self.is_folder_3D_tomo is True:
                f_name = os.path.splitext(os.path.basename(self.current_image_path.split('/')[-1]))[0]
                update(self.box_dictionary[f_name][self.index_3D_tomo], item)
            elif self.is_3D_tomo is True:
                update(self.box_dictionary[self.index_3D_tomo], item)
            else:
                update(self.box_dictionary[filename], item)

        else:
            start = time.time()
            root = self.tree.invisibleRootItem().child(0)
            child_count = root.childCount()

            for i in range(child_count):
                QtCore.QCoreApplication.instance().processEvents()
                if not helper.filter_tuple_is_equal(self.get_filter_state(),state):
                    break
                item = root.child(i)
                filename = os.path.splitext(item.text(0))[0]
                if self.is_folder_3D_tomo is False:
                    if self.is_3D_tomo is True:
                        filename=int(filename)
                    if filename in self.box_dictionary:
                        # num_box = sum(map(lambda x: self.check_if_should_be_visible(x), self.box_dictionary[filename]))
                        # item.setText(1, str(num_box))
                        update(self.box_dictionary[filename], item)
                else:
                    for j in range(item.childCount()):
                        item_item=item.child(j)
                        if filename in self.box_dictionary.keys() and j in self.box_dictionary[filename]:
                            update(self.box_dictionary[filename][j], item_item)



    def boxes_to_rectangle(self,boxes,color):
        return [self.box_to_rectangle(box, color) for box in boxes]

    def box_to_rectangle(self, box, color):
        # if np.random.rand()>0.8:
        x_ll = int(box.x)
        y_ll = int(box.y)
        # if x_ll > (197 - 10) and x_ll < (197 + 10) and y_ll > (
        #        225 - 10) and y_ll < (225 + 10):
        width = int(box.w)
        height = int(box.h)
        avg_size = (width + height) // 2
        self.boxsize = avg_size
        est_size = avg_size
        if "boxsize_estimated" in box.meta:
            est_size = (box.meta["boxsize_estimated"][0] + box.meta["boxsize_estimated"][1]) // 2
            # est_size = min(box.meta["est_size"][0],box.meta["est_size"][1])
            if self.use_estimated_size:
                width = est_size
                height = est_size
                #self.boxsize = est_size

        rect = MyRectangle.MyRectangle(
            (x_ll, y_ll),
            width,
            height,
            est_size=est_size,
            linewidth=1,
            edgecolor=color,
            facecolor="none",
        )
        if box.c:
            rect.set_confidence(box.c)
        else:
            rect.set_confidence(1)
        return rect


    def draw_all_patches(self, rects):
        state = self.get_filter_state()
        visible_rects = [box.getRect() for box in rects if helper.check_if_should_be_visible(box,self.current_conf_thresh, self.upper_size_thresh, self.lower_size_thresh)]

        for rect in visible_rects:
            if rect.get_visible()==False:
                rect.set_visible(True)
            if rect not in self.ax.patches:
                self.ax.add_patch(rect)
            if not helper.filter_tuple_is_equal(self.get_filter_state(),state):
                break

    def _set_selected_folder(self):
        """
        :return: the folder name, as string, selected by the user via GUI
        """
        selected_folder = str(
            QtG.QFileDialog.getExistingDirectory(self, "Select Image Directory")
        )

        if selected_folder == "":
            return

        if self.unsaved_changes:
            msg = "All loaded boxes are discarded. Are you sure?"
            reply = QtG.QMessageBox.question(
                self, "Message", msg, QtG.QMessageBox.Yes, QtG.QMessageBox.Cancel
            )

            if reply == QtG.QMessageBox.Cancel:
                return

        self.current_image_path = None
        return selected_folder

    def open_image3D_folder(self):
        """
        Let the user choose the image folder and adds it to the ImageFolder-Tree
        :return: none
        """
        self.use_estimated_size = False
        self.is_folder_3D_tomo = True
        self.is_3D_tomo = False
        self.item_3D_filename = {}
        # When we select it we open the first slice of the first tomo in the folder.
        # This operation is in the catch of a try-catch statement that is raised in case of self.im = None
        self.im = None
        selected_folder=self._set_selected_folder()
        img_loaded = self._open_image3D_folder(selected_folder)
        if img_loaded:
            self.button_apply_filter.setEnabled(True)

    def open_image_folder(self):
        """
        Let the user choose the image folder and adds it to the ImageFolder-Tree
        :return: none
        """
        self.is_folder_3D_tomo = False
        img_loaded = self._open_image_folder(self._set_selected_folder())
        if img_loaded:
            self.button_apply_filter.setEnabled(True)

    def open_image3D_tomo(self):
        """
        Let the user choose the image 3D  adds it slice to the ImageFolder-Tree.
        :return: none
        """
        self.is_folder_3D_tomo = False
        self.use_estimated_size = False
        self.item_3D_filename = {}
        selected_image = QtG.QFileDialog.getOpenFileName(self, "Select 3D Image File")[0]


        if selected_image == "":
            return

        if self.unsaved_changes:
            msg = "All loaded boxes are discarded. Are you sure?"
            reply = QtG.QMessageBox.question(
                self, "Message", msg, QtG.QMessageBox.Yes, QtG.QMessageBox.Cancel
            )

            if reply == QtG.QMessageBox.Cancel:
                return

        self.current_image_path = selected_image
        img_loaded = self._open_single_image3D(self.current_image_path)

        if img_loaded:
            self.button_apply_filter.setEnabled(True)


    def _open_single_image3D(self, path):
        if path.endswith(("mrc","mrcs","rec")) is False:
            errmsg = QtG.QErrorMessage(self)
            errmsg.showMessage("ERROR: The image '" + str(path) + "' has an invalid format. Must be in .mrc or .mrcs format")
            return False
        self.is_3D_tomo = True
        self.index_3D_tomo = 0
        self.current_image3D_mmap = helper.read_image(path,use_mmap=True) #imagereader.image_read(path,use_mmap=True)

        if len(self.current_image3D_mmap.shape) !=3:
            errmsg = QtG.QErrorMessage(self)
            errmsg.showMessage("ERROR: The image '"+str(path)+"' is not a 3D image")
            return False

        root = QtG.QTreeWidgetItem([path])

        # init item filename and slice_tomo
        purefilename = self.current_image_path.split(".")[0].split("/")[-1]
        self.item_3D_filename.update({purefilename: root})

        self.reset_tree(root,path)

        if self.current_image3D_mmap.shape[0] > 0:
            for i in range(self.current_image3D_mmap.shape[0]):
                QtCore.QCoreApplication.instance().processEvents()
                root.addChild(QtG.QTreeWidgetItem([str(i)]) )
        else:
            errmsg = QtG.QErrorMessage(self)
            errmsg.showMessage("ERROR: The image '"+str(path)+"' is recognized as a 3D image but has no slice (i.e.: mrc.data.shape[0]<1")
            return False

        root.setExpanded(True)
        # Show first image
        img_data=self.current_image3D_mmap[int(root.child(0).text(0)), :, :]
        self.current_tree_item = root.child(0)

        #im = self.read_image_tomo(img_data)

        self.rectangles = []
        # Create figure and axes

        self._set_first_time_img(img_data)

        self.tree.setCurrentItem(
            self.tree.invisibleRootItem().child(0).child(0)
        )
        self.plot.setWindowTitle(os.path.basename(self.current_image_path))
        return True

    def _open_image3D_folder(self, path):
        """
        Reads the image folder, setup the folder daemon and signals
        :param path: Path to image3D folder
        """
        self.current_image3D_mmap = None
        self.is_3D_tomo = True
        self.index_3D_tomo =0
        self.last_index_3D_tomo = self.index_3D_tomo
        self.image_folder = path
        root,onlyfiles,all_items=self._list_files_in_folder(path,True)
        if root is not False and onlyfiles is not False and all_items is not False:
            img_data = None
            if onlyfiles:
                root.setExpanded(True)
                imgdata = None

                #self.current_image_path = os.path.join(self.image_folder, str(root.child(0).text(0)))
                self.current_image_path = self.image_folder
                index=0
                #self.current_tree_item = root.child(0)
                for f in onlyfiles:
                    purefilename=f.split(".")[0]
                    self.box_dictionary.update({purefilename:{}})
                    self.item_3D_filename.update({purefilename: root.child(index)})
                    with mrcfile_mmap(os.path.join(self.image_folder,f), permissive=True, mode="r") as mrc:
                        if mrc.data.shape[0] > 0:
                            if self.current_image3D_mmap is None:
                                self.current_image_path=os.path.join(self.image_folder, f)
                                self.current_image3D_mmap= helper.read_image(self.current_image_path, use_mmap=True)
                                title = os.path.basename(self.current_image_path) + "\tindex: " + str(self.index_3D_tomo)
                            for i in range(mrc.data.shape[0]):
                                QtCore.QCoreApplication.instance().processEvents()
                                root.child(index).addChild(QtG.QTreeWidgetItem([str(i)]))
                        index+=1
                        mrc.close()
            if self.current_image3D_mmap is not None:
                self._set_first_time_img(self.current_image3D_mmap[0, :, :])
                # child_1 = folder  child_2 = list of tomo  child_3 = list of slices
                self.tree.setCurrentItem(self.tree.invisibleRootItem().child(0).child(0).child(0))
                self.plot.setWindowTitle(title)
                return True

        errmsg = QtG.QErrorMessage(self)
        errmsg.showMessage("ERROR: The folder '" + str(path) + "' does not have tomogram")
        return False

    def _open_image_folder(self, path):
        """
        Reads the image folder, setup the folder daemon and signals
        :param path: Path to image folder
        """
        self.is_folder_3D_tomo = False
        self.is_3D_tomo = False
        self.index_3D_tomo =None
        self.image_folder = path
        root,onlyfiles,all_items=self._list_files_in_folder(path,False)
        if root is not False and onlyfiles is not False and all_items is not False:

            if onlyfiles:

                root.setExpanded(True)
                # Show first image
                self.current_image_path = os.path.join(
                    self.image_folder, str(root.child(0).text(0))
                )
                self.current_tree_item = root.child(0)
                im = helper.read_image(self.current_image_path)

                if len(im.shape) !=2:
                    errmsg = QtG.QErrorMessage(self)
                    errmsg.showMessage("Please open an image folder with micrographs")
                    return False

                self.rectangles = []
                self._set_first_time_img(im)

                self.tree.setCurrentItem(
                    self.tree.invisibleRootItem().child(0).child(0)
                )
                self.plot.setWindowTitle(os.path.basename(self.current_image_path))
                return True
            return False

    def myKeyPressEvent(self, event):
        if event.name == "key_press_event" and event.key == "h":
            # if it is a 3D tomo pure_filename identifies the slice of the tomo
            pure_filename = os.path.basename(self.current_image_path)[:-4] if self.is_3D_tomo is False else self.index_3D_tomo

            if pure_filename in self.box_dictionary:
                rects = self.box_dictionary[pure_filename]
                if self.toggle:
                    self.draw_all_patches(rects)
                    self.fig.canvas.draw()
                    self.toggle = False
                else:
                    self.delete_all_patches(rects)
                    self.fig.canvas.draw()
                    self.toggle = True

    def ondraw(self, event):
        if self.zoom_update:
            self.zoom_update = False
            self.background_current = self.fig.canvas.copy_from_bbox(self.ax.bbox)
            self.draw_all_patches(self.rectangles)
            self._draw_all_boxes()

    def onresize(self, event):
        self.delete_all_patches(self.rectangles)
        self.fig.canvas.draw()
        self.background_current = self.fig.canvas.copy_from_bbox(self.ax.bbox)
        self.background_orig = self.fig.canvas.copy_from_bbox(self.ax.bbox)
        self.draw_all_patches(self.rectangles)

    def onmove(self, event):
        if event.inaxes != self.ax:
            return
        if event.button == 1:
            if self.moving_box is not None:
                x = event.xdata - self.moving_box.getRect().get_width() / 2
                y = event.ydata - self.moving_box.getRect().get_width() / 2
                self.boxsize = self.moving_box.getRect().get_width()  # Update the current boxsize
                self.moving_box.getRect().set_x(x)
                self.moving_box.getRect().set_y(y)

                self.fig.canvas.restore_region(self.background_current)
                ## draw all boxes again
                self._draw_all_boxes()

    def onrelease(self, event):
        self.moving_box = None

    def onclick(self, event):

        if self.plot.toolbar._active is not None:
            return

        modifiers = QtG.QApplication.keyboardModifiers()

        if event.xdata is None or event.ydata is None or event.xdata < 0 or event.ydata < 0:
            return

        if self.is_folder_3D_tomo is True:
            pure_filename =  os.path.splitext(os.path.basename(self.current_image_path.split('/')[-1]))[0] #self.current_image_path.split('/')[-1]
            if pure_filename in self.box_dictionary and self.index_3D_tomo in self.box_dictionary[pure_filename]:
                self.rectangles = self.box_dictionary[pure_filename][self.index_3D_tomo]
            else:
                self.rectangles = []
                self.box_dictionary[pure_filename][self.index_3D_tomo] = self.rectangles
        else:
            # if it is a single 3D image tomo pure_filename identifies the slice of the tomo
            pure_filename = os.path.splitext(os.path.basename(self.current_image_path))[0] if self.is_3D_tomo is False else self.index_3D_tomo
            if pure_filename in self.box_dictionary:
                self.rectangles = self.box_dictionary[pure_filename]
            else:
                self.rectangles = []
                self.box_dictionary[pure_filename] = self.rectangles

        if (
            modifiers == QtCore.Qt.ControlModifier
            or modifiers == QtCore.Qt.MetaModifier
        ):
            # Delete box
            box = helper.get_corresponding_box(
                event.xdata - self.boxsize / 2,
                event.ydata - self.boxsize / 2,
                self.rectangles,
                self.current_conf_thresh,
                self.boxsize
            )

            if box is not None:
                self.delete_box(box)
        else:
            self.moving_box = helper.get_corresponding_box(
                event.xdata - self.boxsize / 2,
                event.ydata - self.boxsize / 2,
                self.rectangles,
                self.current_conf_thresh,
                self.boxsize
            )
            if self.moving_box is None:

                # Delete lower confidence box if available
                box = helper.get_corresponding_box(
                    event.xdata - self.boxsize / 2,
                    event.ydata - self.boxsize / 2,
                    self.rectangles,
                    self.current_conf_thresh,
                    self.boxsize,
                    get_low=True,
                )

                if box is not None:
                    self.rectangles.remove(box)

                # Create new box
                x = event.xdata - self.boxsize / 2
                y = event.ydata - self.boxsize / 2

                xy = (x, y)
                rect = MyRectangle.MyRectangle(
                    xy,
                    self.boxsize,
                    self.boxsize,
                    linewidth=1,
                    edgecolor="r",
                    facecolor="none",
                )
                rect.est_size = self.boxsize
                rect.set_confidence(1)

                # plot and consider as new rect only the one with the starting size of the box (i.e.: got via file or set via GUI)
                self.moving_box = rect
                self.rectangles.append(rect)
                # Add the patch to the Axes
                self.ax.add_patch(rect.getRect())
                self.ax.draw_artist(rect.getRect())
                self.fig.canvas.blit(self.ax.bbox)
                self.unsaved_changes = True
                self.update_tree_boxsizes(update_current=True)

            if self.is_3D_tomo:
                self.update_3D_counter()
            # self.fig.canvas.draw()


    def delete_box(self, box):
        box.getRect().remove()
        del self.rectangles[self.rectangles.index(box)]
        self.fig.canvas.restore_region(self.background_current)
        self._draw_all_boxes()
        self.unsaved_changes = True
        self.update_tree_boxsizes(update_current=True)

    def _draw_all_boxes(self):
        state = self.get_filter_state()
        for box in self.rectangles:
            rect = box.getRect()
            if self.use_estimated_size:
                helper.resize_box(rect, box.est_size)
            else:
                helper.resize_box(rect, self.boxsize)
            self.ax.draw_artist(rect)
            if not helper.filter_tuple_is_equal(self.get_filter_state(),state):
                break
        self.fig.canvas.blit(self.ax.bbox)


    # REFACTORING FUNCTIONS
    def reset_tree(self, root, title):
        self.tree.clear()
        self.tree.setColumnCount(2)
        self.tree.setHeaderHidden(False)
        self.tree.setHeaderLabels(["Filename", "Number of boxes"])
        if self.plot is not None:
            self.plot.close()
        self.rectangles = []
        self.box_dictionary = {}
        self.tree.addTopLevelItem(root)
        fm = QFontMetrics(self.font)
        w = fm.width(title)
        self.tree.setMinimumWidth(w + 150)
        self.tree.setColumnWidth(0, 300)

    def _list_files_in_folder(self,path,is_list_tomo=False):
        """
        :param path: path to the folder
        :param is_list_tomo: True if folder of 3D tomo
        :return root: the QTreeWidgetItem
        :return onlyfiles: list of valid 3D tomo files
        :return all_items: items of the root (one for each valid file)
        """
        if path != "" and path is not None:
            title = os.path.join(str(path), self.wildcard) if self.wildcard else str(path)
            root = QtG.QTreeWidgetItem([title])
            self.reset_tree(root, title)

            onlyfiles = helper.get_only_files(path,self.wildcard,is_list_tomo)
            all_items = [QtG.QTreeWidgetItem([file]) for file in onlyfiles]

            pd = None
            if len(all_items) > 0:
                pd = QtG.QProgressDialog("Load images", "Cancel", 0, 100, self)
                pd.show()
            for item_index, item in enumerate(all_items):
                pd.show()
                QtCore.QCoreApplication.instance().processEvents()
                pd.setValue(int((item_index+1)*100/len(all_items)))
                root.addChild(item)
            return root,onlyfiles,all_items
        return False,False,False

    def clean_box_dictionary(self):
        root = self.tree.invisibleRootItem().child(0)
        child_count = root.childCount()
        for i in range(child_count):
            item = root.child(i)
            if self.is_folder_3D_tomo is True:
                for filename in self.box_dictionary.keys():
                    for index in self.box_dictionary[filename]:
                        item.child(index).setText(1, "")
            elif self.is_3D_tomo is True:
                item.setText(1, "")


        if self.is_folder_3D_tomo is True:
            for filename in self.box_dictionary.keys():
                self.box_dictionary[filename] = {}
        else:
            self.box_dictionary = {}

    def update_3D_counter(self):
        """
        It updates the number of total particles in a single tomo
        """
        for f, f_item in self.item_3D_filename.items():
            tot_res, tot_num_box_vis = 0, 0
            list_index = self.box_dictionary[f].keys() if self.is_folder_3D_tomo else self.box_dictionary.keys()
            for index in list_index:
                boxes = self.box_dictionary[f][index] if self.is_folder_3D_tomo else self.box_dictionary[index]
                res = [helper.check_if_should_be_visible(box,self.current_conf_thresh, self.upper_size_thresh, self.lower_size_thresh) for box in boxes]
                tot_res += len(res)
                tot_num_box_vis += int(np.sum(res))

            f_item.setText(1, "{0:> 4d}  / {1:> 4d}".format(tot_num_box_vis, tot_res))


def start_boxmanager(image_dir, box_dir, wildcard, is_tomo_dir):
    app = QtG.QApplication(sys.argv)
    gui = MainWindow(app.font(), images_path=image_dir, boxes_path=box_dir, wildcard=wildcard, is_tomo_dir=is_tomo_dir)
    sys.exit(app.exec_())


def run(args=None):

    args = argparser.parse_args()
    image_dir = args.image_dir
    box_dir = args.box_dir
    wildcard = args.wildcard
    is_tomo_dir=args.is_tomo_dir
    start_boxmanager(image_dir, box_dir, wildcard, is_tomo_dir=is_tomo_dir)


if __name__ == "__main__":
    run()
