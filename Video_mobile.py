import requests
import numpy as np
import cv2
import time
import pytesseract as ps
from PIL import Image
import io
import threading


class NewThread:
    def __init__(self, function):
        self.function = function

    def run(self):
        thread = threading.Thread(target=self.function)
        thread.daemon = True
        thread.start()


class VideoExtraction:
    ps.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\tesseract.exe'

    def __init__(self, url, image=0):
        self.url = url
        self.image = image

    def get_data_from_server(self):
        while True:
            try:
                img = requests.get(self.url)
                self.image = np.array(bytearray(img.content), dtype=np.uint8)
            except requests.exceptions.ConnectionError:
                print("Connection error")

    def extract_text_from_image(self):
        while True:
            if self.image is not None:
                if not isinstance(self.image, int):
                    img = Image.open(io.BytesIO(self.image))
                    text = ps.image_to_string(img)
                    if text != "":
                        print(text)
            else:
                break
            time.sleep(0.25)

    @staticmethod
    def create_thread(function):
        thread = NewThread(function)
        thread.run()

    def show_video(self):
        self.create_thread(self.get_data_from_server)
        self.create_thread(self.extract_text_from_image)
        time.sleep(3)
        while True:
            if self.image is not None:
                img = cv2.imdecode(self.image, - 1)
                img_resize = cv2.resize(img, (800, 600))
                cv2.imshow("AndroidCam", img_resize)

                if cv2.waitKey(1) == 27:
                    break
            else:
                break


if __name__ == "__main__":
    appl = VideoExtraction("http://192.168.0.100:8080/shot.jpg")
    appl.show_video()
