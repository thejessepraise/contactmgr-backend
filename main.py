import os

from dotenv import load_dotenv

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel

from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String
)

from sqlalchemy.orm import (
    declarative_base,
    sessionmaker
)


# ==========================================
# DATABASE CONNECTION
# ==========================================

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError(
        "DATABASE_URL is missing from .env"
    )


engine = create_engine(DATABASE_URL)


SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


Base = declarative_base()


# ==========================================
# CONTACT TABLE
# ==========================================

class ContactDB(Base):

    __tablename__ = "contacts"


    id = Column(
        Integer,
        primary_key=True,
        index=True
    )


    name = Column(
        String,
        nullable=False
    )


    phone = Column(
        String,
        nullable=False
    )


    email = Column(
        String,
        nullable=False
    )


Base.metadata.create_all(bind=engine)


# ==========================================
# CONTACT DATA MODEL
# ==========================================

class Contact(BaseModel):

    name: str

    phone: str

    email: str


# ==========================================
# FASTAPI
# ==========================================

app = FastAPI()


app.add_middleware(

    CORSMiddleware,

    allow_origins=["*"],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"]

)


# ==========================================
# HOME
# ==========================================

@app.get("/")
def home():

    return {
        "message": "Contact Manager API is running"
    }


# ==========================================
# GET CONTACTS
# ==========================================

@app.get("/contacts")
def get_contacts():

    db = SessionLocal()

    try:

        return db.query(ContactDB).all()

    finally:

        db.close()


# ==========================================
# GET ONE CONTACT
# ==========================================

@app.get("/contacts/{contact_id}")
def get_contact(contact_id: int):

    db = SessionLocal()

    try:

        contact = (
            db.query(ContactDB)
            .filter(ContactDB.id == contact_id)
            .first()
        )


        if not contact:

            raise HTTPException(
                status_code=404,
                detail="Contact not found"
            )


        return contact

    finally:

        db.close()


# ==========================================
# ADD CONTACT
# ==========================================

@app.post("/contacts", status_code=201)
def add_contact(contact: Contact):

    db = SessionLocal()

    try:

        new_contact = ContactDB(

            name=contact.name,

            phone=contact.phone,

            email=contact.email

        )


        db.add(new_contact)

        db.commit()

        db.refresh(new_contact)


        return new_contact

    finally:

        db.close()


# ==========================================
# UPDATE CONTACT
# ==========================================

@app.put("/contacts/{contact_id}")
def update_contact(
    contact_id: int,
    updated_contact: Contact
):

    db = SessionLocal()

    try:

        contact = (
            db.query(ContactDB)
            .filter(ContactDB.id == contact_id)
            .first()
        )


        if not contact:

            raise HTTPException(
                status_code=404,
                detail="Contact not found"
            )


        contact.name = updated_contact.name

        contact.phone = updated_contact.phone

        contact.email = updated_contact.email


        db.commit()

        db.refresh(contact)


        return contact

    finally:

        db.close()


# ==========================================
# DELETE CONTACT
# ==========================================

@app.delete("/contacts/{contact_id}")
def delete_contact(contact_id: int):

    db = SessionLocal()

    try:

        contact = (
            db.query(ContactDB)
            .filter(ContactDB.id == contact_id)
            .first()
        )


        if not contact:

            raise HTTPException(
                status_code=404,
                detail="Contact not found"
            )


        db.delete(contact)

        db.commit()


        return {
            "message":
            "Contact deleted successfully"
        }

    finally:

        db.close()