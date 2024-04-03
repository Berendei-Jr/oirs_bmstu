import numpy as np 
import cv2 

YELLOW_COLOR = (0, 250, 240)
BLUE_COLOR = (255, 0, 0)
RED_COLOR = (0, 0, 255)
COLORS = [RED_COLOR, BLUE_COLOR, YELLOW_COLOR]


class ImageGenerator:

    def __init__(self, image):
        self.image = image
        self.shape = image.shape
        self.distance = 80
        self.centers = []

    def _point_is_correct(self, point):
        return point[0] < self.shape[1] and point[1] < self.shape[0] and point[0] > 0 and point[1] > 0

    def _generate_random_point(self):
        point = self._generate_random_coordinate()
        point_approved = False
        while not point_approved:
            for center in self.centers:
                if np.linalg.norm(np.array(point) - np.array(center)) < 2.5*self.distance:
                    point = self._generate_random_coordinate()
                    break
            else:
                point_approved = True
        self.centers.append(point)
        return point

    def _generate_random_coordinate(self):
        return (np.random.randint(self.distance*1.5, self.shape[1] - self.distance*1.5), np.random.randint(self.distance*1.5, self.shape[0] - self.distance*1.5))

    def _mirror_point(self, point, y_value):
        return (point[0], y_value + (y_value - point[1]))

    def add_pentagons(self, count, color, thickness):
        for i in range(count):
            center_point = self._generate_random_point()
            upper_point = [center_point[0], int(center_point[1] - self.distance/2)]
            points = []
            angle = 2*np.pi/5
            for i in range(1, 6):
                x = int(upper_point[0] + self.distance*np.sin(i*angle))
                y = int(upper_point[1] + self.distance*np.cos(i*angle))
                points.append([x, y])
            cv2.polylines(self.image, [np.array(points)], color=color, isClosed=True, thickness=thickness)

    def add_triangles(self, count, color, thickness):
        for i in range(count):
            center_point = self._generate_random_point()
            upper_point = [center_point[0], int(center_point[1] - self.distance/2)]
            right_point = [int(center_point[0] + self.distance/2), int(center_point[1] + self.distance*np.sqrt(3)/2)]
            left_point = [int(center_point[0] - self.distance/2), int(center_point[1] + self.distance*np.sqrt(3)/2)]
            cv2.polylines(self.image, [np.array([upper_point, right_point, left_point])], color=color, isClosed=True, thickness=thickness)

    def add_squares(self, count, color, thickness):
        for i in range(count):
            initial_point = self._generate_random_point()
            second_point = (-1, -1)
            while not self._point_is_correct(second_point):
                side_length = np.random.randint(0.1*self.distance, self.distance)
                second_point = (initial_point[0] + side_length, initial_point[1] + side_length)
            cv2.rectangle(self.image, initial_point, second_point, color=color, thickness=thickness)

    def add_circles(self, count, color, thickness):
        for i in range(count):
            center = self._generate_random_point()
            cv2.circle(self.image, center, np.random.randint(0.1*self.distance, self.distance), color=color, thickness=thickness)


    def show_image(self):
        cv2.imshow('image', self.image) 
        cv2.waitKey(0) 

    def save_image(self, path):
        cv2.imwrite(path, self.image)

    def __del__(self):
        cv2.destroyAllWindows()



if __name__ == '__main__':
    img = np.zeros((1080, 1920, 3), dtype=np.uint8)

    ig = ImageGenerator(img)

    for color in COLORS:
        ig.add_squares(2, color, 3)
        ig.add_triangles(2, color, 3)
        ig.add_circles(2, color, 3)
        ig.add_pentagons(2, color, 3)

    ig.save_image('generated_image.png')
