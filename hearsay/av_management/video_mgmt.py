import subprocess
import uuid
import os


def extract_audio_from_mp4(video_name: str, temporary_folder_location: str) -> str:
    """
    From the given mp4 file, extract the audio file and return the name of the audio.

    :param video_name: name of the mp4 file
    :param temporary_folder_location: location of the temporary folder
    :return: name of the wav file
    """
    audio_name = f"{str(uuid.uuid4())}.wav"
    command = f"ffmpeg -i \"{os.path.join(temporary_folder_location, video_name)}\" -ab 160k -ac 2 -ar 44100 -vn \"{os.path.join(temporary_folder_location, audio_name)}\""
    print(command)
    subprocess.call(command, shell=True)
    return audio_name
