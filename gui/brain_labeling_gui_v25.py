#! /usr/bin/env python

import sys
import os
import datetime
import time
import json
import cPickle as pickle
from collections import defaultdict, OrderedDict

import numpy as np
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from shapely.geometry import Polygon as ShapelyPolygon
from shapely.geometry import Point as ShapelyPoint
from shapely.geometry import LineString as ShapelyLineString
from shapely.geometry import LinearRing as ShapelyLineRing
from skimage.color import label2rgb

sys.path.append(os.environ['REPO_DIR'] + '/utilities')
from utilities2015 import *
from data_manager import DataManager
from metadata import *
from annotation_utilities import *
from gui_utilities import *

from ui.ui_BrainLabelingGui_v15 import Ui_BrainLabelingGui

from widgets.custom_widgets import *
from widgets.SignalEmittingItems import *
from widgets.DrawableZoomableBrowsableGraphicsScene_ForLabeling_v2 import DrawableZoomableBrowsableGraphicsScene_ForLabeling

from DataFeeder import ImageDataFeeder, VolumeResectionDataFeeder

#######################################################################

class ReadImagesThread(QThread):
    def __init__(self, stack, sections):
        QThread.__init__(self)
        self.stack = stack
        self.sections = sections

    def __del__(self):
        self.wait()

    def run(self):
        for sec in self.sections:
            # image = QImage(DataManager.get_image_filepath(stack=self.stack, section=sec, resol='lossless', version='compressed'))
            fp = DataManager.get_image_filepath(stack=self.stack, section=sec, resol='lossless', version='cropped_gray_jpeg')
            if not os.path.exists(fp):
                sys.stderr.write('Image %s does not exist.\n' % fp)
                continue
            image = QImage(fp)
            self.emit(SIGNAL('image_loaded(QImage, int)'), image, sec)

