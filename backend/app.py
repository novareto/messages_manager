import json
from datetime import datetime
from enum import Enum
from typing import Type, Any, Dict, List, Optional

from fastapi import Depends, FastAPI
from pydantic import BaseModel
from pydantic.schema import schema
from starlette.responses import Response
from starlette.middleware.cors import CORSMiddleware

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker
import sqlalchemy as sa


origins = [
    "http://localhost",
    "http://localhost:8091",
]


SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"


engine = sa.create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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

        @staticmethod
        def schema_extra(schema: Dict[str, Any], model: Type['MessageModel']) -> None:
            # We don't want the `id` in the schema, it's added later.
            schema['properties'].pop('id')


Base.metadata.create_all(bind=engine)


@app.get("/messages/new")
def message_schema():
    msg_schema = MessageModel.schema()
    msg_schema['$schema'] = 'http://json-schema.org/draft-04/schema#'
    return json.dumps(msg_schema)


def create_message(db: Session, msg: MessageModel):
    item = Message(**msg.dict())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@app.post("/messages/new", response_model=MessageModel)
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
