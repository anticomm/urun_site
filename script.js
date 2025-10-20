fetch('veriler/urunler.json')
  .then(res => res.json())
  .then(data => {
    const container = document.getElementById('urunler');
    data.forEach(urun => {
      const card = document.createElement('div');
      card.className = 'urun';
      card.innerHTML = `
        <img src="${urun.image}" alt="${urun.title}">
        <h3>${urun.title}</h3>
        <p>${urun.price}</p>
        <a href="${urun.link}" target="_blank">Telegram’da Gör</a>
      `;
      container.appendChild(card);
    });
  });
