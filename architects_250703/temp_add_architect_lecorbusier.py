import architect_db as db

db.create_tables()
architect_id = db.add_architect('Le Corbusier', '1887-10-06', '1965-08-27', 'Swiss-French', '''Pioneer of modern architecture, urban planner, painter, designer, and writer. Known for his philosophy 'a house is a machine for living in' and his 'five points of architecture'.''')
print(f'Added architect with ID: {architect_id}')