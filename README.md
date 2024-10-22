# Project Overview
This project is an event logging system built with Flask for the backend API and a React-based frontend. The system allows users to log and retrieve event data, which is stored in an SQLite database.

## Project Setup

### Running in GitHub Codespaces
If you are using GitHub Codespaces, the environment is preconfigured, so no manual setup is required. Simply open the repository in Codespaces and follow the steps in the Running the Application section.

### Local Setup
To run this project locally, follow these steps:

1. **Clone the repository:**
   - Clone the `RestfulAPI` branch of the repository:
   ```bash
   git clone --branch RestfulAPI https://github.com/folukeOpenuni/AlchemTechChallenge.git
   ```
   > **Note:** Do not clone the `master` branch, as it's not fully functional.

   - Navigate to the repository folder:
   ```bash
   cd AlchemTechChallenge/
   ```

2. **Backend Setup:**

   - Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

   - Set up the database (SQLite is required):
   ```bash
   python api/app.py
   ```
   This will auto-generate the SQLite database file (`event_log.db`).

3. **Frontend Setup (React):**

   - Install Node.js dependencies:
   ```bash
   cd event-management-console
   npm install
   ```

   - Start the frontend:
   ```bash
   npm start
   ```
   The frontend will run on `http://localhost:3000` by default.

### Running the Application in GitHub Codespaces:
   - The Flask API runs on port `5000` and the React frontend on port `3000`.
   - Open the Codespaces **Ports** tab and make the frontend port `3000` public. You can use the generated link to access the frontend.
   - The API should be accessible on port `5000`.

   > **Tip:** When you run the code, a pop-up will appear. You can click **Make public** for the desired port to expose the application.

## API Endpoints
Here are the main API endpoints available:

1. **Create Event (POST):**
   - **Endpoint:** `/event`
   - **Method:** `POST`
   - **Request Body:**
     ```json
     {
       "event_type": "ERROR",
       "event_status": "OPEN",
       "priority": "HIGH",
       "category": "SYSTEM"
     }
     ```
   - **Response:**
     ```json
     {
       "message": "Event created successfully",
       "event_id": 1
     }
     ```

2. **Retrieve Events (GET):**
   - **Endpoint:** `/events`
   - **Method:** `GET`
   - **Response Example:**
     ```json
       {
         "event_id": 1,
         "event_type": "ERROR",
         "event_status": "OPEN",
         "priority": "HIGH",
         "category": "SYSTEM",
         "event_datetime": "2024-10-21 22:45:12"
       },
     ```

## Testing
You can run tests using Playwright for frontend testing or use Flask's built-in unit tests for backend testing.

### Playwright Tests (Frontend):
To run Playwright tests:
```bash
npx playwright test tests/
```

> **Note:** Running Playwright in Codespaces may have issues with headless or XServer configurations. Ensure the tests are running headless by modifying the `playwright.config.js` file.

### Unit Tests (Backend):
You can run the Flask backend tests with:
```bash
python -m unittest api/test_app.py
```

## Simulating Events
The application can automatically generate random events every 2 minutes.

- This logic is controlled using the `time.sleep()` function in `app.py`. You can adjust the interval by changing the `sleep` duration if required.

## Known Issues
- **Playwright Tests:** Currently, there are some issues running Playwright E2E tests in GitHub Codespaces due to environment constraints.
- **Master Branch:** The `master` branch is not fully functional; please clone the `RestfulAPI` branch for the working version.

## Future Improvements
- Improve test coverage and resolve issues with Playwright tests.
- Add more detailed error handling to make the API more robust.
- Add user authentication for secured API access.

