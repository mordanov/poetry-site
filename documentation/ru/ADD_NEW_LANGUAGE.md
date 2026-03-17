# 🌏 Добавление нового языка — Пошаговое руководство

Полное руководство по добавлению нового языка (на примере испанского).

## 📋 План действий

1. Добавить словарь переводов в `I18N`
2. Добавить язык в выпадающий список
3. Протестировать
4. (Опционально) Обновить документацию

## 📝 Шаг 1: Добавление словаря переводов

### Находим словарь в коде

**Файл:** `/frontend/static/js/app.js` (строка ~40)

```javascript
const I18N = {
  en: { /* ... */ },
  ru: { /* ... */ },
  // ← Добавляем испанский здесь
}
```

### Добавляем испанский язык

Откройте `/frontend/static/js/app.js` и найдите объект `I18N`:

```javascript
const I18N = {
  en: {
    'site.title': 'poetry-site — Poetry',
    'nav.home': 'Home',
    // ... все остальные ключи
  },
  ru: {
    'site.title': 'poetry-site — Poetry',
    'nav.home': 'Главная',
    // ... все остальные ключи
  },
  es: {  // ← НОВОЕ: Испанский
    'site.title': 'poetry-site — Poesía',
    'nav.home': 'Inicio',
    'nav.poems': 'Poemas',
    'nav.about': 'Acerca de',
    'nav.admin': 'Admin',
    'nav.login': 'Iniciar sesión',
    'nav.logout': 'Cerrar sesión',
    'hero.title': 'Palabras<br><em>en la oscuridad</em>',
    'hero.subtitle': 'Una colección de versos de poetry-site',
    'hero.cta': 'Leer los poemas →',
    'section.latest': 'Últimos',
    'poems.title': 'Poemas',
    'poems.all': 'Todos',
    'poems.none': 'No se encontraron poemas.',
    'poems.noneHome': 'Sin poemas aún.',
    'poems.loading': 'Cargando…',
    'poems.untitled': '— sin título —',
    'poems.untitledShort': 'sin título',
    'poems.back': '← Volver a poemas',
    'poems.notFound': 'Poema no encontrado.',
    'comments.title': 'Reflexiones ({count})',
    'comments.empty': 'Sé el primero en dejar una reflexión.',
    'comments.namePlaceholder': 'Tu nombre (opcional)',
    'comments.bodyPlaceholder': 'Deja una reflexión…',
    'comments.post': 'Publicar',
    'comments.anonymous': 'Anónimo',
    'comments.posted': 'Reflexión publicada',
    'comments.postError': 'Error al publicar',
    'comments.deleteConfirm': '¿Borrar este comentario?',
    'comments.deleted': 'Comentario eliminado',
    'about.edit': 'Editar página',
    'about.nameLabel': 'Tu nombre',
    'about.photoLabel': 'URL de foto',
    'about.bioLabel': 'Biografía (soporta saltos de línea)',
    'about.save': 'Guardar',
    'about.saved': 'Página guardada',
    'about.saveError': 'Error al guardar',
    'admin.title': 'Admin',
    'admin.tabs.poems': 'Poemas',
    'admin.tabs.about': 'Página "Acerca de"',
    'admin.tabs.password': 'Contraseña',
    'admin.newPoem': '+ Nuevo poema',
    'admin.none': 'Sin poemas aún.',
    'admin.edit': 'Editar',
    'admin.delete': 'Borrar',
    'admin.editPoemTitle': 'Editar poema',
    'admin.newPoemTitle': 'Nuevo poema',
    'admin.form.titleLabel': 'Título (opcional)',
    'admin.form.titlePlaceholder': 'Dejar en blanco si es sin título',
    'admin.form.bodyLabel': 'Cuerpo',
    'admin.form.bodyPlaceholder': 'Escribe tu poema…',
    'admin.form.tagsLabel': 'Etiquetas (separadas por coma)',
    'admin.form.tagsPlaceholder': 'amor, naturaleza, dolor',
    'admin.form.save': 'Guardar cambios',
    'admin.form.publish': 'Publicar',
    'admin.form.cancel': 'Cancelar',
    'admin.form.bodyRequired': 'El cuerpo es obligatorio',
    'admin.poemUpdated': 'Poema actualizado',
    'admin.poemPublished': 'Poema publicado',
    'admin.loadError': 'Error al cargar poema',
    'admin.saveError': 'Error al guardar',
    'admin.deleteConfirm': '¿Borrar este poema y todos sus comentarios?',
    'admin.deleted': 'Poema borrado',
    'admin.deleteError': 'Error al borrar',
    'auth.title': 'Inicio de sesión del administrador',
    'auth.username': 'Nombre de usuario',
    'auth.password': 'Contraseña',
    'auth.login': 'Iniciar sesión',
    'auth.invalid': 'Credenciales inválidas',
    'auth.welcome': '¡Bienvenido de nuevo!',
    'auth.loggedOut': 'Sesión cerrada',
    'password.current': 'Contraseña actual',
    'password.new': 'Nueva contraseña',
    'password.confirm': 'Confirmar nueva',
    'password.change': 'Cambiar contraseña',
    'password.mismatch': 'Las contraseñas no coinciden',
    'password.changed': 'Contraseña cambiada',
    'generic.error': 'Error'
  }
}
```

