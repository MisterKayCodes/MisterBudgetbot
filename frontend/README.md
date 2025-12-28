# Mister Budget - React Frontend

Modern React web interface for Mister Budget application.

## Setup

1. Install dependencies:
```bash
npm install
```

2. Configure environment:
```bash
cp .env.example .env
```

Edit `.env` and set:
```
VITE_API_BASE_URL=http://localhost:8000/api
```

3. Start development server:
```bash
npm run dev
```

The app will be available at http://localhost:3000

## Features

- User authentication (login/register)
- Dashboard with financial overview
- Income management
- Expense tracking
- Goals management
- Financial reports and summaries
- Settings and customization
- Financial advisor insights

## Project Structure

```
src/
├── components/        # Reusable components
├── pages/            # Page components
├── services/         # API client
├── utils/            # Utility functions
├── context/          # React context
├── styles/           # CSS files
├── App.jsx          # Main app component
└── main.jsx         # Entry point
```

## Building for Production

```bash
npm run build
```

The build output will be in the `dist/` directory.

## Technologies

- React 19
- Vite
- React Router
- Axios
- CSS

## Note

Make sure the FastAPI backend is running before starting the frontend.
