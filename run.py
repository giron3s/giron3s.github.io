import http.server
import socketserver
import threading
import webbrowser

from main import Portfolio

PORT = 8000


def build() -> None:
    portfolio = Portfolio()
    context = {key: portfolio.load_config_file(key) for key in portfolio.config_files}
    portfolio.render_template("index.j2", "index.html", context)


def serve() -> None:
    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", PORT), handler) as httpd:
        url = f"http://localhost:{PORT}"
        print(f"Serving portfolio at {url} (Ctrl+C to stop)")
        threading.Timer(0.5, lambda: webbrowser.open(url)).start()
        httpd.serve_forever()


if __name__ == "__main__":
    build()
    try:
        serve()
    except KeyboardInterrupt:
        pass
