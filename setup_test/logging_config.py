import logging

def setup_logging(log_filename='app_log.txt', log_level=logging.INFO):
    # 로거 생성
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)  # 기본 로그 수준 설정

    # 파일 핸들러 추가 (파일에 로그 기록)
    file_handler = logging.FileHandler(log_filename)
    file_handler.setLevel(log_level)  # 파일에 기록할 로그 수준 설정
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # 콘솔 핸들러 추가 (콘솔에 로그 출력)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)  # 콘솔에 출력할 로그 수준 설정
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger
