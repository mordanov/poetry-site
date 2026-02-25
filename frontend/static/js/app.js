// ─── CONFIG ───────────────────────────────────────────────────────────────────
const API = '/api';

// ─── I18N ─────────────────────────────────────────────────────────────────────
const I18N = {
  en: {
    'site.title': 'Lev Gorev — Poetry',
    'nav.home': 'Home',
    'nav.poems': 'Poems',
    'nav.about': 'About',
    'nav.admin': 'Admin',
    'nav.login': 'Login',
    'nav.logout': 'Logout',
    'hero.title': 'Words<br><em>in the dark</em>',
    'hero.subtitle': 'A collection of verses by Lev Gorev',
    'hero.cta': 'Read the poems →',
    'section.latest': 'Latest',
    'poems.title': 'Poems',
    'poems.all': 'All',
    'poems.none': 'No poems found.',
    'poems.noneHome': 'No poems yet.',
    'poems.loading': 'Loading…',
    'poems.untitled': '— untitled —',
    'poems.untitledShort': 'untitled',
    'poems.back': '← Back to poems',
    'poems.notFound': 'Poem not found.',
    'comments.title': 'Reflections ({count})',
    'comments.empty': 'Be the first to leave a reflection.',
    'comments.namePlaceholder': 'Your name (optional)',
    'comments.bodyPlaceholder': 'Leave a reflection…',
    'comments.post': 'Post',
    'comments.anonymous': 'Anonymous',
    'comments.posted': 'Reflection posted',
    'comments.postError': 'Error posting reflection',
    'comments.deleteConfirm': 'Delete this reflection?',
    'comments.deleted': 'Reflection deleted',
    'about.edit': 'Edit page',
    'about.nameLabel': 'Your Name',
    'about.photoLabel': 'Photo URL',
    'about.bioLabel': 'Bio (supports line breaks)',
    'about.save': 'Save',
    'about.saved': 'About page saved',
    'about.saveError': 'Error saving',
    'admin.title': 'Admin',
    'admin.tabs.poems': 'Poems',
    'admin.tabs.about': 'About Page',
    'admin.tabs.comments': 'Reflections',
    'admin.tabs.password': 'Password',
    'admin.newPoem': '+ New Poem',
    'admin.exportPoems': '📥 Export Poems',
    'admin.importPoems': '📤 Import Poems',
    'admin.comments.none': 'No reflectiond yet.',
    'admin.comments.viewPoem': 'View Poem',
    'admin.none': 'No poems yet.',
    'admin.edit': 'Edit',
    'admin.delete': 'Delete',
    'admin.editPoemTitle': 'Edit poem',
    'admin.newPoemTitle': 'New poem',
    'admin.form.titleLabel': 'Title (optional)',
    'admin.form.titlePlaceholder': 'Leave blank for untitled',
    'admin.form.bodyLabel': 'Body',
    'admin.form.bodyPlaceholder': 'Write your poem…',
    'admin.form.tagsLabel': 'Tags (comma-separated)',
    'admin.form.tagsPlaceholder': 'love, nature, grief',
    'admin.form.imageLabel': 'Image (JPG/PNG, max 1MB)',
    'admin.form.imageRemove': 'Remove image',
    'admin.form.imageTypeError': 'Only JPG and PNG are allowed',
    'admin.form.imageTooLarge': 'Image is too large (max 1MB)',
    'admin.form.imageUploadError': 'Image upload failed',
    'admin.form.imageDeleteError': 'Image delete failed',
    'admin.form.draftLabel': 'Save as draft',
    'admin.draft': 'DRAFT',
    'admin.versions.title': 'Version History',
    'admin.versions.current': 'Current',
    'admin.versions.restore': 'Restore',
    'admin.versions.latest': 'Latest',
    'admin.versions.button': '📜 Version History',
    'admin.versions.confirmRestore': 'Restore to version {version}?',
    'admin.versions.restoreError': 'Failed to restore version',
    'admin.versions.loadError': 'Failed to load version history',
    'admin.form.save': 'Save changes',
    'admin.form.publish': 'Publish',
    'admin.form.cancel': 'Cancel',
    'admin.form.bodyRequired': 'Body is required',
    'admin.poemUpdated': 'Poem updated',
    'admin.poemPublished': 'Poem published',
    'admin.loadError': 'Error loading poem',
    'admin.saveError': 'Error saving poem',
    'admin.deleteConfirm': 'Delete this poem and all its reflections?',
    'admin.deleted': 'Poem deleted',
    'admin.deleteError': 'Error deleting poem',
    'auth.title': 'Admin Login',
    'auth.username': 'Username',
    'auth.password': 'Password',
    'auth.login': 'Login',
    'auth.invalid': 'Invalid credentials',
    'auth.welcome': 'Welcome back!',
    'auth.loggedOut': 'Logged out',
    'password.current': 'Current Password',
    'password.new': 'New Password',
    'password.confirm': 'Confirm New',
    'password.change': 'Change Password',
    'password.mismatch': 'Passwords do not match',
    'password.changed': 'Password changed',
    'generic.error': 'Error'
  },
  ru: {
    'site.title': 'Lev Gorev — Poetry',
    'nav.home': 'Главная',
    'nav.poems': 'Стихи',
    'nav.about': 'Об авторе',
    'nav.admin': 'Админ',
    'nav.login': 'Войти',
    'nav.logout': 'Выйти',
    'hero.title': 'Слова<br><em>в темноте</em>',
    'hero.subtitle': 'Собрание стихов Льва Горевa',
    'hero.cta': 'Читать стихи →',
    'section.latest': 'Новое',
    'poems.title': 'Стихи',
    'poems.all': 'Все',
    'poems.none': 'Стихи не найдены.',
    'poems.noneHome': 'Пока нет стихов.',
    'poems.loading': 'Загрузка…',
    'poems.untitled': '— без названия —',
    'poems.untitledShort': 'без названия',
    'poems.back': '← Назад к стихам',
    'poems.notFound': 'Стихотворение не найдено.',
    'comments.title': 'Размышления ({count})',
    'comments.empty': 'Станьте первым, кто оставит размышление.',
    'comments.namePlaceholder': 'Ваше имя (необязательно)',
    'comments.bodyPlaceholder': 'Оставьте размышление…',
    'comments.post': 'Отправить',
    'comments.anonymous': 'Аноним',
    'comments.posted': 'Размышление опубликовано',
    'comments.postError': 'Ошибка при отправке',
    'comments.deleteConfirm': 'Удалить это размышление?',
    'comments.deleted': 'Размышление удалено',
    'about.edit': 'Редактировать',
    'about.nameLabel': 'Ваше имя',
    'about.photoLabel': 'URL фото',
    'about.bioLabel': 'Био (поддерживает переносы строк)',
    'about.save': 'Сохранить',
    'about.saved': 'Страница сохранена',
    'about.saveError': 'Ошибка сохранения',
    'admin.title': 'Админ',
    'admin.tabs.poems': 'Стихи',
    'admin.tabs.about': 'Страница "Об авторе"',
    'admin.tabs.comments': 'Размышления',
    'admin.tabs.password': 'Пароль',
    'admin.newPoem': '+ Новый стих',
    'admin.exportPoems': '📥 Экспорт стихов',
    'admin.importPoems': '📤 Импорт стихов',
    'admin.comments.none': 'Размышлений пока нет.',
    'admin.comments.viewPoem': 'Смотреть стих',
    'admin.none': 'Пока нет стихов.',
    'admin.edit': 'Редактировать',
    'admin.delete': 'Удалить',
    'admin.editPoemTitle': 'Редактировать стих',
    'admin.newPoemTitle': 'Новый стих',
    'admin.form.titleLabel': 'Название (необязательно)',
    'admin.form.titlePlaceholder': 'Оставьте пустым, если без названия',
    'admin.form.bodyLabel': 'Текст',
    'admin.form.bodyPlaceholder': 'Напишите стих…',
    'admin.form.tagsLabel': 'Теги (через запятую)',
    'admin.form.tagsPlaceholder': 'любовь, природа, печаль',
    'admin.form.imageLabel': 'Картинка (JPG/PNG, до 1MB)',
    'admin.form.imageRemove': 'Удалить картинку',
    'admin.form.imageTypeError': 'Допустимы только JPG и PNG',
    'admin.form.imageTooLarge': 'Картинка слишком большая (макс. 1MB)',
    'admin.form.imageUploadError': 'Ошибка загрузки картинки',
    'admin.form.imageDeleteError': 'Ошибка удаления картинки',
    'admin.form.draftLabel': 'Сохранить как черновик',
    'admin.draft': 'ЧЕРНОВИК',
    'admin.versions.title': 'История версий',
    'admin.versions.current': 'Текущая',
    'admin.versions.restore': 'Восстановить',
    'admin.versions.latest': 'Последняя',
    'admin.versions.button': '📜 История версий',
    'admin.versions.confirmRestore': 'Восстановить версию {version}?',
    'admin.versions.restoreError': 'Ошибка восстановления версии',
    'admin.versions.loadError': 'Ошибка загрузки истории версий',
    'admin.form.save': 'Сохранить',
    'admin.form.publish': 'Опубликовать',
    'admin.form.cancel': 'Отмена',
    'admin.form.bodyRequired': 'Текст обязателен',
    'admin.poemUpdated': 'Стих обновлен',
    'admin.poemPublished': 'Стих опубликован',
    'admin.loadError': 'Ошибка загрузки стиха',
    'admin.saveError': 'Ошибка сохранения',
    'admin.deleteConfirm': 'Удалить стих и все размышления?',
    'admin.deleted': 'Стих удален',
    'admin.deleteError': 'Ошибка удаления',
    'auth.title': 'Вход администратора',
    'auth.username': 'Имя пользователя',
    'auth.password': 'Пароль',
    'auth.login': 'Войти',
    'auth.invalid': 'Неверные данные',
    'auth.welcome': 'С возвращением!',
    'auth.loggedOut': 'Вы вышли',
    'password.current': 'Текущий пароль',
    'password.new': 'Новый пароль',
    'password.confirm': 'Подтвердите новый',
    'password.change': 'Сменить пароль',
    'password.mismatch': 'Пароли не совпадают',
    'password.changed': 'Пароль изменен',
    'generic.error': 'Ошибка'
  }
};

