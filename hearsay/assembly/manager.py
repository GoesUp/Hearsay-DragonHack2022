from pydantic import BaseModel
import requests


ASSEMBLYAI_BASE_URL = "https://api.assemblyai.com/v2"
ASSEMBLYAI_API_TOKEN = "INSERT_TOKEN_HERE"


class UploadResult(BaseModel):
    upload_url: str


class TranscriptionJob(BaseModel):
    id: str
    status: str


class Word(BaseModel):
    confidence: float
    end: int
    start: int
    text: str


class TranscriptionResult(BaseModel):
    id: str
    punctuate: bool
    status: str
    text: str | None = None
    words: list[Word] | None = None


def upload_audio_to_assembly(audio_path: str) -> UploadResult:
    def read_file(filename, chunk_size=5242880):
        with open(filename, "rb") as _file:
            while True:
                data = _file.read(chunk_size)
                if not data:
                    break
                yield data

    headers = {"authorization": ASSEMBLYAI_API_TOKEN}
    response = requests.post(
        f"{ASSEMBLYAI_BASE_URL}/upload",
        headers=headers,
        data=read_file(audio_path),
    )

    return UploadResult(**response.json())


def submit_for_transcription(audio_url: str) -> TranscriptionJob:
    endpoint = f"{ASSEMBLYAI_BASE_URL}/transcript"
    json = {"audio_url": audio_url}
    headers = {
        "authorization": ASSEMBLYAI_API_TOKEN,
        "content-type": "application/json",
    }
    response = requests.post(endpoint, json=json, headers=headers)
    return TranscriptionJob(**response.json())


def get_transcription_result(job_id: str) -> TranscriptionResult:
    endpoint = f"{ASSEMBLYAI_BASE_URL}/transcript/{job_id}"
    headers = {"authorization": ASSEMBLYAI_API_TOKEN}
    response = requests.get(endpoint, headers=headers)
    return TranscriptionResult(**response.json())
