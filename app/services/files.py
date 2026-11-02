import base64
import os


def save_base64_file(base64_data, file_name, folder):
    if not base64_data or not file_name:
        return None
    try:
        if isinstance(base64_data, str) and base64_data.startswith("data:"):
            base64_data = base64_data.split(",", 1)[1]

        file_data = base64.b64decode(base64_data)
        safe_name = os.path.basename(file_name).replace("..", "_")
        os.makedirs(folder, exist_ok=True)
        file_path = os.path.join(folder, safe_name)
        with open(file_path, "wb") as file:
            file.write(file_data)
        return file_path.replace("\\", "/")
    except Exception as exc:
        print(f"Error al guardar archivo base64: {exc}")
        return None
