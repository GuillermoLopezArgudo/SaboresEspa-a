from flask import Blueprint, jsonify

from app.models import ping_database
from app.services.files import cloudinary_status

health_bp = Blueprint("health", __name__)


@health_bp.get("/health")
def health():
    status = cloudinary_status()
    db_ok, db_detail = ping_database()
    payload = {
        "status": "ok" if db_ok else "degraded",
        "database": {"ok": db_ok, "detail": db_detail if not db_ok else "ok"},
        "cloudinary": {
            "configured": status.get("configured"),
            "sdk_installed": status.get("sdk_installed"),
        },
    }
    return jsonify(payload), (200 if db_ok else 503)
