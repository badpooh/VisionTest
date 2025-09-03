import cv2
import numpy as np
import time
import sys
from PySide6 import QtWidgets
from PySide6.QtWidgets import QMainWindow
from PySide6.QtWidgets import *
from paddleocr import PaddleOCR


class WebCam:
    def __init__(self, main_window=None):
        super().__init__()
        self.capture = self.find_available_camera()
        self.streaming = False
        self.dragging = False
        self.x1, self.y1, self.x2, self.y2 = -1, -1, -1, -1
        self.selected_area = None
        self.last_ocr_time = 0
        self.main_window = main_window
        self.selected_area_window_created = False
        self.last_boundary_update = time.time()
        self.last_ocr_update = time.time()
        self.boundary_box = None
        # self.use_gpu = torch.cuda.is_available()
        self.reader = PaddleOCR(use_angle_cls=False, lang='en',
                                use_space_char=True, show_log=False,)
        self.ocr_results = []  # OCR 결과 저장
        self.ocr_display_end_time = 0  # OCR 결과 표시 종료 시간
        self.ocr_display_time = 3
        self.focus_value = 120
        self.mouse_x = 0  # 마우스 커서의 x 좌표
        self.mouse_y = 0  # 마우스 커서의 y 좌표
        self.green_detected_last_frame = False
        self.green_printed = False
        self.initial_selected_area = None
        self.middle_box_detected = False
        self.template = cv2.imread(
            r"image_test\a3700nwiring.png", cv2.IMREAD_COLOR)

    def find_available_camera(self):
        max_tested = 10
        for i in range(max_tested):
            cap = cv2.VideoCapture(i, cv2.CAP_DSHOW)
            if cap.isOpened():
                print(f"Camera found at index {i}")
                cap.set(cv2.CAP_PROP_AUTOFOCUS, 0)
                cap.set(cv2.CAP_PROP_FOCUS, 120)  # 수동 포커스
                cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.25)  # 자동 노출 비활성화
                cap.set(cv2.CAP_PROP_EXPOSURE, -5)  # 수동 노출 설정 (값은 조정 필요)
                cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)  # 최대 해상도 설정
                cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
                return cap
            cap.release()
        print("No available camera found.")
        return None

    def mouse_callback(self, event, x, y, flags, param):
        self.mouse_x, self.mouse_y = x, y  # 마우스 커서 좌표 업데이트
        if event == cv2.EVENT_LBUTTONDOWN:
            self.dragging = True
            self.x1, self.y1 = x, y
        elif event == cv2.EVENT_MOUSEMOVE:
            if self.dragging:
                self.x2, self.y2 = x, y
        elif event == cv2.EVENT_LBUTTONUP:
            self.dragging = False
            self.x2, self.y2 = x, y
            if self.x1 != x and self.y1 != y:
                self.selected_area = (self.x1, self.y1, self.x2, self.y2)
                # self.start_selected_streaming()

    def start_streaming(self):
        if not self.capture:
            print("카메라를 사용할 수 없습니다.")
            return

        cv2.namedWindow("Video Stream")
        cv2.moveWindow("Video Stream", 100, 100)
        cv2.setMouseCallback("Video Stream", self.mouse_callback)
        self.streaming = True
        self.stream_video()

    def stop_streaming(self):
        try:
            if cv2.getWindowProperty("Video Stream", 0) >= 0:
                cv2.destroyWindow("Video Stream")
        except cv2.error as e:
            print("Error:", e)
        finally:
            self.streaming = False

    def start_selected_streaming(self):
        if not self.capture:
            print("카메라를 사용할 수 없습니다.")
            return

        cv2.namedWindow("Selected Stream")
        cv2.moveWindow("Selected Stream", 800, 100)
        self.selected_area_window_created = True

    def stop_selected_streaming(self):
        try:
            if cv2.getWindowProperty("Selected Stream", 0) >= 0:
                cv2.destroyWindow("Selected Stream")
        except cv2.error as e:
            print("Error:", e)
        finally:
            self.selected_area_window_created = False
        self.selected_area = None

    def adjust_focus(self):
        if self.capture:
            self.capture.set(cv2.CAP_PROP_AUTOFOCUS, 0)
            self.capture.set(cv2.CAP_PROP_FOCUS, self.focus_value)

    def preprocess_image(self, image):

        kernel = np.ones((2, 3), np.uint8)
        eroded = cv2.erode(image, kernel, iterations=1)

        blurred_image = cv2.GaussianBlur(eroded, (1, 1), 0)
        removed_blur_image = cv2.addWeighted(image, 2, blurred_image, -1, 1)
        return blurred_image

    def template_matching(self, image, template, threshold=0.8):
        result = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
        loc = np.where(result >= threshold)
        if len(loc[0]) > 0:
            return True
        return False

    def draw_boundary_box(self, image):
        if self.boundary_box is not None:
            x, y, w, h = self.boundary_box
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        return image

    def ocr_and_draw_text(self, image):
        if self.selected_area is not None:
            x1, y1, x2, y2 = self.selected_area
            if x1 < x2 and y1 < y2:  # 선택된 영역이 유효한지 확인
                cropped_image = image[y1:y2, x1:x2]
                if cropped_image.size != 0:  # cropped_image가 비어있지 않은지 확인
                    self.ocr_results = self.reader.readtext(cropped_image)
        return image

    def draw_ocr_results(self, image):
        if self.ocr_results:
            for (bbox, text, prob) in self.ocr_results:
                (tl, tr, br, bl) = bbox
                if self.selected_area is not None:
                    x1, y1, _, _ = self.selected_area
                    tl = (int(tl[0] + x1), int(tl[1] + y1))
                    tr = (int(tr[0] + x1), int(tr[1] + y1))
                    br = (int(br[0] + x1), int(br[1] + y1))
                    bl = (int(bl[0] + x1), int(bl[1] + y1))

                # 박스 그리기
                cv2.rectangle(image, tl, br, (0, 0, 255), 2)
                # 텍스트 그리기
                cv2.putText(
                    image, text, (tl[0], tl[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        if self.selected_area:
            x1, y1, x2, y2 = self.selected_area
            relative_mouse_x = self.mouse_x - x1
            relative_mouse_y = self.mouse_y - y1
            cv2.putText(image, f"({relative_mouse_x}, {relative_mouse_y})", (self.mouse_x + 10, self.mouse_y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        return image

    def color_distance(self, color1, color2):
        return np.sqrt(np.sum((color1 - color2) ** 2))

    # 특정 색상과의 거리가 10 이하인 픽셀을 감지하는 함수
    def detect_color(self, image, target_color=(0, 84, 74), threshold=10):
        # 색상 거리 계산을 위해 OpenCV의 벡터 연산을 사용
        target_color = np.array(target_color, dtype=np.uint8)
        diff = cv2.absdiff(image, target_color)
        mask = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        _, mask = cv2.threshold(mask, threshold, 255, cv2.THRESH_BINARY_INV)
        return mask

    def find_highest_color_ratio_area(self, image, color=(47, 180, 139), grid_size=(50, 50)):
        height, width, _ = image.shape
        max_ratio = 0
        best_rect = None

        for y in range(0, height - grid_size[1], grid_size[1]):
            for x in range(0, width - grid_size[0], grid_size[0]):
                grid = image[y:y + grid_size[1], x:x + grid_size[0]]
                mask = cv2.inRange(grid, color, color)
                ratio = cv2.countNonZero(mask) / (grid_size[0] * grid_size[1])

                if ratio > max_ratio:
                    max_ratio = ratio
                    best_rect = (x, y, grid_size[0], grid_size[1])

        return best_rect, max_ratio

    def stream_video(self):
        last_ocr_update = time.time()
        last_focus_time = time.time()

        while self.streaming:
            ret, frame = self.capture.read()
            if not ret:
                break

            self.display_frame = frame
            current_time = time.time()

            # 템플릿 매칭을 통한 팝업 감지
            res = cv2.matchTemplate(frame, self.template, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
            threshold = 0.6  # 매칭 임계값 설정
            template_matched = False
            highest_color_ratio_rect = None

            if max_val >= threshold:
                top_left = max_loc
                h, w = self.template.shape[:2]
                bottom_right = (top_left[0] + w, top_left[1] + h)
                cv2.rectangle(self.display_frame, top_left,
                              bottom_right, (0, 255, 0), 2)
                self.middle_box_detected = True
                template_matched = True

                # 템플릿 매칭된 영역 내에서 가장 높은 색 비율 영역 찾기
                template_area = frame[top_left[1]
                    :bottom_right[1], top_left[0]:bottom_right[0]]
                highest_color_ratio_rect, _ = self.find_highest_color_ratio_area(
                    template_area, color=(47, 180, 139))

                if highest_color_ratio_rect:
                    x, y, w, h = highest_color_ratio_rect
                    x1, y1 = top_left[0] + x, top_left[1] + y
                    x2, y2 = x1 + w, y1 + h
                    cv2.rectangle(self.display_frame, (x1, y1),
                                  (x2, y2), (255, 0, 0), 2)
            else:
                self.middle_box_detected = False

            if current_time - last_ocr_update >= 1:
                if template_matched and highest_color_ratio_rect:
                    # 템플릿 매칭된 부분 내에서 가장 높은 색 비율 영역 OCR 수행
                    cropped_image = frame[y1:y2, x1:x2]
                    self.ocr_results = self.reader.readtext(cropped_image)
                elif self.selected_area is not None:
                    # 선택한 부분 OCR 수행
                    x1, y1, x2, y2 = self.selected_area
                    if x1 < x2 and y1 < y2:  # 선택된 영역이 유효한지 확인
                        cropped_image = frame[y1:y2, x1:x2]
                        if cropped_image.size != 0:  # cropped_image가 비어있지 않은지 확인
                            self.ocr_results = self.reader.readtext(
                                cropped_image)

                last_ocr_update = current_time

            self.display_frame = self.draw_ocr_results(self.display_frame)

            if current_time - last_focus_time >= 3:
                self.adjust_focus()
                last_focus_time = current_time

            focus_value = self.capture.get(cv2.CAP_PROP_FOCUS)
            cv2.putText(self.display_frame, f"Focus: {focus_value}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

            if self.dragging:
                cv2.rectangle(self.display_frame, (self.x1, self.y1),
                              (self.x2, self.y2), (0, 255, 0), 2)

            # 경계 박스 그리기
            self.display_frame = self.draw_boundary_box(self.display_frame)

            cv2.imshow('Video Stream', self.display_frame)

            key = cv2.waitKey(1)
            if key & 0xFF == ord('q'):
                break
