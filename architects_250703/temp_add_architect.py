import architect_db as db

db.create_tables()
architect_id = db.add_architect('Frank Lloyd Wright', '1867-06-08', '1959-04-09', 'American', '''Prolific American architect known for his 'organic architecture' philosophy, emphasizing harmony between humanity and its environment. Designed over 1,000 structures, with 532 realized, including Fallingwater and the Solomon R. Guggenheim Museum.''')
print(f'Added architect with ID: {architect_id}')