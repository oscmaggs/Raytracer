class Intersection:
    def __init__(self, intersects=False, distance=None, point=None, normal=None, object=None):
        self.intersects = intersects
        self.distance = distance
        self.point = point
        self.normal = normal
        self.object = object

    @staticmethod
    def nearestIntersection(intersections):
        hits = [i for i in intersections if i.intersects]
        if not hits:
            return None
        return min(hits, key=lambda i: i.distance)