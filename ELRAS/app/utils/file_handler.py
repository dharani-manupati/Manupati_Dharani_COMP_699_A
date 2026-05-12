import os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = "app/static/uploads"


class FileHandler:

    @staticmethod
    def save_file(file):
        if not file:
            return None

        filename = secure_filename(file.filename)
        file_path = os.path.join(UPLOAD_FOLDER, filename)

        # Ensure folder exists
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)

        file.save(file_path)

        return file_path

    @staticmethod
    def delete_file(file_path):
        if file_path and os.path.exists(file_path):
            os.remove(file_path)
            return True
        return False