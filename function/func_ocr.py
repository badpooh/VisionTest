import numpy as np
import cv2
from paddleocr import PaddleOCR
from itertools import chain
import os

from config.config_demo_roi import Configs

class PaddleOCRManager:

    def __init__(self, n=3):
        self.n = n
        self.config = Configs(n=self.n)
        self.rois = self.config.roi_params()
        self.phasor_condition = 0

    def color_detection(self, image, color_data):
        x, y, w, h, R, G, B = color_data
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        selected_area = image_rgb[y:y+h, x:x+w]
        average_color = np.mean(selected_area, axis=(0, 1))
        target_color = np.array([R, G, B])
        color_difference = np.linalg.norm(average_color - target_color)
        return color_difference
    
    def update_n(self, new_n):
        self.n = new_n
        self.config.update_n(new_n)
        self.rois = self.config.roi_params()
        # print(f"n 값이 {new_n}으로 변경되었습니다.")

    def update_phasor_condition(self, new_c):
        self.phasor_condition = new_c

    def paddleocr_basic(self, image, roi_keys):
        execution_directory = os.getcwd()

        rec_model_folder_path = os.path.join(execution_directory, 'ppocr', 'rec', 'en_PP-OCRv5_mobile_rec_infer')
        rec_model_folder_path = os.path.normpath(rec_model_folder_path).replace('\\', '/')

        det_model_folder_path = os.path.join(execution_directory, 'ppocr', 'det', 'PP-OCRv5_server_det_infer')
        det_model_folder_path = os.path.normpath(det_model_folder_path).replace('\\', '/')

        img_path = image  # 원본 경로 보존 (로그용)
        image = cv2.imread(img_path)
        if image is None:
            print(f"이미지를 읽을 수 없습니다: {img_path}")
            # roi_keys 개수만큼 빈 문자열로 채워서 인덱스 일치 유지
            return [""] * len(roi_keys)

        ocr = PaddleOCR(
            use_doc_orientation_classify=False,
            use_doc_unwarping=False,
            use_textline_orientation=False,
            text_detection_model_name="PP-OCRv5_server_det",
            text_detection_model_dir=det_model_folder_path,
            text_recognition_model_name="en_PP-OCRv5_mobile_rec",
            text_recognition_model_dir=rec_model_folder_path,
            lang='en',
        )

        results_in_order = []
        min_score = 0.5  # 필요 시 조정

        for roi_key in roi_keys:
            self.update_n(1)

            if roi_key not in self.rois:
                print(f"{roi_key}가 self.rois에 존재하지 않습니다.")
                results_in_order.append("")   # 자리 보전
                continue

            x, y, w, h = self.rois[roi_key]
            roi_image = image[y:y+h, x:x+w]

            # pred_list = ocr.predict(roi_image, use_textline_orientation=False)
            pred_list = ocr.predict(roi_image)

            joined_text = ""  # 기본값: 감지 실패 시 빈 문자열
            if pred_list:
                # v5는 결과 "객체" 리스트 (len>=1 가정)
                r_obj = pred_list[0]
                if hasattr(r_obj, "to_dict"):
                    r = r_obj.to_dict().get("res", {})
                elif hasattr(r_obj, "res"):
                    r = r_obj.res
                elif isinstance(r_obj, dict):
                    r = r_obj.get("res", r_obj)
                else:
                    r = {}

                rec_texts  = r.get("rec_texts", []) or []
                rec_scores = r.get("rec_scores", []) or []
                rec_polys  = r.get("rec_polys", r.get("dt_polys", [])) or []

                # 점수 필터 통과하는 텍스트만 모으기
                collected = []
                for text, score in zip(rec_texts, rec_scores):
                    t = (text or "").strip()
                    if t and float(score) >= min_score:
                        collected.append(t)

                # 여러 라인/박스면 한 칸으로 합치기 (필요 시 '\n'.join으로 바꿔도 됨)
                joined_text = " ".join(collected).strip()

            results_in_order.append(joined_text)

            print(f"{roi_key}: {joined_text}")

        return results_in_order

    def merge_texts(self, orig_text, new_text, orig_coords, new_coords):
        if len(new_text) < len(orig_text):
            if new_coords[0][0] > orig_coords[0][0]:
                return orig_text[:len(orig_text)-len(new_text)] + new_text
            else:    
                return new_text + orig_text[len(new_text):]
        else:
            return new_text

    def handle_special_cases(self, text):
        if not isinstance(text, str):
             print(f"Warning: handle_special_cases received non-string input: {type(text)}")
             return "handle_special_cases type error"
        words = text.strip().split()
        processed_words = []
        for i, word in enumerate(words):
            original_word = word
            if word == 'V':
                has_word_before = (i > 0)
                has_word_after = (i < len(words) - 1)
                if has_word_before and has_word_after:
                    # 앞뒤로 단어가 있는 경우 'V'를 제외
                    print(f"예외 처리: '{word}'를 결과에서 제외")
                    continue  # 'V'를 결과에서 제외하고 다음 단어로 이동

            if word.upper() == 'O':
                has_word_before = (i > 0)
                has_word_after = (i < len(words) - 1)
                if not has_word_before or not has_word_after:
                    print(f"예외 처리 (Isolated O->0): '{original_word}'를 '0'으로 변경")
                    word = '0'
                # else: # 중간에 있는 'O'는 변경하지 않음
                #     print(f"Info: Keeping middle 'O': '{original_word}'")

            processed_words.append(word)
        return ' '.join(processed_words)
    


