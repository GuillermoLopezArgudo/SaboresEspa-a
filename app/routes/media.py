import os

from flask import Blueprint, current_app, send_from_directory

media_bp = Blueprint("media", __name__)


@media_bp.get("/uploads/images/<path:filename>")
@media_bp.get("/static/images/<path:filename>")
def serve_image(filename):
    folder = current_app.config["UPLOAD_FOLDER_IMAGES"]
    # compat: si se pidió con subruta antigua
    filename = os.path.basename(filename)
    return send_from_directory(folder, filename)


@media_bp.get("/uploads/videos/<path:filename>")
@media_bp.get("/static/videos/<path:filename>")
def serve_video(filename):
    folder = current_app.config["UPLOAD_FOLDER_VIDEOS"]
    filename = os.path.basename(filename)
    return send_from_directory(folder, filename)
