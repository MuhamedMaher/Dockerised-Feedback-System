from flask import Flask, jsonify, request, render_template
import redis
import json
import psycopg2
import os
import time

app = Flask(__name__)

# Connect to Redis (using the service name "redis")
redis_client = redis.Redis(host="redis", port=6379, db=0)

# Get DB password from environment (default to "password")
DB_PASSWORD = os.environ.get("POSTGRES_PASSWORD", "password")

def get_db_connection():
    for i in range(10):
        try:
            conn = psycopg2.connect(
                dbname="feedbackdb",
                user="postgres",
                password=DB_PASSWORD,
                host="db"
            )
            return conn
        except psycopg2.OperationalError:
            print(f"Database connection failed, retrying in 2 seconds... ({i+1}/10)")
            time.sleep(2)
    raise Exception("Could not connect to the database")

def create_feedback_table():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS feedback (
            id SERIAL PRIMARY KEY,
            product_id INT NOT NULL,
            choice VARCHAR(50) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    conn.commit()
    conn.close()

# API endpoint: Submit feedback
@app.route("/api/feedback", methods=["POST"])
def submit_feedback():
    feedback = request.json
    redis_client.publish("feedback", json.dumps(feedback))
    return jsonify(feedback), 200

# API endpoint: Get aggregated feedback results
@app.route("/api/results", methods=["GET"])
def get_results():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT product_id, choice, COUNT(*) FROM feedback GROUP BY product_id, choice")
    results = cur.fetchall()
    conn.close()

    feedback_results = {}
    for product_id, choice, count in results:
        if product_id not in feedback_results:
            feedback_results[product_id] = {}
        feedback_results[product_id][choice] = count

    return jsonify(feedback_results), 200

# Serve the Feedback Form Page
@app.route("/feedback", methods=["GET"])
def feedback_page():
    return render_template("feedback.html")

# Serve the Results Page
@app.route("/results", methods=["GET"])
def results_page():
    return render_template("results.html")

if __name__ == "__main__":
    create_feedback_table()
    app.run(host="0.0.0.0", port=5000, debug=True)

