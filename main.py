from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models import product
from database import SessionLocal, engine
import database_models
from sqlalchemy.orm import Session

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001",
        "http://localhost:3002",
        "https://balajidev-trac-frontend.onrender.com" 
    ],
    allow_methods=["*"],
    allow_headers=["*"]
)
database_models.Base.metadata.create_all(bind=engine)

@app.get("/")
def greet():
    return "hello hii every one"

products = [
    product(id=1, name="phone", description="budget phone", price=99, quantity=10),
    product(id=2, name="Laptop",description="costly", price=19, quantity=56),
    product(id=3, name="iphone", description="top model", price=200000, quantity = 1)
]

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    db = SessionLocal()

    count = db.query(database_models.Product).count()

    if count == 0:
        for product in products:
            db.add(database_models.Product(**product.model_dump()))
        
        db.commit()

init_db()
#this is for to the to get the all product into server I'll explain how it work // localhost:8000/products, use this will get the products
@app.get("/products")
def get_all_products(db: Session = Depends(get_db)):
    #db connection
    db_product = db.query(database_models.Product).all()

    return db_product


#this is the fetching the only one record based on the id.

@app.get("/products/{id}")
def get_product_by_id(id: int, db: Session = Depends(get_db) ):
    db_products = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    if db_products :
            return db_products
        
    return "product not found"


#this is the add a product using the post 
@app.post("/products")
def add_product(product: product, db: Session = Depends(get_db)):
    db.add(database_models.Product(**product.model_dump()))
    db.commit()
    return product

#this api use to update the product
@app.put("/products/{id}")
def update_product(id: int, product: product,  db: Session = Depends(get_db)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    if db_product:
            db_product.name = product.name
            db_product.description = product.description
            db_product.price = product.price
            db_product.quantity = product.quantity
            db.commit()
            return "product updated"
    else:
         "product not found"

#this api is delete the product
@app.delete("/products/{id}")
def delete_product(id:int, db: Session = Depends(get_db)):

    db_product = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    if db_product:
         db.delete(db_product)
         db.commit()
         return "deleted"
    else:
       "product not found"
