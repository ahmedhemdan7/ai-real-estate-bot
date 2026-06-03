from sqlalchemy import create_engine

DATABASE_URL = "postgresql://postgres:An800900@localhost:5432/ai bot"

engine = create_engine(DATABASE_URL)

connection = engine.connect()

print("Database Connected!")