import requests
url = 'http://192.168.0.100:8000/predict/'
r = requests.post(url, data={'detected_faces':'in object_detection module'})
import numpy as np
##import requests
r = requests.post(url, data={'detected_faces':'before tf'})
import tensorflow as tf
import sys
from PIL import Image
import cv2
import sys

from utils import label_map_util
from utils import visualization_utils as vis_util


r = requests.post(url, data={'detected_faces':'after tf and path set'})

# ------------------ Knife Model Initialization ------------------------------ #
knife_label_map = label_map_util.load_labelmap('training/labelmap.pbtxt')
r = requests.post(url, data={'detected_faces':'loading labelmap'})
knife_categories = label_map_util.convert_label_map_to_categories(
    knife_label_map, max_num_classes=1, use_display_name=True)
knife_category_index = label_map_util.create_category_index(knife_categories)
r = requests.post(url, data={'detected_faces':'knife model started...'})
knife_detection_graph = tf.Graph()

with knife_detection_graph.as_default():
    knife_od_graph_def = tf.GraphDef()
    with tf.gfile.GFile('inference_graph_3/frozen_inference_graph.pb', 'rb') as fid:
        knife_serialized_graph = fid.read()
        knife_od_graph_def.ParseFromString(knife_serialized_graph)
        tf.import_graph_def(knife_od_graph_def, name='')

    knife_session = tf.Session(graph=knife_detection_graph)

knife_image_tensor = knife_detection_graph.get_tensor_by_name('image_tensor:0')
knife_detection_boxes = knife_detection_graph.get_tensor_by_name(
    'detection_boxes:0')
knife_detection_scores = knife_detection_graph.get_tensor_by_name(
    'detection_scores:0')
knife_detection_classes = knife_detection_graph.get_tensor_by_name(
    'detection_classes:0')
knife_num_detections = knife_detection_graph.get_tensor_by_name(
    'num_detections:0')
# ---------------------------------------------------------------------------- #
r = requests.post(url, data={'detected_faces':'knife model ok'})
# ------------------ General Model Initialization ---------------------------- #
general_label_map = label_map_util.load_labelmap('data/mscoco_label_map.pbtxt')
general_categories = label_map_util.convert_label_map_to_categories(
    general_label_map, max_num_classes=90, use_display_name=True)
general_category_index = label_map_util.create_category_index(
    general_categories)

general_detection_graph = tf.Graph()

with general_detection_graph.as_default():
    general_od_graph_def = tf.GraphDef()
    with tf.gfile.GFile('ssd_mobilenet_v1_coco_2017_11_17/frozen_inference_graph.pb', 'rb') as fid:
        general_serialized_graph = fid.read()
        general_od_graph_def.ParseFromString(general_serialized_graph)
        tf.import_graph_def(general_od_graph_def, name='')

    general_session = tf.Session(graph=general_detection_graph)

general_image_tensor = general_detection_graph.get_tensor_by_name(
    'image_tensor:0')
general_detection_boxes = general_detection_graph.get_tensor_by_name(
    'detection_boxes:0')
general_detection_scores = general_detection_graph.get_tensor_by_name(
    'detection_scores:0')
general_detection_classes = general_detection_graph.get_tensor_by_name(
    'detection_classes:0')
general_num_detections = general_detection_graph.get_tensor_by_name(
    'num_detections:0')
# ---------------------------------------------------------------------------- #

def knife(image_path):
    try:
        image = cv2.imread(image_path)
        image_expanded = np.expand_dims(image, axis=0)
        (boxes, scores, classes, num) = knife_session.run(
            [knife_detection_boxes, knife_detection_scores,
                knife_detection_classes, knife_num_detections],
            feed_dict={knife_image_tensor: image_expanded})

        classes = np.squeeze(classes).astype(np.int32)
        scores = np.squeeze(scores)
        boxes = np.squeeze(boxes)

        for c in range(0, len(classes)):
            class_name = knife_category_index[classes[c]]['name']
            if class_name == 'knife' and scores[c] > .80:
                confidence = scores[c] * 100
                break
            else:
                confidence = 0.00
    except:
        confidence = 0.0   # Some error has occurred
    return confidence


def general(image_path):
    try:
        image = cv2.imread(image_path)
        image_expanded = np.expand_dims(image, axis=0)
        (boxes, scores, classes, num) = general_session.run(
            [general_detection_boxes, general_detection_scores,
                general_detection_classes, general_num_detections],
            feed_dict={general_image_tensor: image_expanded})

        classes = np.squeeze(classes).astype(np.int32)
        scores = np.squeeze(scores)
        boxes = np.squeeze(boxes)

        object_name = []
        object_score = []

        for c in range(0, len(classes)):
            class_name = general_category_index[classes[c]]['name']
            if scores[c] > .30:   # If confidence level is good enough
                object_name.append(class_name)
                object_score.append(str(scores[c] * 100)[:5])
    except:
        object_name = ['']
        object_score = ['']
    return object_name, object_score


if __name__ == '__main__':
    print(' in main')
