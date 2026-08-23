import json
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

from back import answer_question
from rag.db import save_message, get_history


class handler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            query = parse_qs(urlparse(self.path).query)
            visitor_id = query.get("visitor_id", [None])[0]

            if not visitor_id:
                self.send_response(400)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"error": "No visitor_id provided."}).encode())
                return

            history = get_history(visitor_id)

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"history": history}).encode())

        except Exception as error:
            print("ERROR:", error)
            self.send_response(500)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Something went wrong."}).encode())

    def do_POST(self):
        try:
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length)

            data = json.loads(body)
            question = data.get("question")
            visitor_id = data.get("visitor_id")
            name = data.get("name")

            if not question:
                self.send_response(400)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"error": "No question provided."}).encode())
                return

            answer = answer_question(question)
            save_message(visitor_id, name, question, answer)

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"reply": answer}).encode())

        except Exception as error:
            print("ERROR:", error)
            self.send_response(500)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Something went wrong."}).encode())