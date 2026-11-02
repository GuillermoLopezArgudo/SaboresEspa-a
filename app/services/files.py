import base64
import io
import os
import uuid

ALLOWED_IMAGE_EXT = {".png", ".jpg", ".jpeg", ".gif", ".webp"}
ALLOWED_VIDEO_EXT = {".mp4", ".mov", ".avi", ".webm"}
MAX_BASE64_BYTES = 8 * 1024 * 1024  # 8 MB

# Último error de Cloudinary (para /health)
LAST_CLOUDINARY_ERROR: str | None = None

_MIME = {
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".gif": "image/gif",
    ".webp": "image/webp",
    ".mp4": "video/mp4",
    ".mov": "video/quicktime",
    ".avi": "video/x-msvideo",
    ".webm": "video/webm",
}


def _extension(file_name: str) -> str:
    return os.path.splitext(os.path.basename(file_name or ""))[1].lower()


def _detect_image_ext(data: bytes) -> str | None:
    if data.startswith(b"\xff\xd8\xff"):
        return ".jpg"
    if data.startswith(b"\x89PNG\r\n\x1a\n"):
        return ".png"
    if data.startswith(b"GIF87a") or data.startswith(b"GIF89a"):
        return ".gif"
    if len(data) >= 12 and data[:4] == b"RIFF" and data[8:12] == b"WEBP":
        return ".webp"
    return None


def _detect_video_ext(data: bytes) -> str | None:
    if len(data) >= 12 and data[4:8] == b"ftyp":
        brand = data[8:12]
        if brand in (b"qt  ",):
            return ".mov"
        return ".mp4"
    if data.startswith(b"\x1aE\xdf\xa3"):
        return ".webm"
    if len(data) >= 12 and data[:4] == b"RIFF" and data[8:12] == b"AVI ":
        return ".avi"
    return None


def _decode_base64(base64_data) -> bytes | None:
    try:
        if isinstance(base64_data, str) and base64_data.startswith("data:"):
            base64_data = base64_data.split(",", 1)[1]
        return base64.b64decode(base64_data, validate=False)
    except Exception:
        return None


def _clean_env(value: str) -> str:
    return (value or "").strip().strip('"').strip("'")


def _configure_cloudinary():
    import cloudinary
    from app.config import Config

    url = _clean_env(Config.CLOUDINARY_URL)
    cloud = _clean_env(Config.CLOUDINARY_CLOUD_NAME)
    key = _clean_env(Config.CLOUDINARY_API_KEY)
    secret = _clean_env(Config.CLOUDINARY_API_SECRET)

    if url:
        # Formato: cloudinary://API_KEY:API_SECRET@CLOUD_NAME
        os.environ["CLOUDINARY_URL"] = url
        cloudinary.config(secure=True)
    elif cloud and key and secret:
        cloudinary.config(
            cloud_name=cloud,
            api_key=key,
            api_secret=secret,
            secure=True,
        )
    else:
        raise RuntimeError(
            "Cloudinary no configurado (faltan CLOUDINARY_URL o CLOUD_NAME/API_KEY/API_SECRET)"
        )

    cfg = cloudinary.config()
    if not cfg.cloud_name or not cfg.api_key or not cfg.api_secret:
        raise RuntimeError("Cloudinary config incompleta tras inicializar")
    return cfg


def _upload_cloudinary(file_data: bytes, kind: str, ext: str) -> str | None:
    global LAST_CLOUDINARY_ERROR
    LAST_CLOUDINARY_ERROR = None
    try:
        import cloudinary.uploader

        cfg = _configure_cloudinary()
        resource = "image" if kind == "image" else "video"
        folder = "sabores/images" if kind == "image" else "sabores/videos"
        mime = _MIME.get(ext) or (
            "image/jpeg" if kind == "image" else "video/mp4"
        )
        data_uri = f"data:{mime};base64,{base64.b64encode(file_data).decode('ascii')}"

        result = cloudinary.uploader.upload(
            data_uri,
            resource_type=resource,
            folder=folder,
            public_id=uuid.uuid4().hex,
            overwrite=False,
            unique_filename=False,
        )
        url = result.get("secure_url") or result.get("url")
        if not url:
            raise RuntimeError(f"Cloudinary sin URL en respuesta: {result}")
        print(f"[cloudinary] ok cloud={cfg.cloud_name} -> {url[:80]}")
        return url
    except Exception as exc:
        LAST_CLOUDINARY_ERROR = str(exc)
        print(f"[cloudinary] ERROR: {exc}")
        return None


def _save_local(file_data: bytes, folder: str, ext: str) -> str | None:
    try:
        safe_name = f"{uuid.uuid4().hex}{ext}"
        os.makedirs(folder, exist_ok=True)
        file_path = os.path.join(folder, safe_name)
        with open(file_path, "wb") as file:
            file.write(file_data)
        kind_folder = "images" if "images" in folder.replace("\\", "/") else "videos"
        return f"/uploads/{kind_folder}/{safe_name}"
    except Exception as exc:
        print(f"Error al guardar archivo local: {exc}")
        return None


def save_base64_file(base64_data, file_name, folder, kind="image"):
    """
    Valida extensión + magic bytes. Sube a Cloudinary si está configurado;
    si no, guarda en disco local (efímero en Render).
    """
    if not base64_data or not file_name:
        return None

    file_data = _decode_base64(base64_data)
    if file_data is None:
        return None
    if len(file_data) > MAX_BASE64_BYTES:
        print("Archivo demasiado grande")
        return None
    if len(file_data) < 12:
        print("Archivo demasiado pequeño / inválido")
        return None

    claimed_ext = _extension(file_name)
    allowed = ALLOWED_IMAGE_EXT if kind == "image" else ALLOWED_VIDEO_EXT
    if claimed_ext and claimed_ext not in allowed:
        print(f"Extensión no permitida: {claimed_ext}")
        return None

    detected = (
        _detect_image_ext(file_data) if kind == "image" else _detect_video_ext(file_data)
    )
    if not detected:
        print("Contenido no coincide con imagen/vídeo permitido")
        return None

    if claimed_ext:
        jpeg_ok = claimed_ext in {".jpg", ".jpeg"} and detected == ".jpg"
        if not jpeg_ok and claimed_ext != detected:
            print(f"Magic mismatch: claimed {claimed_ext}, got {detected}")
            return None

    ext = detected

    from app.config import Config

    if Config.USE_CLOUDINARY:
        url = _upload_cloudinary(file_data, kind, ext)
        if url:
            return url
        # En producción no caemos a disco efímero (Render pierde /static al redeploy)
        if Config.IS_PRODUCTION:
            print(
                "[error] Cloudinary falló en producción; no hay fallback local "
                f"({LAST_CLOUDINARY_ERROR})"
            )
            return None
        print(
            "[warn] Cloudinary falló; fallback a disco local "
            f"({LAST_CLOUDINARY_ERROR})"
        )

    if Config.IS_PRODUCTION and not Config.USE_CLOUDINARY:
        print(
            "[error] Producción sin Cloudinary: rechazando upload a disco efímero"
        )
        return None

    return _save_local(file_data, folder, ext)


def cloudinary_status() -> dict:
    """Estado seguro (sin secretos ni detalles de error) para /health."""
    from app.config import Config

    status = {
        "configured": bool(Config.USE_CLOUDINARY),
        "sdk_installed": False,
    }
    try:
        import cloudinary  # noqa: F401

        status["sdk_installed"] = True
    except Exception:
        status["sdk_installed"] = False
    return status
