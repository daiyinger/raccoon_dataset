import cv2
import numpy as np
import tensorflow as tf
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as vis_util


class TOD(object):
    def __init__(self):
        self.PATH_TO_CKPT = r'E:\code\raccoon_dataset\training\output_inference_graph.pb'
        self.PATH_TO_LABELS = r'E:\code\raccoon_dataset\training\object-detection.pbtxt'
        self.NUM_CLASSES = 1
        self.detection_graph = self._load_model()
        self.category_index = self._load_label_map()

    def _load_model(self):
        detection_graph = tf.Graph()
        with detection_graph.as_default():
            od_graph_def = tf.GraphDef()
            with tf.gfile.GFile(self.PATH_TO_CKPT, 'rb') as fid:
                serialized_graph = fid.read()
                od_graph_def.ParseFromString(serialized_graph)
                tf.import_graph_def(od_graph_def, name='')
        return detection_graph

    def _load_label_map(self):
        label_map = label_map_util.load_labelmap(self.PATH_TO_LABELS)
        categories = label_map_util.convert_label_map_to_categories(label_map,
                                                                    max_num_classes=self.NUM_CLASSES,
                                                                    use_display_name=True)
        category_index = label_map_util.create_category_index(categories)
        return category_index

    def detect(self, image):
        result = False
        with self.detection_graph.as_default():
            with tf.Session(graph=self.detection_graph) as sess:
                # Expand dimensions since the model expects images to have shape: [1, None, None, 3]
                image_np_expanded = np.expand_dims(image, axis=0)
                image_tensor = self.detection_graph.get_tensor_by_name('image_tensor:0')
                boxes = self.detection_graph.get_tensor_by_name('detection_boxes:0')
                scores = self.detection_graph.get_tensor_by_name('detection_scores:0')
                classes = self.detection_graph.get_tensor_by_name('detection_classes:0')
                num_detections = self.detection_graph.get_tensor_by_name('num_detections:0')
                # Actual detection.
                (boxes, scores, classes, num_detections) = sess.run(
                    [boxes, scores, classes, num_detections],
                    feed_dict={image_tensor: image_np_expanded})
                # Visualization of the results of a detection.
                vis_util.visualize_boxes_and_labels_on_image_array(
                    image,
                    np.squeeze(boxes),
                    np.squeeze(classes).astype(np.int32),
                    np.squeeze(scores),
                    self.category_index,
                    use_normalized_coordinates=True,
                    line_thickness=8)

                #s_boxes = boxes[scores > 0.5]
                s_classes = classes[scores > 0.5]
                #s_scores=scores[scores>0.5]
                if(len(s_classes) > 0):
                    result = True
            return (result,image)


if __name__ == '__main__':
    image_list = ['test\\raccoon-1.jpg','test\\raccoon-2.jpg','test\\raccoon-5.jpg',
                  'test\\raccoon-3.jpg','test\\raccoon-4.jpg', 'test\\image.jpg']
    detecotr = TOD()
    num = 0
    for data in image_list:
        result, image = detecotr.detect(cv2.imread(data))
        print(result)
        num += 1
        cv2.imshow("detection"+str(num), image)
        cv2.waitKey(2000)
        cv2.destroyAllWindows()
