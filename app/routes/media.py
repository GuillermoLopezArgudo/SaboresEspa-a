import os

from flask import Blueprint, current_app, send_from_directory

media_bp = Blueprint("media", __name__)


def _safe_send(folder: str, filename: str):
    """Sirve fichero local con basename (anti path-traversal).

    Nota: la visibilidad de recetas es a nivel API (listado/detalle).
    Los bytes locales usan UUID opacos; <img>/<video> no pueden enviar Bearer JWT,
    así que no se puede gatear aquí sin romper la UI. Cloudinary CDN es público
    por diseño salvo signed URLs (fuera de alcance).
    """
    filename = os.path.basename(filename or "")
    if not filename or filename in {".", ".."}:
        from flask import abort

        abort(404)
    return send_from_directory(folder, filename)


@media_bp.get("/uploads/images/<path:filename>")
@media_bp.get("/static/images/<path:filename>")
def serve_image(filename):
    return _safe_send(current_app.config["UPLOAD_FOLDER_IMAGES"], filename)


@media_bp.get("/uploads/videos/<path:filename>")
@media_bp.get("/static/videos/<path:filename>")
def serve_video(filename):
    return _safe_send(current_app.config["UPLOAD_FOLDER_VIDEOS"], filename)
