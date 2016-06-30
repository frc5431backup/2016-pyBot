import cv2
import numpy as np

'''
When calibrated change these values
'''

greenish = [[97, 110, 0], [171, 177, 97]]
canny = [145, 255]
med_blur = 7

# [0, 1, 2], [0, 1, 2] BGR to Upper BGR

cv2.namedWindow("image_calibration")
cv2.namedWindow("source_image")
cv2.namedWindow("output")
load = False


def details(contours, length):
    moment_list = []
    area_list = []
    perim_list = []
    approx_poly = []
    convexity = []
    hulls = []
    defects = []
    for ind in range(0, length):
        try:
            cnt = contours[1][ind]
            area_list.append(cv2.contourArea(cnt))
            perim_list.append(cv2.arcLength(cnt, True))
            approx_poly.append(cv2.approxPolyDP(cnt, 0.01 * perim_list[ind], True))
            convexity.append(cv2.isContourConvex(cnt))
            hulls.append(cv2.convexHull(cnt, returnPoints=True))
            defects.append(cv2.convexityDefects(cnt, cv2.convexHull(cnt, returnPoints=False)))
            m = cv2.moments(hulls[ind])
            centered = (int(m['m10'] / m['m00']), int(m['m01'] / m['m00']))
            moment_list.append(centered)
        except:
            pass
    return moment_list, area_list, perim_list, approx_poly, convexity, hulls, defects


'''
Calc values
'''

min_sides = 3
max_sides = 11

min_defects = 1
max_defects = 20

screen_half = 170
center_target = 0


def pass_poly(approx):
    return 2 < len(approx) < 6


def pass_pos(x, y):
    return (x != 0) and (y != 0)


def pass_size():
    pass


def target(large, center, top):
    print("TARGETS: %d : %d : %d" % (large, center, top))
    if large == center == top:
        return large
    elif large == center != top:
        return center
    elif large != center == top:
        return top
    elif large != center != top:
        return large
    else:
        return large


def get_res(contours, source_img):
    mom, area, perim, app, conv, hulls, defs = details(contours, len(contours))

    largest_num = 0
    largest_ind = 0

    center_num = 900
    center_ind = 0

    toppest_num = 900
    toppest_ind = 0

    for ind in range(0, len(mom)):
        try:
            sides = len(app[ind])
            print("Sides... %d" % sides)

            if min_sides <= sides <= max_sides:  # Faster than (and <=)
                print("Sides pass %d" % ind)

                defects = len(defs[ind])
                print("Defects... %d" % defects)

                if min_defects <= defects <= max_defects:
                    print("Defects passed %d" % ind)

                    areas = area[ind]
                    print("Area %d" % areas)
                    if areas > largest_num:
                        print("Largest area %d" % int(areas))
                        largest_num = areas
                        largest_ind = ind

                    from_center = mom[ind][0] - screen_half
                    centerosity = int(abs(from_center))
                    print("center distance... %d" % centerosity)

                    if centerosity < center_num:
                        print("Closest center %d" % ind)
                        center_num = centerosity
                        center_ind = ind

                    if mom[ind][1] < toppest_num:
                        print("Closest top %d" % ind)
                        toppest_num = mom[ind][1]
                        toppest_ind = ind
        except Exception as err:
            print("ERROR: %s" % err)

    targ = target(largest_ind, center_ind, toppest_ind)
    print("Selected target: %d" % targ)

    cnt = contours[1][targ]
    x, y, w, h = cv2.boundingRect(cnt)
    source_img = cv2.rectangle(source_img, (x, y), (x + w, y + h), (255, 255, 255), 2)
    source_img = cv2.circle(source_img, (mom[targ][0], mom[targ][1]), 10, (255, 255, 255), -1)
    for i in range(defs[targ].shape[0]):
        s, e, f, d = defs[targ][i, 0]
        start = tuple(cnt[s][0])
        end = tuple(cnt[e][0])
        far = tuple(cnt[f][0])
        cv2.line(source_img, start, end, [255, 255, 255], 2)
        cv2.circle(source_img, far, 5, [255, 255, 255], -1)

    return source_img


def render(x):
    global greenish, canny, med_blur

    if load:
        greenish[0][0] = cv2.getTrackbarPos("L0", "image_calibration")
        greenish[0][1] = cv2.getTrackbarPos("L1", "image_calibration")
        greenish[0][2] = cv2.getTrackbarPos("L2", "image_calibration")
        greenish[1][0] = cv2.getTrackbarPos("U0", "image_calibration")
        greenish[1][1] = cv2.getTrackbarPos("U1", "image_calibration")
        greenish[1][2] = cv2.getTrackbarPos("U2", "image_calibration")
        canny[0] = cv2.getTrackbarPos("CANL", "image_calibration")
        canny[1] = cv2.getTrackbarPos("CANU", "image_calibration")
        med_blur = cv2.getTrackbarPos("blur", "image_calibration")

    image = cv2.imread("/home/smerkous/Desktop/U.jpg")
    orig = image.copy()
    lower = np.array(greenish[0], dtype="uint8")
    upper = np.array(greenish[1], dtype="uint8")
    mask = cv2.inRange(image, lower, upper)
    image = cv2.bitwise_and(image, image, mask=mask)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # gray = cv2.bilateralFilter(gray, 11, 17, 17)
    kernel = np.ones((2, 2), np.uint8)
    gray = cv2.erode(gray, kernel, iterations=1)
    gray = cv2.medianBlur(gray, med_blur)
    edged = cv2.Canny(gray, canny[0], canny[1])
    contours = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    edged = cv2.drawContours(edged, contours[1], -1, (255, 255, 255, 30), 2)
    get_res(contours, gray)
    cv2.imshow("image_calibration", orig)
    cv2.imshow("source_image", image)
    cv2.imshow("output", np.hstack([gray, edged]))
    print("change %s" % str(x))


cv2.createTrackbar("L0", "image_calibration", 0, 255, render)
cv2.createTrackbar("L1", "image_calibration", 0, 255, render)
cv2.createTrackbar("L2", "image_calibration", 0, 255, render)
cv2.createTrackbar("U0", "image_calibration", 0, 255, render)
cv2.createTrackbar("U1", "image_calibration", 0, 255, render)
cv2.createTrackbar("U2", "image_calibration", 0, 255, render)
cv2.createTrackbar("blur", "image_calibration", 0, 60, render)
cv2.createTrackbar("CANL", "image_calibration", 0, 500, render)
cv2.createTrackbar("CANU", "image_calibration", 0, 500, render)

cv2.setTrackbarPos("L0", "image_calibration", greenish[0][0])
cv2.setTrackbarPos("L1", "image_calibration", greenish[0][1])
cv2.setTrackbarPos("L2", "image_calibration", greenish[0][2])
cv2.setTrackbarPos("U0", "image_calibration", greenish[1][0])
cv2.setTrackbarPos("U1", "image_calibration", greenish[1][1])
cv2.setTrackbarPos("U2", "image_calibration", greenish[1][2])
cv2.setTrackbarPos("CANL", "image_calibration", canny[0])
cv2.setTrackbarPos("CANU", "image_calibration", canny[1])
cv2.setTrackbarPos("blur", "image_calibration", med_blur)
# noinspection PyRedeclaration
load = True
cv2.waitKey(0)
cv2.destroyAllWindows()
