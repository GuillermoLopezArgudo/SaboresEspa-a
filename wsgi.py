from app import app

if __name__ == "__main__":
    import os

    port = int(os.getenv("PORT", "5000"))
    # Default OFF: evita debugger expuesto si alguien arranca wsgi.py en un entorno real
    app.run(host="0.0.0.0", port=port, debug=os.getenv("FLASK_DEBUG", "0") == "1")
