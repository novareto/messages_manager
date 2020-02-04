from enum import Enum
from typing import List, Optional
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from pydantic import BaseModel
from starlette.responses import Response
from fastapi import Depends, FastAPI
import sqlalchemy as sa
from sqlalchemy.orm import Session


SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"


engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

app = FastAPI()


class Level(str, Enum):
    ALERT = "alert"
    INFO = "infos"
    ADVERT = "advert"


class Availability(str, Enum):
    ON_DATES = u"on_dates"
    DISABLED = u"disabled"
    ENABLED = u"enabled"


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


class Message(Base):
    __tablename__ = "messages"

    id = sa.Column(sa.Integer, primary_key=True)
    message = sa.Column(sa.Text, nullable=False)
    type = sa.Column(sa.String(32), nullable=False)
    activation = sa.Column(sa.String(32), nullable=False)
    enable = sa.Column(sa.DateTime, nullable=False, default=datetime.now())
    disable = sa.Column(sa.DateTime, nullable=False, default=datetime.now())


class MessageModel(BaseModel):

    id: Optional[int]
    message: str
    type: Level = Level.INFO
    activation: Availability = Availability.ON_DATES
    enable: datetime = None
    disable: datetime = None

    class Config:
        orm_mode = True


Base.metadata.create_all(bind=engine)


def create_message(db: Session, msg: MessageModel):
    item = Message(**msg.dict())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@app.post("/messages", response_model=MessageModel)
def create_new_message(model: MessageModel, db: Session=Depends(get_db)):
    return create_message(db=db, msg=model)


@app.delete("/messages/{msg_id}")
def delete_message(
        msg_id: int, response: Response, db: Session=Depends(get_db)):
    item = db.query(Message).get(msg_id)
    if item is not None:
        db.delete(item)
        db.commit()
        response.status_code = 202
        return
    response.status_code = 404
    return


@app.get("/messages/list", response_model=List[MessageModel])
def list_messages(db: Session=Depends(get_db), start: int=0, limit: int=25):
    return db.query(Message).offset(start).limit(limit).all()


@app.get("/messages/valid", response_model=List[MessageModel])
def valid_messages(db: Session=Depends(get_db), start: int=0, limit: int=25):
    now = datetime.now()
    enabled = [Message.activation == Availability.ENABLED]
    valid = [Message.activation == Availability.ON_DATES,
             Message.enable <= now,
             Message.disable >= now]
    return db.query(Message).\
             filter(sa.or_(*enabled, sa.and_(*valid))).\
             offset(start).limit(limit).all()
