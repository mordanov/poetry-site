# 🌍 Многоязычность (i18n) — Подробное руководство

## 📖 Обзор

Сайт Poetry Site поддерживает полную локализацию интерфейса на **двух языках**:

- 🇬🇧 **English** (EN)
- 🇷🇺 **Русский** (RU)

Система переводов построена на **клиентской стороне** с помощью JavaScript и `localStorage`.

## 🎯 Как это работает

### 1. Инициализация языка

При загрузке сайта:

1. Проверяется `localStorage` на наличие сохранённого языка
2. Если нет — используется язык браузера (`navigator.language`)
3. Если браузер настроен на русский → выбирается русский
4. Иначе → английский по умолчанию

```javascript
let currentLang = (localStorage.getItem('lang') || (navigator.language || 'en'))
  .toLowerCase()
  .startsWith('ru')
  ? 'ru'
  : 'en';
```

### 2. Переключение языка

При нажатии на кнопку языка (EN/RU):

1. Текущий язык меняется
2. Сохраняется в `localStorage`
3. Все элементы переводятся
4. Страница перерендеривается

```javascript
function setLanguage(lang, rerender = true) {
  if (!I18N[lang]) return;
  currentLang = lang;
  localStorage.setItem('lang', lang);           // Сохранение
  document.documentElement.lang = lang;         // Обновление HTML lang
  applyTranslations();                          // Перевод элементов
  updateLangUI();                               // Обновление UI кнопок
  if (rerender) handleRoute();                  // Перерендеринг страницы
}
```

## 📚 Словарь переводов (I18N)

Все переводы хранятся в файле: **`/frontend/static/js/app.js`**

Структура:

```javascript
const I18N = {
  en: {
    'nav.home': 'Home',
    'nav.poems': 'Poems',
    'poems.title': 'Poems',
    'poems.none': 'No poems found.',
    // ... 100+ ключей
  },
  ru: {
    'nav.home': 'Главная',
    'nav.poems': 'Стихи',
    'poems.title': 'Стихи',
    'poems.none': 'Стихи не найдены.',
    // ... 100+ ключей
  }
}
```

### Текущие категории переводов:

| Категория | Ключи | Примеры |
|-----------|-------|---------|
| **nav** | Навигация | `nav.home`, `nav.poems`, `nav.login` |
| **hero** | Главная страница | `hero.title`, `hero.subtitle`, `hero.cta` |
| **poems** | Страница стихов | `poems.title`, `poems.none`, `poems.untitled` |
| **comments** | Комментарии | `comments.title`, `comments.empty`, `comments.post` |
| **about** | Об авторе | `about.edit`, `about.nameLabel`, `about.save` |
| **admin** | Админ-панель | `admin.title`, `admin.newPoem`, `admin.delete` |
| **auth** | Аутентификация | `auth.title`, `auth.login`, `auth.invalid` |
| **password** | Смена пароля | `password.current`, `password.new`, `password.change` |
| **generic** | Общие | `generic.error` |

**Всего переводов**: 100+ ключей для каждого языка

## 🔧 Как добавить новый перевод

### Шаг 1: Добавьте ключ в словарь

Откройте `/frontend/static/js/app.js` и найдите объект `I18N`:

```javascript
const I18N = {
  en: {
    'nav.home': 'Home',
    'my.newKey': 'My new English text',  // ← Добавьте здесь
    // ...
  },
  ru: {
    'nav.home': 'Главная',
    'my.newKey': 'Мой новый русский текст',  // ← И здесь
    // ...
  }
}
```

### Шаг 2: Используйте в HTML

Используйте атрибут `data-i18n`:

```html
<!-- Простой текст -->
<button data-i18n="my.newKey">Click me</button>

<!-- HTML (как в hero.title) -->
<h1 data-i18n-html="my.newKey">Click me</h1>
```

### Шаг 3: Используйте в JavaScript

```javascript
// Простой вызов
const text = t('my.newKey');
console.log(text);  // "My new English text" или "Мой новый русский текст"

// С переменными
const count = 5;
const text = t('comments.title', { count });
// Result: "Reflections (5)" или "Размышления (5)"
```

### Шаг 4: Примените переводы

При загрузке страницы или при смене языка автоматически вызывается:

```javascript
function applyTranslations() {
  // Переводит все элементы с data-i18n
  document.querySelectorAll('[data-i18n]').forEach(el => {
    el.textContent = t(el.dataset.i18n);
  });
  
  // Переводит все элементы с data-i18n-html
  document.querySelectorAll('[data-i18n-html]').forEach(el => {
    el.innerHTML = t(el.dataset.i18nHtml);
  });
}
```

## 💡 Примеры использования

### Пример 1: Добавление нового элемента навигации

```javascript
// 1. В app.js добавьте переводы:
I18N.en['nav.gallery'] = 'Gallery';
I18N.ru['nav.gallery'] = 'Галерея';

// 2. В HTML добавьте элемент:
<li><a href="/gallery" data-page="gallery" data-i18n="nav.gallery">Gallery</a></li>

// 3. Языки автоматически применятся при загрузке или смене языка
```

