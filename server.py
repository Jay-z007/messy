# -*- coding: utf-8 -*-
"""Local web server for the student marks report."""

from http.server import BaseHTTPRequestHandler, HTTPServer

from messy import MARKS, STUDENTS, process_class

HOST = "127.0.0.1"
PORT = 8000


def build_html(report):
    """Return an HTML page for the class report."""
    rows_html = ""
    for row in report["rows"]:
        result_class = row["result"].lower()
        rows_html += (
            "<tr>"
            f"<td>{row['name']}</td>"
            f"<td>{row['marks']}</td>"
            f"<td>{row['grade']}</td>"
            f"<td class='{result_class}'>{row['result']}</td>"
            f"<td>{row['message']}</td>"
            "</tr>"
        )

    students_status = "Students found" if report["students_found"] else "No students found"
    processing_status = (
        "Processing completed" if report["total_students"] > 0 else "No students found"
    )

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Student Marks Processor</title>
  <style>
    body {{ font-family: Arial, sans-serif; margin: 40px; background: #f4f6f8; color: #1f2933; }}
    h1 {{ margin-bottom: 8px; }}
    .summary {{ display: flex; gap: 16px; flex-wrap: wrap; margin: 24px 0; }}
    .card {{ background: white; padding: 16px 20px; border-radius: 8px; min-width: 160px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.08); }}
    .card span {{ display: block; color: #52606d; font-size: 13px; }}
    .card strong {{ font-size: 22px; }}
    table {{ width: 100%; border-collapse: collapse; background: white;
             box-shadow: 0 1px 3px rgba(0,0,0,0.08); }}
    th, td {{ text-align: left; padding: 12px 14px; border-bottom: 1px solid #e4e7eb; }}
    th {{ background: #243b53; color: white; }}
    .pass {{ color: #14804a; font-weight: bold; }}
    .fail {{ color: #c53030; font-weight: bold; }}
    .invalid {{ color: #b7791f; font-weight: bold; }}
    .footer {{ margin-top: 16px; color: #52606d; }}
  </style>
</head>
<body>
  <h1>Student Marks Processor</h1>
  <p>Local report for the class list in messy.py</p>
  <div class="summary">
    <div class="card"><span>Average marks</span><strong>{report['average']}</strong></div>
    <div class="card"><span>Above average</span><strong>{report['above_average_count']}</strong></div>
    <div class="card"><span>Total students</span><strong>{report['total_students']}</strong></div>
    <div class="card"><span>Total marks</span><strong>{report['total_marks']}</strong></div>
  </div>
  <table>
    <thead>
      <tr><th>Name</th><th>Marks</th><th>Grade</th><th>Result</th><th>Message</th></tr>
    </thead>
    <tbody>
      {rows_html}
    </tbody>
  </table>
  <p class="footer">{students_status} · {processing_status}</p>
</body>
</html>
"""


class ReportHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        """Serve the class report page."""
        report = process_class(STUDENTS, MARKS)
        page = build_html(report).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(page)))
        self.end_headers()
        self.wfile.write(page)


def main():
    """Start the local report server."""
    server = HTTPServer((HOST, PORT), ReportHandler)
    print(f"Serving student report at http://{HOST}:{PORT}")
    server.serve_forever()


if __name__ == "__main__":
    main()