let currentLang = (localStorage.getItem('lang') || (navigator.language || 'en'))
  .toLowerCase()
  .startsWith('ru')
  ? 'ru'
  : 'en';

function t(key, vars = {}) {
  const dict = I18N[currentLang] || I18N.en;
  let str = dict[key] || I18N.en[key] || key;
  Object.keys(vars).forEach(k => {
    str = str.replace(new RegExp(`\\{${k}\\}`, 'g'), vars[k]);
  });
  return str;
}

function applyTranslations() {
  document.querySelectorAll('[data-i18n]').forEach(el => {
    el.textContent = t(el.dataset.i18n);
  });
  document.querySelectorAll('[data-i18n-html]').forEach(el => {
    el.innerHTML = t(el.dataset.i18nHtml);
  });
}

function updateLangUI() {
  document.querySelectorAll('.lang-switch button').forEach(btn => {
    const active = btn.dataset.lang === currentLang;
    btn.classList.toggle('active', active);
    btn.setAttribute('aria-pressed', active ? 'true' : 'false');
  });
}

function setLanguage(lang, rerender = true) {
  if (!I18N[lang]) return;
  currentLang = lang;
  localStorage.setItem('lang', lang);
  document.documentElement.lang = lang;
  applyTranslations();
  updateLangUI();
  if (rerender) handleRoute();
}