## 🔘 Шаг 2: Добавление языка в выпадающий список

### Находим переключатель

**Файл:** `/frontend/templates/index.html` (строка ~21)

```html
<div class="lang-switch" aria-label="Language">
  <select class="lang-select" id="lang-select" aria-label="Language">
    <option value="en" data-i18n="lang.en">English</option>
    <option value="ru" data-i18n="lang.ru">Русский</option>
    <!-- ← Добавляем испанский здесь -->
  </select>
</div>
```

### Добавляем испанский

```html
<div class="lang-switch" aria-label="Language">
  <select class="lang-select" id="lang-select" aria-label="Language">
    <option value="en" data-i18n="lang.en">English</option>
    <option value="ru" data-i18n="lang.ru">Русский</option>
    <option value="es" data-i18n="lang.es">Español</option>  <!-- ← НОВОЕ -->
  </select>
</div>
```

## 🧪 Шаг 3: Тестирование

### 1. Перезагрузите браузер

```
F5 или Cmd+R
```

### 2. Проверьте переключатель

- В правом верхнем углу должен быть выпадающий список
- Выберите `ES`
- Интерфейс должен переключиться на испанский

### 3. Проверьте переводы

| Элемент | Должно быть |
|---------|-----------|
| Заголовок | "poetry-site — Poesía" |
| Меню | "Inicio", "Poemas", "Acerca de" |
| Кнопка "Login" | "Iniciar sesión" |
| Кнопка "Logout" | "Cerrar sesión" |
| Админ-панель | "Admin", "Nuevo poema" |

### 4. Проверьте сохранение

- Переключитесь на испанский
- Обновите страницу
- Язык должен остаться испанским

### 5. Протестируйте все страницы

- Главная (`/`) — должна быть на испанском
- Стихи (`/poems`) — должна быть на испанском
- Об авторе (`/about`) — должна быть на испанском
- Админ-панель (`/admin`, требует вход) — должна быть на испанском

## 🎯 Дополнительные языки

### Французский (FR)

```javascript
'fr': {
  'site.title': 'poetry-site — Poésie',
  'nav.home': 'Accueil',
  'nav.poems': 'Poèmes',
  'nav.about': 'À propos',
  // ... остальные ключи на французском
}
```

**Опция в HTML:**

```html
<option value="fr" data-i18n="lang.fr">Français</option>
```

### Немецкий (DE)

```javascript
'de': {
  'site.title': 'poetry-site — Poesie',
  'nav.home': 'Startseite',
  'nav.poems': 'Gedichte',
  'nav.about': 'Über',
  // ... остальные ключи на немецком
}
```

**Опция в HTML:**
```html
<option value="de" data-i18n="lang.de">Deutsch</option>
```

### Итальянский (IT)

```javascript
'it': {
  'site.title': 'poetry-site — Poesia',
  'nav.home': 'Home',
  'nav.poems': 'Poesie',
  'nav.about': 'Chi sono',
  // ... остальные ключи на итальянском
}
```

**Опция в HTML:**
```html
<option value="it" data-i18n="lang.it">Italiano</option>
```

## 📚 Справочник кодов языков

| Язык | Код | Опция |
|------|-----|-------|
| Английский | en | English |
| Русский | ru | Русский |
| Испанский | es | Español |
| Французский | fr | Français |
| Немецкий | de | Deutsch |
| Итальянский | it | Italiano |
| Португальский | pt | Português |
| Японский | ja | 日本語 |
| Китайский | zh | 中文 |

