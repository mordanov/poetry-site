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
    'comments.postError': 'Error posting comment',
    'comments.deleteConfirm': 'Delete this comment?',
    'comments.deleted': 'Comment deleted',
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
    'admin.tabs.password': 'Password',
    'admin.newPoem': '+ New Poem',
    'admin.exportPoems': '📥 Export Poems',
    'admin.importPoems': '📤 Import Poems',
    'admin.exportComments': '💬 Export Comments',
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
    'admin.form.save': 'Save changes',
    'admin.form.publish': 'Publish',
    'admin.form.cancel': 'Cancel',
    'admin.form.bodyRequired': 'Body is required',
    'admin.poemUpdated': 'Poem updated',
    'admin.poemPublished': 'Poem published',
    'admin.loadError': 'Error loading poem',
    'admin.saveError': 'Error saving poem',
    'admin.deleteConfirm': 'Delete this poem and all its comments?',
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
    'comments.deleteConfirm': 'Удалить этот комментарий?',
    'comments.deleted': 'Комментарий удален',
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
    'admin.tabs.password': 'Пароль',
    'admin.newPoem': '+ Новый стих',
    'admin.exportPoems': '📥 Экспорт стихов',
    'admin.importPoems': '📤 Импорт стихов',
    'admin.exportComments': '💬 Экспорт комментариев',
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
    'admin.form.save': 'Сохранить',
    'admin.form.publish': 'Опубликовать',
    'admin.form.cancel': 'Отмена',
    'admin.form.bodyRequired': 'Текст обязателен',
    'admin.poemUpdated': 'Стих обновлен',
    'admin.poemPublished': 'Стих опубликован',
    'admin.loadError': 'Ошибка загрузки стиха',
    'admin.saveError': 'Ошибка сохранения',
    'admin.deleteConfirm': 'Удалить стих и все комментарии?',
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
    const poems = await apiFetch('/poems');
    const container = document.getElementById('home-poems');
    const latest = poems.slice(0, 6);
    if (!latest.length) {
      container.innerHTML = `<p style="color:var(--muted);font-style:italic;font-size:1rem">${t('poems.noneHome')}</p>`;
      return;
    }
    container.innerHTML = latest.map(renderPoemCard).join('');
  } catch(e) { console.error(e); }
}

// ─── POEMS LIST ───────────────────────────────────────────────────────────────
async function loadPoems(tag = null) {
  currentTag = tag;
  try {
    const [poems, allTags] = await Promise.all([
      apiFetch('/poems' + (tag ? `?tag=${encodeURIComponent(tag)}` : '')),
      apiFetch('/poems/tags')
    ]);

    // Render tags bar
    const tagsBar = document.getElementById('tags-bar');
    tagsBar.innerHTML = [
      `<button class="tag-filter ${!tag ? 'active' : ''}" onclick="loadPoems()">${t('poems.all')}</button>`,
      ...allTags.map(tg =>
        `<button class="tag-filter ${tag === tg.name ? 'active' : ''}" onclick="loadPoems('${esc(tg.name)}')">${esc(tg.name)} <span style="opacity:.6">(${tg.count})</span></button>`
      )
    ].join('');

    // Render poem rows
    const list = document.getElementById('poems-list');
    if (!poems.length) {
      list.innerHTML = `<p style="color:var(--muted);font-style:italic;padding:3rem 0">${t('poems.none')}</p>`;
      return;
    }
    list.innerHTML = poems.map(p => `
      <div class="poem-row" onclick="navigate('poem', true, ${p.id})">
        <div>
          <div class="poem-row-title ${!p.title ? 'untitled' : ''}">${p.title || t('poems.untitled')}</div>
          <div class="poem-row-preview">${esc(p.body.slice(0, 120))}</div>
        </div>
        <div class="poem-row-right">
          <div class="poem-row-tags">${p.tags.map(tg => `<span class="tag" onclick="event.stopPropagation();loadPoems('${esc(tg)}')">${esc(tg)}</span>`).join('')}</div>
          <div class="poem-row-date">${fmtDate(p.created_at)}</div>
        </div>
      </div>
    `).join('');
  } catch(e) { console.error(e); }
}

