from flask import Flask, render_template
import markdown 

app = Flask(__name__)

# Ruta para servir archivos estáticos
@app.route('/static/<path:filename>')
def serve_static(filename):
    return app.send_static_file(filename)

# Ruta principal para renderizar la página
@app.route('/')
def home():
    # Leer contenido Markdown
    content_path = 'content/ejemplo.md'
    with open(content_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Convertir Markdown a HTML
    html_content = markdown.markdown(content)

    # Renderizar plantilla
    context = {'content': html_content}
    return render_template('index.html', **context)

if __name__ == "__main__":
    app.run(debug=True)