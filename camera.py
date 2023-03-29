from pyzbar import pyzbar
import numpy as np
import cv2
from PIL import Image
from pylibdmtx.pylibdmtx import decode
import zxing
from kraken import binarization
from sheets import check, get_data
def get_camera():
    video_cap = cv2.VideoCapture(0)

    cv2.namedWindow("frame")
    data = get_data()

    while True:
        success, frame = video_cap.read()
        frame = cv2.resize(frame, (320,240))
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        barcodes = decode(frame)
        item = dict()
        for barcode in barcodes:
            split = barcode.data.split(b'\x1d')
            print(barcode.data)
            for i in split:
                if i[:2] == b'1P':
                    item['MFGPN'] = i[2:].decode('utf-8')
                if i[:1] == b'Q':
                    item['QUANTITY'] = i[1:].decode('utf-8')
                if i[:3] == b'11K':
                    item['ORDER'] = i[3:].decode('utf-8')
                    item['FROM'] = "Mouser"
                if i[:2] == b'3P':
                    item['ORDER'] = i[2:].decode('utf-8')
                    item['FROM'] = "Farnell"
        if item:
            for v in data.values():
                if v['MFGPN'] == item['MFGPN']:
                    for order in v['ORDERS']:
                        if order[0] == item['FROM'] and order[1] == int(item['ORDER']):
                            break
                    else:
                        video_cap.release()
                        cv2.destroyAllWindows()
                        return item
                else:
                    video_cap.release()
                    cv2.destroyAllWindows()
                    return item
        cv2.imshow("frame", frame)
        if cv2.waitKey(1) == ord('q'):
            video_cap.release()
            cv2.destroyAllWindows()
            return None

    