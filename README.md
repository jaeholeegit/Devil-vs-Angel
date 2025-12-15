# Angel vs Devil - Sentiment Analysis App

A full-stack web application that visualizes the collective sentiment of user comments as a battle between "Angel Power" (Positive) and "Devil Power" (Negative).

## Features
- **Sentiment Analysis**: Uses AI (TextBlob) to analyze the sentiment polarity of comments.
- **Real-time Dashboard**: Visualizes the balance of power between positive and negative sentiments.
- **Comment System**: Users can post comments (max 300 characters).
- **Recent Activity**: Displays a list of recent comments with their sentiment classifications.

## Tech Stack
- **Backend**: Flask (Python)
- **Database**: 
  - SQLite (Default for local development)
  - MySQL (Supported via configuration)
- **Frontend**: React (Vite) + Vanilla CSS
- **AI/ML**: TextBlob (Natural Language Processing)

## Getting Started

### Prerequisites
- Python 3.8+
- Node.js & npm

### Backend Setup
1. Navigate to the backend directory:
   ```bash
   cd backend
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the server:
   ```bash
   python app.py
   ```
   The backend runs on `http://localhost:5000`.

### Frontend Setup
1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Run the development server:
   ```bash
   npm run dev
   ```
   The application will look for the backend at `http://localhost:5000`.

## Configuration
The database connection can be configured in `backend/.env`. By default, it uses a local SQLite database for ease of setup. To use MySQL, update the `DATABASE_URL` variable.

## License
MIT
