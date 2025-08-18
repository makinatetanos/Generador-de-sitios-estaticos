import os
import shutil
import markdown
from flask import Flask
from jinja2 import Environment, FileSystemLoader

app = Flask(__name__)

# Configuración inicial
def main():
    print("Generador de sitios estáticos en Python")
    generate_site()

def render_template(template_name, context, output_path):
    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template(template_name)
    output = template.render(context)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(output)

def copy_static_files(src, dest):
    if os.path.exists(dest):
        shutil.rmtree(dest)
    shutil.copytree(src, dest)

def generate_site():
    # Crear carpeta de salida si no existe
    output_dir = 'dist'
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(os.path.join(output_dir, 'static'), exist_ok=True)

    # Copiar archivos estáticos
    copy_static_files('static', os.path.join(output_dir, 'static'))

    # Leer contenido Markdown
    content_path = 'content'
    for filename in os.listdir(content_path):
        if filename.endswith('.md'):
            with open(os.path.join(content_path, filename), 'r', encoding='utf-8') as f:
                content = f.read()

            # Convertir Markdown a HTML
            html_content = markdown.markdown(content)

            # Renderizar plantilla
            context = {'content': html_content}
            output_file = os.path.join(output_dir, filename.replace('.md', '.html'))
            render_template('index.html', context, output_file)

    print(f"Sitio generado en la carpeta '{output_dir}'.")

@app.route('/')
def home():
    return app.send_static_file('index.html')

@app.route('/<path:path>')
def serve_static(path):
    return app.send_static_file(path)

if __name__ == "__main__":
    main()
    app.run(debug=True)