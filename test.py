import cv2
img = cv2.imread("cat.png")
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

ret, thresh = cv2.threshold(img_gray, 127, 255, cv2.THRESH_BINARY)
contours, hierarchy = cv2.findContours(
    thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

color = (255, 255, 0)

for contour in contours:

    # 境界の描画 ( img データに contours データをマージ )
    cv2.drawContours(img, contours, -1, color, 2)

cv2.imshow('conturing', img)

cv2.waitKey(0)
cv2.destroyAllWindows()
