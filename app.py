import os
import shutil
import markdown 
from flask import Flask, render_template
from jinja2 import Environment, FileSystemLoader


app = Flask(__name__)

# Flask sirve automáticamente los archivos de una carpeta llamada 'static'
# en la raíz de tu proyecto. Por lo tanto, esta ruta manual no es necesaria
# si tu archivo 'styles.css' está en 'static/styles.css'.

# Ruta principal para renderizar la página
@app.route('/')
def home():
    # Leer contenido Markdown
    content_path = 'content/post.md'
    try:
        with open(content_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        content = "El archivo 'post.md' no fue encontrado en la ruta especificada."

    # Convertir Markdown a HTML
    html_content = markdown.markdown(content)

    # Renderizar plantilla
    return render_template('index.html', content=html_content)

@app.cli.command("build")
def build():
    """Genera el sitio estático en la carpeta 'dist'."""
    DIST_DIR = 'dist'
    STATIC_DIR = 'static'

    # Limpiar y recrear el directorio de destino
    if os.path.exists(DIST_DIR):
        shutil.rmtree(DIST_DIR)
    
    # Copiar la carpeta de archivos estáticos
    shutil.copytree(STATIC_DIR, os.path.join(DIST_DIR, STATIC_DIR))

    # Leer y convertir el contenido Markdown (igual que en la ruta home)
    with open('content/post.md', 'r', encoding='utf-8') as f:
        content = f.read()
    html_content = markdown.markdown(content)

    # Configurar Jinja2 para renderizar la plantilla de forma independiente
    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template('index.html')
    output_html = template.render(content=html_content)

    # Guardar el HTML generado
    with open(os.path.join(DIST_DIR, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(output_html)
    
    print("✅ Sitio estático generado correctamente en la carpeta 'dist'.")

if __name__ == "__main__":
    app.run(debug=True)