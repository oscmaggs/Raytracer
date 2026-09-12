class Ray:
    def __init__(self, origin, D):
        self.origin = origin
        self.D = D.normalise()  # direction in vector

    def sphereDiscriminant(self, sphere, point=0):      # set point to 1 when you want the second intersection
        O = self.origin
        D = self.D
        C = sphere.centre
        r = sphere.radius
        L = C.subtractVector(O)

        tca = L.dotProduct(D)
        if tca < 0:     # intersection is behind origin - this doesn't work when line is inside sphere
           return Intersection()

        d = None
        try:
            d = math.sqrt(L.dotProduct(L) - tca**2)
        except:
            d = 0       # crude error protection - in case D & L are too similar
        if d > r:       # line misses sphere
            return Intersection()

        thc = math.sqrt(r**2 - d**2)
        t0 = tca - thc      # distance to first intersection
        t1 = tca + thc      # distance to second intersection

        tmin = [t0, t1][point]

        phit = O.addVector(D.scaleByLength(tmin))     # point of intersection
        nhit = phit.subtractVector(C).normalise()     # normal of intersection

        return Intersection(
            intersects=True,
            distance = tmin,
            point = phit,
            normal = nhit,
            object = sphere
        )

  def nearestSphereIntersect(self, spheres, suppress_ids=[], bounces=0, max_bounces=1, through_count=0):

        intersections = []

        for i, sphere in enumerate(spheres):
            if sphere.id not in suppress_ids:
                intersections.append(self.sphereDiscriminant(sphere))

        nearestIntersection = Intersection.nearestIntersection(intersections)
        
        if nearestIntersection == None:
            return None

        if bounces > max_bounces:
            return None

        nearestIntersection.bounces = bounces
        nearestIntersection.through_count = through_count

        return nearestIntersection