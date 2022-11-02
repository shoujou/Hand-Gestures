from http.client import ImproperConnectionState
import cv2
import datetime
import os

path = './data'
NUMBER = 100


def make_mask(frame):
    im_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    th, output = cv2.threshold(
        im_gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    # print(th)  # 87.0

    # 白黒反転
    output = 255 - output
    cv2.imshow("otsu", output)

    return output


def save_frame_camera_key(device_num, dir_path, basename,  ext='jpg', delay=1, window_name='frame'):
    # 認識範囲
    xmin, xmax = 240, 440
    ymin, ymax = 120, 360
    cap = cv2.VideoCapture(device_num)
    save_mode = False

    if not cap.isOpened():
        return

    ori_path = os.path.join(dir_path, 'original')
    mask_path = os.path.join(dir_path, 'mask')
    os.makedirs(ori_path, exist_ok=True)
    os.makedirs(mask_path, exist_ok=True)

    print(cap.set(cv2.CAP_PROP_FPS, 3))

    n = 0
    while True:
        ret, frame = cap.read()
        frame = cv2.flip(frame, 1)
        cv2.rectangle(frame, (xmin, ymin), (xmax, ymax),
                      (0, 0, 255), 2)  # 指定範囲に赤枠6
        cv2.imshow(window_name, frame)
        dataframe = frame[ymin:ymax, xmin:xmax]  # 背
        mask_img = make_mask(dataframe)
        key = cv2.waitKey(delay) & 0xFF
        if key == ord('c'):
            save_mode = True
        elif key == ord('q'):
            break
        if save_mode == True:
            cv2.imwrite('{}/{}_{}.{}'.format(ori_path,
                        basename, n, ext), dataframe)
            cv2.imwrite('{}/{}_{}.{}'.format(mask_path,
                        basename, n, ext), mask_img)
            n += 1
            if n == NUMBER:
                break

    cv2.destroyWindow(window_name)


if __name__ == "__main__":
    gesture = input("ジェスチャー：")

    path = os.path.join(path, gesture)
    now = datetime.datetime.now()

    save_frame_camera_key(0, path, now.strftime('%Y%m%d_%H%M'))
