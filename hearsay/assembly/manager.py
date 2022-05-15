from pydantic import BaseModel
import requests


ASSEMBLYAI_BASE_URL = "https://api.assemblyai.com/v2"
ASSEMBLYAI_API_TOKEN = "PUT_YOUR_TOKEN_HERE"


class UploadResult(BaseModel):
    """
    Contains the result of AssemblyAI's upload of the file.
    """
    upload_url: str


class TranscriptionJob(BaseModel):
    """
    Contains data about the status of the transcription job.
    """
    id: str
    status: str


class Word(BaseModel):
    """
    Contains confidence information of every word that is detected by AssemblyAI.
    """
    confidence: float
    end: int
    start: int
    text: str


class TranscriptionResult(BaseModel):
    """
    Contains the complete transcription result by AssemblyAI.
    """
    id: str
    punctuate: bool
    status: str
    text: str | None = None
    words: list[Word] | None = None


def upload_audio_to_assembly(audio_path: str) -> UploadResult:
    """
    Upload the audio track to AssemblyAI and return the upload result.

    :param audio_path: path of the audio track
    :return: upload result class
    """
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
    """
    Submit the specified audio track for transcription on AssemblyAI.

    :param audio_url: the URL of the audio on AssemblyAI's server.
    :return: the transcription job class
    """
    endpoint = f"{ASSEMBLYAI_BASE_URL}/transcript"
    json = {"audio_url": audio_url}
    headers = {
        "authorization": ASSEMBLYAI_API_TOKEN,
        "content-type": "application/json",
    }
    response = requests.post(endpoint, json=json, headers=headers)
    return TranscriptionJob(**response.json())


def get_transcription_result(job_id: str) -> TranscriptionResult:
    """
    Get the result of the transcription job. Is returned even if the job is not yet completed.

    :param job_id: ID of the transcription job
    :return: current state of the transcription job
    """
    endpoint = f"{ASSEMBLYAI_BASE_URL}/transcript/{job_id}"
    headers = {"authorization": ASSEMBLYAI_API_TOKEN}
    response = requests.get(endpoint, headers=headers)
    return TranscriptionResult(**response.json())