### Пример 2: Динамический текст с переменными

```javascript
// 1. В словаре:
I18N.en['comments.title'] = 'Reflections ({count})';
I18N.ru['comments.title'] = 'Размышления ({count})';

// 2. Использование функции t():
const count = comments.length;
const title = t('comments.title', { count });
// "Reflections (5)" или "Размышления (5)"
```

### Пример 3: HTML с форматированием

```javascript
// 1. В словаре:
I18N.en['hero.title'] = 'Words<br><em>in the dark</em>';
I18N.ru['hero.title'] = 'Слова<br><em>в темноте</em>';

// 2. В HTML используйте data-i18n-html:
<h1 data-i18n-html="hero.title"></h1>

// 3. Результат:
// <h1>Words<br><em>in the dark</em></h1>
```

## 🎨 Переключатель языков

### Внешний вид в навигации

```html
<div class="lang-switch" role="group" aria-label="Language">
  <button type="button" data-lang="en" class="lang-btn">EN</button>
  <button type="button" data-lang="ru" class="lang-btn">RU</button>
</div>
```

### Стили (CSS)

```css
.lang-switch {
  display: inline-flex; 
  align-items: center; 
  gap: 0.35rem;
  border: 1px solid var(--border); 
  border-radius: 999px;
  padding: 2px;
}

.lang-btn.active {
  background: var(--ink); 
  color: var(--cream);
}
```

### Инициализация (JavaScript)

```javascript
function initLanguage() {
  setLanguage(currentLang, false);  // Установка начального языка
  
  // Добавление обработчиков на кнопки
  document.querySelectorAll('.lang-switch button').forEach(btn => {
    btn.addEventListener('click', () => setLanguage(btn.dataset.lang));
  });
}
```

## 🔄 Поток выполнения смены языка

```
Пользователь нажимает на кнопку языка (EN/RU)
          ↓
    setLanguage(lang)
          ↓
  ┌─────────────────────────────────────┐
  │ currentLang = lang                  │
  │ localStorage.setItem('lang', lang)  │
  │ document.documentElement.lang = lang│
  │ applyTranslations()                 │
  │ updateLangUI()                      │
  │ handleRoute() [опционально]         │
  └─────────────────────────────────────┘
          ↓
  applyTranslations() переводит все элементы
  updateLangUI() обновляет активную кнопку
          ↓
  Страница отображается на новом языке
```

## 💾 Сохранение выбора

Выбранный язык **сохраняется в localStorage** браузера:

```javascript
localStorage.setItem('lang', 'ru');  // Сохранено как 'ru'

// При следующем визите:
let currentLang = localStorage.getItem('lang') || 'en';
// currentLang = 'ru'
```

Это означает, что пользовательский выбор языка **сохраняется между сеансами**.

## 🌐 Расширение на новые языки

Если нужно добавить третий язык (например, французский):

### 1. Добавьте язык в I18N

```javascript
const I18N = {
  en: { /* ... */ },
  ru: { /* ... */ },
  fr: {  // ← Новый язык
    'nav.home': 'Accueil',
    'nav.poems': 'Poèmes',
    // ... добавьте все 100+ ключей
  }
}
```

### 2. Обновите кнопки переключения

```html
<div class="lang-switch" role="group" aria-label="Language">
  <button type="button" data-lang="en" class="lang-btn">EN</button>
  <button type="button" data-lang="ru" class="lang-btn">RU</button>
  <button type="button" data-lang="fr" class="lang-btn">FR</button>  <!-- Новое -->
</div>
```

### 3. Функция автоматически поддержит новый язык

```javascript
// Эта функция работает для любого языка в I18N
function setLanguage(lang, rerender = true) {
  if (!I18N[lang]) return;  // Проверка наличия языка
  // ... остальной код
}
```

## 🚨 Обработка ошибок

Если ключ перевода не найден:

```javascript
function t(key, vars = {}) {
  const dict = I18N[currentLang] || I18N.en;
  let str = dict[key] || I18N.en[key] || key;  // Fallback
  // Возвращает само значение key, если перевод не найден
  return str;
}
```

Пример:
```javascript
t('nonexistent.key');  // Вернёт: 'nonexistent.key'
```

## 📱 Мобильная поддержка

Переключатель языков **полностью адаптивен**:

- На десктопе: видно в правом углу навигации
- На мобиле: переключатель остаётся видимым (может быть скрыт в меню)

## 🔐 Безопасность

- Все переводы **хранятся на фронтенде** (нет API запросов для i18n)
- `localStorage` используется **только для хранения выбора пользователя**
- Не требуется подключение к серверу для переключения языков

## 📊 Статистика переводов

```
Всего ключей в словаре: 100+
Поддерживаемые языки: 2 (EN, RU)
Категории переводов: 9
Статус: 100% локализирован ✅
```

---

**Нужна помощь с переводами?** Отредактируйте словарь в `/frontend/static/js/app.js` и перезагрузите страницу.

