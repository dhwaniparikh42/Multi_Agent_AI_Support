# Core Concepts Used in This Project

A high-level overview of every major concept used across the frontend and backend.
Each entry explains what the concept is and how it is used in this specific project.

---

## Backend Concepts

### Web Framework
- **FastAPI** — a tool that lets you build APIs in Python; this project uses it to create all the routes that the frontend talks to.

### API Design
- **REST API** — a standard way of designing URLs so each URL does one clear thing (create user, send message, delete session); this project follows this pattern across all its routes.
- **Route / Endpoint** — a specific URL + action pair (e.g. POST /auth/register); every feature in this project has its own dedicated route.
- **HTTP Methods** — verbs that describe what you want to do: GET = fetch data, POST = create/send data, DELETE = remove data; used throughout the routers.
- **HTTP Status Codes** — numbers that tell the client what happened: 200 = ok, 201 = created, 401 = not logged in, 404 = not found, 409 = conflict; every route in this project returns the appropriate code.

### Data Validation
- **Pydantic Model** — a blueprint that defines exactly what data must look like; used here to validate every request coming in (e.g. RegisterRequest) and to control what goes out in responses (e.g. UserOut).
- **Request Body** — the data a client sends along with a POST request; validated automatically by Pydantic before your code runs.
- **Response Model** — filters what data gets sent back to the client, preventing accidental exposure of sensitive fields like passwords.

### Authentication & Security
- **JWT (JSON Web Token)** — a compact, signed string that proves who you are without the server storing sessions; issued on login and sent with every request in this project.
- **Bearer Token** — the format for sending the JWT in request headers (`Authorization: Bearer <token>`); all protected routes in this project require this.
- **Password Hashing** — converts plain passwords into scrambled strings before storing them; used in this project so raw passwords are never saved to the database.
- **Protected Route** — a route that requires a valid JWT to access; most chat and session routes in this project are protected.

### Dependency Injection
- **Depends** — FastAPI's way of automatically running helper functions before your route runs; used here to open a database connection and verify the logged-in user on every protected request.

### Database
- **SQLAlchemy** — a Python library for talking to databases without writing raw SQL; used here to save and fetch users, sessions, and messages.
- **ORM (Object Relational Mapper)** — lets you work with database rows as Python objects instead of SQL queries; the User, ChatSession, and Message classes in this project are ORM models.
- **Database Model** — a class that maps to a database table; this project has three: User, ChatSession, and Message.
- **Migration / Table Creation** — the step that creates database tables from model definitions; runs automatically on every server startup in this project.
- **SQLite** — a lightweight database stored as a single file (`support.db`); used here as the database for the whole project.

### Application Structure
- **Router** — a way to group related routes into separate files; this project splits routes into `auth_router.py` and `chat_router.py` to keep code organized.
- **Middleware** — code that runs on every single request before it reaches your route; used here for CORS (cross-origin) checking.
- **CORS** — a browser security rule that blocks requests from different origins; the middleware in this project allows the frontend (different port) to call the backend.
- **Environment Variables (.env)** — a file that stores secret settings like API keys and database URLs outside of the code; this project uses it for the OpenAI key, JWT secret, and database path.

### Error Handling
- **HTTPException** — a way to stop a request early and send an error back to the client; used throughout this project for cases like wrong password, duplicate email, or session not found.

---

## AI / Multi-Agent Concepts

- **Multi-Agent System** — a design where different AI "specialists" handle different topics; this project routes each user message to one of six agents: Billing, Technical, Product, Complaint, FAQ, or General.
- **Intent Detection** — figuring out what the user is asking about by scanning for keywords; used here to decide which agent should respond before calling the AI.
- **System Prompt** — instructions given to the AI before the conversation starts to define its personality and role; each agent in this project has its own system prompt.
- **Conversation History** — the last several messages sent to the AI so it remembers context; this project sends the last 6 messages with every new request to OpenAI.
- **OpenAI API** — the external service that generates AI replies; called inside `intent.py` after the agent type is determined.

---

## Frontend Concepts

### UI Framework
- **React** — a JavaScript library for building user interfaces out of reusable pieces; the entire frontend of this project is built with React.
- **Component** — a self-contained, reusable piece of UI; this project has components for the chat window, message bubbles, login form, and conversation history sidebar.
- **JSX** — a syntax that lets you write HTML-like code inside JavaScript; used in every component file (`.jsx`) in this project.

### State & Data Flow
- **State (useState)** — data that, when changed, causes the UI to update automatically; used here to track messages, loading status, form inputs, and the active session.
- **Effect (useEffect)** — code that runs automatically when the component loads or when specific data changes; used here to fetch messages and sessions when the user opens a chat.
- **Context API** — a way to share data (like the logged-in user) across all components without passing it manually; used here in `AuthContext` to make the current user and login/logout functions available everywhere.
- **useRef** — a way to directly access a DOM element; used here to auto-scroll to the latest message and to keep focus on the text input after sending.

### Navigation
- **React Router** — handles switching between pages in a single-page app without reloading the browser; used here to navigate between the login page and the chat page.
- **Protected Route** — a route that redirects you to login if you are not authenticated; the chat page in this project uses this so only logged-in users can access it.

### API Communication
- **Axios** — a JavaScript library for making HTTP requests to the backend; used in `api.js` to call all backend routes.
- **Interceptor** — code that automatically runs on every request or response; used here to attach the JWT token to every outgoing request, and to redirect to login if a 401 is received.
- **async / await** — a way to write code that waits for a response without freezing the browser; used in every function that calls the backend API.

### Browser Storage
- **localStorage** — the browser's built-in key-value storage that persists across page refreshes; used here to save the JWT token so users stay logged in after closing the tab.

### Styling
- **Tailwind CSS** — a utility-based styling library where you apply styles directly as class names in HTML/JSX; used throughout this project for all layout, colors, spacing, and responsive design.