class BrainLabelingGUI(QMainWindow, Ui_BrainLabelingGui):
# class BrainLabelingGUI(QMainWindow, Ui_RectificationGUI):

    def __init__(self, parent=None, stack=None, first_sec=None, last_sec=None, downsample=None):
        """
        Initialization of BrainLabelingGUI.
        """

        # t0 = time.time()

        # self.app = QApplication(sys.argv)
        QMainWindow.__init__(self, parent)

        self.stack = stack
        self.sagittal_downsample = downsample

        self.setupUi(self)

        self.button_save.clicked.connect(self.save)
        self.button_load.clicked.connect(self.load)
        self.button_inferSide.clicked.connect(self.infer_side)
        self.button_displayOptions.clicked.connect(self.select_display_options)
        self.button_displayStructures.clicked.connect(self.select_display_structures)
        self.lineEdit_username.returnPressed.connect(self.username_changed)

        self.structure_volumes = {}
        self.structure_adjustment_3d = defaultdict(list)

        self.volume_cache = {}
        for ds in [8, 32]:
        # for ds in [32]:
            try:
                self.volume_cache[ds] = DataManager.load_intensity_volume(self.stack, downscale=ds)
            except:
                sys.stderr.write('Intensity volume of downsample %d does not exist.\n' % ds)

        self.coronal_gscene = DrawableZoomableBrowsableGraphicsScene_ForLabeling(id='coronal', gui=self, gview=self.coronal_gview)
        self.coronal_gview.setScene(self.coronal_gscene)

        self.horizontal_gscene = DrawableZoomableBrowsableGraphicsScene_ForLabeling(id='horizontal', gui=self, gview=self.horizontal_gview)
        self.horizontal_gview.setScene(self.horizontal_gscene)

        self.sagittal_gscene = DrawableZoomableBrowsableGraphicsScene_ForLabeling(id='sagittal', gui=self, gview=self.sagittal_gview)
        self.sagittal_gview.setScene(self.sagittal_gscene)

        self.sagittal_gscene.set_default_line_width(5)
        self.sagittal_gscene.set_default_line_color('b')
        self.sagittal_gscene.set_default_vertex_radius(10)
        self.sagittal_gscene.set_default_vertex_color('r')

        self.gscenes = {'coronal': self.coronal_gscene, 'sagittal': self.sagittal_gscene, 'horizontal': self.horizontal_gscene}

        for gscene in self.gscenes.itervalues():
            gscene.drawings_updated.connect(self.drawings_updated)
            gscene.crossline_updated.connect(self.crossline_updated)
            gscene.active_image_updated.connect(self.active_image_updated)
            gscene.structure_volume_updated.connect(self.update_structure_volume)
            gscene.set_structure_volumes(self.structure_volumes)
            # gscene.set_drawings(self.drawings)

        from functools import partial
        self.gscenes['sagittal'].set_conversion_func_section_to_z(partial(DataManager.convert_section_to_z, stack=self.stack))
        self.gscenes['sagittal'].set_conversion_func_z_to_section(partial(DataManager.convert_z_to_section, stack=self.stack))

        ##################
        # self.slider_downsample.valueChanged.connect(self.downsample_factor_changed)

        ###################
        self.contextMenu_set = True

        self.recent_labels = []

        self.structure_names = load_structure_names(os.environ['REPO_DIR']+'/gui/structure_names.txt')
        self.new_labelnames = load_structure_names(os.environ['REPO_DIR']+'/gui/newStructureNames.txt')
        self.structure_names = OrderedDict(sorted(self.new_labelnames.items()) + sorted(self.structure_names.items()))

        self.installEventFilter(self)

        first_sec0, last_sec0 = DataManager.load_cropbox(self.stack)[4:]
        self.sections = range(first_sec0, last_sec0 + 1)

        image_feeder = ImageDataFeeder('image feeder', stack=self.stack, sections=self.sections, use_data_manager=False)
        image_feeder.set_orientation('sagittal')
        # image_feeder.set_downsample_factor(1)
        image_feeder.set_downsample_factor(self.sagittal_downsample)
        self.gscenes['sagittal'].set_data_feeder(image_feeder)

        volume_resection_feeder = VolumeResectionDataFeeder('volume resection feeder', self.stack)

        if hasattr(self, 'volume_cache') and self.volume_cache is not None:

            coronal_volume_resection_feeder = VolumeResectionDataFeeder('coronal resection feeder', self.stack)
            coronal_volume_resection_feeder.set_volume_cache(self.volume_cache)
            coronal_volume_resection_feeder.set_orientation('coronal')
            # coronal_volume_resection_feeder.set_downsample_factor(32)
            coronal_volume_resection_feeder.set_downsample_factor(8)
            self.gscenes['coronal'].set_data_feeder(coronal_volume_resection_feeder)
            self.gscenes['coronal'].set_active_i(50)

            horizontal_volume_resection_feeder = VolumeResectionDataFeeder('horizontal resection feeder', self.stack)
            horizontal_volume_resection_feeder.set_volume_cache(self.volume_cache)
            horizontal_volume_resection_feeder.set_orientation('horizontal')
            # horizontal_volume_resection_feeder.set_downsample_factor(32)
            horizontal_volume_resection_feeder.set_downsample_factor(8)
            self.gscenes['horizontal'].set_data_feeder(horizontal_volume_resection_feeder)
            self.gscenes['horizontal'].set_active_i(150)

        if self.gscenes['sagittal'].data_feeder.downsample == 1:
            self.read_images_thread = ReadImagesThread(self.stack, range(first_sec, last_sec+1))
            self.connect(self.read_images_thread, SIGNAL("image_loaded(QImage, int)"), self.image_loaded)
            self.read_images_thread.start()
            self.button_stop.clicked.connect(self.read_images_thread.terminate)
        else:
            self.gscenes['sagittal'].data_feeder.load_images()
            self.gscenes['sagittal'].set_vertex_radius(3)
            self.gscenes['sagittal'].set_line_width(3)

        try:
            self.gscenes['sagittal'].set_active_section(first_sec)
        except Exception as e:
            sys.stderr.write(e.message + '\n')

    @pyqtSlot()
    def image_loaded(self, qimage, sec):
        self.gscenes['sagittal'].data_feeder.set_image(sec=sec, qimage=qimage)
        print 'Image', sec, 'received.'
        if self.gscenes['sagittal'].active_section == sec:
            self.gscenes['sagittal'].update_image()
        self.statusBar().showMessage('Image %d loaded.\n' % sec)

    @pyqtSlot()
    def username_changed(self):
        self.username = str(self.sender().text())
        print 'username changed to', self.username

    def get_username(self):
        if not hasattr(self, 'username') or self.username is None:
            username, okay = QInputDialog.getText(self, "Username", "Please enter your username:", QLineEdit.Normal, 'anon')
            if not okay: return
            self.username = str(username)
            self.lineEdit_username.setText(self.username)

        return self.username

    def structure_tree_changed(self, item, column):

        tree_widget = self.sender()
        complete_name = str(item.text(column))
        abbr = re.findall('^.*?(\((.*)\))?$', complete_name)[0][1]

        check_state = item.checkState(column)
        if check_state == Qt.Unchecked:

            for gscene in self.gscenes.values():
                for section_index, polygons in gscene.drawings.iteritems():
                    for polygon in polygons:
                        if polygon.label == abbr:
                            polygon.setVisible(False)

        elif check_state == Qt.PartiallyChecked:
            pass
        elif check_state == Qt.Checked:
            for gscene in self.gscenes.values():
                for section_index, polygons in gscene.drawings.iteritems():
                    for polygon in polygons:
                        if polygon.label == abbr:
                            polygon.setVisible(True)
        else:
            raise Exception('Unknown check state.')

        # selected_items = tree_widget.selectedItems()
        # print [str(it.text(0)) for it in selected_items]


    @pyqtSlot()
    def select_display_structures(self):
        loaded_structure_abbrs = set([convert_name_to_unsided(name_s) for name_s in self.gscenes['sagittal'].get_label_section_lookup().keys()])

        structure_tree_dict = json.load(open('structure_tree.json'))
        # structure_tree_dict = {name: d for name, d in structure_tree_dict_all.iteritems() if d['abbr'] in loaded_structure_names}
        # structure_tree_names = {'brainstem': {}}

        def structure_entry_to_str(node):
            if 'abbr' in node and len(node['abbr']) > 0:
                key = node['fullname'] + ' (' + node['abbr'] + ')'
            else:
                key = node['fullname']
            return key

        def get_children_names(name):
            node = structure_tree_dict[name]
            key = structure_entry_to_str(node)
            return (key, dict([get_children_names(child_name) for child_name in node['children']]))

        structure_name_tree = dict([get_children_names('brainstem')])

        # extract_names(structure_tree_names['brainstem'], structure_tree_dict['brainstem'], structure_tree_dict)
        # structure_tree_names = {'midbrain': ['IC', 'SC'], 'hindbrain': {'pons': ['7N', '5N'], 'medulla': ['7n', 'SCP']}}

        display_structures_widget = QDialog(self)

        tree_widget = QTreeWidget(display_structures_widget)
        tree_widget.setHeaderLabels(['Structures'])
        fill_tree_widget(tree_widget, structure_name_tree, loaded_structure_abbrs)
        # tree_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        tree_widget.setMinimumHeight(1000)
        tree_widget.setMinimumWidth(500)

        # http://stackoverflow.com/questions/27521391/signal-a-qtreewidgetitem-toggled-checkbox
        tree_widget.itemChanged.connect(self.structure_tree_changed)

        dialog_layout = QVBoxLayout(display_structures_widget)
        dialog_layout.addWidget(tree_widget)
        display_structures_widget.setLayout(dialog_layout)
        # display_structures_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        display_structures_widget.setWindowTitle("Select structures to show")
        # display_structures_widget.exec_()
        display_structures_widget.show()

    # @pyqtSlot()
    # def select_display_structures(self):
    #
    #     display_structures_widget = QDialog(self)
    #
    #     scroll = QScrollArea(display_structures_widget)
    #
    #     viewport = QWidget(display_structures_widget)
    #     scroll.setWidget(viewport)
    #     scroll.setWidgetResizable(True)
    #
    #     viewport_layout = QVBoxLayout(viewport)
    #
    #     structure_names = set([convert_name_to_unsided(name_s) for name_s in self.gscenes['sagittal'].get_label_section_lookup().keys()])
    #
    #     if not hasattr(self, 'show_structure'):
    #         self.show_structure = {}
    #
    #     for name in sorted(structure_names):
    #         if name not in self.show_structure:
    #             self.show_structure[name] = True
    #
    #         checkbox_showStructure = QCheckBox(name)
    #         checkbox_showStructure.setChecked(self.show_structure[name])
    #         checkbox_showStructure.stateChanged.connect(self.checkbox_showStructure_callback)
    #         viewport_layout.addWidget(checkbox_showStructure)
    #
    #     viewport.setLayout(viewport_layout)
    #
    #     dialog_layout = QVBoxLayout(display_structures_widget)
    #     dialog_layout.addWidget(scroll)
    #     display_structures_widget.setLayout(dialog_layout)
    #
    #     display_structures_widget.setWindowTitle("Select structures to show")
    #     # display_structures_widget.exec_()
    #     display_structures_widget.show()


    # def checkbox_showStructure_callback(self, checked):
    #     name = str(self.sender().text())
    #     self.show_structure[name] = bool(checked)
    #
    #     for gscene in self.gscenes.values():
    #         for section_index, polygons in gscene.drawings.iteritems():
    #             for polygon in polygons:
    #                 if polygon.label == name:
    #                     polygon.setVisible(bool(checked))

    @pyqtSlot()
    def select_display_options(self):

        if not hasattr(self, 'show_polygons'):
            self.show_polygons = True
            self.show_vertices = True
            self.show_labels = True
            self.hide_interpolated = False

        display_option_widget = QDialog(self)

        layout = QVBoxLayout()

        checkbox_showPolygons = QCheckBox("Polygon")
        checkbox_showPolygons.setChecked(self.show_polygons)
        checkbox_showPolygons.stateChanged.connect(self.checkbox_showPolygons_callback)
        layout.addWidget(checkbox_showPolygons)

        checkbox_showVertices = QCheckBox("Vertices")
        checkbox_showVertices.setChecked(self.show_vertices)
        checkbox_showVertices.stateChanged.connect(self.checkbox_showVertices_callback)
        layout.addWidget(checkbox_showVertices)

        checkbox_showLabels = QCheckBox("Labels")
        checkbox_showLabels.setChecked(self.show_labels)
        checkbox_showLabels.stateChanged.connect(self.checkbox_showLabels_callback)
        layout.addWidget(checkbox_showLabels)

        checkbox_hideInterpolated = QCheckBox("Hide interpolated")
        checkbox_hideInterpolated.setChecked(self.hide_interpolated)
        checkbox_hideInterpolated.stateChanged.connect(self.checkbox_hideInterpolated_callback)
        layout.addWidget(checkbox_hideInterpolated)

        display_option_widget.setLayout(layout)
        display_option_widget.setWindowTitle("Select display options")
        display_option_widget.exec_()

    @pyqtSlot(int)
    def checkbox_showLabels_callback(self, checked):
        self.show_labels = checked
        for gscene in self.gscenes.itervalues():
            for section_index, polygons in gscene.drawings.iteritems():
                for polygon in polygons:
                    polygon.label_textItem.setVisible(checked)

    @pyqtSlot(int)
    def checkbox_showVertices_callback(self, checked):
        self.show_vertices = checked
        for gscene in self.gscenes.itervalues():
            for section_index, polygons in gscene.drawings.iteritems():
                for polygon in polygons:
                    for v in polygon.vertex_circles:
                        v.setVisible(checked)

    @pyqtSlot(int)
    def checkbox_showPolygons_callback(self, checked):
        self.show_polygons = checked
        for gscene in self.gscenes.itervalues():
            for section_index, polygons in gscene.drawings.iteritems():
                for polygon in polygons:
                    polygon.setVisible(checked)

    @pyqtSlot(int)
    def checkbox_hideInterpolated_callback(self, checked):
        self.hide_interpolated = checked
        for gscene in self.gscenes.itervalues():
            for section_index, polygons in gscene.drawings.iteritems():
                for polygon in polygons:
                    if polygon.type == 'interpolated':
                        polygon.setVisible(not bool(checked))

    @pyqtSlot()
    def infer_side(self):
        self.gscenes['sagittal'].infer_side()
        self.gscenes['coronal'].infer_side()
        self.gscenes['horizontal'].infer_side()
    #
    # def merge_contour_entries(self, new_entries_df):
    #     """
    #     Merge new entries into loaded entries.
    #     new_entries: dict. {polygon_id: entry}
    #     Return: new dict.
    #     """
    #
    #     self.contour_df_loaded.update(new_entries_df)



    @pyqtSlot()
    def save(self):

        username = self.get_username()

        # if not hasattr(self, 'username') or self.username is None:
        #     self.username_dialog_requested()
            # username, okay = QInputDialog.getText(self, "Username", "Please enter your username:", QLineEdit.Normal, 'anon')
            # if not okay: return
            # self.username = str(username)
            # self.lineEdit_username.setText(self.username)

        # labelings_dir = create_if_not_exists('/home/yuncong/CSHL_labelings_new/%(stack)s/' % dict(stack=self.stack))
        labelings_dir = create_if_not_exists(os.path.join(ANNOTATION_ROOTDIR, stack))

        import datetime
        timestamp = datetime.datetime.now().strftime("%m%d%Y%H%M%S")

        # contour_entries_all = []
        # for gscene_id, gscene in self.gscenes.iteritems():
        #     # gscene.save_drawings(fn_template=os.path.join(labelings_dir, '%(stack)s_%(orientation)s_%(downsample)d_%(username)s_%(timstamp)s.pkl' % dict(username=self.username)))
        #     # gscene.save_drawings(fn_template=os.path.join(labelings_dir, '%(stack)s_%(orientation)s_downsample%(downsample)d_'+self.username+'_'+timestamp+'.pkl'))
        #     # gscene.save_drawings(fn_template=os.path.join(labelings_dir, '%(stack)s_%(orientation)s_downsample%(downsample)d_%(username)s_%(timestamp)s.pkl'), timestamp=timestamp, username=self.username)
        #     contour_entries = gscene.convert_drawings_to_entries(timestamp=timestamp, username=self.username)
        #     contour_entries_all += contour_entries.items()

        sagittal_contour_entries_curr_session = self.gscenes['sagittal'].convert_drawings_to_entries(timestamp=timestamp, username=self.username).items()

        if hasattr(self, 'contour_df_loaded'):
            d = self.contour_df_loaded.T.to_dict()
        else:
            d = {}
        print 'loaded', d.keys()
        d.update(sagittal_contour_entries_curr_session)

        print 'updated', d.keys()

        from pandas import DataFrame
        df_aligned_cropped = DataFrame(dict(d)).T

        # df_aligned_cropped = DataFrame(dict(contour_entries_all)).T

        fn = os.path.join(labelings_dir, '%(stack)s_annotation_v3_%(timestamp)s.h5' % dict(stack=stack, timestamp=timestamp))
        df_original = convert_annotation_v3_aligned_cropped_to_original(df_aligned_cropped, stack=self.stack)
        df_original.to_hdf(fn, 'contours')

        execute_command('cd %(labelings_dir)s; rm -f %(stack)s_annotation_v3.h5; ln -s %(stack)s_annotation_v3_%(timestamp)s.h5 %(stack)s_annotation_v3.h5' % dict(labelings_dir=labelings_dir, stack=stack, timestamp=timestamp))

        self.statusBar().showMessage('Labelings saved to %s.' % fn)

        # pickle.dump(self.structure_volumes, open(os.path.join(labelings_dir, '%(stack)s_structure_volumes.pkl' % dict(stack=stack))))

        # # if sec is not None:
        # #
        # #     accepted_proposal_props = []
        # #     for polygon, props in self.accepted_proposals_allSections[sec].iteritems():
        # #
        # #         props_saved = props.copy()
        # #
        # #         # props_saved['vertices'] = [(v.scenePos().x(), v.scenePos().y()) for v in props['vertexCircles']]
        # #
        # #         path = polygon.path()
        # #
        # #         if path.elementCount() > 1 and polygon_is_closed(path=path):
        # #             props_saved['subtype'] = PolygonType.CLOSED
        # #             props_saved['vertices'] = [(int(path.elementAt(i).x), int(path.elementAt(i).y)) for i in range(path.elementCount()-1)]
        # #         else:
        # #             props_saved['subtype'] = PolygonType.OPEN
        # #             props_saved['vertices'] = [(int(path.elementAt(i).x), int(path.elementAt(i).y)) for i in range(path.elementCount())]
        # #
        # #         label_pos = props['labelTextArtist'].scenePos()
        # #         props_saved['labelPos'] = (label_pos.x(), label_pos.y())
        # #
        # #         props_saved.pop('vertexCircles')
        # #         props_saved.pop('labelTextArtist')
        # #
        # #         accepted_proposal_props.append(props_saved)
        #
        #     # print '#############'
        #     # print accepted_proposal_props
        #
        #     # labeling_path = self.dms[sec].save_annotation(accepted_proposal_props, self.username, timestamp)
        #     labeling_path = DataManager.save_annotation(accepted_proposal_props, self.stack, sec, self.username, timestamp,
        #     annotation_rootdir=annotation_midbrainIncluded_rootdir)
        #
        #     # print self.new_labelnames
        #     self.dms[sec].add_labelnames(self.new_labelnames, os.environ['REPO_DIR']+'/gui/newStructureNames.txt')
        #
        #     self.statusBar().showMessage('Labelings saved to %s' % (self.username+'_'+timestamp))
        #
        #     if sec in self.gscenes:
        #         pix = QPixmap(self.dms[sec].image_width/8, self.dms[sec].image_height/8)
        #         painter = QPainter(pix)
        #
        #         self.gscenes[sec].render(painter, QRectF(0,0,self.dms[sec].image_width/8, self.dms[sec].image_height/8),
        #                                 QRectF(0,0,self.dms[sec].image_width, self.dms[sec].image_height))
        #         pix.save(labeling_path[:-4] + '.jpg', "JPG")
        #         print 'Preview image saved to', labeling_path[:-4] + '.jpg'
        #         del painter
        #         del pix

    @pyqtSlot()
    def load(self):
        """
        Load stored annotations.
        """
        # self.gscenes['sagittal'].load_drawings(username='Lauren', timestamp='latest', annotation_rootdir=annotation_midbrainIncluded_v2_rootdir)
        # self.gscenes['sagittal'].load_drawings(username='yuncong', timestamp='latest', annotation_rootdir=annotation_midbrainIncluded_v2_rootdir

        # Load traditional version of labelings
        # contour_df_original, structure_df = DataManager.load_annotation_v3(stack=self.stack)
        # contour_df = convert_annotation_v3_original_to_aligned_cropped(contour_df_original, stack=self.stack)

        # Load pipeline generated atlas-aligned annotations
        contour_df, _ = DataManager.load_annotation_v3(stack=self.stack, by_human=False,
        stack_m='atlasV3', warp_setting=8, classifier_setting_m=37, classifier_setting_f=37)

        self.contour_df_loaded = contour_df
        sagittal_contours = contour_df[(contour_df['orientation'] == 'sagittal') & (contour_df['downsample'] == self.gscenes['sagittal'].data_feeder.downsample)]
        self.gscenes['sagittal'].load_drawings(sagittal_contours)

        try:
            coronal_contours = contour_df[(contour_df['orientation'] == 'coronal') & (contour_df['downsample'] == self.gscenes['coronal'].data_feeder.downsample)]
            self.gscenes['coronal'].load_drawings(coronal_contours)
        except Exception as e:
            sys.stderr.write("Error loading coronal contours: str(e)\n")

        try:
            horizontal_contours = contour_df[(contour_df['orientation'] == 'horizontal') & (contour_df['downsample'] == self.gscenes['horizontal'].data_feeder.downsample)]
            self.gscenes['horizontal'].load_drawings(horizontal_contours)
        except Exception as e:
            sys.stderr.write("Error loading horizontal contours: str(e)\n")

        # self.sagittal_contours_loaded = sagittal_contours
        # self.coronal_contours_loaded = coronal_contours
        # self.horizontal_contours_loaded = horizontal_contours

    @pyqtSlot()
    def active_image_updated(self):
        self.setWindowTitle('BrainLabelingGUI, stack %(stack)s, fn %(fn)s, section %(sec)d, z=%(z).2f, x=%(x).2f, y=%(y).2f' % \
        dict(stack=self.stack,
        sec=self.gscenes['sagittal'].active_section
        if self.gscenes['sagittal'].active_section is not None else -1,
        fn=metadata_cache['sections_to_filenames'][self.stack][self.gscenes['sagittal'].active_section] \
        if self.gscenes['sagittal'].active_section is not None else '',
        z=self.gscenes['sagittal'].active_i,
        x=self.gscenes['coronal'].active_i if self.gscenes['coronal'].active_i is not None else 0,
        y=self.gscenes['horizontal'].active_i if self.gscenes['horizontal'].active_i is not None else 0))

    @pyqtSlot(int, int, int, str)
    def crossline_updated(self, cross_x_lossless, cross_y_lossless, cross_z_lossless, source_gscene_id):
        print 'GUI: update all crosses to', cross_x_lossless, cross_y_lossless, cross_z_lossless, 'from', source_gscene_id

        for gscene_id, gscene in self.gscenes.iteritems():
            # if gscene_id != source_gscene_id:
            #     gscene.update_cross(cross_x_lossless, cross_y_lossless, cross_z_lossless)
            gscene.update_cross(cross_x_lossless, cross_y_lossless, cross_z_lossless)

    @pyqtSlot(object)
    def drawings_updated(self, polygon):
        print 'Drawings updated.'
        # self.save()

        # sagittal_label_section_lookup = self.gscenes['sagittal'].get_label_section_lookup()
        # labels = sagittal_label_section_lookup.keys()

        # self.gscenes['coronal'].get_label_section_lookup()
        # self.gscenes['horizontal'].get_label_section_lookup()


    @pyqtSlot(str, str, bool, bool)
    def update_structure_volume(self, name_u, side, use_confirmed_only, recompute_from_contours):
        """
        This function is triggered by `structure_volume_updated` signal from
        any of the three gscenes.

        - Retrieve the volumes stored internally for each view.
        The volumes in different views are potentially different.
        - Compute the average volume across all views.
        - Use this average volume to update the stored version in each view.

        Args:
            use_confirmed_only (bool): If True, when reconstructing the volume, only use confirmed contours.
            recompute_from_contours (bool): Set to True, if want to re-compute the volume based on contours,
            replacing the volume in `self.structure_volumes` if it already exists.
            Set to False, if `self.structure_volumes` already stores the new volume and therefore
            calling this function is just to update the contours.
        """

        # Arguments passed in are Qt Strings. This guarantees they are python str.
        name_u = str(name_u)
        side = str(side)

        # Set the downsample factor for the structure volumes.
        # Try to match the highest resolution among all gviews, but upper limit is 1/8.
        self.volume_downsample_factor = max(8, np.min([gscene.data_feeder.downsample for gscene in self.gscenes.itervalues()]))
        for gscene in self.gscenes.values():
            gscene.set_structure_volumes_downscale_factor(self.volume_downsample_factor)

        # Reconstruct the volume for each gview.
        # Only interpolate between confirmed contours.

        # volumes_3view = {}
        # bboxes_3view = {}

        # for gscene_id, gscene in self.gscenes.iteritems():

        if (name_u, side) not in self.structure_volumes or recompute_from_contours:

            print 'Re-computing volume from contours.'

            gscene_id = self.sender().id
            gscene = self.gscenes[gscene_id]

            if use_confirmed_only:
                matched_confirmed_polygons = [p for i, polygons in gscene.drawings.iteritems() for p in polygons \
                                    if p.properties['label'] == name_u and \
                                    p.properties['side'] == side and \
                                    p.properties['type'] != 'interpolated']
            else:
                matched_confirmed_polygons = [p for i, polygons in gscene.drawings.iteritems() for p in polygons \
                if p.properties['label'] == name_u and \
                p.properties['side'] == side]

            if len(matched_confirmed_polygons) < 2:
                sys.stderr.write('%s: Cannot interpolate because there are fewer than two confirmed polygons for structure %s.\n' % (gscene_id, (name_u, side)))
                return

            factor_volResol = float(gscene.data_feeder.downsample) / self.volume_downsample_factor

            if gscene_id == 'sagittal':
                contour_points_grouped_by_pos = {p.properties['position'] * factor_volResol: \
                                                [(c.scenePos().x() * factor_volResol,
                                                c.scenePos().y() * factor_volResol)
                                                for c in p.vertex_circles] for p in matched_confirmed_polygons}
                self.structure_volumes[(name_u, side)] = interpolate_contours_to_volume(contour_points_grouped_by_pos, 'z')

            elif gscene_id == 'coronal':
                contour_points_grouped_by_pos = {p.properties['position'] * factor_volResol: \
                                                [(c.scenePos().y() * factor_volResol,
                                                (gscene.data_feeder.z_dim - 1 - c.scenePos().x()) * factor_volResol)
                                                for c in p.vertex_circles] for p in matched_confirmed_polygons}
                # volume, bbox = interpolate_contours_to_volume(contour_points_grouped_by_pos, 'x')
                # self.gscenes[gscene_id].structure_volumes[(name_u, side)] = volume, bbox
                self.structure_volumes[(name_u, side)] = interpolate_contours_to_volume(contour_points_grouped_by_pos, 'x')

            elif gscene_id == 'horizontal':
                contour_points_grouped_by_pos = {p.properties['position'] * factor_volResol: \
                                                [(c.scenePos().x() * factor_volResol,
                                                (gscene.data_feeder.z_dim - 1 - c.scenePos().y()) * factor_volResol)
                                                for c in p.vertex_circles] for p in matched_confirmed_polygons}
                # volume, bbox = interpolate_contours_to_volume(contour_points_grouped_by_pos, 'y')
                # self.gscenes[gscene_id].structure_volumes[(name_u, side)] = volume, bbox
                # self.gscenes[gscene_id].structure_volumes[(name_u, side)] = interpolate_contours_to_volume(contour_points_grouped_by_pos, 'y')
                self.structure_volumes[(name_u, side)] = interpolate_contours_to_volume(contour_points_grouped_by_pos, 'y')

            # volumes_3view[gscene_id] = volume
            # bboxes_3view[gscene_id] = bbox

        # self.structure_volumes[(name_u, side)] = \
        # average_multiple_volumes(volumes_3view.values(), bboxes_3view.values())
        # self.structure_volumes[(name_u, side)] = self.gscenes['sagittal'].structure_volumes[(name_u, side)]

        self.gscenes['coronal'].update_drawings_from_structure_volume(name_u, side)
        self.gscenes['horizontal'].update_drawings_from_structure_volume(name_u, side)
        self.gscenes['sagittal'].update_drawings_from_structure_volume(name_u, side)

        print '3D structure updated.'
        self.statusBar().showMessage('3D structure updated.')

    def eventFilter(self, obj, event):
        # print obj.metaObject().className(), event.type()

        if event.type() == QEvent.KeyPress:
            key = event.key()
            if key == Qt.Key_1:
                self.gscenes['sagittal'].show_previous()
            elif key == Qt.Key_2:
                self.gscenes['sagittal'].show_next()
            elif key == Qt.Key_3:
                self.gscenes['coronal'].show_previous()
            elif key == Qt.Key_4:
                self.gscenes['coronal'].show_next()
            elif key == Qt.Key_5:
                self.gscenes['horizontal'].show_previous()
            elif key == Qt.Key_6:
                self.gscenes['horizontal'].show_next()

            elif key == Qt.Key_Space:
                if not event.isAutoRepeat():
                    for gscene in self.gscenes.itervalues():
                        gscene.set_mode('crossline')

            elif key == Qt.Key_U:

                curr_structure_label = self.gscenes['sagittal'].active_polygon.properties['label']
                curr_structure_side = self.gscenes['sagittal'].active_polygon.properties['side']

                name_side_tuple = (curr_structure_label, curr_structure_side)
                assert name_side_tuple in self.structure_volumes, \
                "structure_volumes does not have %s. Need to reconstruct this structure first." % str(name_side_tuple)

                if name_side_tuple in self.gscenes['sagittal'].uncertainty_lines:
                    print "Remove uncertainty line"
                    for gscene in self.gscenes.itervalues():
                        gscene.hide_uncertainty_line(name_side_tuple)
                else:
                    print "Add uncertainty line"
                    if curr_structure_side == 'S':
                        name = curr_structure_label
                    else:
                        name = curr_structure_label + '_' + curr_structure_side
                    current_structure_hessians = DataManager.load_confidence(stack_m='atlasV3', stack_f=self.stack, classifier_setting_m=37, classifier_setting_f=37, warp_setting=8,
                    param_suffix=name, what='hessians')
                    H, fmax = current_structure_hessians[84.64]

                    U, S, UT = np.linalg.svd(H)
                    flattest_dir = U[:,-1]

                    current_structure_peakwidth = DataManager.load_confidence(stack_m='atlasV3', stack_f=self.stack, classifier_setting_m=37, classifier_setting_f=37, warp_setting=8,
                    param_suffix=name, what='peak_radius')
                    pw_max_um, _, _ = current_structure_peakwidth[118.75][84.64]
                    len_lossless_res = pw_max_um / XY_PIXEL_DISTANCE_LOSSLESS

                    vol, bbox = self.structure_volumes[name_side_tuple]
                    c_vol_res_gl = np.mean(np.where(vol), axis=1)[[1,0,2]] + (bbox[0], bbox[2], bbox[4])

                    e1 = c_vol_res_gl * self.volume_downsample_factor - len_lossless_res * flattest_dir
                    e2 = c_vol_res_gl * self.volume_downsample_factor + len_lossless_res * flattest_dir

                    for gscene in self.gscenes.itervalues():
                        e1_gscene = point3d_to_point2d(e1, gscene)
                        e2_gscene = point3d_to_point2d(e2, gscene)
                        print gscene.id, e1_gscene, e2_gscene
                        gscene.set_uncertainty_line(name_side_tuple, e1_gscene, e2_gscene)

                if name_side_tuple in self.gscenes['sagittal'].structure_onscreen_messages:
                    self.gscenes['sagittal'].hide_structure_onscreen_message(name_side_tuple)
                else:
                    current_structure_zscores = DataManager.load_confidence(stack_m='atlasV3', stack_f=self.stack, classifier_setting_m=37, classifier_setting_f=37, warp_setting=8,
                    param_suffix=name, what='zscores')
                    zscore, fmax, mean, std = current_structure_zscores[118.75]
                    print str((zscore, fmax, mean, std)), np.array(e1_gscene + e2_gscene)/2
                    self.gscenes['sagittal'].set_structure_onscreen_message(name_side_tuple, "zscore = %.2f" % zscore, (e1_gscene + e2_gscene)/2)

        elif event.type() == QEvent.KeyRelease:
            key = event.key()
            if key == Qt.Key_Space:
                if not event.isAutoRepeat():
                    for gscene in self.gscenes.itervalues():
                        gscene.set_mode('idle')

        return False

