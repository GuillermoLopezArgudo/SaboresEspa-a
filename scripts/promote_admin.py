"""
Promueve un usuario a admin por email.

Uso (local SQLite):
  set USE_SQLITE=1
  .venv\\Scripts\\python.exe scripts/promote_admin.py tu@email.com

Con Neon:
  set DATABASE_URL=postgresql://...
  .venv\\Scripts\\python.exe scripts/promote_admin.py tu@email.com
"""
import os
import sys

# Asegurar imports del paquete app
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from app.models import Users  # noqa: E402


def main():
    if len(sys.argv) < 2:
        print("Uso: python scripts/promote_admin.py email@ejemplo.com")
        sys.exit(1)
    email = sys.argv[1].strip().lower()
    user = Users.get_or_none(Users.user_email == email)
    if not user:
        print(f"No existe usuario con email {email}")
        sys.exit(1)
    Users.update(user_type="admin").where(Users.id == user.id).execute()
    print(f"OK: {email} ahora es admin (id={user.id})")


if __name__ == "__main__":
    main()
