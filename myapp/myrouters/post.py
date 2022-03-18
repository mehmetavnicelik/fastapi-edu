from fastapi import FastAPI,Response,status,HTTPException,Depends,APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from myapp import oauth2
from .. import models,schemas,oauth2
from ..database import get_db
from typing import List,Optional


router=APIRouter(
    prefix="/posts",
    tags=["POSTS"]
)

#@router.get("/",response_model=List[schemas.PostServiceResponse])
@router.get("/")
#@router.get("/",response_model=List[schemas.PostServiceResponse4Vote]) #this should have been working but there is an error which i couldnt solve.

def get_posts(db: Session =Depends(get_db),current_user:int=Depends(oauth2.get_current_user),limit: int=5,skip: int=0,search: Optional[str]=""):             
    #cursor.execute("""SELECT * FROM posts """)
    #posts = cursor.fetchall()
    #print(posts)
    ##next line provides that the user cann see only his own posts
    ##posts=db.query(models.Post).filter(models.Post.owner_id==current_user.id).all()
    #posts=db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    results=db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(models.Vote,models.Vote.post_id==models.Post.id,isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    print(results)
    return results

@router.get("/latest")
def get_latest_post(db: Session =Depends(get_db)):
    #post=db.query(models.Post).order_by(models.Post.created_at.desc())
    all_post=db.query(models.Post).all()
    size=len(all_post)
    post=all_post[size-1]

    return post

@router.get("/first")
def get_first_post(db: Session =Depends(get_db)):
    post=db.query(models.Post).first()
    return post

#@router.get("/{id}",response_model=schemas.PostServiceResponse4Vote)   #this should have been working but there is an error which i couldnt solve.                                         
@router.get("/{id}")                                         
def get_posts(id:int, response:Response,db: Session =Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
    #post=db.query(models.Post).filter(models.Post.id==id).first()
    post=db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(models.Vote,models.Vote.post_id==models.Post.id,isouter=True).group_by(models.Post.id).filter(models.Post.id==id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with ID {id} could not be found")
    return post

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.PostServiceResponse)
def create_posts(post: schemas.PostCreate,db: Session =Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
    #new_post=models.Post(title=post.title,content=post.content,published=post.published)
    
    new_post=models.Post(owner_id=current_user.id,**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    print(current_user.email)
    return new_post

@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int,db: Session =Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
    post_query=db.query(models.Post).filter(models.Post.id==id)
    post=post_query.first()
    if post==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {id} does not exist")
    if post.owner_id!= current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorized to perfom requested action.")
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}",response_model=schemas.PostServiceResponse)                                                 #database connected
def update_post(id:int,updated_post:schemas.PostCreate,db: Session =Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
    post_query=db.query(models.Post).filter(models.Post.id==id)
    post=post_query.first()
    if post==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {id} does not exist")
    post_query.update(updated_post.dict(),synchronize_session=False)
    db.commit()
    return post_query.first()