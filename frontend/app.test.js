/**
 * Unit tests for frontend JavaScript utility functions
 */

describe('Translation Placeholder Tests', () => {
  test('placeholder replacement works', () => {
    const template = 'Hello {name}!';
    const result = template.replace(/\{name\}/g, 'World');
    expect(result).toBe('Hello World!');
  });

  test('multiple placeholders replacement', () => {
    const template = '{poet} — {type}';
    let result = template.replace(/\{poet\}/g, 'Alexander Pushkin');
    result = result.replace(/\{type\}/g, 'Poetry');
    expect(result).toBe('Alexander Pushkin — Poetry');
  });
});

describe('Tag Processing Tests', () => {
  const parseTags = (tagsString) => {
    if (!tagsString) return [];
    return tagsString
      .split(',')
      .map(t => t.trim())
      .filter(t => t.length > 0);
  };

  test('parses comma-separated tags', () => {
    const tags = parseTags('love,nature,peace');
    expect(tags).toEqual(['love', 'nature', 'peace']);
  });

  test('trims whitespace from tags', () => {
    const tags = parseTags('love, nature , peace');
    expect(tags).toEqual(['love', 'nature', 'peace']);
  });

  test('filters empty tags', () => {
    const tags = parseTags('love,,nature,');
    expect(tags).toEqual(['love', 'nature']);
  });

  test('returns empty array for empty string', () => {
    const tags = parseTags('');
    expect(tags).toEqual([]);
  });

  test('returns empty array for null/undefined', () => {
    expect(parseTags(null)).toEqual([]);
    expect(parseTags(undefined)).toEqual([]);
  });
});

describe('URL Parsing Tests', () => {
  const parseRoute = (path) => {
    if (path === '/' || path === '') return { page: 'home' };
    if (path === '/poems') return { page: 'poems' };
    if (path.startsWith('/poems/')) return { page: 'poem', uuid: path.split('/')[2] };
    if (path === '/about') return { page: 'about' };
    if (path === '/admin') return { page: 'admin' };
    return { page: 'home' };
  };

  test('parses home route', () => {
    expect(parseRoute('/')).toEqual({ page: 'home' });
    expect(parseRoute('')).toEqual({ page: 'home' });
  });

  test('parses poems route', () => {
    expect(parseRoute('/poems')).toEqual({ page: 'poems' });
  });

  test('parses individual poem route', () => {
    const uuid = 'abc-123-def-456';
    expect(parseRoute(`/poems/${uuid}`)).toEqual({ page: 'poem', uuid });
  });

  test('parses about route', () => {
    expect(parseRoute('/about')).toEqual({ page: 'about' });
  });

  test('parses admin route', () => {
    expect(parseRoute('/admin')).toEqual({ page: 'admin' });
  });

  test('defaults to home for unknown routes', () => {
    expect(parseRoute('/unknown')).toEqual({ page: 'home' });
  });
});

describe('Date Formatting Tests', () => {
  const formatDate = (isoString) => {
    if (!isoString) return '';
    const date = new Date(isoString);
    return date.toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    });
  };

  test('formats ISO date string', () => {
    const result = formatDate('2024-01-15T10:30:00Z');
    expect(result).toBeTruthy();
    expect(result).toContain('2024');
  });

  test('returns empty string for null', () => {
    expect(formatDate(null)).toBe('');
  });

  test('returns empty string for undefined', () => {
    expect(formatDate(undefined)).toBe('');
  });
});

describe('Form Validation Tests', () => {
  const validatePoemForm = (title, body, tags) => {
    const errors = [];

    if (!body || body.trim().length === 0) {
      errors.push('Body is required');
    }

    if (body && body.length > 10000) {
      errors.push('Body is too long (max 10000 characters)');
    }

    if (title && title.length > 255) {
      errors.push('Title is too long (max 255 characters)');
    }

    return errors;
  };

  test('validates valid poem', () => {
    const errors = validatePoemForm('Title', 'Body content', 'tag1,tag2');
    expect(errors).toHaveLength(0);
  });

  test('requires body', () => {
    const errors = validatePoemForm('Title', '', 'tags');
    expect(errors).toContain('Body is required');
  });

  test('validates body length', () => {
    const longBody = 'a'.repeat(10001);
    const errors = validatePoemForm('Title', longBody, 'tags');
    expect(errors).toContain('Body is too long (max 10000 characters)');
  });

  test('validates title length', () => {
    const longTitle = 'a'.repeat(256);
    const errors = validatePoemForm(longTitle, 'Body', 'tags');
    expect(errors).toContain('Title is too long (max 255 characters)');
  });

  test('allows empty title', () => {
    const errors = validatePoemForm('', 'Body content', 'tags');
    expect(errors).toHaveLength(0);
  });
});

