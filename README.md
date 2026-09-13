# LIFE RPG

Turn your real-world activities into epic quests, earn XP, and level up your life! 

## Features
- **Character System**: Choose a class, earn XP, and level up.
- **Quest System**: Complete real-life tasks categorized by attributes (Strength, Intellect, etc.).
- **Progression Engine**: Non-linear level scaling.
- **Streak System**: Maintain daily activity to increase your streak.
- **Achievements**: Unlock milestones and badges.
- **Shop & Inventory**: Spend Gold on virtual items, titles, and themes.
- **Analytics**: Visualize your real-world growth over time.
- **Responsive UI**: "Dark Fantasy × Futuristic RPG" aesthetics.

## Technology Stack
- **Backend**: Python 3.12+, Django 5+, Django REST Framework
- **Database**: PostgreSQL (Development on SQLite default fallback)
- **Frontend**: Django Templates, Vanilla HTML/CSS/JS, Fetch API, Chart.js

## Local Installation

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\Activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Environment Variables:
   Copy `.env.example` to `.env` and fill in your details (Database URL, Secret Key, etc.).

4. Run migrations:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. Seed game data and create a demo user:
   ```bash
   python manage.py seed_game_data
   python manage.py create_demo_data
   ```
   *Demo credentials: `demo_hero` / `password123`*

6. Run the server:
   ```bash
   python manage.py runserver
   ```

## API Documentation
- `POST /api/auth/login/` - JWT Login (if integrating a separate frontend)
- `GET /api/quests/` - List user quests
- `POST /api/quests/` - Create a quest
- `POST /api/quests/<id>/complete/` - Complete quest and trigger reward engine
- `GET /api/shop/` - View available items
- `POST /api/shop/<id>/purchase/` - Buy item with Gold

🔗 Project Links
Django: https://www.djangoproject.com/
Django REST Framework: https://www.django-rest-framework.org/
PostgreSQL: https://www.postgresql.org/
Python: https://www.python.org/
Chart.js: https://www.chartjs.org/
📚 References
Django Documentation — https://docs.djangoproject.com/
Django Authentication — https://docs.djangoproject.com/en/stable/topics/auth/
Django Models & ORM — https://docs.djangoproject.com/en/stable/topics/db/models/
Django Security — https://docs.djangoproject.com/en/stable/topics/security/
Django REST Framework Documentation — https://www.django-rest-framework.org/
PostgreSQL Documentation — https://www.postgresql.org/docs/
MDN Web Docs — https://developer.mozilla.org/
OWASP Web Security — https://owasp.org/www-project-top-ten/
Chart.js Documentation — https://www.chartjs.org/docs/
🎮 Gamification References
Octalysis Framework — https://yukaichou.com/gamification-examples/octalysis-complete-gamification-framework/
Self-Determination Theory — https://selfdeterminationtheory.org/
Habit formation research — https://jamesclear.com/habit-guide/

## Testing
Run the test suite:
```bash
python manage.py test
```

## Security
- All endpoints protected by `IsAuthenticated` (except auth registration).
- Object-level permissions enforced (Users can only complete their own quests).
- Atomic transactions prevent duplicate rewards and race conditions.

---
Built as a master full-stack demonstration.
