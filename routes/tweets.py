from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import models
import schemas
from database import get_db
from routes.oauth2 import get_current_user

router = APIRouter(prefix="/twitter", tags=["Twitter"])

@router.post("/newtweet", response_model=schemas.twitternewuser)
async def newtweet(
    tweet: schemas.TwitterCreate,
    db: Session = Depends(get_db),
    current_user: schemas.TokenData = Depends(get_current_user),
):

    user = db.query(models.users).filter(
        models.users.email == current_user.id
    ).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User account not found",
        )

    new_tweet = models.Twitter(userid=user.userid, content=tweet.content)
    db.add(new_tweet)
    db.commit()
    db.refresh(new_tweet)
    return new_tweet
@router.get("/gettweet/{id}",response_model=schemas.twitternewuser)
async def gettweet(id:int,db:Session=Depends(get_db),current_user:schemas.TokenData=Depends(get_current_user)):
    twtq=db.query(models.Twitter).filter(models.Twitter.tweetid==id)
    tweet=twtq.first()
    if not tweet:
        raise(HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Tweet is not available"))
    return tweet

@router.delete("/deletetweet/{id}")
async def deletetweet(id:int,db:Session=Depends(get_db),current_user:schemas.TokenData=Depends(get_current_user)):
    twt=db.query(models.Twitter).filter(models.Twitter.tweetid==id).first()
    if not twt:
        raise(HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Tweet doesn't found"))
    user = db.query(models.users).filter(
        models.users.email == current_user.id
    ).first()
    if not user or twt.userid != user.userid:
        raise(HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="You can delete only your Tweets"))
    db.delete(twt)
    db.commit()
    return "Tweet Deleted"

@router.get("/alltweets/{user_id}")
async def getalltweets(user_id:int,db:Session=Depends(get_db),current_user:schemas.TokenData=Depends(get_current_user),limit:int=10):
    tweets=db.query(models.Twitter).filter(models.Twitter.userid==user_id).limit(limit).all()
    if not tweets:
        raise(HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="No Tweets Found"))
    return tweets


@router.post("/like")
async def liketweet(like:schemas.liketweet,db: Session = Depends(get_db),current_user: schemas.TokenData = Depends(get_current_user),):
    user = db.query(models.users).filter(
        models.users.email == current_user.id
    ).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User account not found",
        )

    tweet = db.query(models.Twitter).filter(
        models.Twitter.tweetid == like.tweetid
    ).first()
    if not tweet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tweet is not available",
        )

    existing_like = db.query(models.Likes).filter(
        models.Likes.tweetid == like.tweetid,
        models.Likes.userid == user.userid,
    ).first()

    if like.like and not existing_like:
        db.add(models.Likes(tweetid=like.tweetid, userid=user.userid))
    elif not like.like and existing_like:
        db.delete(existing_like)

    db.commit()
    return {"liked": like.like}


    