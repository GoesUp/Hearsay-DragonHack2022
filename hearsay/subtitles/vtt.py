import webvtt


def convert_file_to_vtt(file_location: str) -> str:
    result = webvtt.from_srt(file_location)
    result.save()
    name = file_location.removesuffix(".srt") + ".vtt"
    return name


if __name__ == '__main__':
    convert_file_to_vtt("C:\\Users\\grego\\Downloads\\The Forger_track3_eng.srt")