function initLanguage() {
  setLanguage(currentLang, false);
  document.querySelectorAll('.lang-switch button').forEach(btn => {
    btn.addEventListener('click', () => setLanguage(btn.dataset.lang));
  });
}

// ─── STATE ────────────────────────────────────────────────────────────────────
let token = localStorage.getItem('token') || null;
let currentTag = null;
let editingPoemId = null;

// ─── INIT ─────────────────────────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
  initLanguage();
  updateAuthUI();
  handleRoute();
  window.addEventListener('popstate', handleRoute);
});

// ─── ROUTING ──────────────────────────────────────────────────────────────────
function handleRoute() {
  const path = location.pathname;
  if (path === '/' || path === '') navigate('home', false);
  else if (path === '/poems') navigate('poems', false);
  else if (path.startsWith('/poems/')) navigate('poem', false, path.split('/')[2]);
  else if (path === '/about') navigate('about', false);
  else if (path === '/admin') navigate('admin', false);
  else navigate('home', false);
}

function navigate(page, push = true, param = null) {
  document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
  document.querySelectorAll('.nav-links a').forEach(a => a.classList.remove('active'));

  const pageEl = document.getElementById(`page-${page}`);
  if (!pageEl) return;
  pageEl.classList.add('active');

  const link = document.querySelector(`.nav-links a[data-page="${page}"]`);
  if (link) link.classList.add('active');

  if (push) {
    let url = '/';
    if (page === 'poems') url = '/poems';
    else if (page === 'poem') url = `/poems/${param}`;
    else if (page === 'about') url = '/about';
    else if (page === 'admin') url = '/admin';
    history.pushState({page, param}, '', url);
  }

  window.scrollTo(0, 0);

  if (page === 'home') loadHome();
  else if (page === 'poems') loadPoems();
  else if (page === 'poem') loadPoem(param);
  else if (page === 'about') loadAbout();
  else if (page === 'admin') {
    if (!token) { showLoginModal(); return; }
    loadAdminPoems();
    loadAboutForm();
  }
}

// ─── API HELPERS ──────────────────────────────────────────────────────────────
async function apiFetch(path, opts = {}) {
  const headers = { 'Content-Type': 'application/json', ...(opts.headers || {}) };
  if (token) headers['Authorization'] = `Bearer ${token}`;
  const res = await fetch(API + path, { ...opts, headers });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || res.statusText);
  }
  if (res.status === 204) return null;
  return res.json();
}

// ─── AUTH ─────────────────────────────────────────────────────────────────────
async function login(e) {
  e.preventDefault();
  const user = document.getElementById('login-user').value;
  const pass = document.getElementById('login-pass').value;
  const err = document.getElementById('login-error');
  err.textContent = '';
  try {
    const body = new URLSearchParams({ username: user, password: pass });
    const res = await fetch(API + '/auth/login', { method: 'POST', body });
    if (!res.ok) throw new Error(t('auth.invalid'));
    const data = await res.json();
    token = data.access_token;
    localStorage.setItem('token', token);
    updateAuthUI();
    closeModal();
    toast(t('auth.welcome'));
    navigate('admin');
  } catch (e) {
    err.textContent = e.message;
  }
}

function logout() {
  token = null;
  localStorage.removeItem('token');
  updateAuthUI();
  navigate('home');
  toast(t('auth.loggedOut'));
}

function updateAuthUI() {
  const isLoggedIn = !!token;
  document.getElementById('nav-login-btn').style.display = isLoggedIn ? 'none' : '';
  document.getElementById('nav-logout-btn').style.display = isLoggedIn ? '' : 'none';
  document.getElementById('nav-admin-link').style.display = isLoggedIn ? '' : 'none';
}

// ─── HOME ─────────────────────────────────────────────────────────────────────
async function loadHome() {
  try {
    const poemsData = await apiFetch('/poems?limit=6');
    const poems = poemsData.poems || [];
    const container = document.getElementById('home-poems');
    if (!poems.length) {
      container.innerHTML = `<p style="color:var(--muted);font-style:italic;font-size:1rem">${t('poems.noneHome')}</p>`;
      return;
    }
    container.innerHTML = poems.map(renderPoemCard).join('');
  } catch(e) { console.error(e); }
}

