from core.texture import Texture
from geometry.sphereGeometry import SphereGeometry
from material.textureMaterial import TextureMaterial
from core.mesh  import Mesh
import math

def create_planet(name, radius, texture_path, distance, rotation):
    """
    Crea un Mesh para un planeta con sus características.
    name: Nombre del planeta
    radius: Radio de la esfera
    texture_path: Ruta de la textura
    distance: Distancia orbital desde el Sol
    """
    geometry = SphereGeometry(radius)
    texture = Texture(texture_path)
    material = TextureMaterial(texture)
    planet = Mesh(geometry, material)
    planet.setPosition([distance, 0, 0])  # Distancia desde el Sol
    planet.rotation_speed = 2 * math.pi / abs(rotation)  # Velocidad angular de rotación
    planet.is_retrograde = rotation < 0  # True si es retrógrado

    return planet