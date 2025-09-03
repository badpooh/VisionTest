import cv2
import numpy as np
import pyautogui
import time

def opencv_find_and_click(template_path, coordinates):
    
    # 1) 화면 전체 스크린샷
    screenshot = pyautogui.screenshot()
    screenshot = np.array(screenshot)  # Pillow → np array (RGB)
    screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)  # BGR로 변환

    # cv2.imshow("test", screenshot)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    # 2) 템플릿 이미지 로드
    template = cv2.imread(template_path, cv2.IMREAD_COLOR)
    h, w, _ = template.shape

    # 3) 매칭
    result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    threshold = 0.8
    if max_val >= threshold:
        w_1, h_1 = coordinates

        top_left = max_loc
        center_x = top_left[0] + w_1*w
        center_y = top_left[1] + h_1*h

        ### 181, 12

        # 4) 마우스 클릭
        pyautogui.moveTo(center_x, center_y, duration=0.5)
        time.sleep(1)
        box_width, box_height = w, h
        screenshot_region = pyautogui.screenshot(region=(top_left[0], top_left[1], box_width, box_height))
        screenshot_region.save("check_b4_click.png")
        pyautogui.click()

        # 5) 부분 스크린샷
        # time.sleep(1)
        # box_width, box_height = w, h
        # screenshot_region = pyautogui.screenshot(region=(top_left[0], top_left[1], box_width, box_height))
        

        print("템플릿 매칭 성공, 클릭 완료!")
    else:
        print("템플릿 매칭 실패 (score=%.3f)" % max_val)

if __name__ == "__main__":
    template_path = r"C:\PNT\AutoProgram\Vision\image_test\wiring_wye.png"
    coordinates = [0.75, 0.5]
    opencv_find_and_click(template_path, coordinates)
    time.sleep(1)
    template_path = r"C:\PNT\AutoProgram\Vision\image_test\wye_delta.png"
    coordinates = [0.5, 0.75]
    opencv_find_and_click(template_path, coordinates)
    template_path = r"C:\PNT\AutoProgram\Vision\image_test\meas_apply_refresh.png"
    coordinates = [0.33, 0.5]
    opencv_find_and_click(template_path, coordinates)
    template_path = r"C:\PNT\AutoProgram\Vision\image_test\warning_confirm_cancel.png"
    coordinates = [0.7, 0.83]
    opencv_find_and_click(template_path, coordinates)
    template_path = r"C:\PNT\AutoProgram\Vision\image_test\apply_yes_no_cancel.png"
    coordinates = [0.15, 0.5]
    opencv_find_and_click(template_path, coordinates)
