import cv2
import pickle
from math import sqrt

width, height = 40, 23
pt1_x, pt1_y, pt2_x, pt2_y = None, None, None, None
line_count = 0

try:
    with open('park_positions', 'rb') as f:
        park_positions = pickle.load(f)
except:
    park_positions = []


def parking_line_counter():
    global line_count
    line_count = int((sqrt((pt2_x - pt1_x) ** 2 + (pt2_y - pt1_y) ** 2)) / height)
    return line_count


def mouse_events(event, x, y, flag, param):
    global pt1_x, pt1_y, pt2_x, pt2_y

    if event == cv2.EVENT_LBUTTONDOWN:
        pt1_x, pt1_y = x, y

    elif event == cv2.EVENT_LBUTTONUP:
        pt2_x, pt2_y = x, y
        parking_spaces = parking_line_counter()
        if parking_spaces == 0:
            park_positions.append((x, y))
        else:
            for i in range(parking_spaces):
                park_positions.append((pt1_x, pt1_y + i * height))

    if event == cv2.EVENT_RBUTTONDOWN:
        for i, position in enumerate(park_positions):
            x1, y1 = position
            if x1 < x < x1 + width and y1 < y < y1 + height:
                park_positions.pop(i)

    with open('park_positions', 'wb') as f:
        pickle.dump(park_positions, f)


while True:

    img = cv2.imread('input/parking.png')

    for position in park_positions:
        cv2.rectangle(img, position, (position[0] + width, position[1] + height), (255, 0, 255), 3)

    cv2.namedWindow('image', cv2.WINDOW_NORMAL)
    cv2.setWindowProperty('image', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    cv2.imshow('image', img)
    cv2.setMouseCallback('image', mouse_events)

    key = cv2.waitKey(30)
    if key == 27:
        break

cv2.destroyAllWindows()