// ─── POEMS LIST ───────────────────────────────────────────────────────────────
async function loadPoems(tag = null, page = 1) {
  currentTag = tag;
  try {
    const tagParam = tag ? `&tag=${encodeURIComponent(tag)}` : '';
    const [poemsData, allTags] = await Promise.all([
      apiFetch(`/poems?page=${page}&limit=10${tagParam}`),
      apiFetch('/poems/tags')
    ]);

    const poems = poemsData.poems || [];
    const total = poemsData.total || 0;
    const totalPages = poemsData.total_pages || 1;
    const currentPage = poemsData.page || 1;

    // Render tags bar
    const tagsBar = document.getElementById('tags-bar');
    tagsBar.innerHTML = [
      `<button class="tag-filter ${!tag ? 'active' : ''}" onclick="loadPoems(null, 1)">${t('poems.all')}</button>`,
      ...allTags.map(tg =>
        `<button class="tag-filter ${tag === tg.name ? 'active' : ''}" onclick="loadPoems('${esc(tg.name)}', 1)">${esc(tg.name)} <span style="opacity:.6">(${tg.count})</span></button>`
      )
    ].join('');

    // Render poem cards
    const list = document.getElementById('poems-list');
    if (!poems.length) {
      list.innerHTML = `<p style="color:var(--muted);font-style:italic;padding:3rem 0">${t('poems.none')}</p>`;
      return;
    }
    list.innerHTML = poems.map(renderPoemCard).join('');

    // Render pagination
    renderPagination(currentPage, totalPages, tag);
  } catch(e) { console.error(e); }
}

function renderPagination(currentPage, totalPages, tag) {
  const paginationContainer = document.getElementById('pagination');
  if (!paginationContainer) {
    // Create pagination container if it doesn't exist
    const list = document.getElementById('poems-list');
    const container = document.createElement('div');
    container.id = 'pagination';
    container.className = 'pagination';
    list.parentNode.insertBefore(container, list.nextSibling);
  }

  const pagination = document.getElementById('pagination');

  if (totalPages <= 1) {
    pagination.innerHTML = '';
    return;
  }

  let pages = [];

  // Previous button
  if (currentPage > 1) {
    pages.push(`<button class="page-btn" onclick="loadPoems(${tag ? `'${esc(tag)}'` : 'null'}, ${currentPage - 1})">←</button>`);
  }

  // Page numbers
  const maxVisible = 5;
  let startPage = Math.max(1, currentPage - Math.floor(maxVisible / 2));
  let endPage = Math.min(totalPages, startPage + maxVisible - 1);

  if (endPage - startPage < maxVisible - 1) {
    startPage = Math.max(1, endPage - maxVisible + 1);
  }

  if (startPage > 1) {
    pages.push(`<button class="page-btn" onclick="loadPoems(${tag ? `'${esc(tag)}'` : 'null'}, 1)">1</button>`);
    if (startPage > 2) {
      pages.push(`<span class="page-ellipsis">...</span>`);
    }
  }

  for (let i = startPage; i <= endPage; i++) {
    const active = i === currentPage ? 'active' : '';
    pages.push(`<button class="page-btn ${active}" onclick="loadPoems(${tag ? `'${esc(tag)}'` : 'null'}, ${i})">${i}</button>`);
  }

  if (endPage < totalPages) {
    if (endPage < totalPages - 1) {
      pages.push(`<span class="page-ellipsis">...</span>`);
    }
    pages.push(`<button class="page-btn" onclick="loadPoems(${tag ? `'${esc(tag)}'` : 'null'}, ${totalPages})">${totalPages}</button>`);
  }

  // Next button
  if (currentPage < totalPages) {
    pages.push(`<button class="page-btn" onclick="loadPoems(${tag ? `'${esc(tag)}'` : 'null'}, ${currentPage + 1})">→</button>`);
  }

  pagination.innerHTML = pages.join('');
}

// ─── SINGLE POEM ──────────────────────────────────────────────────────────────
async function loadPoem(uuid) {
  const container = document.getElementById('poem-detail');
  container.innerHTML = `<p style="padding:4rem 0;color:var(--muted);font-style:italic">${t('poems.loading')}</p>`;
  try {
    const poem = await apiFetch(`/poems/uuid/${uuid}`);
    const comments = await apiFetch(`/comments/${poem.id}`);

    const adminActions = token ? `
      <div class="poem-admin-actions">
        <button class="btn-secondary" onclick="openEditPoem(${poem.id})">${t('admin.edit')}</button>
        <button class="btn-danger" onclick="deletePoem(${poem.id})">${t('admin.delete')}</button>
      </div>` : '';

    const imageBlock = poem.image_url
      ? `<img class="poem-image" src="${esc(poem.image_url)}" alt="${esc(poem.title || t('poems.untitled'))}">`
      : '';

    const layoutClass = poem.image_url ? 'poem-layout' : 'poem-layout no-image';

    container.innerHTML = `
      <div class="poem-back" onclick="navigate('poems')">${t('poems.back')}</div>
      <div class="${layoutClass}">
        ${imageBlock}
        <div class="poem-text">
          <h1 class="poem-full-title ${!poem.title ? 'untitled' : ''}">${poem.title || t('poems.untitled')}</h1>
          <div class="poem-full-meta">
            ${poem.tags.map(tg => `<span class="tag" onclick="navigate('poems');setTimeout(()=>loadPoems('${esc(tg)}', 1),50)">${esc(tg)}</span>`).join('')}
            <span class="poem-date">${fmtDateTime(poem.created_at)}</span>
          </div>
          <div class="poem-body">${esc(poem.body)}</div>
          ${adminActions}
        </div>
      </div>
      <div class="comments-section">
        <h3>${t('comments.title', { count: comments.length })}</h3>
        <div id="comments-list">${renderComments(comments, poem.id)}</div>
        <form class="comment-form" onsubmit="addComment(event, ${poem.id})">
          <input type="text" id="comment-author" placeholder="${t('comments.namePlaceholder')}" maxlength="80">
          <textarea id="comment-body" rows="3" placeholder="${t('comments.bodyPlaceholder')}" required></textarea>
          <button class="btn-primary" type="submit">${t('comments.post')}</button>
        </form>
      </div>
    `;
  } catch(e) {
    container.innerHTML = `<p style="padding:4rem;color:var(--muted)">${t('poems.notFound')}</p>`;
  }
}

