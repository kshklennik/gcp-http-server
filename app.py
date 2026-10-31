import os
from http.server import BaseHTTPRequestHandler, HTTPServer

import psycopg


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/db":
            try:
                with psycopg.connect(
                    host="127.0.0.1",
                    port=5432,
                    dbname=os.environ["DB_NAME"],
                    user=os.environ["DB_USER"],
                    password=os.environ["DB_PASSWORD"],
                    connect_timeout=5,
                ) as conn:
                    with conn.cursor() as cur:
                        cur.execute("SELECT current_database()")
                        database = cur.fetchone()[0]
                status = 200
                body = f"Database connected: {database}\n".encode()
            except Exception:
                status = 503
                body = b"Database connection failed\n"
        else:
            status = 200
            body = b"Hello from Kubernetes!\n"

        self.send_response(status)
        self.send_header("Content-Type", "text/plain")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


HTTPServer(("0.0.0.0", 8080), Handler).serve_forever()
