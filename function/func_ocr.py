import cv2
from paddleocr import PaddleOCR
import os

from config.config_demo_roi import Configs

class PaddleOCRManager:

    def __init__(self, n=3):
        self.n = n
        self.config = Configs(n=self.n)
        self.rois = self.config.roi_params()
        self.phasor_condition = 0
    
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

