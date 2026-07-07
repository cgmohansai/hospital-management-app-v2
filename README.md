# Hospital Management App v2

A Vue 3 + Flask hospital management application with patient, doctor, and appointment workflows.

## Frontend deployment on Vercel

1. Import the project into Vercel.
2. Set the project root to the frontend folder.
3. Use these build settings:
   - Build Command: `npm run build`
   - Output Directory: `dist`
4. Add this environment variable in Vercel:
   - `VITE_API_BASE_URL=https://your-backend-url/api`

## Backend deployment note

The Flask API is not suited for Vercel hosting as-is. Deploy the backend separately (for example on Render, Railway, or Fly.io) and point the frontend to that public URL with `VITE_API_BASE_URL`.

## Local development

- Frontend: `cd frontend && npm install && npm run dev`
- Backend: `cd backend && python3 -m pip install -r req.txt && python3 app.py`
