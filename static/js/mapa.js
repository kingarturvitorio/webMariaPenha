// Função para abrir o modal e exibir o mapa
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

let websocket; // Variável para armazenar a instância do WebSocket
let map; // Variável global para o mapa

function openWebSocketMapPopup(lat, long) {
    lat = parseFloat(lat.replace(',', '.'));
  long = parseFloat(long.replace(',', '.'));
  console.log("Abrindo WebSocket para coordenadas - Latitude:", lat, "Longitude:", long);

  // Se o mapa já estiver inicializado, não o inicialize novamente
  if (!map) {
      // Inicializa o mapa no novo modal com o nível de zoom ajustado
      map = L.map('websocketMap').setView([lat, long], 30); // Ajuste o nível de zoom aqui, por exemplo, 15

      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
          maxZoom: 19,
      }).addTo(map);
  } else {
      // Se o mapa já existir, apenas atualize sua posição
      map.setView([lat, long], 15);
  }

  // Adiciona ou atualiza o marcador
  let marker = L.marker([lat, long]).addTo(map);

  // Conecte-se ao WebSocket
  websocket = new WebSocket('ws://3.20.168.85:8000/ws/gps/');

  websocket.onopen = function() {
      console.log("Conexão WebSocket aberta.");
      // Envie as coordenadas iniciais
      websocket.send(JSON.stringify({ latitude: lat, longitude: long }));
  };

  websocket.onmessage = function(event) {
      console.log("Mensagem recebida:", event.data);
      const data = JSON.parse(event.data); // Supondo que a mensagem seja um JSON
      // Atualiza a posição do marcador e do mapa
      marker.setLatLng([data.latitude, data.longitude]);
      map.setView([data.latitude, data.longitude], 15); // Atualiza a visualização do mapa
  };

  websocket.onclose = function() {
      console.log("Conexão WebSocket fechada.");
  };

  websocket.onerror = function(error) {
      console.error("Erro WebSocket:", error);
  };

  // Mostra o novo modal do WebSocket
  document.getElementById('websocketMapModal').style.display = 'block';

  // Força o mapa a recalcular seu tamanho
  setTimeout(function() {
      if (map) {
          map.invalidateSize(); // Recalcula as dimensões do mapa
      }
  }, 500); // Um pequeno atraso pode ajudar, ajuste conforme necessário
}

// Função para fechar o modal do WebSocket e encerrar a conexão
function closeWebSocketMapPopup() {
    document.getElementById('websocketMapModal').style.display = 'none';
    if (websocket) {
        websocket.close(); // Encerra a conexão WebSocket
        websocket = null; // Limpa a variável
    }
    if (map) {
        // Se necessário, você pode redefinir o mapa ou remover o marcador aqui
        // Mas, por enquanto, apenas deixamos o mapa como está
    }
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
