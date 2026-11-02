import base64
import os
import uuid

ALLOWED_IMAGE_EXT = {".png", ".jpg", ".jpeg", ".gif", ".webp"}
ALLOWED_VIDEO_EXT = {".mp4", ".mov", ".avi", ".webm"}
MAX_BASE64_BYTES = 8 * 1024 * 1024  # 8 MB

# Firmas mágicas (inicio del archivo)
_IMAGE_SIGNATURES = (
    (b"\xff\xd8\xff", ".jpg"),  # JPEG
    (b"\x89PNG\r\n\x1a\n", ".png"),
    (b"GIF87a", ".gif"),
    (b"GIF89a", ".gif"),
    (b"RIFF", ".webp"),  # WebP: RIFF....WEBP
)
_VIDEO_SIGNATURES = (
    (b"\x00\x00\x00", ".mp4"),  # ftyp often at offset 4; checked below
    (b"\x1aE\xdf\xa3", ".webm"),  # EBML / WebM / MKV
)


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
    # ISO BMFF (mp4/mov): ....ftyp
    if len(data) >= 12 and data[4:8] == b"ftyp":
        brand = data[8:12]
        if brand in (b"qt  ",):
            return ".mov"
        return ".mp4"
    if data.startswith(b"\x1aE\xdf\xa3"):
        return ".webm"
    # AVI: RIFF....AVI
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


def _upload_cloudinary(file_data: bytes, kind: str, ext: str) -> str | None:
    try:
        import cloudinary
        import cloudinary.uploader
        from app.config import Config

        if Config.CLOUDINARY_URL:
            cloudinary.config(cloudinary_url=Config.CLOUDINARY_URL)
        else:
            cloudinary.config(
                cloud_name=Config.CLOUDINARY_CLOUD_NAME,
                api_key=Config.CLOUDINARY_API_KEY,
                api_secret=Config.CLOUDINARY_API_SECRET,
                secure=True,
            )

        resource = "image" if kind == "image" else "video"
        folder = "sabores/images" if kind == "image" else "sabores/videos"
        result = cloudinary.uploader.upload(
            f"data:application/octet-stream;base64,{base64.b64encode(file_data).decode()}",
            resource_type=resource,
            folder=folder,
            public_id=uuid.uuid4().hex,
            overwrite=False,
        )
        return result.get("secure_url") or result.get("url")
    except Exception as exc:
        print(f"Error Cloudinary: {exc}")
        return None


def _save_local(file_data: bytes, folder: str, ext: str) -> str | None:
    try:
        safe_name = f"{uuid.uuid4().hex}{ext}"
        os.makedirs(folder, exist_ok=True)
        file_path = os.path.join(folder, safe_name)
        with open(file_path, "wb") as file:
            file.write(file_data)
        return file_path.replace("\\", "/")
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

    detected = _detect_image_ext(file_data) if kind == "image" else _detect_video_ext(file_data)
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
        print("Cloudinary falló; no se hace fallback a disco en producción")
        if Config.IS_PRODUCTION:
            return None

    if Config.IS_PRODUCTION and not Config.USE_CLOUDINARY:
        print(
            "[warn] Producción sin Cloudinary: los ficheros en disco se pierden al redeploy"
        )

    return _save_local(file_data, folder, ext)
