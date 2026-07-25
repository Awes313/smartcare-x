"""
Secure file upload handling for profile photos and lab/medical reports.
Every saved file gets a UUID-based name to avoid collisions and to stop
users from controlling server-side file paths via the original filename.
"""

import os
import uuid

from flask import current_app
from werkzeug.utils import secure_filename


def _allowed(filename, allowed_extensions):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in allowed_extensions


def _unique_filename(original_filename):
    ext = secure_filename(original_filename).rsplit(".", 1)[-1].lower()
    return f"{uuid.uuid4().hex}.{ext}"


def save_profile_photo(file_storage):
    """
    file_storage: werkzeug.datastructures.FileStorage from request.files
    Returns the saved filename (not the full path) to store on User.profile_photo,
    or None if no valid file was provided.
    """
    if not file_storage or file_storage.filename == "":
        return None

    allowed = current_app.config["ALLOWED_IMAGE_EXTENSIONS"]
    if not _allowed(file_storage.filename, allowed):
        raise ValueError("Unsupported image format. Allowed: " + ", ".join(sorted(allowed)))

    filename = _unique_filename(file_storage.filename)
    subdir = current_app.config["PROFILE_PHOTO_SUBDIR"]
    dest_path = os.path.join(current_app.config["UPLOAD_FOLDER"], subdir, filename)
    file_storage.save(dest_path)
    return filename


def save_medical_report(file_storage):
    """
    Saves a lab report / scan document (PDF or image).
    Returns the relative path to store on MedicalReport.file_path.
    """
    if not file_storage or file_storage.filename == "":
        raise ValueError("No file was provided.")

    allowed = current_app.config["ALLOWED_DOCUMENT_EXTENSIONS"]
    if not _allowed(file_storage.filename, allowed):
        raise ValueError("Unsupported file format. Allowed: " + ", ".join(sorted(allowed)))

    filename = _unique_filename(file_storage.filename)
    subdir = current_app.config["LAB_REPORT_SUBDIR"]
    dest_path = os.path.join(current_app.config["UPLOAD_FOLDER"], subdir, filename)
    file_storage.save(dest_path)
    return f"{subdir}/{filename}"


def delete_uploaded_file(relative_path):
    """Best-effort delete; never raises if the file is already gone."""
    full_path = os.path.join(current_app.config["UPLOAD_FOLDER"], relative_path)
    try:
        os.remove(full_path)
    except OSError:
        pass