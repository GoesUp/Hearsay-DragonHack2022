# Imports the Google Cloud Translation library
from google.cloud import translate


def translate_text(text, project_id="hearsay-python"):
    """
    Translate the given text into some language (currently hardcoded to french :) ).

    :param text: the text to translate
    :param project_id: project ID of the google cloud project
    :return: the translated text
    """

    client = translate.TranslationServiceClient()

    location = "global"

    parent = f"projects/{project_id}/locations/{location}"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "mime_type": "text/plain",  # mime types: text/plain, text/html
            "source_language_code": "en-US",
            "target_language_code": "fr",
        }
    )

    # Display the translation for each input text provided
    for translation in response.translations:
        return translation


if __name__ == '__main__':
    translate_text()
