import base64
import os
import uuid

ALLOWED_IMAGE_EXT = {".png", ".jpg", ".jpeg", ".gif", ".webp"}
ALLOWED_VIDEO_EXT = {".mp4", ".mov", ".avi", ".webm"}
MAX_BASE64_BYTES = 8 * 1024 * 1024  # 8 MB


def _extension(file_name: str) -> str:
    return os.path.splitext(os.path.basename(file_name or ""))[1].lower()


def save_base64_file(base64_data, file_name, folder, kind="image"):
    if not base64_data or not file_name:
        return None
    try:
        if isinstance(base64_data, str) and base64_data.startswith("data:"):
            base64_data = base64_data.split(",", 1)[1]

        file_data = base64.b64decode(base64_data, validate=False)
        if len(file_data) > MAX_BASE64_BYTES:
            print("Archivo demasiado grande")
            return None

        ext = _extension(file_name)
        allowed = ALLOWED_IMAGE_EXT if kind == "image" else ALLOWED_VIDEO_EXT
        if ext not in allowed:
            print(f"Extensión no permitida: {ext}")
            return None

        # Evitar path traversal y colisiones
        safe_name = f"{uuid.uuid4().hex}{ext}"
        os.makedirs(folder, exist_ok=True)
        file_path = os.path.join(folder, safe_name)
        with open(file_path, "wb") as file:
            file.write(file_data)
        return file_path.replace("\\", "/")
    except Exception as exc:
        print(f"Error al guardar archivo base64: {exc}")
        return None
