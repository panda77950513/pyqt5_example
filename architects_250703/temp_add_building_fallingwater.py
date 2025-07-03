import architect_db as db

architect_id = 1 # Frank Lloyd Wright의 ID
db.add_building(architect_id, "Fallingwater", "Mill Run, Pennsylvania, USA", 1939, "A house designed by Frank Lloyd Wright for the Kaufmann family, built partly over a waterfall. A masterpiece of organic architecture, emphasizing harmony between humanity, architecture, and nature. Designated a UNESCO World Heritage Site in 2019.")
print("Added Fallingwater to the database.")