function renderComments(comments, poemId) {
  if (!comments.length) return `<p style="color:var(--muted);font-style:italic;font-size:.95rem;margin-bottom:1.5rem">${t('comments.empty')}</p>`;
  return comments.map(c => `
    <div class="comment" id="comment-${c.id}">
      <div class="comment-author">${esc(c.author)}</div>
      <div class="comment-body">${esc(c.body)}</div>
      <div class="comment-date">${fmtDateTime(c.created_at)}</div>
      ${token ? `<span class="comment-delete" onclick="deleteComment(${c.id}, ${poemId})">✕</span>` : ''}
    </div>
  `).join('');
}

async function addComment(e, poemId) {
  e.preventDefault();
  const author = document.getElementById('comment-author').value.trim() || t('comments.anonymous');
  const body = document.getElementById('comment-body').value.trim();
  if (!body) return;
  try {
    await apiFetch(`/comments/${poemId}`, {
      method: 'POST',
      body: JSON.stringify({ author, body })
    });
    document.getElementById('comment-author').value = '';
    document.getElementById('comment-body').value = '';
    const comments = await apiFetch(`/comments/${poemId}`);
    document.getElementById('comments-list').innerHTML = renderComments(comments, poemId);
    toast(t('comments.posted'));
  } catch(e) { toast(t('comments.postError'), true); }
}

async function deleteComment(commentId, poemId) {
  console.log('[Comment] Deleting comment:', commentId, 'from poem:', poemId);
  if (!confirm(t('comments.deleteConfirm'))) return;
  try {
    await apiFetch(`/comments/${commentId}`, { method: 'DELETE' });
    if (!poemId) {
      console.warn('[Comment] poemId is undefined!');
      return;
    }
    const comments = await apiFetch(`/comments/${poemId}`);
    document.getElementById('comments-list').innerHTML = renderComments(comments, poemId);
    toast(t('comments.deleted'));
  } catch(e) {
    console.error('[Comment] Error:', e);
    toast(t('generic.error'), true);
  }
}

async function deleteCommentFromAdmin(commentId) {
  console.log('[Admin] Deleting comment:', commentId);
  if (!confirm(t('comments.deleteConfirm'))) return;
  try {
    console.log('[Admin] Sending DELETE request for comment:', commentId);
    const response = await apiFetch(`/comments/${commentId}`, { method: 'DELETE' });
    console.log('[Admin] Delete response:', response);
    toast(t('comments.deleted'));
    console.log('[Admin] Reloading comments list...');
    await loadAdminComments();
    console.log('[Admin] Comments list reloaded');
  } catch(e) {
    console.error('[Admin] Error deleting comment:', e);
    toast(t('generic.error'), true);
  }
}

// ─── ABOUT ────────────────────────────────────────────────────────────────────
async function loadAbout() {
  try {
    const data = await apiFetch('/about');
    const container = document.getElementById('about-content');
    const photo = data.photo_url
      ? `<img src="${esc(data.photo_url)}" class="about-photo" alt="${esc(data.name)}">`
      : '';
    const editBtn = token
      ? `<button class="btn-secondary about-edit-btn" onclick="navigate('admin');setTimeout(()=>adminTab('about'),100)">${t('about.edit')}</button>`
      : '';
    container.innerHTML = `
      ${photo}
      <h1 class="about-name">${esc(data.name)}</h1>
      <div class="about-bio">${esc(data.bio)}</div>
      ${editBtn}
    `;
  } catch(e) { console.error(e); }
}

// ─── ADMIN ────────────────────────────────────────────────────────────────────
function adminTab(name) {
  document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
  document.querySelectorAll('.admin-panel').forEach(p => p.style.display = 'none');
  event.target.classList.add('active');
  document.getElementById(`admin-${name}`).style.display = '';
  if (name === 'comments') {
    loadAdminComments();
  }
}

// Admin poems list
async function loadAdminPoems() {
  try {
    const poemsData = await apiFetch('/poems?limit=1000');
    const poems = poemsData.poems || [];
    const list = document.getElementById('admin-poems-list');
    if (!poems.length) {
      list.innerHTML = `<p style="color:var(--muted);font-style:italic;padding:1rem 0">${t('admin.none')}</p>`;
      return;
    }
    list.innerHTML = poems.map(p => `
      <div class="admin-poem-item ${p.is_draft ? 'admin-poem-item-draft' : ''}">
        ${p.is_draft ? `<span class="admin-poem-draft-badge">${t('admin.draft')}</span>` : ''}
        <span class="admin-poem-item-title ${!p.title ? '' : ''}">${p.title || `<em>${t('poems.untitledShort')}</em>`}</span>
        <div class="admin-poem-item-tags">${p.tags.map(tg => `<span class="tag">${esc(tg)}</span>`).join('')}</div>
        <div class="admin-poem-item-actions">
          <button class="btn-secondary" onclick="openEditPoem(${p.id})">${t('admin.edit')}</button>
          <button class="btn-danger" onclick="deletePoem(${p.id})">${t('admin.delete')}</button>
        </div>
      </div>
    `).join('');
  } catch(e) { console.error(e); }
}

