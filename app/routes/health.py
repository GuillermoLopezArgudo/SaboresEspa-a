from flask import Blueprint, jsonify

from app.services.files import cloudinary_status

health_bp = Blueprint("health", __name__)


@health_bp.get("/health")
def health():
    # Solo flags seguros (sin secretos ni mensajes de error internos)
    status = cloudinary_status()
    return jsonify(
        status="ok",
        cloudinary={
            "configured": status.get("configured"),
            "sdk_installed": status.get("sdk_installed"),
        },
    )
