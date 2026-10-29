# Práctica 1.4 — Middleware

**Alumno:** Miguel Luzón Prado

Partiendo de la práctica 1.3, he añadido en `app/main.py`:

- **CORSMiddleware**: permite que el frontend, que irá en `http://localhost:5173`, pueda hacer peticiones a la API. Sin esto el navegador las bloquea porque vienen de otro origen.
- **Middleware propio `tiempo_respuesta`**: mide lo que tarda cada petición y lo devuelve en la cabecera `X-Process-Time` (en milisegundos). Sale en todas las respuestas, también en los errores.
- **Handler global de excepciones**: si salta un error que no está controlado, la API devuelve un 500 con `{"error": "Error interno del servidor"}` sin enseñar el stacktrace, y el servidor sigue funcionando.
- **Ruta `GET /error`**: solo sirve para forzar un error y comprobar que el handler funciona.

## Estructura

```
Practica1.4/
├── app/
│   ├── __init__.py
│   ├── main.py          (middlewares y handlers)
│   ├── schemas.py
│   └── routers/
│       ├── __init__.py
│       ├── tasks.py
│       └── projects.py
├── capturas/
├── README.md
└── requirements.txt
```

## Cómo arrancarlo

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```