## 🔄 Правила выбора языка по умолчанию

1. Если в `localStorage` есть язык — используется он
2. Иначе используется язык браузера
3. Если язык браузера неизвестен — используется русский (`ru`)

## 🔍 Как убедиться, что все ключи добавлены?

### Способ 1: Проверка консоли браузера

Откройте консоль браузера (F12) и введите:

```javascript
// Сравнение ключей в словаре
Object.keys(I18N.en).sort().toString() === Object.keys(I18N.es).sort().toString()
```

Если результат `true` → все ключи одинаковые ✅
Если `false` → какой-то ключ забыли ❌

### Способ 2: Вывести отличия

```javascript
// Найти ключи, которые есть в EN, но нет в ES
Object.keys(I18N.en).filter(k => !I18N.es.hasOwnProperty(k))

// Найти ключи, которые есть в ES, но нет в EN
Object.keys(I18N.es).filter(k => !I18N.en.hasOwnProperty(k))
```

### Способ 3: Быстрая проверка

```javascript
// Количество ключей должно быть одинаковым
Object.keys(I18N.en).length   // Например: 100
Object.keys(I18N.es).length   // Должно быть тоже 100
```

## 🐛 Если что-то не работает

### Проблема: Кнопка не появилась

**Решение:** Очистите кеш браузера
```javascript
// В консоли браузера:
localStorage.clear()
location.reload()
```

### Проблема: Язык не переключается

**Решение:** Проверьте консоль браузера (F12) на ошибки

```javascript
// Проверьте, что язык добавлен в I18N
I18N.es  // Должен вернуть объект с переводами
```

### Проблема: Текст остаётся на английском

**Решение:** Ключ перевода может быть неправильным

```javascript
// Проверьте, что ключ существует
t('nav.home')  // Должно вернуть перевод
```

## 📝 Обновление документации

После добавления испанского языка обновите этот файл:

```markdown
### Поддерживаемые языки

- 🇬🇧 **English** (EN)
- 🇷🇺 **Русский** (RU)
- 🇪🇸 **Español** (ES)  <!-- ← НОВОЕ -->
```

## 🎓 Автоматизация (для продвинутых)

### Создайте скрипт для проверки

Файл: `check-i18n.js`

```javascript
const fs = require('fs');

// Читать файл app.js
const content = fs.readFileSync('./frontend/static/js/app.js', 'utf8');

// Найти объект I18N (примерный парсинг)
// ... код парсинга ...

// Проверить, что все языки имеют одинаковые ключи
// ... код проверки ...

console.log('✅ Все языки синхронизированы!');
```

Запуск:
```bash
node check-i18n.js
```

## 🌍 Когда добавлять новый язык?

Рекомендуется добавлять новый язык, если:

1. ✅ Все 100+ ключей переведены правильно
2. ✅ Опция добавлена в HTML
3. ✅ Протестировано в браузере
4. ✅ Проверено, что переводы качественные (используйте Гугл Переводчик, но затем отредактируйте вручную)
5. ✅ Обновлена документация

## 📚 Дополнительные ресурсы

### Онлайн переводчики

- Google Translate: https://translate.google.com/
- DeepL: https://www.deepl.com/translator
- Reverso Context: https://context.reverso.net/

### Советы по переводу

1. **Сохраняйте контекст** — некоторые фразы могут быть длинными
2. **Проверяйте грамматику** — переводчик может ошибаться
3. **Используйте специализированные словари** — для технических терминов
4. **Тестируйте в браузере** — интерфейс может выглядеть по-другому на других языках
5. **Просите носителей языка** — проверить качество перевода

## ✨ Пример: Полная интеграция испанского

### 1. Отредактировать app.js ✅
Добавлены все переводы для `es`

### 2. Отредактировать index.html ✅
Добавлена опция `<option value="es" data-i18n="lang.es">Español</option>`

### 3. Протестировать ✅
- Переключение на ES работает
- Все элементы переводятся
- Выбор сохраняется в localStorage

### 4. Обновить документацию ✅
- I18N_GUIDE.md: добавить информацию об испанском

### 5. Готово! 🎉
Испанский язык полностью интегрирован

---

**Нужна помощь?** Обратитесь к `I18N_GUIDE.md` для более подробной информации о системе переводов.

**Счастливой локализации! 🌍**