// Admin comments list
async function loadAdminComments() {
  try {
    console.log('[Admin] Loading all comments...');
    const comments = await apiFetch('/comments/admin/all');
    console.log('[Admin] Loaded comments:', comments.length);
    const list = document.getElementById('admin-comments-list');
    if (!comments.length) {
      list.innerHTML = `<p style="color:var(--muted);font-style:italic;padding:1rem 0">${t('admin.comments.none')}</p>`;
      return;
    }
    list.innerHTML = comments.map(c => `
      <div class="admin-comment-item">
        <div class="admin-comment-header">
          <span class="admin-comment-author">${esc(c.author)}</span>
          <span class="admin-comment-date">${fmtDateTime(c.created_at)}</span>
        </div>
        <div class="admin-comment-body">${esc(c.body)}</div>
        <div class="admin-comment-footer">
          <a href="/poems/${c.poem_uuid}" onclick="navigate('poems');setTimeout(()=>loadPoem('${c.poem_uuid}'),100)" class="admin-comment-poem-link">
            📖 ${esc(c.poem_title)} →
          </a>
          <button class="btn-danger btn-small" onclick="deleteCommentFromAdmin(${c.id})">${t('admin.delete')}</button>
        </div>
      </div>
    `).join('');
    console.log('[Admin] Comments list updated');
  } catch(e) {
    console.error('[Admin] Error loading comments:', e);
  }
}

