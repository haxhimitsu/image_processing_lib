'''
 tutorial_008.py
 ウィンドウ上のマウス入力を処理する
'''
import cv2
import numpy as np

img = np.zeros((480, 640, 3), np.uint8)  # y座標, x座標, チャンネル

def onMouse(event, x, y, flags, param):
    event_description = ""

    if event == cv2.EVENT_MOUSEMOVE:
        event_description += "MOUSE_MOVE"
    elif event == cv2.EVENT_LBUTTONDOWN:
        event_description += "LBUTTON_DOWN"
        print("centerX: " + str(param["centerX"]) +
              ", centerY: " + str(param["centerY"]))
        param["centerX"] = -1
        param["centerY"] = -1
    elif event == cv2.EVENT_RBUTTONDOWN:
        event_description += "LBUTTON_DOWN"
    elif event == cv2.EVENT_MBUTTONDOWN:
        event_description += "MBUTTON_DOWN"
    elif event == cv2.EVENT_LBUTTONUP:
        event_description += "LBUTTON_UP"
    elif event == cv2.EVENT_RBUTTONUP:
        event_description += "RBUTTON_UP"
    elif event == cv2.EVENT_MBUTTONUP:
        event_description += "MBUTTON_UP"
    elif event == cv2.EVENT_LBUTTONDBLCLK:
        event_description += "LBUTTON_DBLCLK"
        cv2.circle(img, (x, y), 100, (0, 0, 255), 3)
    elif event == cv2.EVENT_RBUTTONDBLCLK:
        event_description += "RBUTTON_DBLCLK"
    elif event == cv2.EVENT_MBUTTONDBLCLK:
        event_description += "MBUTTON_DBLCLK"
    else:
        event_description += ""

    if flags & cv2.EVENT_FLAG_LBUTTON:
        event_description += " + LBUTTON"

    if flags & cv2.EVENT_FLAG_RBUTTON:
        event_description += " + RBUTTON"

    if flags & cv2.EVENT_FLAG_MBUTTON:
        event_description += " + MBUTTON"

    if flags & cv2.EVENT_FLAG_CTRLKEY:
        event_description += " + CTRL"

    if flags & cv2.EVENT_FLAG_SHIFTKEY:
        event_description += " + SHIFT"

    if flags & cv2.EVENT_FLAG_ALTKEY:
        event_description += " + ALT"

    print(event_description)


def tutorial_008():

    # 画面全体を青色にする
    img[:, :] = [255, 0, 0]
    cv2.namedWindow("img", cv2.WINDOW_AUTOSIZE)
    cv2.moveWindow("img", 100, 100)

    param = {"centerX": 10, "centerY": 20, "color": 0}

    cv2.setMouseCallback('img', onMouse, param)

    while(True):
        cv2.imshow('img', img)
        key = cv2.waitKey(20) & 0xFF
        if key == 0x1b or key == ord("q"):
            break
        elif key == ord("1"):
            param["centerX"] = 100
            param["centerY"] = 200
        elif key == ord("0"):
            param["centerX"] = 10
            param["centerY"] = 20
        elif key == ord("p"):
            print("centerX: " + str(param["centerX"]) +
                  ", centerY: " + str(param["centerY"]))
        else:
            pass

    cv2.destroyAllWindows()


if __name__ == "__main__":
    tutorial_008()
