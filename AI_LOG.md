# AI Collaboration Log

This project was built with the help of two AI bots. I used it as a development assistant throughout the project, mainly for generating boilerplate code, discussing implementation ideas, debugging issues, and improving the frontend. All code was reviewed, tested, and adjusted before being added to the project.

---

## AI Tool Used

* ChatGPT (OpenAI GPT-5.5)
* Google Gemini (Gemini 3.5 Flash)

---

## How I Used AI

I didn't generate the whole project in one prompt. Instead, I built it step by step.

The workflow looked like this:

* Planned the project structure
* Built the FastAPI backend
* Created the database models
* Added the scheduler
* Built the React frontend
* Connected the frontend to the backend
* Added Docker support
* Improved the UI
* Wrote the documentation

Working in smaller steps made debugging much easier.

---

## Example Prompts

### Backend

> Create a FastAPI backend for an uptime monitor where users can register URLs, periodically check them, and store the latest HTTP status code, response time, and timestamp.

### Scheduler

> Update the scheduler so newly added URLs are checked immediately instead of waiting for the next scheduled run.

### Frontend

> Build a React dashboard that lists monitored URLs, their current status, HTTP status code, and response time. Allow users to add new URLs from the interface.

### UI

> Improve the dashboard styling with modern CSS while keeping the existing React components unchanged.

### Docker

> Create Dockerfiles and a docker-compose.yml so the frontend and backend can be started with one command.

---

## Course Corrections

One issue I ran into was that newly added URLs stayed in a **PENDING** state until the scheduler ran again. I updated the implementation so that a health check happens immediately after a URL is added.

Another issue was with websites returning HTTP 403 because of bot protection. Initially these were marked as **DOWN**, but after testing I changed the logic so they are shown as **RESTRICTED**, which better reflects the actual result.

I also spent time refining the frontend layout because some generated CSS didn't produce the spacing and alignment I wanted. I iterated on the styling until the dashboard looked cleaner and more consistent.

---

## Final Thoughts

Using AI helped speed up repetitive work such as creating boilerplate code, generating initial UI components, and debugging individual issues. I still tested each feature manually, adjusted the generated code where needed, and made the final implementation decisions myself.