// Show new poem form
function showPoemForm(poem = null) {
  editingPoemId = poem ? poem.id : null;
  const form = document.getElementById('admin-poem-form');
  const imagePreview = poem?.image_url
    ? `<div class="poem-image-preview"><img src="${esc(poem.image_url)}" alt="${esc(poem.title || t('poems.untitled'))}"></div>`
    : '';
  const removeBtn = poem?.image_url
    ? `<button class="btn-danger btn-small" type="button" onclick="removePoemImage()">${t('admin.form.imageRemove')}</button>`
    : '';
  form.style.display = '';
  form.innerHTML = `
    <div class="poem-form">
      <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 1.5rem;">
        <h3 style="font-family:'IM Fell English',serif;font-size:1.4rem;margin:0">${poem ? t('admin.editPoemTitle') : t('admin.newPoemTitle')}</h3>
        <label style="display: flex; align-items: center; gap: 0.5rem; margin: 0; font-family: 'Montserrat', sans-serif; font-size: 0.7rem; font-weight: 500; letter-spacing: 0.1em; text-transform: uppercase; color: var(--muted); width: 20%;">
          <input type="checkbox" id="pf-draft" style="width: 20%; min-width: 18px;" ${poem?.is_draft ? 'checked' : ''}>
          <span style="width: 80%;">${t('admin.form.draftLabel')}</span>
        </label>
      </div>
        </label>
      </div>
      <label>${t('admin.form.titleLabel')}
        <input type="text" id="pf-title" value="${esc(poem?.title || '')}" placeholder="${t('admin.form.titlePlaceholder')}">
      </label>
      <label>${t('admin.form.bodyLabel')}
        <textarea id="pf-body" rows="12" placeholder="${t('admin.form.bodyPlaceholder')}" required>${esc(poem?.body || '')}</textarea>
      </label>
      <label>${t('admin.form.tagsLabel')}
        <input type="text" id="pf-tags" value="${esc((poem?.tags || []).join(', '))}" placeholder="${t('admin.form.tagsPlaceholder')}">
      </label>
      <label>${t('admin.form.imageLabel')}
        <input type="file" id="pf-image" accept="image/jpeg,image/png" onchange="previewPoemImage(event)">
      </label>
      <div id="pf-image-preview">${imagePreview}</div>
      ${removeBtn}
      ${editingPoemId ? `<button class="btn-secondary btn-small" type="button" onclick="showVersionHistory(${editingPoemId})" data-i18n="admin.versions.button">📜 Version History</button>` : ''}
      <div class="poem-form-actions">
        <button class="btn-primary" onclick="savePoem()">${poem ? t('admin.form.save') : t('admin.form.publish')}</button>
        <button class="btn-secondary" onclick="closePoemForm()">${t('admin.form.cancel')}</button>
      </div>
    </div>
  `;
  form.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

function closePoemForm() {
  document.getElementById('admin-poem-form').style.display = 'none';
  editingPoemId = null;
}

async function openEditPoem(id) {
  try {
    const poem = await apiFetch(`/poems/${id}`);
    // If we're on poem detail page, go to admin
    if (document.getElementById('page-admin').classList.contains('active')) {
      showPoemForm(poem);
    } else {
      navigate('admin');
      setTimeout(() => showPoemForm(poem), 100);
    }
  } catch(e) { toast(t('admin.loadError'), true); }
}

async function savePoem() {
  const title = document.getElementById('pf-title').value.trim();
  const body = document.getElementById('pf-body').value.trim();
  const tagsRaw = document.getElementById('pf-tags').value;
  const tags = tagsRaw.split(',').map(tg => tg.trim()).filter(Boolean);
  const is_draft = document.getElementById('pf-draft').checked ? 1 : 0;
  const imageFile = document.getElementById('pf-image').files[0];
  if (!body) { toast(t('admin.form.bodyRequired'), true); return; }
  if (imageFile) {
    if (!['image/jpeg', 'image/png'].includes(imageFile.type)) {
      toast(t('admin.form.imageTypeError'), true);
      return;
    }
    if (imageFile.size > 1024 * 1024) {
      toast(t('admin.form.imageTooLarge'), true);
      return;
    }
  }
  try {
    let poem;
    if (editingPoemId) {
      poem = await apiFetch(`/poems/${editingPoemId}`, {
        method: 'PUT',
        body: JSON.stringify({ title, body, tags, is_draft })
      });
      toast(t('admin.poemUpdated'));
    } else {
      poem = await apiFetch('/poems', {
        method: 'POST',
        body: JSON.stringify({ title, body, tags, is_draft })
      });
      toast(t('admin.poemPublished'));
    }

    if (imageFile) {
      try {
        await uploadPoemImage(poem.id, imageFile);
      } catch (e) {
        toast(t('admin.form.imageUploadError'), true);
      }
    }

    closePoemForm();
    loadAdminPoems();
  } catch(e) { toast(t('admin.saveError'), true); }
}

async function uploadPoemImage(poemId, file) {
  const formData = new FormData();
  formData.append('file', file);
  const headers = token ? { 'Authorization': `Bearer ${token}` } : {};
  const res = await fetch(API + `/poems/${poemId}/image`, {
    method: 'POST',
    headers,
    body: formData
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || res.statusText);
  }
  return res.json();
}

async function removePoemImage() {
  const preview = document.getElementById('pf-image-preview');
  if (!editingPoemId) {
    document.getElementById('pf-image').value = '';
    preview.innerHTML = '';
    return;
  }
  try {
    await apiFetch(`/poems/${editingPoemId}/image`, { method: 'DELETE' });
    preview.innerHTML = '';
  } catch (e) {
    toast(t('admin.form.imageDeleteError'), true);
  }
}

async function deletePoem(poemId) {
  if (!confirm(t('admin.deleteConfirm'))) return;

  try {
    await apiFetch(`/poems/${poemId}`, { method: 'DELETE' });
    toast(t('admin.deleted'));
    loadAdminPoems();
  } catch(e) {
    toast(t('admin.deleteError'), true);
  }
}

// Version history
async function showVersionHistory(poemId) {
  try {
    const data = await apiFetch(`/poems/${poemId}/versions`);
    const modal = document.createElement('div');
    modal.className = 'version-history-modal';
    modal.innerHTML = `
      <div class="modal version-history" style="display: block; top: 50%; left: 50%; transform: translate(-50%, -50%); max-width: 600px; max-height: 80vh; overflow-y: auto;">
        <h2 style="font-size:1.3rem;margin-bottom:1.5rem" data-i18n="admin.versions.title">${t('admin.versions.title')}</h2>
        <button class="btn-secondary" style="position:absolute;top:1rem;right:1rem;padding:0.4rem 0.8rem;font-size:0.9rem" onclick="this.closest('.version-history-modal').remove();document.querySelector('.version-history-overlay').remove()">✕</button>
        ${renderVersionsList(data)}
      </div>
    `;

    const overlay = document.createElement('div');
    overlay.className = 'modal-overlay version-history-overlay';
    overlay.style.display = 'block';
    overlay.onclick = () => { modal.remove(); overlay.remove(); };

    document.body.appendChild(overlay);
    document.body.appendChild(modal);
  } catch(e) {
    toast(t('admin.versions.loadError'), true);
  }
}

function renderVersionsList(data) {
  const versions = [data.current_version, ...data.history];
  return `
    <div style="display:grid;gap:1rem">
      ${versions.map(v => `
        <div style="border:1px solid var(--border);padding:1rem;border-radius:2px">
          <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.8rem">
            <span style="font-weight:500;font-size:0.9rem">Version ${v.version_number}${v.is_current ? ` <span data-i18n="admin.versions.current">(${t('admin.versions.current')})</span>` : ''}</span>
            <span style="font-size:0.8rem;color:var(--muted)">${fmtDateTime(v.created_at)}</span>
          </div>
          <div style="margin-bottom:0.8rem;padding:0.8rem;background:var(--parchment);border-radius:2px;font-size:0.9rem;max-height:120px;overflow-y:auto">
            <strong>${v.title || '— untitled —'}</strong>
            <div style="font-style:italic;color:var(--muted);white-space:pre-wrap;margin-top:0.4rem">${v.body.slice(0, 200)}</div>
          </div>
          ${!v.is_current ? `<button class="btn-secondary btn-small" onclick="restoreVersion(${data.poem_id}, ${v.version_number})" data-i18n="admin.versions.restore">${t('admin.versions.restore')}</button>` : `<span style="color:var(--muted);font-size:0.9rem" data-i18n="admin.versions.latest">${t('admin.versions.latest')}</span>`}
        </div>
      `).join('')}
    </div>
  `;
}

async function restoreVersion(poemId, versionNumber) {
  if (!confirm(t('admin.versions.confirmRestore', { version: versionNumber }))) return;

  try {
    const result = await apiFetch(`/poems/${poemId}/restore/${versionNumber}`, { method: 'POST' });
    toast(result.message);
    document.querySelectorAll('.version-history-modal, .version-history-overlay').forEach(el => el.remove());
    openEditPoem(poemId);
  } catch(e) {
    toast(t('admin.versions.restoreError'), true);
  }
}

function previewPoemImage(event) {
  const file = event.target.files[0];
  const preview = document.getElementById('pf-image-preview');
  if (!file) {
    preview.innerHTML = '';
    return;
  }
  const reader = new FileReader();
  reader.onload = () => {
    preview.innerHTML = `<div class="poem-image-preview"><img src="${reader.result}" alt="preview"></div>`;
  };
  reader.readAsDataURL(file);
}


// Export poems to JSON
async function exportPoems() {
  try {
    const headers = token ? { 'Authorization': `Bearer ${token}` } : {};
    const res = await fetch(API + '/poems/export/poems', { headers });
    if (!res.ok) throw new Error('Export failed');
    const blob = await res.blob();
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `poems-export-${new Date().toISOString().split('T')[0]}.zip`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    toast('Exported poems');
  } catch(e) {
    toast('Export failed', true);
    console.error(e);
  }
}

// Export comments to JSON
async function exportComments() {
  try {
    const data = await apiFetch('/poems/export/comments');
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `comments-export-${new Date().toISOString().split('T')[0]}.json`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    toast(`Exported ${data.total} comments`);
  } catch(e) {
    toast('Export failed', true);
    console.error(e);
  }
}

// Show import dialog
function showImportPoems() {
  const input = document.createElement('input');
  input.type = 'file';
  input.accept = 'application/zip,.zip';
  input.onchange = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    if (!confirm(`Import poems from ${file.name}? This will add them to your collection.`)) {
      return;
    }

    try {
      const formData = new FormData();
      formData.append('file', file);
      const headers = token ? { 'Authorization': `Bearer ${token}` } : {};
      const res = await fetch(API + '/poems/import', {
        method: 'POST',
        headers,
        body: formData
      });
      if (!res.ok) {
        const err = await res.json().catch(() => ({}));
        throw new Error(err.detail || 'Import failed');
      }
      const result = await res.json();
      const msg = `Imported ${result.imported_poems} poems and ${result.imported_comments} comments`;
      toast(msg);
      if (result.errors.length > 0) {
        console.warn('Import errors:', result.errors);
      }
      loadAdminPoems();
    } catch(e) {
      toast('Import failed: ' + e.message, true);
      console.error(e);
    }
  };
  input.click();
}


