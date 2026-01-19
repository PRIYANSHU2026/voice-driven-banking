from fastapi import FastAPI
from pydantic import BaseModel
from voicebank.workflows.pipeline import process_command_text


app = FastAPI(title="VoiceBank API")


class Command(BaseModel):
    user_id: str
    text: str


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/workflows/command")
async def workflows_command(cmd: Command):
    return process_command_text(cmd.text, cmd.user_id)
