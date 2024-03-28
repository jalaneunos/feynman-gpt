import os
import tempfile
from google.cloud import storage
import textract


def upload_text(request):
    if request.method == 'POST' and request.files:
        file = request.files['file']
        bucket_name = 'feynman-bucket-1'

        storage_client = storage.Client()
        bucket = storage_client.get_bucket(bucket_name)

        file_content = file.read()
        file_extension = file.filename.split('.')[-1].lower()

        with tempfile.NamedTemporaryFile(delete=False, suffix=f'.{file_extension}') as temp_file:
            temp_file.write(file_content)
            temp_file_path = temp_file.name

        text = extract_text(temp_file_path, file_extension)

        os.unlink(temp_file_path)  # Remove the temporary file

        filename = file.filename.split('.')[0]
        blob = bucket.blob(filename + '.txt')
        blob.upload_from_string(text)

        return f'Text uploaded successfully. Extracted text: {text}'
    else:
        return 'Invalid request'


def extract_text(file_path, file_extension):
    try:
        text = textract.process(file_path, extension=file_extension, encoding='utf-8')
        return text.decode('utf-8')
    except (textract.exceptions.MissingFileError, textract.exceptions.ExtensionNotSupported,
            textract.exceptions.ShellError) as e:
        raise Exception(str(e))
    except Exception as e:
        raise Exception(f'An error occurred: {str(e)}')