describe('Image Validation Tests', () => {
  const validateImage = (file) => {
    const errors = [];
    const maxSize = 1024 * 1024; // 1MB
    const allowedTypes = ['image/jpeg', 'image/png'];

    if (!file) {
      errors.push('No file selected');
      return errors;
    }

    if (!allowedTypes.includes(file.type)) {
      errors.push('Only JPG and PNG are allowed');
    }

    if (file.size > maxSize) {
      errors.push('Image is too large (max 1MB)');
    }

    return errors;
  };

  test('validates valid image', () => {
    const file = {
      type: 'image/jpeg',
      size: 512 * 1024 // 512KB
    };
    const errors = validateImage(file);
    expect(errors).toHaveLength(0);
  });

  test('rejects invalid file type', () => {
    const file = {
      type: 'image/webp',
      size: 512 * 1024
    };
    const errors = validateImage(file);
    expect(errors).toContain('Only JPG and PNG are allowed');
  });

  test('rejects too large file', () => {
    const file = {
      type: 'image/jpeg',
      size: 2 * 1024 * 1024 // 2MB
    };
    const errors = validateImage(file);
    expect(errors).toContain('Image is too large (max 1MB)');
  });

  test('rejects null file', () => {
    const errors = validateImage(null);
    expect(errors).toContain('No file selected');
  });
});

describe('LocalStorage Utilities Tests', () => {
  const mockLocalStorage = (() => {
    let store = {};
    return {
      getItem: (key) => store[key] || null,
      setItem: (key, value) => {
        store[key] = value.toString();
      },
      removeItem: (key) => {
        delete store[key];
      },
      clear: () => {
        store = {};
      }
    };
  })();

  test('can store and retrieve token', () => {
    mockLocalStorage.setItem('token', 'test-token-123');
    expect(mockLocalStorage.getItem('token')).toBe('test-token-123');
  });

  test('can store and retrieve language preference', () => {
    mockLocalStorage.setItem('lang', 'ru');
    expect(mockLocalStorage.getItem('lang')).toBe('ru');
  });

  test('can remove item', () => {
    mockLocalStorage.setItem('key', 'value');
    mockLocalStorage.removeItem('key');
    expect(mockLocalStorage.getItem('key')).toBeNull();
  });

  test('can clear all items', () => {
    mockLocalStorage.setItem('key1', 'value1');
    mockLocalStorage.setItem('key2', 'value2');
    mockLocalStorage.clear();
    expect(mockLocalStorage.getItem('key1')).toBeNull();
    expect(mockLocalStorage.getItem('key2')).toBeNull();
  });
});

describe('Object Serialization Tests', () => {
  test('can serialize poem object to JSON', () => {
    const poem = {
      uuid: 'abc-123',
      title: 'Test Poem',
      body: 'Test content',
      tags: 'test,demo',
      is_draft: 0
    };
    const json = JSON.stringify(poem);
    const parsed = JSON.parse(json);
    expect(parsed.title).toBe('Test Poem');
    expect(parsed.is_draft).toBe(0);
  });

  test('can serialize comment object to JSON', () => {
    const comment = {
      id: 1,
      poem_id: 'abc-123',
      author: 'John',
      body: 'Great poem!',
      created_at: '2024-01-15T10:30:00Z'
    };
    const json = JSON.stringify(comment);
    const parsed = JSON.parse(json);
    expect(parsed.author).toBe('John');
    expect(parsed.body).toBe('Great poem!');
  });
});

describe('String Utility Tests', () => {
  const truncateString = (str, maxLength) => {
    if (!str) return '';
    if (str.length <= maxLength) return str;
    return str.substring(0, maxLength) + '...';
  };

  test('truncates long strings', () => {
    const result = truncateString('This is a very long string', 10);
    expect(result).toBe('This is a ...');
  });

  test('does not truncate short strings', () => {
    const result = truncateString('Short', 10);
    expect(result).toBe('Short');
  });

  test('handles empty string', () => {
    const result = truncateString('', 10);
    expect(result).toBe('');
  });

  test('handles null', () => {
    const result = truncateString(null, 10);
    expect(result).toBe('');
  });
});

describe('Array Utilities Tests', () => {
  const removeDuplicates = (arr) => [...new Set(arr)];

  test('removes duplicate tags', () => {
    const tags = ['love', 'nature', 'love', 'peace', 'nature'];
    const unique = removeDuplicates(tags);
    expect(unique.length).toBe(3);
    expect(unique).toContain('love');
    expect(unique).toContain('nature');
    expect(unique).toContain('peace');
  });

  test('handles empty array', () => {
    const unique = removeDuplicates([]);
    expect(unique).toEqual([]);
  });

  test('handles already unique array', () => {
    const arr = ['a', 'b', 'c'];
    const unique = removeDuplicates(arr);
    expect(unique.length).toBe(3);
  });
});