// About form
async function loadAboutForm() {
  try {
    const data = await apiFetch('/about');
    document.getElementById('about-name').value = data.name || '';
    document.getElementById('about-photo').value = data.photo_url || '';
    document.getElementById('about-bio').value = data.bio || '';
  } catch(e) {}
}

async function saveAbout(e) {
  e.preventDefault();

  const name = document.getElementById('about-name').value.trim();
  const photo_url = document.getElementById('about-photo').value.trim() || null;
  const bio = document.getElementById('about-bio').value.trim();

  try {
    await apiFetch('/about', {
      method: 'PUT',
      body: JSON.stringify({
        name: name || null,
        photo_url: photo_url,
        bio: bio || null
      })
    });

    toast(t('about.saved'));
    loadAbout();
  } catch(e) {
    toast(t('about.saveError'), true);
  }
}

function renderPoemCard(p) {
  const image = p.image_url
    ? `<div class="poem-card-image"><img src="${esc(p.image_url)}" alt="${esc(p.title || t('poems.untitled'))}"></div>`
    : '';
  const commentBadge = p.comment_count > 0
    ? `<div class="poem-card-comments">${p.comment_count}</div>`
    : '';
  return `
    <div class="poem-card" onclick="navigate('poem', true, '${esc(p.uuid)}')">
      ${commentBadge}
      ${image}
      <div class="poem-card-title ${!p.title ? 'untitled' : ''}">${p.title || t('poems.untitled')}</div>
      <div class="poem-card-preview">${esc(p.body.slice(0, 200))}</div>
      <div class="poem-card-meta">
        ${p.tags.map(tg => `<span class="tag" onclick="event.stopPropagation();navigate('poems');setTimeout(()=>loadPoems('${esc(tg)}', 1),50)">${esc(tg)}</span>`).join('')}
        <span class="poem-date">${fmtDateTime(p.created_at)}</span>
      </div>
    </div>
  `;
}

function esc(str) {
  if (!str) return '';
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}

function fmtDate(iso) {
  if (!iso) return '';
  const locale = currentLang === 'ru' ? 'ru-RU' : 'en-US';
  return new Date(iso).toLocaleDateString(locale, { year: 'numeric', month: 'long', day: 'numeric' });
}

function fmtDateTime(iso) {
  if (!iso) return '';
  const locale = currentLang === 'ru' ? 'ru-RU' : 'en-US';
  return new Date(iso).toLocaleString(locale, {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  });
}

let toastTimer;
function toast(msg, isError = false) {
  const el = document.getElementById('toast');
  el.textContent = msg;
  el.style.background = isError ? 'var(--rust)' : 'var(--ink)';
  el.classList.add('show');
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => el.classList.remove('show'), 3000);
}

function showLoginModal() {
  document.getElementById('modal-overlay').classList.add('open');
  document.getElementById('login-modal').classList.add('open');
  setTimeout(() => document.getElementById('login-user').focus(), 100);
}

function closeModal() {
  document.getElementById('modal-overlay').classList.remove('open');
  document.getElementById('login-modal').classList.remove('open');
}
