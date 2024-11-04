// Função para abrir o modal e exibir o mapa
document.addEventListener("DOMContentLoaded", function() {
    openMapPopup(lat, long);
    openWebSocketMapPopup(lat, long);
});


function openMapPopup(lat, long) {
  lat = parseFloat(lat.replace(',', '.'));
  long = parseFloat(long.replace(',', '.'));
  console.log("Latitude:", lat, "Longitude:", long);
  
  const zoomLevel = 70;
  const offset = 0.005 / Math.pow(2, zoomLevel - 15);
  const mapUrl = `https://www.openstreetmap.org/export/embed.html?bbox=${long - offset},${lat - offset},${long + offset},${lat + offset}&layer=mapnik&marker=${lat},${long}`;
  
  document.getElementById('mapFrame').src = mapUrl;
  document.getElementById('mapModal').style.display = 'block';
}





// Função para fechar o modal
function closeMapPopup() {
document.getElementById('mapModal').style.display = 'none';
document.getElementById('mapFrame').src = '';
}

// Fechar o modal se clicar fora dele
window.onclick = function(event) {
const modal = document.getElementById('mapModal');
if (event.target == modal) {
  closeMapPopup();
}
};
