/* Behaviour for the static product pages under /products/.
   The quote list is shared with the main site through localStorage (key az_quote_v1),
   so anything added here shows up in the quote drawer and contact form on the home page. */
(function () {
  var KEY = 'az_quote_v1';
  function $(id) { return document.getElementById(id); }
  function load() { try { var c = JSON.parse(localStorage.getItem(KEY) || '[]'); return Array.isArray(c) ? c : []; } catch (e) { return []; } }
  function save(c) { try { localStorage.setItem(KEY, JSON.stringify(c)); } catch (e) {} }

  /* mobile nav */
  var nav = document.querySelector('.site-nav'), burger = $('nav-burger');
  function closeNav() { if (nav) nav.classList.remove('open'); if (burger) burger.setAttribute('aria-expanded', 'false'); }
  if (burger) burger.addEventListener('click', function () {
    nav.classList.toggle('open');
    burger.setAttribute('aria-expanded', nav.classList.contains('open') ? 'true' : 'false');
  });
  document.addEventListener('click', function (e) { if (nav && nav.classList.contains('open') && !nav.contains(e.target)) closeNav(); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') closeNav(); });

  /* quote-list indicators (nav pill, bottom bar, button state) */
  function refresh() {
    var c = load(), n = c.length, pill = $('nav-quote'), bar = $('qbar'), form = $('add-form'), btn = $('add-btn');
    if (pill) { pill.hidden = !n; $('nav-quote-n').textContent = n; }
    if (bar) {
      bar.hidden = !n;
      $('qbar-n').textContent = n;
      $('qbar-w').textContent = n === 1 ? 'item' : 'items';
      document.body.classList.toggle('has-qbar', n > 0);
    }
    if (form && btn) {
      var inList = false;
      for (var i = 0; i < c.length; i++) if (c[i].pkey === form.getAttribute('data-pkey')) inList = true;
      btn.textContent = inList ? 'In your list · Add more' : 'Add to quote list';
      btn.classList.toggle('done', inList);
    }
  }

  var timer;
  function toast(msg) {
    var t = $('toast'); if (!t) return;
    $('toast-msg').textContent = msg;
    t.classList.add('show'); clearTimeout(timer);
    timer = setTimeout(function () { t.classList.remove('show'); }, 3500);
  }

  /* add to quote list */
  var form = $('add-form');
  if (form) {
    var qty = $('qty');
    var steps = form.querySelectorAll('[data-d]');
    for (var i = 0; i < steps.length; i++) steps[i].addEventListener('click', function () {
      qty.value = Math.max(1, (parseInt(qty.value, 10) || 1) + parseInt(this.getAttribute('data-d'), 10));
    });
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var sizeEl = form.elements.namedItem('size'), ratingEl = form.elements.namedItem('rating'), noteEl = form.elements.namedItem('note');
      var size = sizeEl ? sizeEl.value : 'Standard', rating = ratingEl ? ratingEl.value : '';
      var q = Math.max(1, parseInt(qty.value, 10) || 1), note = noteEl ? noteEl.value.trim() : '';
      var pkey = form.getAttribute('data-pkey'), name = form.getAttribute('data-name');
      var item = { key: pkey + '|' + size + '|' + rating, pkey: pkey, name: name, fam: form.getAttribute('data-fam'), img: form.getAttribute('data-img'), size: size, rating: rating, qty: q, note: note };
      var c = load(), ex = null;
      for (var j = 0; j < c.length; j++) if (c[j].key === item.key) ex = c[j];
      if (ex) { ex.qty += q; if (note) ex.note = note; } else c.push(item);
      save(c); refresh();
      toast('Added: ' + name + (size && size !== 'Other / not sure' && size !== 'Standard' ? ' · ' + size : ''));
      qty.value = 1; if (noteEl) noteEl.value = '';
    });
  }
  refresh();
  window.addEventListener('storage', function (e) { if (e.key === KEY) refresh(); });
})();
