import cv2
import numpy as np
import math

from core.base  import Base
from core.renderer import Renderer
from core.scene import Scene
from core.camera  import Camera
from core.mesh  import Mesh
from core.texture import Texture
from math import pi
from extras.movementRig import MovementRig
from extras.axesHelper import AxesHelper
from extras.gridHelper import GridHelper
from geometry.sphereGeometry import SphereGeometry
from material.textureMaterial import TextureMaterial

# Crear un planeta
def create_planet(name, radius, texture_path, semi_major_axis, semi_minor_axis, rotation):
    geometry = SphereGeometry(radius)
    texture = Texture(texture_path)
    material = TextureMaterial(texture)
    planet = Mesh(geometry, material)
    planet.semi_major_axis = semi_major_axis  # Semieje mayor (a)
    planet.semi_minor_axis = semi_minor_axis  # Semieje menor (b)
    planet.rotation_speed = 2 * math.pi / abs(rotation)  # Velocidad angular de rotación
    planet.is_retrograde = rotation < 0  # True si es retrógrado
    planet.orbit_speed = 1 / math.sqrt(semi_major_axis)  # Velocidad angular orbital
    return planet


class Test(Base):
    def initialize(self):
        print("Initializing program...")
        self.renderer = Renderer()
        self.scene = Scene()
        self.camera = Camera(aspectRatio=800 / 600)
        self.camera.setPosition([0, 0, 100])
        self.rig = MovementRig()
        self.rig.add(self.camera)
        self.rig.setPosition([0.5, 1, 60])
        self.scene.add(self.rig)

        # Crear planetas
        self.planets = [
            create_planet("Mercury", 0.3, "imgs/Venus.jpg", 5, 4.9, 58.6),
            create_planet("Venus", 0.5, "imgs/Tierra.jpg", 8, 7.8, -243),
            create_planet("Earth", 1, "imgs/Marte.jpg", 12, 11.8, 1),
            create_planet("Mars", 0.8, "imgs/Jupiter.jpg", 16, 15.5, 1.03),
            create_planet("Jupiter", 2, "imgs/Saturno.jpg", 20, 19.5, 0.41),
            create_planet("Saturn", 1.5, "imgs/Urano.jpg", 30, 29, 0.45),
            create_planet("Uranus", 1.2, "imgs/Neptuno.jpg", 40, 39, 0.72),
            create_planet("Neptune", 1.1, "imgs/Sol.jpg", 50, 48.5, 0.67),
            create_planet("Sun", 3, "imgs/Mercurio.jpg", 0.1, 0.1, 0.1),
        ]

        for planet in self.planets:
            self.scene.add(planet)


        # Configuración para grabar
        self.recording = True
        self.frame_width = 800  # Cambiar según el tamaño del render
        self.frame_height = 600
        fourcc = cv2.VideoWriter_fourcc(*"XVID")
        self.output_video = cv2.VideoWriter("output.avi", fourcc, 30.0, (self.frame_width, self.frame_height))
        print("Grabación iniciada. Presiona Ctrl+C para detener.")

    def update(self):
        self.rig.update(self.input, self.deltaTime)

        for i, planet in enumerate(self.planets):
            # Obtener posición en órbita elíptica
            angle = self.time * planet.orbit_speed  # Velocidad orbital proporcional
            x = planet.semi_major_axis * math.cos(angle)
            y = planet.semi_minor_axis * math.sin(angle)
            planet.setPosition([x, y, 0])

            # Rotación sobre su eje
            rotation_angle = self.deltaTime * planet.rotation_speed
            if planet.is_retrograde:
                rotation_angle = -rotation_angle
            planet.rotateY(rotation_angle)

        # Renderizar escena
        self.renderer.render(self.scene, self.camera)

        # Capturar el frame y escribirlo en el archivo de video
        if self.recording:
            frame = self.renderer.getFrame()  # Método para obtener el frame renderizado
            frame_bgr = cv2.cvtColor(np.array(frame), cv2.COLOR_RGB2BGR)  # Asegúrate de convertir a BGR
            self.output_video.write(frame_bgr)

    def finalize(self):
        # Detener la grabación y liberar recursos
        if self.recording:
            self.output_video.release()
            print("Grabación finalizada y guardada como 'output.avi'.")

Test(screenSize=[800, 600]).run()
