(() => {
  'use strict';
  document.querySelectorAll('table').forEach(table => {
    const wrapper = document.createElement('div'); wrapper.className = 'table-scroll'; wrapper.tabIndex = 0;
    wrapper.setAttribute('role', 'region'); wrapper.setAttribute('aria-label', 'Tabla de referencia');
    table.before(wrapper); wrapper.append(table);
  });
  function revealAnchor() {
    const target = document.getElementById(decodeURIComponent(location.hash.slice(1)));
    if (target?.matches('details')) { target.open = true; target.scrollIntoView(); }
  }
  window.addEventListener('hashchange', revealAnchor); revealAnchor();
  const form = document.querySelector('.filters');
  if (!form) return;
  const query = document.getElementById('query'), group = document.getElementById('group');
  const format = document.getElementById('format'), type = document.getElementById('type');
  const accounts = [...document.querySelectorAll('.account')];
  const norm = s => s.normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase();
  function filter() {
    let count = 0, accountCount = 0;
    accounts.forEach(account => {
      let matches = 0;
      account.querySelectorAll('.reference').forEach(card => {
        const visible = (group.value === 'all' || group.value === account.dataset.group)
          && (format.value === 'all' || format.value === card.dataset.format)
          && (type.value === 'all' || card.dataset.types.split('|').includes(type.value))
          && norm(account.querySelector('h2').textContent + ' ' + card.textContent).includes(norm(query.value.trim()));
        card.hidden = !visible; if (visible) matches++;
      });
      account.hidden = matches === 0; count += matches; if (matches) accountCount++;
    });
    document.getElementById('result-count').textContent = `${count} referencias · ${accountCount} cuentas · Captura del 14 nov 2026`;
    document.getElementById('no-results').hidden = count > 0;
  }
  form.addEventListener('input', filter); form.addEventListener('change', filter);
  form.addEventListener('reset', () => { query.value = ''; group.value = 'national'; format.value = 'all'; type.value = 'all'; filter(); });
  filter();
})();
