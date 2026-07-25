"""CSV export builder used by admin reports (patients, doctors, appointments, revenue, etc.)."""

import csv
import io


def build_csv(headers, rows):
    """
    headers: list[str]
    rows: iterable of iterables (already stringified/formatted values)

    Returns a UTF-8 encoded CSV string, ready to hand to a Flask Response.
    """
    buffer = io.StringIO()
    writer = csv.writer(buffer)
    writer.writerow(headers)
    writer.writerows(rows)
    return buffer.getvalue()


def csv_response(filename, headers, rows):
    """Convenience helper returning a Flask Response with proper CSV headers."""
    from flask import Response

    csv_data = build_csv(headers, rows)
    return Response(
        csv_data,
        mimetype="text/csv",
        headers={"Content-Disposition": f"attachment; filename={filename}"},
    )
