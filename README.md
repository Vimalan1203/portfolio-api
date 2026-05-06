# Vimalan Portfolio – FastAPI Backend

A production-ready FastAPI backend that powers all data for the Angular portfolio project.

---

## Project Structure

```
fastapi-portfolio/
├── main.py                        # App entry point
├── requirements.txt
├── .env.example
└── app/
    ├── core/
    │   └── security.py            # JWT token creation & verification
    ├── db/
    │   ├── database.py            # SQLAlchemy engine, session, init_db
    │   └── seed.py                # Initial data (matches Angular hardcoded data)
    ├── models/
    │   └── portfolio_models.py    # ORM models (Project, Skill, Experience, ContactMessage)
    ├── schemas/
    │   └── schemas.py             # Pydantic request/response schemas
    └── routers/
        ├── auth.py                # POST /api/auth/login
        ├── projects.py            # CRUD /api/projects
        ├── skills.py              # CRUD /api/skills
        ├── experiences.py         # CRUD /api/experiences
        └── contact.py             # POST /api/contact (public), GET (admin)
```

---

## Quick Start

### 1. Install dependencies

```bash
cd fastapi-portfolio
python -m venv venv
source venv/bin/activate       # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure environment

```bash
cp .env.example .env
# Edit .env to change SECRET_KEY, ADMIN_USER, ADMIN_PASS
```

### 3. Run the server

```bash
uvicorn main:app --reload --port 8000
```

The API will be live at **http://localhost:8000**  
Swagger UI: **http://localhost:8000/docs**  
ReDoc:       **http://localhost:8000/redoc**

---

## API Endpoints

### Auth
| Method | Endpoint            | Auth     | Description        |
|--------|---------------------|----------|--------------------|
| POST   | `/api/auth/login`   | Public   | Get JWT token      |
| POST   | `/api/auth/logout`  | Public   | No-op placeholder  |

**Login body:**
```json
{ "username": "vimalan", "password": "Admin@2025" }
```
**Response:**
```json
{ "username": "vimalan", "token": "<jwt>", "token_type": "bearer" }
```

---

### Projects
| Method | Endpoint               | Auth     | Description         |
|--------|------------------------|----------|---------------------|
| GET    | `/api/projects/`       | Public   | List all projects   |
| GET    | `/api/projects/{id}`   | Public   | Get single project  |
| POST   | `/api/projects/`       | 🔒 Admin | Create project      |
| PUT    | `/api/projects/{id}`   | 🔒 Admin | Update project      |
| DELETE | `/api/projects/{id}`   | 🔒 Admin | Delete project      |

---

### Skills
| Method | Endpoint             | Auth     | Description      |
|--------|----------------------|----------|------------------|
| GET    | `/api/skills/`       | Public   | List all skills  |
| GET    | `/api/skills/{id}`   | Public   | Get single skill |
| POST   | `/api/skills/`       | 🔒 Admin | Create skill     |
| PUT    | `/api/skills/{id}`   | 🔒 Admin | Update skill     |
| DELETE | `/api/skills/{id}`   | 🔒 Admin | Delete skill     |

---

### Experiences
| Method | Endpoint                  | Auth     | Description          |
|--------|---------------------------|----------|----------------------|
| GET    | `/api/experiences/`       | Public   | List all experiences |
| POST   | `/api/experiences/`       | 🔒 Admin | Add experience       |
| DELETE | `/api/experiences/{id}`   | 🔒 Admin | Delete experience    |

---

### Contact
| Method | Endpoint          | Auth     | Description              |
|--------|-------------------|----------|--------------------------|
| POST   | `/api/contact/`   | Public   | Submit contact message   |
| GET    | `/api/contact/`   | 🔒 Admin | View all messages        |

---

## Integrating with Angular

### Step 1 – Update `environment.ts`

```typescript
// src/environments/environment.ts
export const environment = {
  production: false,
  apiUrl: 'http://localhost:8000/api'
};
```

### Step 2 – Replace `PortfolioDataService`

Replace the in-memory BehaviorSubject implementation with real HTTP calls:

```typescript
// src/app/core/services/portfolio-data.service.ts
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Project, Skill, Experience } from '../models/portfolio.models';
import { environment } from '../../../environments/environment';

