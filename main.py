from sqlalchemy.orm import Session 
import models , schemas
from database import engine , get_db
from fastapi import FastAPI , Depends , HTTPException , Query
import auths
from fastapi.staticfiles import StaticFiles 
import file_upload
#find item in database
from schemas import ItemStatusUpdate



models.Base.metadata.create_all(bind=engine)

app =FastAPI(title="FindIt API")
app.include_router(auths.router)

#home
@app.get("/")
def home():
    return {
        "message" : "welcome to FastAPI"
    }
#find item in database
@app.patch("/items/lost/{item_id}/status")
def update_item_status(item_id : int , data : ItemStatusUpdate , db: Session = Depends(get_db)):

    item = db.query(models.LostItem).filter(models.LostItem.id == item_id).first()

    if item is None :
        raise HTTPException(
            status_code=404,
            detail="Item not found"
        )

    item.status = data.status
    db.commit()
    db.refresh(item)

    return item 


#filesuploads
app.include_router(file_upload.router)
app.mount(
    "/files",
    StaticFiles(directory=file_upload.UPLOAD_DIR),
    name="files"
    
)

#pagination 
@app.get("/items/lost")
def get_pagination(
    page : int = Query(default=1 , ge=1 , le=50),  
    limit : int = Query(default=4 , ge=1 ,le=100),
    search : str = Query(default=""),
    category : str = Query(default=""),
    db : Session = Depends(get_db)
):

    query = db.query(models.LostItem)

    if search :  
        query = query.filter(
            models.LostItem.name.ilike(f"%{search}%")

        )

    if category:
        query = query.filter(
            models.LostItem.category.ilike(f"%{category}%")

        )

    total = query.count()
    start = (page - 1) * limit
    items = query.offset(start).limit(limit).all()


    return {
        "page" : page,
        "limit" : limit,
        "total": total,
        "data" : items
    }


@app.post("/items/lost",response_model=schemas.LostItemResponse,status_code=201)
def report_lost_item(item : schemas.LostItemCreate , db: Session = Depends(get_db)):

    new_item = models.LostItem(
        name=item.name,
        description=item.description,
        location=item.location,
        category=item.category

    )

    db.add(new_item)
    db.commit()
    db.refresh(new_item)

    return new_item



@app.put("/items/lost/{item_id}" , response_model=schemas.LostItemResponse)
def update_item(item_id : int , updated_item: schemas.LostItemCreate , db: Session = Depends(get_db)):
    item = db.query(models.LostItem).filter(models.LostItem.id == item_id).first()

    if not item :
        raise HTTPException(
            status_code=401,
            detail="invalid and error in token generate"
        )

    item.name = updated_item.name
    item.description = updated_item.description
    item.location = updated_item.location
    item.category = updated_item.category

    db.commit()
    db.refresh(item)

    return item 

@app.delete("/delete/item/{item_id}")
def delete_id (item_id : int , db: Session = Depends(get_db)):


    item = db.query(models.LostItem).filter(models.LostItem.id == item_id).first()

    if item is None :
        raise HTTPException(
            status_code=404,
            detail="Lost item not found"
        )

    db.delete(item)
    db.commit()

    return {
        "message" : "lost item deleted sucessfully"
    }




