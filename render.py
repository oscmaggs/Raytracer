from vector import Vector
from sphere import Sphere
from rays import Ray


WIDTH, HEIGHT = 400, 200
ASPECT = WIDTH / HEIGHT
BACKGROUND = (0.05, 0.05, 0.12)

camera = Vector(0, 0, 0)

spheres = [
    Sphere(centre=Vector(-1.2,  0.0, -5), radius=1.0, colour=(0.9, 0.2, 0.2), id="red"),
    Sphere(centre=Vector( 1.2,  0.3, -7), radius=1.5, colour=(0.2, 0.5, 0.9), id="blue"),
    Sphere(centre=Vector( 0.0, -101, -6), radius=100, colour=(0.3, 0.8, 0.3), id="ground"),
]

with open("scene1.ppm", "w") as f:
    f.write(f"P3\n{WIDTH} {HEIGHT}\n255\n")

    for j in range(HEIGHT):
        for i in range(WIDTH):
            x = (2 * (i + 0.5) / WIDTH - 1) * ASPECT
            y = 1 - 2 * (j + 0.5) / HEIGHT

            rays = Ray(origin=camera, D=Vector(x, y, -1))
            hit = rays.nearestSphereIntersect(spheres)

            colour = hit.object.colour if hit else BACKGROUND
            f.write(" ".join(str(int(255.999 * c)) for c in colour) + "\n")

print("wrote scene.ppm")