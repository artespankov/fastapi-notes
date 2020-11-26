from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import databases
from config import DATABASE_URL
from models import Note, NoteIn, NotesTable

database = databases.Database(DATABASE_URL)

app = FastAPI(title="REST API for Notes")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.post("/notes", response_model=Note)
async def create_note(note: NoteIn):
    query = NotesTable.insert().values(text=note.text, completed=note.completed)
    last_record_id = await database.execute(query)
    return {"id": last_record_id, **note.dict()}


@app.get("/notes", response_model=List[Note])
async def read_notes(skip: int = 0, take: int = 20):
    query = NotesTable.select().offset(skip).limit(take)
    return await database.fetch_all(query)


@app.put("/notes/{note_id}", response_model=Note)
async def update_note(note_id: int, payload: NoteIn):
    query = NotesTable.update().where(NotesTable.c.id == note_id).values(text=payload.text, completed=payload.completed)
    await database.execute(query)
    return {"id": note_id, **payload.dict()}


@app.get("/notes/{note_id}", response_model=Note)
async def retrieve_note(note_id: int):
    return await database.fetch_one(NotesTable.select().where(NotesTable.c.id == note_id))


@app.delete("/notes/{note_id}")
async def delete_note(note_id: int):
    await database.execute(NotesTable.delete().where(NotesTable.c.id == note_id))
    return {"message": f"Note # {note_id} deleted"}
