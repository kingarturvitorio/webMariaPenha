// Função para abrir o modal e exibir o mapa
function openMapPopup(lat, long) {
    lat = parseFloat(lat.replace(',', '.'));  // Substitui vírgula por ponto
    long = parseFloat(long.replace(',', '.')); // Substitui vírgula por ponto
    console.log("Latitude:", lat, "Longitude:", long);
    
    const zoomLevel = 70; // Ajuste o nível de zoom aqui

    // Calcule a bbox de acordo com o nível de zoom
    const offset = 0.005 / Math.pow(2, zoomLevel - 15); // Aumente ou diminua este valor para ajustar o zoom
    const mapUrl = `https://www.openstreetmap.org/export/embed.html?bbox=${long - offset},${lat - offset},${long + offset},${lat + offset}&layer=mapnik&marker=${lat},${long}`;
    
    document.getElementById('mapFrame').src = mapUrl;
    document.getElementById('mapModal').style.display = 'block';
}

// Função para fechar o modal
function closeMapPopup() {
  document.getElementById('mapModal').style.display = 'none';
  document.getElementById('mapFrame').src = '';  // Limpa o iframe
}

// Fechar o modal se clicar fora dele
window.onclick = function(event) {
  const modal = document.getElementById('mapModal');
  if (event.target == modal) {
    closeMapPopup();
  }
}

// Adicionando o listener de evento para abrir o mapa ao clicar na card
document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.car-card').forEach(function(card) {
        card.addEventListener('click', function() {
            const lat = card.getAttribute('data-lat');
            const long = card.getAttribute('data-long');
            openMapPopup(lat, long);
        });
    });
});