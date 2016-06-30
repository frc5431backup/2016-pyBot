import cv2
import numpy as np

if __name__ == "__main__":
    sample_U = cv2.imread("/home/smerkous/Desktop/UUU.jpg")

    find_U = cv2.imread("/home/smerkous/Desktop/one.png")

    ratio = find_U.shape[0] / 300

    orig = find_U.copy()

    #find_U = cv2.resize(find_U, (ratio, 300), interpolation=cv2.INTER_CUBIC)


    imgray3 = cv2.cvtColor(sample_U, cv2.COLOR_BGR2GRAY)

    ret3, thresh3 = cv2.threshold(imgray3, 240, 255, cv2.THRESH_BINARY)

    contours3 = cv2.findContours(thresh3, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    edged3 = cv2.drawContours(sample_U, contours3[1], -1, (255, 0, 255, 30), 2)

    '''
    Part two
    '''

    imgray2 = cv2.cvtColor(find_U, cv2.COLOR_BGR2GRAY)

    ret2, thresh2 = cv2.threshold(imgray2, 100, 255, cv2.THRESH_BINARY)

    contours2 = cv2.findContours(thresh2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    cnts = sorted(contours2[1], key=cv2.contourArea, reverse=True)

    U_con = None

    for cnt in cnts:
        peri = cv2.arcLength(cnt, True)
        hull = cv2.convexHull(cnt, returnPoints=True)
        approx = cv2.approxPolyDP(hull, 0.02 * peri, True)

        if 3 <= len(approx) <= 8:
            U_con = approx
            break

    edged2 = cv2.drawContours(find_U, [U_con], -1, (255, 255, 0, 30), 2)

    pts = U_con.reshape(4, 2)
    rect = np.zeros((4, 2), dtype="float32")

    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]

    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]

    rect *= 1

    (tl, tr, br, bl) = rect
    widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))

    # ...and now for the height of our new image
    heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))

    # take the maximum of the width and height values to reach
    # our final dimensions
    maxWidth = max(int(widthA), int(widthB))
    maxHeight = max(int(heightA), int(heightB))

    # construct our destination points which will be used to
    # map the screen to a top-down, "birds eye" view
    dst = np.array([
        [0, 0],
        [maxWidth - 1, 0],
        [maxWidth - 1, maxHeight - 1],
        [0, maxHeight - 1]], dtype="float32")

    # calculate the perspective transform matrix and warp
    # the perspective to grab the screen
    M = cv2.getPerspectiveTransform(rect, dst)
    warp = cv2.warpPerspective(orig, M, (maxWidth, maxHeight))
    #warp = cv2.cvtColor(warp, cv2.COLOR_BGR2GRAY)
    warp = cv2.GaussianBlur(warp, (5, 5), 0)

    bop = int(0.05 * warp.shape[0])
    light = int(0.05 * warp.shape[1])

    warp = cv2.copyMakeBorder(warp, bop, bop, light, light, cv2.BORDER_CONSTANT, (255, 255, 0))
    edged = cv2.Canny(warp, 230, 500)
    contours = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    conts = sorted(contours[1], key=cv2.contourArea, reverse=True)
    warp = cv2.drawContours(warp, conts, -1, (255, 255, 0, 30), 2)
    for cnt in conts:
        peri = cv2.arcLength(cnt, True)
        #appr = cv2.approxPolyDP(cnt, 0.02 * peri, True)
        #appr2 = cv2.approxPolyDP(contours3[1][0], 0.02 * cv2.arcLength(contours3[1][0], True), True)
        #warp = cv2.drawContours(warp, cnt, -1, (0, 255, 0, 30), 2)
        match_num = cv2.matchShapes(cnt, contours3[0], 2, 1)
        print("MATCH: %s" % str(match_num))
    cv2.imshow("source", edged3)
    cv2.imshow("source2", edged2)
    cv2.imshow("warp", warp)
    cv2.imwrite("/home/smerkous/Desktop/UUU.jpg", warp)
    cv2.waitKey(0)
    cv2.destroyAllWindows()