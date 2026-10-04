"""
Vercel Python Serverless Entry Point
Wraps the Streamlit app with a FastAPI/WSGI proxy.
Since Streamlit is a long-running server and Vercel is serverless,
this serves a redirect page to the Streamlit Community Cloud deployment
while also exposing a /health API endpoint.

For full Streamlit hosting, deploy to:
  https://share.streamlit.io
"""
from http.server import BaseHTTPRequestHandler
import json
import os

STREAMLIT_URL = os.environ.get(
    "STREAMLIT_APP_URL",
    "https://skill-gap-ai.streamlit.app"
)


class handler(BaseHTTPRequestHandler):
    """Vercel serverless handler."""

    def do_GET(self):
        if self.path == "/health" or self.path == "/api/health":
            self._send_json(200, {
                "status": "ok",
                "service": "Skill-Gap AI Platform",
                "streamlit_url": STREAMLIT_URL
            })
        elif self.path == "/api/info":
            self._send_json(200, {
                "app": "Skill-Gap Aware Employability Assessment Platform",
                "version": "1.0.0",
                "framework": "Streamlit",
                "language": "Python 3.11",
                "features": [
                    "Resume Analysis",
                    "Skill Gap Detection",
                    "Job Role Matching",
                    "AI Career Mentor",
                    "Learning Roadmap"
                ],
                "deployment": {
                    "vercel": "proxy/redirect",
                    "primary": STREAMLIT_URL
                }
            })
        else:
            # Redirect all other traffic to Streamlit Community Cloud
            self._send_redirect(STREAMLIT_URL)

    def do_POST(self):
        self._send_json(405, {"error": "Use the Streamlit app directly at: " + STREAMLIT_URL})

    def _send_json(self, code, data):
        body = json.dumps(data, indent=2).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("X-Frame-Options", "DENY")
        self.send_header("X-XSS-Protection", "1; mode=block")
        self.end_headers()
        self.wfile.write(body)

    def _send_redirect(self, url):
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta http-equiv="refresh" content="0; url={url}">
  <title>Skill-Gap AI Platform</title>
  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{
      background: linear-gradient(135deg, #020617 0%, #071127 45%, #0f172a 100%);
      min-height: 100vh;
      display: flex;
      align-items: center;
      justify-content: center;
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
      color: white;
    }}
    .container {{
      text-align: center;
      padding: 40px;
    }}
    h1 {{
      font-size: 2.5rem;
      font-weight: 900;
      background: linear-gradient(90deg, #22d3ee, #60a5fa, #8b5cf6);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      margin-bottom: 16px;
    }}
    p {{ color: #cbd5e1; margin-bottom: 24px; font-size: 1.1rem; }}
    a {{
      display: inline-block;
      padding: 14px 32px;
      border-radius: 16px;
      background: linear-gradient(90deg, #06b6d4, #3b82f6, #8b5cf6);
      color: white;
      text-decoration: none;
      font-weight: 700;
      font-size: 1rem;
      transition: transform 0.2s, box-shadow 0.2s;
    }}
    a:hover {{ transform: translateY(-2px); box-shadow: 0 0 30px rgba(34,211,238,0.4); }}
    .loader {{
      width: 40px; height: 40px;
      border: 3px solid rgba(34,211,238,0.3);
      border-top-color: #22d3ee;
      border-radius: 50%;
      animation: spin 0.8s linear infinite;
      margin: 20px auto;
    }}
    @keyframes spin {{ to {{ transform: rotate(360deg); }} }}
  </style>
</head>
<body>
  <div class="container">
    <h1>⚡ Skill-Gap AI Platform</h1>
    <p>Redirecting you to the application...</p>
    <div class="loader"></div>
    <a href="{url}">Open App →</a>
  </div>
</body>
</html>"""
        body = html.encode("utf-8")
        self.send_response(302)
        self.send_header("Location", url)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format, *args):
        pass  # Suppress default logging