@Injectable({ providedIn: 'root' })
export class PortfolioDataService {
  private base = environment.apiUrl;

  constructor(private http: HttpClient) {}

  // Projects
  getProjects(): Observable<Project[]>        { return this.http.get<Project[]>(`${this.base}/projects/`); }
  addProject(p: Project): Observable<Project> { return this.http.post<Project>(`${this.base}/projects/`, p); }
  updateProject(p: Project): Observable<Project> { return this.http.put<Project>(`${this.base}/projects/${p.id}`, p); }
  deleteProject(id: string): Observable<void> { return this.http.delete<void>(`${this.base}/projects/${id}`); }

  // Skills
  getSkills(): Observable<Skill[]>          { return this.http.get<Skill[]>(`${this.base}/skills/`); }
  addSkill(s: Skill): Observable<Skill>     { return this.http.post<Skill>(`${this.base}/skills/`, s); }
  updateSkill(s: Skill): Observable<Skill>  { return this.http.put<Skill>(`${this.base}/skills/${s.id}`, s); }
  deleteSkill(id: string): Observable<void> { return this.http.delete<void>(`${this.base}/skills/${id}`); }

  // Experiences
  getExperiences(): Observable<Experience[]> { return this.http.get<Experience[]>(`${this.base}/experiences/`); }
}
```

### Step 3 – Update `AuthService`

```typescript
// src/app/core/services/auth.service.ts
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { BehaviorSubject, tap } from 'rxjs';
import { Router } from '@angular/router';
import { environment } from '../../../environments/environment';

export interface AuthUser { username: string; token: string; }

@Injectable({ providedIn: 'root' })
export class AuthService {
  private readonly TOKEN_KEY = 'vs_portfolio_token';
  private currentUserSubject = new BehaviorSubject<AuthUser | null>(this.loadUser());
  currentUser$ = this.currentUserSubject.asObservable();

  constructor(private http: HttpClient, private router: Router) {}

  get isLoggedIn() { return !!this.currentUserSubject.value; }
  get currentUser() { return this.currentUserSubject.value; }

  login(username: string, password: string) {
    return this.http.post<AuthUser>(`${environment.apiUrl}/auth/login`, { username, password }).pipe(
      tap(user => {
        localStorage.setItem(this.TOKEN_KEY, JSON.stringify(user));
        this.currentUserSubject.next(user);
      })
    );
  }

  logout() {
    localStorage.removeItem(this.TOKEN_KEY);
    this.currentUserSubject.next(null);
    this.router.navigate(['/']);
  }

  private loadUser(): AuthUser | null {
    try { return JSON.parse(localStorage.getItem(this.TOKEN_KEY) || 'null'); }
    catch { return null; }
  }
}
```

### Step 4 – Update `ContactComponent`

```typescript
submit() {
  if (this.form.invalid) { this.form.markAllAsTouched(); return; }
  this.http.post(`${environment.apiUrl}/contact/`, this.form.value).subscribe({
    next: () => {
      this.submitted = true;
      this.snack.open("Message sent! I'll get back to you soon. 🚀", 'Close', { duration: 4000 });
      this.form.reset();
      setTimeout(() => this.submitted = false, 3000);
    },
    error: () => this.snack.open('Something went wrong. Please try again.', 'Close', { duration: 3000 })
  });
}
```

---

## Database

- Uses **SQLite** by default (`portfolio.db` created automatically on first run)
- To switch to PostgreSQL, change `DATABASE_URL` in `app/db/database.py`:
  ```
  DATABASE_URL = "postgresql://user:password@localhost/portfolio_db"
  pip install psycopg2-binary
  ```

---

## Admin Credentials (default)

| Field    | Value        |
|----------|--------------|
| Username | `vimalan`    |
| Password | `Admin@2025` |

> ⚠️ Change these in your `.env` file before deploying to production.
