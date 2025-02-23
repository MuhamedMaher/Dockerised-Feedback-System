import time
import redis
import json
import psycopg2
import os

redis_client = redis.Redis(host="redis", port=6379, db=0)
pubsub = redis_client.pubsub()
pubsub.subscribe("feedback")

DB_PASSWORD = os.environ.get("POSTGRES_PASSWORD", "password")

def connect_to_db():
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
            print("Waiting for database...")
            time.sleep(2)
    raise Exception("Could not connect to the database")

def process_feedback(feedback):
    conn = connect_to_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO feedback (product_id, choice) VALUES (%s, %s)",
                (feedback["product_id"], feedback["choice"]))
    conn.commit()
    conn.close()

for message in pubsub.listen():
    if message["type"] == "message":
        feedback = json.loads(message["data"])
        process_feedback(feedback)
        print("Processed feedback:", feedback)

