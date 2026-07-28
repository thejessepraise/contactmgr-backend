from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()


# ==========================================
# CORS
# Allows your JavaScript frontend to
# communicate with FastAPI
# ==========================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==========================================
# CONTACT MODEL
# ==========================================

class Contact(BaseModel):
    name: str
    phone: str
    email: str
    img: str = "https://i.pravatar.cc/150"


# ==========================================
# TEMPORARY DATABASE
# ==========================================

contacts = [
    {
        "id": 1,
        "name": "Ann Bator",
        "phone": "212-200-4402",
        "email": "ann@example.com",
        "img": "https://i.pravatar.cc/150?img=11"
    },
    {
        "id": 2,
        "name": "Alex Lipshutz",
        "phone": "323-858-4856",
        "email": "alex@example.com",
        "img": "https://i.pravatar.cc/150?img=12"
    },
    {
        "id": 3,
        "name": "Alexander Torff",
        "phone": "559-401-9243",
        "email": "alexander@example.com",
        "img": "https://i.pravatar.cc/150?img=13"
    },
    {
        "id": 4,
        "name": "Britney Siphron",
        "phone": "707-874-5941",
        "email": "britney@example.com",
        "img": "https://i.pravatar.cc/150?img=14"
    },
    {
        "id": 5,
        "name": "Bennett Lipshutz",
        "phone": "760-483-3097",
        "email": "bennett@example.com",
        "img": "https://i.pravatar.cc/150?img=15"
    }
]


# ==========================================
# HOME
# ==========================================

@app.get("/")
def home():

    return {
        "message": "Contact Manager API is running"
    }


# ==========================================
# GET ALL CONTACTS
# ==========================================

@app.get("/contacts")
def get_contacts():

    return contacts


# ==========================================
# GET ONE CONTACT
# ==========================================

@app.get("/contacts/{contact_id}")
def get_contact(contact_id: int):

    for contact in contacts:

        if contact["id"] == contact_id:
            return contact

    raise HTTPException(
        status_code=404,
        detail="Contact not found"
    )


# ==========================================
# ADD CONTACT
# ==========================================

@app.post("/contacts", status_code=201)
def add_contact(contact: Contact):

    # Generate a new ID

    if contacts:
        new_id = max(
            existing_contact["id"]
            for existing_contact in contacts
        ) + 1

    else:
        new_id = 1


    new_contact = {
        "id": new_id,
        **contact.model_dump()
    }


    contacts.append(new_contact)

    return new_contact


# ==========================================
# UPDATE CONTACT
# ==========================================

@app.put("/contacts/{contact_id}")
def update_contact(
    contact_id: int,
    updated_contact: Contact
):

    for contact in contacts:

        if contact["id"] == contact_id:

            contact["name"] = updated_contact.name
            contact["phone"] = updated_contact.phone
            contact["email"] = updated_contact.email
            contact["img"] = updated_contact.img

            return contact


    raise HTTPException(
        status_code=404,
        detail="Contact not found"
    )


# ==========================================
# DELETE CONTACT
# ==========================================

@app.delete("/contacts/{contact_id}")
def delete_contact(contact_id: int):

    for contact in contacts:

        if contact["id"] == contact_id:

            contacts.remove(contact)

            return {
                "message": "Contact deleted successfully"
            }


    raise HTTPException(
        status_code=404,
        detail="Contact not found"
    )