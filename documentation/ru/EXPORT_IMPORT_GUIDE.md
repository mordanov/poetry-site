# Export/Import Guide for Poetry Site

## Overview
The admin panel now supports exporting and importing poems, as well as exporting comments. This allows you to backup your content or migrate between instances.

## Features

### 1. Export Poems (📥 Export Poems)
- **Access**: Admin Panel → Poems tab
- **Format**: JSON file
- **Filename**: `poems-export-YYYY-MM-DD.json`
- **Content**: All poems with their titles, bodies, tags, and timestamps
- **Use case**: 
  - Backup your entire poetry collection
  - Migrate to another instance
  - Edit poems in bulk offline

### 2. Import Poems (📤 Import Poems)
- **Access**: Admin Panel → Poems tab
- **Format**: JSON file (same format as export)
- **Behavior**: Adds poems to existing collection (does not replace)
- **Validation**: Checks that each poem has a `body` field
- **Error handling**: Reports any failed imports

#### Import File Format
```json
{
  "poems": [
    {
      "title": "Optional Title",
      "body": "Required poem content",
      "tags": ["tag1", "tag2"]
    }
  ]
}
```

**Notes:**
- `body` field is required for each poem
- `title` is optional (defaults to empty string)
- `tags` is optional (defaults to empty array)
- `created_at` and `updated_at` from export are ignored (new timestamps will be generated)

### 3. Export Comments (💬 Export Comments)
- **Access**: Admin Panel → Poems tab
- **Format**: JSON file
- **Filename**: `comments-export-YYYY-MM-DD.json`
- **Content**: All comments with author, body, timestamp, and associated poem info
- **Use case**:
  - Backup reader feedback
  - Analyze engagement
  - Moderate comments offline

## API Endpoints

All endpoints require admin authentication via Bearer token.

### Export Poems
```
GET /api/poems/export/all
Authorization: Bearer <token>
```

Response:
```json
{
  "poems": [...],
  "total": 42,
  "exported_at": "2026-02-21T10:30:00.000000"
}
```

### Import Poems
```
POST /api/poems/import/all
Authorization: Bearer <token>
Content-Type: application/json

{
  "poems": [...]
}
```

Response:
```json
{
  "imported": 40,
  "errors": ["Poem #5: missing 'body' field"],
  "total_attempted": 42
}
```

### Export Comments
```
GET /api/poems/export/comments
Authorization: Bearer <token>
```

Response:
```json
{
  "comments": [
    {
      "comment_id": 1,
      "author": "Anonymous",
      "body": "Beautiful!",
      "created_at": "2026-02-20T15:00:00.000000",
      "poem": {
        "id": 5,
        "title": "Winter Song",
        "body_preview": "Snow falls gently..."
      }
    }
  ],
  "total": 10
}
```

## Usage Examples

### Backup Workflow
1. Log into admin panel
2. Click "📥 Export Poems" to download all poems
3. Click "💬 Export Comments" to download all comments
4. Store these JSON files safely

### Bulk Import Workflow
1. Create or edit a JSON file with poems in the correct format
2. Log into admin panel
3. Click "📤 Import Poems"
4. Select your JSON file
5. Confirm the import
6. Check the success message and console for any errors

### Migration Workflow
1. Export from old instance (poems + comments)
2. Set up new instance
3. Import poems into new instance
4. Comments are tied to poem IDs, so manual migration may be needed

## Tips

- **Always backup before importing**: Export your current data first
- **Test with small files**: Try importing 1-2 poems first to verify format
- **Check console for errors**: Import errors are logged to browser console
- **Tags are created automatically**: If a tag doesn't exist, it will be created
- **Duplicates**: Import doesn't check for duplicates, so importing twice will create duplicate poems

## Troubleshooting

**Import fails with "Invalid format" error**
- Ensure your JSON has a `"poems"` array at the root level
- Validate JSON syntax using an online validator

**Some poems fail to import**
- Check browser console for specific error messages
- Ensure each poem has at least a `body` field
- Verify tags are in array format `["tag1", "tag2"]`

**Export produces empty file**
- Ensure you're logged in as admin
- Check that you have poems in the database
- Check browser console for API errors