### 기존 코드
# def paddleocr_basic(self, image, roi_keys):
#         execution_directory = os.getcwd()

#         rec_model_folder_path = os.path.join(execution_directory, 'ppocr', 'rec', 'en_PP-OCRv5_mobile_rec_infer')
#         rec_model_folder_path = os.path.normpath(rec_model_folder_path)
#         rec_model_folder_path = rec_model_folder_path.replace('\\', '/')

#         det_model_folder_path = os.path.join(execution_directory, 'ppocr', 'det', 'PP-OCRv5_server_det_infer')
#         det_model_folder_path = os.path.normpath(det_model_folder_path)
#         det_model_folder_path = det_model_folder_path.replace('\\', '/')

#         image = cv2.imread(image)
#         if image is None:
#             print(f"이미지를 읽을 수 없습니다: {image}")
#             return []

#         ocr = PaddleOCR(
#                         use_doc_orientation_classify=False,
#                         use_doc_unwarping=False,
#                         use_textline_orientation=False,
#                         text_detection_model_name="PP-OCRv5_server_det",
#                         text_detection_model_dir=det_model_folder_path,

#                         text_recognition_model_name="en_PP-OCRv5_mobile_rec",
#                         text_recognition_model_dir=rec_model_folder_path,
#                         lang='en',
#                         )

#         ocr_results = {}
#         for roi_key in roi_keys:
#             self.update_n(1)

#             if roi_key in self.rois:
#                 extracted_texts = []
#                 low_confidence_texts = []
#                 x, y, w, h = self.rois[roi_key]
#                 roi_image = image[y:y+h, x:x+w]

#                 # cv2.imshow("test", roi_image)
#                 # cv2.waitKey(0)
#                 # cv2.destroyAllWindows()

#                 # pred_list = ocr.predict(roi_image, use_textline_orientation=False)
#                 pred_list = ocr.predict(roi_image)
                

#                 original_results = []
#                 if pred_list:
#                     # v5는 결과 "객체" 리스트를 돌려줍니다.
#                     # 객체 -> dict로 안전하게 변환
#                     r_obj = pred_list[0]
#                     # 가능한 케이스별로 dict 꺼내기
#                     if hasattr(r_obj, "to_dict"):
#                         r = r_obj.to_dict().get("res", {})
#                     elif hasattr(r_obj, "res"):
#                         r = r_obj.res  # 일부 버전은 .res에 dict가 들어있음
#                     elif isinstance(r_obj, dict):
#                         r = r_obj.get("res", r_obj)
#                     else:
#                         r = {}

#                     rec_texts  = r.get("rec_texts", [])
#                     rec_scores = r.get("rec_scores", [])
#                     rec_polys  = r.get("rec_polys", r.get("dt_polys", []))  # 폴리곤 좌표

#                     flat_text_results = []
#                     for poly, text, score in zip(rec_polys, rec_texts, rec_scores):
#                         text = (text or "").strip()
#                         score = float(score)
#                         coords = poly.tolist() if hasattr(poly, "tolist") else poly
#                         flat_text_results.append((coords, (text, score)))
#                         original_results.append((coords, text, score))

#                         if score < 0.5:
#                             low_confidence_texts.append((coords, text, score))
#                 else:
#                     print("text_results error")
#                     flat_text_results = []
#                     extracted_texts.append("empty")

#                 height, width = roi_image.shape[:2]
#                 margin = 5
#                 # 신뢰도 낮은 텍스트 처리
                
#                 extracted_texts = [text for coords, text, conf in original_results]
#                 extracted_texts = ' '.join(extracted_texts)
#                 # extracted_texts = self.handle_special_cases(extracted_texts)
#                 if extracted_texts:
#                     ocr_results[roi_key] = extracted_texts
#             else:
#                 print(f"{roi_key}가 self.rois에 존재하지 않습니다.")

#         for roi_key, text in ocr_results.items():
#             print(f'{roi_key}: {text}')

#         # 유효한 텍스트만 리스트로 반환
#         ocr_results_list = [text for text in ocr_results.values() if text]
#         return ocr_results_list