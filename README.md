# Dockerized Feedback System

A containerized product feedback system that allows users to submit feedback for products and view aggregated results. This project uses Flask for the backend, Redis for messaging, and PostgreSQL for persistent storage. The entire stack is orchestrated with Docker and Docker Compose.

![image](https://github.com/user-attachments/assets/955ed20c-f927-4d17-b04b-fec9a5e72d62)

## Features

- **Submit Feedback:** Users can submit feedback (e.g., Bad, Good, Great) for products.
- **View Results:** Aggregated feedback results are displayed in real time.
- **API Endpoints:** Exposes RESTful API endpoints for feedback submission and result retrieval.
- **Worker Process:** A background worker listens for feedback events via Redis and writes them to PostgreSQL.
- **Dockerised:** All services are containerized for easy deployment and scalability.

## Technologies Used

- **Backend:** Python, Flask
- **Database:** PostgreSQL
- **Caching & Messaging:** Redis
- **Frontend:** HTML, CSS, JavaScript, Bootstrap
- **Containerization:** Docker, Docker Compose

## Getting Started

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

### Setup

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/YourUsername/Dockerized-Feedback-System.git
   cd product-feedback-system
   
2. **Set Up the Database Password:**

   Ensure that the .env file contains your PostgreSQL password. 

3. **Build and Start All Services:**
   ```bash
   docker-compose up -d --build

4. To access the feedback:
   
   ```bash
   http://localhost:5000/api/feedback

5. to access the Results:
   ```bash
   curl http://localhost:5000/api/results
