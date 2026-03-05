# Poet Name Configuration

All references to "Lev Gorev" have been extracted into an environment variable `POET_NAME` for easy customization.

## How to Configure

### 1. Set the Poet Name in `.env`

Add or update this line in your `.env` file:

```env
POET_NAME=Your Poet Name Here
```

**Default value:** "Famous poet" (as specified in `.env.example`)

### 2. Apply the Changes

If running with Docker:
```bash
docker compose restart backend
docker compose restart nginx
```

If running locally:
```bash
# Restart your FastAPI server
```

The frontend will automatically fetch the poet name from the `/api/config` endpoint.

## What Was Changed

### Backend Changes

1. **`.env.example`** - Added `POET_NAME=Famous poet`
2. **`.env`** - Added `POET_NAME=Lev Gorev` (you can change this)
3. **`backend/.env`** - Added `POET_NAME=Lev Gorev`
4. **`backend/main.py`** - Added `/api/config` endpoint that returns the poet name
5. **`backend/database.py`** - Uses `POET_NAME` env var for default About page
6. **`backend/models.py`** - Updated default value to "Famous poet"

### Frontend Changes

1. **`frontend/static/js/app.js`**:
   - Added `POET_NAME` global variable
   - Added `loadConfig()` function to fetch poet name from API
   - Updated `t()` function to automatically replace `{poet}` placeholder
   - Replaced all hardcoded "Lev Gorev" with `{poet}` placeholder in all language translations (en, ru, es, fr)

2. **`frontend/templates/index.html`** - Replaced hardcoded name with "Famous poet"
3. **`frontend/static/manifest.json`** - Replaced hardcoded name with "Famous poet"

### Documentation & Configuration

1. **`README.md`** - Replaced "levgorev.com" with "yourdomain.com" in deployment examples
2. **`nginx/default-https.conf`** - Replaced "levgorev.com" with "yourdomain.com"
3. **`documentation/ADD_NEW_LANGUAGE.md`** - Used `{POET_NAME}` placeholder
4. **`documentation/TESTING_GUIDE.md`** - Replaced with "Famous poet"

## How It Works

1. Backend loads `POET_NAME` from environment variable
2. Frontend fetches the poet name via `/api/config` endpoint on page load
3. All translations use `{poet}` placeholder which is automatically replaced
4. The poet name appears in:
   - Page title: `{poet} — Poetry`
   - Hero subtitle: `A collection of verses by {poet}`
   - Meta descriptions
   - PWA manifest

## Example Usage

To change the poet name to "Alexander Pushkin":

```env
POET_NAME=Alexander Pushkin
```

After restarting the services, the site will display:
- **Title:** "Alexander Pushkin — Poetry"
- **Subtitle:** "A collection of verses by Alexander Pushkin"

## API Endpoint

**GET** `/api/config`

Returns:
```json
{
  "poet_name": "Lev Gorev"
}
```

This endpoint is public and doesn't require authentication.