def point3d_to_point2d(pt3d, gscene):
    """
    Convert a 3D point to 2D point on a gscene.

    Args:
        pt3d ((3,)-ndarray): a point coordinate in lossless-resolution coordinate.
        gscene (QGraphicScene)
    """
    pt3d_gscene_res = pt3d / gscene.data_feeder.downsample
    if gscene.id == 'sagittal':
        pt2d = (pt3d_gscene_res[0], pt3d_gscene_res[1])
    elif gscene.id == 'coronal':
        pt2d = (gscene.data_feeder.z_dim - 1 - pt3d_gscene_res[2], pt3d_gscene_res[1])
    elif gscene.id == 'horizontal':
        pt2d = (pt3d_gscene_res[0], gscene.data_feeder.z_dim - 1 - pt3d_gscene_res[2])
    return np.array(pt2d)

def load_structure_names(fn):
    """
    Load structure names from a file.

    Args:
        fn (str): a file containing rows of structure names.
    Returns:
        (list of str)
    """
    names = {}
    with open(fn, 'r') as f:
        for ln in f.readlines():
            abbr, fullname = ln.split('\t')
            names[abbr] = fullname.strip()
    return names


if __name__ == "__main__":

    import argparse
    import sys
    import time

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description='Launch brain labeling GUI.')

    parser.add_argument("stack_name", type=str, help="stack name")
    parser.add_argument("-f", "--first_sec", type=int, help="first section")
    parser.add_argument("-l", "--last_sec", type=int, help="last section")
    parser.add_argument("-d", "--downsample", type=int, help="downsample", default=1)
    args = parser.parse_args()

    from sys import argv, exit
    appl = QApplication(argv)

    stack = args.stack_name
    downsample = args.downsample

    default_first_sec, default_last_sec = DataManager.load_cropbox(stack)[4:]

    first_sec = default_first_sec if args.first_sec is None else args.first_sec
    last_sec = default_last_sec if args.last_sec is None else args.last_sec

    m = BrainLabelingGUI(stack=stack, first_sec=first_sec, last_sec=last_sec, downsample=downsample)

    m.showMaximized()
    m.raise_()
    exit(appl.exec_())
