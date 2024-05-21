from ultralytics import YOLO
import cv2


class ChessResize:
    def __init__(self, model_path, device_type):
        self.model = YOLO(model_path).to(device_type)

    def resize(self, frame):
        result = self.model.predict(frame)

        x1, y1, x2, y2 = result[0].boxes.xyxy[0]

        image = cv2.imread(result[0].path)

        return image[int(y1):int(y2), int(x1):int(x2)]
