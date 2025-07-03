import architect_db as db
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
assets_dir = os.path.join(script_dir, 'assets', 'architects')

# Frank Lloyd Wright (ID: 1)
image_path = os.path.join(assets_dir, 'frank_lloyd_wright.jpg')
db.update_architect_image_path(1, image_path)
print(f"Updated Frank Lloyd Wright image path to: {image_path}")

# Le Corbusier (ID: 2)
image_path = os.path.join(assets_dir, 'le_corbusier.jpg')
db.update_architect_image_path(2, image_path)
print(f"Updated Le Corbusier image path to: {image_path}")

# Mies van der Rohe (ID: 3)
image_path = os.path.join(assets_dir, 'mies_van_der_rohe.jpg')
db.update_architect_image_path(3, image_path)
print(f"Updated Mies van der Rohe image path to: {image_path}")

# Zaha Hadid (ID: 4)
image_path = os.path.join(assets_dir, 'zaha_hadid.jpg')
db.update_architect_image_path(4, image_path)
print(f"Updated Zaha Hadid image path to: {image_path}")

# Tadao Ando (ID: 5)
image_path = os.path.join(assets_dir, 'tadao_ando.jpg')
db.update_architect_image_path(5, image_path)
print(f"Updated Tadao Ando image path to: {image_path}")

# Santiago Calatrava (ID: 7)
image_path = os.path.join(assets_dir, 'santiago_calatrava.jpg')
db.update_architect_image_path(7, image_path)
print(f"Updated Santiago Calatrava image path to: {image_path}")
