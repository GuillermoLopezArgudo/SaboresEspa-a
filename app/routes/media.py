from flask import Blueprint, current_app, send_from_directory

media_bp = Blueprint("media", __name__)


@media_bp.get("/static/images/<path:filename>")
def serve_image(filename):
    return send_from_directory(current_app.config["UPLOAD_FOLDER_IMAGES"], filename)


@media_bp.get("/static/videos/<path:filename>")
def serve_video(filename):
    return send_from_directory(current_app.config["UPLOAD_FOLDER_VIDEOS"], filename)
