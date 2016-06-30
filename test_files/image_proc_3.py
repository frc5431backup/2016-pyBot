import mahotas
from skimage import exposure
import imutils
import cv2
import numpy as np


class cv2_ext:
    @staticmethod
    def resize(image, ratio):
        r = ratio / image.shape[1]
        dim = (ratio, int(image.shape[0] * r))
        return cv2.resize(image, dim, interpolation=cv2.INTER_AREA)


class Main:
    def __init__(self):
        self.source = "/home/smerkous/Desktop/294.jpg"
        self.compare = "/home/smerkous/Desktop/sample.jpg"
        self.image = cv2.imread(self.source)
        self.sample = cv2.imread(self.compare)

        self.n = 300
        self.ratio = self.image.shape[0] / self.n
        self.orig = self.image.copy()
        self.image = imutils.resize(self.image, height=self.n)

        self.pass_sides = 4
        self.match_thresh = 5.0

        self.s_gray = cv2.cvtColor(self.sample, cv2.COLOR_BGR2GRAY)
        self.s_canny = cv2.Canny(self.s_gray, 300, 500)
        _, self.s_cnt, _ = cv2.findContours(self.s_canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        self.sample = cv2.drawContours(self.sample, self.s_cnt, -1, (255, 255, 255, 255), 3)

    @staticmethod
    def filter(image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.bilateralFilter(gray, 11, 17, 17)
        return cv2.Canny(gray, 30, 200)

    @staticmethod
    def find_contours(image, tree=False):
        _, cnts, _ = cv2.findContours(image, cv2.RETR_EXTERNAL if not tree else cv2.RETR_TREE,
                                      cv2.CHAIN_APPROX_SIMPLE)
        return sorted(cnts, key=cv2.contourArea, reverse=True)

    @staticmethod
    def wait_destroy():
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def sides_check(self, approx_sides):
        return approx_sides == self.pass_sides

    def warp_rect(self, u_cont):
        pts = u_cont.reshape(4, 2)
        rect = np.zeros((4, 2), dtype="float32")

        s = pts.sum(axis=1)
        rect[0] = pts[np.argmin(s)]
        rect[2] = pts[np.argmax(s)]

        diff = np.diff(pts, axis=1)
        rect[1] = pts[np.argmin(diff)]
        rect[3] = pts[np.argmax(diff)]

        rect *= self.ratio

        (tl, tr, br, bl) = rect
        width_a = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
        width_b = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
        height_a = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
        height_b = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
        max_w = max(int(width_a), int(width_b))
        max_h = max(int(height_a), int(height_b))

        dst = np.array([
            [0, 0], [max_w - 1, 0], [max_w - 1, max_h - 1], [0, max_h - 1]],
            dtype="float32")

        m = cv2.getPerspectiveTransform(rect, dst)
        warp = cv2.warpPerspective(self.orig, m, (max_w, max_h))
        warp = exposure.rescale_intensity(warp, out_range=(0, 255))
        bop = 15
        light = 15
        return cv2.copyMakeBorder(warp, bop, bop, light, light, cv2.BORDER_CONSTANT, (255, 255, 0))

    def start(self):
        edged = self.filter(self.image)
        cnts = self.find_contours(edged.copy())

        passed = []

        conts = cv2.drawContours(self.image.copy(), cnts, -1, (255, 255, 0, 255), 2)

        for ind, cnt in enumerate(cnts):
            hull = cv2.convexHull(cnt, returnPoints=True)
            perim = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(hull, 21, True)  # * perim, True)
            sides = len(approx)
            formats = [hull, perim, approx, sides]
            if self.sides_check(sides):
                print("%d passed with %d sides" % (ind, sides))
                conts = cv2.drawContours(conts, [approx], -1, (0, 0, 255, 255), 4)
                passed.append([ind, formats])

        u_passed_list = []

        for con in passed:
            ind = con[0]
            warp = self.warp_rect(con[1][2])
            blur = cv2.medianBlur(warp, 3)
            canny = cv2.Canny(blur, 300, 500)
            cv2.imshow("can " + str(ind), canny)
            contour = self.find_contours(canny, True)[0]  # Get largest contour
            match = cv2.matchShapes(self.s_cnt[0], contour, 3, 1)
            u_passed_list.append([ind, match])
            warp = cv2.drawContours(warp, [contour], -1, (0, 0, 255, 255), 4)
            warp = cv2.putText(warp, str(ind), (45, 45), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 1, (255, 255, 255, 255), 3, 8)
            cv2.imshow("warp " + str(ind), warp)

        low_high = sorted(u_passed_list, key=lambda x: x[1])
        lowest = low_high[0][0]

        print("Selecting contour %d" % lowest)
        hull = cv2.convexHull(cnts[lowest], returnPoints=True)
        m = cv2.moments(hull)
        centered = (int(m['m10'] / m['m00']), int(m['m01'] / m['m00']))
        print("Selected object center %d : %d" % centered)
        conts = cv2.putText(conts, str("Target"), (centered[0] - 40, centered[1] - 30), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX,
                            1, (255, 255, 255, 255), 1, 8)
        conts = cv2.putText(conts, str("%d : %d" % centered),
                            (centered[0] - 50, centered[1] + 60), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 1,
                            (255, 255, 255, 255), 1, 8)
        cv2.imshow("source", self.image)
        cv2.imshow("edged", edged)
        cv2.imshow("contours", conts)
        self.wait_destroy()


class ZernikeMoments:
    def __init__(self, radius):
        self.radius = radius

    def describe(self, image):
        return mahotas.features.zernike_moments(image, self.radius)


if __name__ == "__main__":
    main = Main()
    main.start()
