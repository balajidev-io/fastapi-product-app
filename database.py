#8 
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

db_url = "postgresql://fastapi_user:MgLDqyg1MjW0A8oA27qcJWuVnvJUe5Oy@dpg-d81hoggg4nts739h8f2g-a.oregon-postgres.render.com/fastapi_db_4zu0"

engine = create_engine(db_url)
SessionLocal = sessionmaker(autocommit = False, autoflush=False, bind=engine)