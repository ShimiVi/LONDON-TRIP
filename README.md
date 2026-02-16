# 🇬🇧 London Trip Planner

אפליקציית ווב אישית לטיול בלונדון — מובייל פירסט.

## מה יש כאן

- 📍 **מקומות** — מסעדות, מוזיאונים, מסיבות, תחבורה, חובה לראות
- 💷 **כסף** — מעקב הוצאות לפי קטגוריה ומטבע
- 📝 **הערות** — זכרונות וטיפים מהדרך
- 🏠 **בית** — סטטיסטיקות + קישורים שימושיים (TfL, Citymapper, המרת מטבע)

## הפעלה מקומית

```bash
# 1. התקנת תלויות
pip install flask

# 2. הפעלת השרת
python app.py

# 3. פתיחה בדפדפן
# http://localhost:5000
```

## מבנה הפרויקט

```
london-trip/
├── app.py              ← Flask server + כל ה-API routes
├── requirements.txt    ← תלויות Python
├── data/
│   └── trips.json      ← נוצר אוטומטית, כאן נשמרים הנתונים
└── templates/
    └── index.html      ← כל הפרונט (HTML + CSS + JS)
```

## API Routes

| Method | Route | מה עושה |
|--------|-------|---------|
| GET | `/api/places` | כל המקומות (או `?category=museum`) |
| POST | `/api/places` | הוספת מקום |
| PATCH | `/api/places/<id>` | עדכון מקום (למשל סימון כ"ביקרתי") |
| DELETE | `/api/places/<id>` | מחיקת מקום |
| GET | `/api/expenses` | כל ההוצאות |
| POST | `/api/expenses` | הוספת הוצאה |
| DELETE | `/api/expenses/<id>` | מחיקת הוצאה |
| GET | `/api/notes` | כל ההערות |
| POST | `/api/notes` | הוספת הערה |
| DELETE | `/api/notes/<id>` | מחיקת הערה |
| GET | `/api/stats` | סטטיסטיקות כלליות |

## להשתמש מהטלפון בטיול

**אפשרות א׳ — דרך הרשת הביתית:**
1. הרץ את השרת על המחשב שלך
2. מצא את ה-IP של המחשב (`ipconfig` / `ifconfig`)
3. כנס מהטלפון ל-`http://192.168.x.x:5000`
4. הוסף למסך הבית (Add to Home Screen)

**אפשרות ב׳ — העלאה לענן (מומלץ לטיול):**
- [Railway.app](https://railway.app) — חינמי, פשוט
- [Render.com](https://render.com) — חינמי, פשוט

## שלבים הבאים ללמידה

- [ ] הוסף SQLite במקום JSON (תלמד `sqlite3` ב-Python)
- [ ] הוסף API של מזג אוויר (OpenWeatherMap)
- [ ] הוסף ממיר מטבע אמיתי (ExchangeRate-API)
- [ ] הוסף אימות משתמש פשוט
- [ ] העלה ל-Railway או Render
