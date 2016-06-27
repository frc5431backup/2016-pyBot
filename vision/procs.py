from cv2 import __version__, imread, threshold, \
    findContours, moments, contourArea, arcLength, \
    imshow, waitKey, destroyAllWindows, approxPolyDP, \
    isContourConvex, boundingRect, rectangle, cvtColor, \
    COLOR_BAYER_RG2BGR, drawContours
import numpy as np


class Vision:
    is_test = True

    def __init__(self):
        if str(__version__) != "3.1.0":
            print("OpenCV is not the correct version!")
        self.computer_img = "/home/smerkous/Desktop/U.jpg"
        self.robot_img_url = "http://axis-camera/mjpegstream"
        self.image_width = 640
        self.image_height = 480

        self.min_thresh = 5
        self.max_thresh = 255

        self.source_img = None
        self.grayed = None
        self.threshed = None
        self.contours = None
        self.contour_amount = 0

    def simple_load(self):
        self.source_img = imread(self.computer_img if self.is_test else self.robot_img_url, 0)
        print(self.source_img.shape)
        #self.grayed = cvtColor(self.source_img, COLOR_BAYER_RG2BGR)
        self.threshed = threshold(self.source_img, self.min_thresh, self.max_thresh, 0)
        self.contours = findContours(self.threshed[1], 1, 2)
        self.contour_amount = len(self.contours[1])
        self.source_img = drawContours(self.source_img, self.contours[1], -1, (255, 255, 255, 30), 2)

    def set_source(self, path):
        self.computer_img = path

    def set_url_source(self, url):
        self.robot_img_url = url

    def details(self):
        moment_list = []
        area_list = []
        perim_list = []
        approx_poly = []
        convexity = []
        for ind in range(0, self.contour_amount):
            try:
                cnt = self.contours[1][ind]
                m = moments(cnt)
                centered = (int(m['m10']/m['m00']), int(m['m01']/m['m00']))
                moment_list.append(centered)
                area_list.append(contourArea(cnt))
                perim_list.append(arcLength(cnt, True))
                approx_poly.append(approxPolyDP(cnt, 0.01 * perim_list[ind], True))
                convexity.append(isContourConvex(cnt))
            except:
                pass

        return moment_list, area_list, perim_list, approx_poly, convexity

    def get_res(self):
        self.simple_load()
        mom, area, perim, app, conv = self.details()

        for ind in range(0, len(mom)):
            try:
                cnt = self.contours[1][ind]
                x, y, w, h = boundingRect(cnt)
                self.source_img = rectangle(self.source_img, (x, y), (x+w, y+h), (0, 255, 0), 2)
            except:
                pass
        return self.source_img

    @staticmethod
    def display_output(img):
        imshow("OUTPUT", img)
        waitKey(0)
        destroyAllWindows()


if __name__ == "__main__":  # Check loaded file is ran
    if Vision.is_test:  # Double check if it's the computer
        print("Running on computer...\nVersion: %s" % __version__)
        vision = Vision()
        out = vision.get_res()
        vision.display_output(out)
