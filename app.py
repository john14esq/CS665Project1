from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

def get_db():
    conn = sqlite3.connect('CS665Project.db')  #Using database CS665Project.db
    return conn

@app.route('/reports')
def reports():
    return render_template('reports.html')

@app.route('/report/attendees-per-event')
def attendees_per_event():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT e.title, COUNT(r.rsvp_id) AS attendee_count
        FROM Events e
        LEFT JOIN RSVPs r ON e.event_id = r.event_id
        GROUP BY e.title
        ORDER BY attendee_count DESC
    """)
    data = cur.fetchall()
    conn.close()
    return render_template('report_result.html', title="Attendees per Event", data=data, headers=["Event Title", "Attendee Count"])

@app.route('/report/events-with-venue')
def events_with_venue():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT e.title, v.name AS venue_name, e.date_time
        FROM Events e
        JOIN Venues v ON e.venue_id = v.venue_id
    """)
    data = cur.fetchall()
    conn.close()
    return render_template('report_result.html', title="Events with Venue", data=data, headers=["Event Title", "Venue", "Date"])

@app.route('/report/most-attended')
def most_attended():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT e.title, COUNT(r.rsvp_id) AS total_attendees
        FROM Events e
        JOIN RSVPs r ON e.event_id = r.event_id
        GROUP BY e.title
        ORDER BY total_attendees DESC
        LIMIT 1
    """)
    data = cur.fetchall()
    conn.close()
    return render_template('report_result.html', title="Most Attended Event", data=data, headers=["Event Title", "Attendees"])

@app.route('/report/events-multiple-attendees')
def events_multiple_attendees():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT e.title, COUNT(r.rsvp_id) AS total_rsvps
        FROM Events e
        JOIN RSVPs r ON e.event_id = r.event_id
        GROUP BY e.event_id, e.title
        HAVING COUNT(r.rsvp_id) > 1
    """)
    data = cur.fetchall()
    conn.close()
    return render_template('report_result.html', title="Events with Multiple RSVPs", data=data, headers=["Event Title", "RSVP Count"])

if __name__ == "__main__":
    app.run(debug=True)
