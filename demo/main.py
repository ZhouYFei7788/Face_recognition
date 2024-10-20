import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
import cv2
import dlib
import numpy as np
from scipy.spatial import distance as dist
from ui.ui import Ui_MainWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # 初始化 Dlib 的人脸检测器和形状预测器
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor(r"D:\py_xiangmu\zq\demo\models\shape_predictor_68_face_landmarks.dat")

        # 存储已知人脸特征和对应姓名
        self.known_faces = {}  # {特征编码: 姓名}
        self.load_known_faces()  # 加载已知人脸

        # 连接按钮操作
        self.ui.pushButton.clicked.connect(self.open_camera)
        self.ui.pushButton_3.clicked.connect(self.start_recognition)

        # 初始化变量
        self.cap = None
        self.recognition_running = False
        self.blink_count = 0
        self.mouth_open_count = 0
        self.mouth_open = False  # 初始化标志位

    def load_known_faces(self):
        """加载已知���脸"""
        known_faces_names = ["yulidi", "lvchen"]  # 可添加更多姓名

        for name in known_faces_names:
            img_path = f"D:\\py_xiangmu\\zq\\demo\\data\\Face_data\\{name}.png"
            print(f"尝试加载图像: {img_path}")

            image = cv2.imread(img_path)

            if image is None:
                print(f"无法打开图像文件: {img_path}")
                continue

            gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            faces = self.detector(gray_image)
            if len(faces) > 0:
                landmarks = self.predictor(gray_image, faces[0])
                face_encoding = self.encode_face(landmarks)
                self.known_faces[name] = face_encoding

    def encode_face(self, landmarks):
        """提取人脸特征编码"""
        face_encoding = []
        for i in range(68):
            face_encoding.append((landmarks.part(i).x, landmarks.part(i).y))
        return np.array(face_encoding)

    def open_camera(self):
        """打开摄像头"""
        try:
            if self.cap is None:
                self.cap = cv2.VideoCapture(1)  # 打开第一个摄像头
                if not self.cap.isOpened():
                    raise Exception("无法打开摄像头")
                self.update_frame()  # 开始更新画面
        except Exception as e:
            print(f"Error: {e}")
            QtWidgets.QMessageBox.critical(self, "错误", str(e))

    def update_frame(self):
        """更新画面"""
        if self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                # 将 OpenCV 图像转换为 Qt 可用格式
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = rgb_frame.shape
                bytes_per_line = ch * w
                # 显示画面
                convert_to_Qt_format = QtGui.QImage(rgb_frame.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
                self.ui.label.setPixmap(QtGui.QPixmap.fromImage(convert_to_Qt_format))
                # 人脸识别
                if self.recognition_running:
                    # 识别人脸并显示结果
                    rgb_frame_with_recognition = self.recognize_face(rgb_frame)
                    convert_to_Qt_format = QtGui.QImage(rgb_frame_with_recognition.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
                    self.ui.label.setPixmap(QtGui.QPixmap.fromImage(convert_to_Qt_format))

                QtCore.QTimer.singleShot(1, self.update_frame)  # 每1毫秒更新一次画面

    def start_recognition(self):
        """开始人脸识别"""
        self.recognition_running = True
        self.update_frame()  # 开始更新画面

    def recognize_face(self, frame):
        """识别人脸并显示结果"""
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        faces = self.detector(gray_frame)

        for face in faces:
            # 获取人脸特征点
            landmarks = self.predictor(gray_frame, face)
            x1, y1, x2, y2 = face.left(), face.top(), face.right(), face.bottom()
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

            current_face_encoding = self.encode_face(landmarks)
            name, accuracy = self.find_best_match(current_face_encoding)

            if name:
                # 显示姓名和准确率
                self.ui.label_6.setText(name)
                self.ui.label_8.setText(f"{accuracy:.2f}%")
                cv2.putText(frame, name, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                cv2.putText(frame, f"{accuracy:.2f}%", (x1, y1 - 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

                face_image = frame[y1:y2, x1:x2]
                face_image = cv2.resize(face_image, (100, 100))
                face_qimage = QtGui.QImage(face_image.data, face_image.shape[1], face_image.shape[0],
                                           face_image.strides[0], QtGui.QImage.Format_RGB888)
                self.ui.label_2.setPixmap(QtGui.QPixmap.fromImage(face_qimage))

                # 更新进度条
                self.ui.progressBar.setValue(int(accuracy))

            # 眨眼检测
            left_eye_ratio = self.eye_aspect_ratio(landmarks, [36, 37, 38, 39, 40, 41])
            right_eye_ratio = self.eye_aspect_ratio(landmarks, [42, 43, 44, 45, 46, 47])
            if left_eye_ratio < 0.25 and right_eye_ratio < 0.25:
                self.blink_count += 1
                self.ui.yn.setText(f"眨眼次数: {self.blink_count}")

            # 张嘴���测
            mouth_ratio = self.mouth_aspect_ratio(landmarks, [60, 62, 64, 66])
            if mouth_ratio > 0.5:  # 降低阈值
                if not self.mouth_open:
                    self.mouth_open_count += 1
                    print("张嘴:", self.mouth_open_count)
                    self.ui.YN.setText(f"张嘴次数: {self.mouth_open_count}")
                    self.mouth_open = True
            else:
                self.mouth_open = False

        return frame

    def eye_aspect_ratio(self, landmarks, eye_points):
        """计算眼睛纵横比"""
        A = dist.euclidean((landmarks.part(eye_points[1]).x, landmarks.part(eye_points[1]).y),
                           (landmarks.part(eye_points[5]).x, landmarks.part(eye_points[5]).y))
        B = dist.euclidean((landmarks.part(eye_points[2]).x, landmarks.part(eye_points[2]).y),
                           (landmarks.part(eye_points[4]).x, landmarks.part(eye_points[4]).y))
        C = dist.euclidean((landmarks.part(eye_points[0]).x, landmarks.part(eye_points[0]).y),
                           (landmarks.part(eye_points[3]).x, landmarks.part(eye_points[3]).y))
        ear = (A + B) / (2.0 * C)
        return ear

    def mouth_aspect_ratio(self, landmarks, mouth_points):
        """计算嘴巴纵横比"""
        A = dist.euclidean((landmarks.part(mouth_points[1]).x, landmarks.part(mouth_points[1]).y),
                           (landmarks.part(mouth_points[3]).x, landmarks.part(mouth_points[3]).y))
        B = dist.euclidean((landmarks.part(mouth_points[0]).x, landmarks.part(mouth_points[0]).y),
                           (landmarks.part(mouth_points[2]).x, landmarks.part(mouth_points[2]).y))
        mar = A / B * 2
        return mar

    def find_best_match(self, current_face_encoding):
        """查找最佳匹配"""
        best_match_name = None
        best_match_distance = float('inf')
        print("当前人脸特征编码:", current_face_encoding)  # 添加调试信息

        # 标准化当前人脸特征编码
        current_face_encoding = (current_face_encoding - np.mean(current_face_encoding)) / np.std(current_face_encoding)

        for name, known_face_encoding in self.known_faces.items():
            # 标准化已知人脸特征编码
            known_face_encoding = (known_face_encoding - np.mean(known_face_encoding)) / np.std(known_face_encoding)
            # 计��欧氏距离
            distance = np.linalg.norm(known_face_encoding - current_face_encoding)
            print(f"与 {name} 的距离: {distance}")  # 添加调试信息
            if distance < best_match_distance:
                best_match_distance = distance
                best_match_name = name

        # 计算准确率 (0-100)
        accuracy = max(0, 100 - best_match_distance * 10)  # 调整系数以提高准确率
        print(f"最佳匹配: {best_match_name}, 准确率: {accuracy:.2f}%")  # 添加调试信息
        return best_match_name, accuracy

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())