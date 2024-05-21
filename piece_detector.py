from ultralytics import YOLO


class PieceDetector:
    def __init__(self, model_path, device_type):
        self.model = YOLO(model_path).to(device_type)

    def detect_piece(self, frame):
        result = self.model.predict(frame)

        board_matrix = [['.' for _ in range(8)] for _ in range(8)]

        boxes = result[0].boxes
        names = result[0].names

        piece_name_map = {
            'b-rook': 'bR', 'b-knight': 'bN', 'b-bishop': 'bB', 'b-queen': 'bQ', 'b-king': 'bK', 'b-pawn': 'bp',
            'w-rook': 'wR', 'w-knight': 'wN', 'w-bishop': 'wB', 'w-queen': 'wQ', 'w-king': 'wK', 'w-pawn': 'wp'
        }

        for box in boxes:
            class_id = int(box.cls.item())
            piece_type = names[class_id]

            x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()

            col = int((x1 + x2) / 2 // (result[0].orig_shape[1] / 8))
            row = int((y1 + y2) / 2 // (result[0].orig_shape[0] / 8))

            piece = piece_name_map.get(piece_type, '.')

            board_matrix[row][col] = piece

        return board_matrix
