CREATE TABLE IF NOT EXISTS record (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  "uuid" TEXT NOT NULL UNIQUE,
  "title_before" TEXT,
  "first_name" TEXT NOT NULL,
  "middle_name" TEXT,
  "last_name" TEXT NOT NULL,
  "title_after" TEXT,
  "picture_url" TEXT,
  "location" TEXT,
  "claim" TEXT,
  "bio" TEXT,
  "tags" TEXT,
  "price_per_hour" INTEGER,
  "contact" TEXT NOT NULL
);
-- CREATE TABLE "lecturers" (
--   "uuid"  TEXT NOT NULL UNIQUE
-- );


-- {
-- "uuid": "67fda282-2bca-41ef-9caf-039cc5c8dd69",
--   "title_before": "Mgr.",
--   "first_name": "Petra",
--   "middle_name": "Swil",
--   "last_name": "Plachá",
--   "title_after": "MBA",
--   "picture_url": "https://picsum.photos/200",
--   "location": "Brno",
--   "claim": "Bez dobré prezentace je i nejlepší myšlenka k ničemu.",
--   "bio": "<b>Formátovaný text</b> s <i>bezpečnými</i> tagy.",
--   "tags": [
--     {
--       "uuid": "c20b98dd-f37e-4fa7-aac1-73300abf086e",
--       "name": "Marketing"
--     }
--   ],
--   "price_per_hour": 720,
--   "contact": {
--     "telephone_numbers": [
--       "+123 777 338 111"
--     ],
--     "emails": [
--       "user@example.com"
--     ]
--   }
-- }