// ─── SINGLE POEM ──────────────────────────────────────────────────────────────
async function loadPoem(id) {
  const container = document.getElementById('poem-detail');
  container.innerHTML = `<p style="padding:4rem 0;color:var(--muted);font-style:italic">${t('poems.loading')}</p>`;
  try {
    const [poem, comments] = await Promise.all([
      apiFetch(`/poems/${id}`),
      apiFetch(`/comments/${id}`)
    ]);

    const adminActions = token ? `
      <div class="poem-admin-actions">
        <button class="btn-secondary" onclick="openEditPoem(${poem.id})">${t('admin.edit')}</button>
        <button class="btn-danger" onclick="deletePoem(${poem.id})">${t('admin.delete')}</button>
      </div>` : '';

    container.innerHTML = `
      <div class="poem-back" onclick="navigate('poems')">${t('poems.back')}</div>
      <h1 class="poem-full-title ${!poem.title ? 'untitled' : ''}">${poem.title || t('poems.untitled')}</h1>
      <div class="poem-full-meta">
        ${poem.tags.map(tg => `<span class="tag" onclick="navigate('poems');setTimeout(()=>loadPoems('${esc(tg)}'),50)">${esc(tg)}</span>`).join('')}
        <span class="poem-date">${fmtDate(poem.created_at)}</span>
      </div>
      <div class="poem-body">${esc(poem.body)}</div>
      ${adminActions}
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
      <div class="comment-date">${fmtDate(c.created_at)}</div>
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
  if (!confirm(t('comments.deleteConfirm'))) return;
  try {
    await apiFetch(`/comments/${commentId}`, { method: 'DELETE' });
    const comments = await apiFetch(`/comments/${poemId}`);
    document.getElementById('comments-list').innerHTML = renderComments(comments, poemId);
    toast(t('comments.deleted'));
  } catch(e) { toast(t('generic.error'), true); }
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
}

// Admin poems list
async function loadAdminPoems() {
  try {
    const poems = await apiFetch('/poems');
    const list = document.getElementById('admin-poems-list');
    if (!poems.length) {
      list.innerHTML = `<p style="color:var(--muted);font-style:italic;padding:1rem 0">${t('admin.none')}</p>`;
      return;
    }
    list.innerHTML = poems.map(p => `
      <div class="admin-poem-item">
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

// Show new poem form
function showPoemForm(poem = null) {
  editingPoemId = poem ? poem.id : null;
  const form = document.getElementById('admin-poem-form');
  form.style.display = '';
  form.innerHTML = `
    <div class="poem-form">
      <h3 style="font-family:'IM Fell English',serif;font-size:1.4rem;margin-bottom:1.5rem">${poem ? t('admin.editPoemTitle') : t('admin.newPoemTitle')}</h3>
      <label>${t('admin.form.titleLabel')}
        <input type="text" id="pf-title" value="${esc(poem?.title || '')}" placeholder="${t('admin.form.titlePlaceholder')}">
      </label>
      <label>${t('admin.form.bodyLabel')}
        <textarea id="pf-body" rows="12" placeholder="${t('admin.form.bodyPlaceholder')}" required>${esc(poem?.body || '')}</textarea>
      </label>
      <label>${t('admin.form.tagsLabel')}
        <input type="text" id="pf-tags" value="${esc((poem?.tags || []).join(', '))}" placeholder="${t('admin.form.tagsPlaceholder')}">
      </label>
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
  if (!body) { toast(t('admin.form.bodyRequired'), true); return; }
  try {
    if (editingPoemId) {
      await apiFetch(`/poems/${editingPoemId}`, {
        method: 'PUT',
        body: JSON.stringify({ title, body, tags })
      });
      toast(t('admin.poemUpdated'));
    } else {
      await apiFetch('/poems', {
        method: 'POST',
        body: JSON.stringify({ title, body, tags })
      });
      toast(t('admin.poemPublished'));
    }
    closePoemForm();
    loadAdminPoems();
  } catch(e) { toast(t('admin.saveError'), true); }
}

async function deletePoem(id) {
  if (!confirm(t('admin.deleteConfirm'))) return;
  try {
    await apiFetch(`/poems/${id}`, { method: 'DELETE' });
    toast(t('admin.deleted'));
    if (document.getElementById('page-poem').classList.contains('active')) {
      navigate('poems');
    } else {
      loadAdminPoems();
    }
  } catch(e) { toast(t('admin.deleteError'), true); }
}

// Export poems to JSON
async function exportPoems() {
  try {
    const data = await apiFetch('/poems/export/all');
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `poems-export-${new Date().toISOString().split('T')[0]}.json`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    toast(`Exported ${data.total} poems`);
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
  input.accept = 'application/json,.json';
  input.onchange = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    try {
      const text = await file.text();
      const data = JSON.parse(text);

      if (!data.poems || !Array.isArray(data.poems)) {
        toast('Invalid file format: expected {poems: [...]}', true);
        return;
      }

      if (!confirm(`Import ${data.poems.length} poems? This will add them to your collection.`)) {
        return;
      }

      const result = await apiFetch('/poems/import/all', {
        method: 'POST',
        body: JSON.stringify(data)
      });

      toast(`Imported ${result.imported} of ${result.total_attempted} poems`);
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
  const name = document.getElementById('about-name').value;
  const photo_url = document.getElementById('about-photo').value;
  const bio = document.getElementById('about-bio').value;
  try {
    await apiFetch('/about', { method: 'PUT', body: JSON.stringify({ name, photo_url, bio }) });
    toast(t('about.saved'));
  } catch(e) { toast(t('about.saveError'), true); }
}

async function changePassword(e) {
  e.preventDefault();
  const current = document.getElementById('pw-current').value;
  const newPw = document.getElementById('pw-new').value;
  const confirm = document.getElementById('pw-confirm').value;
  if (newPw !== confirm) { toast(t('password.mismatch'), true); return; }
  try {
    await apiFetch('/auth/change-password', {
      method: 'POST',
      body: JSON.stringify({ current_password: current, new_password: newPw })
    });
    toast(t('password.changed'));
    e.target.reset();
  } catch(e) { toast(e.message || t('generic.error'), true); }
}

// ─── LOGIN MODAL ──────────────────────────────────────────────────────────────
function showLoginModal() {
  document.getElementById('modal-overlay').classList.add('open');
  document.getElementById('login-modal').classList.add('open');
  setTimeout(() => document.getElementById('login-user').focus(), 100);
}
function closeModal() {
  document.getElementById('modal-overlay').classList.remove('open');
  document.getElementById('login-modal').classList.remove('open');
}

// ─── UTILS ────────────────────────────────────────────────────────────────────
function renderPoemCard(p) {
  return `
    <div class="poem-card" onclick="navigate('poem', true, ${p.id})">
      <div class="poem-card-title ${!p.title ? 'untitled' : ''}">${p.title || t('poems.untitled')}</div>
      <div class="poem-card-preview">${esc(p.body.slice(0, 200))}</div>
      <div class="poem-card-meta">
        ${p.tags.map(tg => `<span class="tag" onclick="event.stopPropagation();navigate('poems');setTimeout(()=>loadPoems('${esc(tg)}'),50)">${esc(tg)}</span>`).join('')}
        <span class="poem-date">${fmtDate(p.created_at)}</span>
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

let toastTimer;
function toast(msg, isError = false) {
  const el = document.getElementById('toast');
  el.textContent = msg;
  el.style.background = isError ? 'var(--rust)' : 'var(--ink)';
  el.classList.add('show');
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => el.classList.remove('show'), 3000);
}

