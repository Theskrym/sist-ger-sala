document.addEventListener('DOMContentLoaded', function() {
    const floorSelector = document.querySelector('.floor-plan-selector');
    const container = document.createElement('div');
    container.className = 'floor-plan-container';
    
    // Remover container existente se houver
    const existingContainer = document.querySelector('.floor-plan-container');
    if (existingContainer) {
        existingContainer.remove();
    }
    
    let marker = document.createElement('div');
    marker.className = 'location-marker';
    
    if (floorSelector) {
        // Adicionar o container após o select do floor plan
        floorSelector.parentElement.insertBefore(container, floorSelector.nextSibling);
        container.appendChild(marker);
        
        // Carregar planta inicial se houver valor selecionado
        if (floorSelector.value) {
            loadFloorPlan(floorSelector.value);
        }
        
        floorSelector.addEventListener('change', function(e) {
            if (e.target.value) {
                loadFloorPlan(e.target.value);
            } else {
                container.innerHTML = '<p>Selecione um andar para ver a planta</p>';
                container.appendChild(marker);
            }
        });
    }
});

function loadFloorPlan(floorId) {
    if (!floorId) return;
    
    const container = document.querySelector('.floor-plan-container');
    if (!container) return;
    
    // Limpar container mantendo apenas o marker
    const marker = container.querySelector('.location-marker');
    container.innerHTML = '<div class="loading">Carregando planta...</div>';
    container.appendChild(marker);
    
    fetch(`/api/floor-plans/${floorId}/`)
        .then(response => response.json())
        .then(data => {
            container.innerHTML = ''; // Limpar o container
            
            const img = document.createElement('img');
            img.className = 'floor-plan-image';
            img.style.display = 'none'; // Esconder até carregar
            
            // Usar a imagem do servidor ou URL externa
            img.src = data.plan_image || data.plan_image_url;
            
            // Mostrar imagem apenas quando carregar
            img.onload = function() {
                img.style.display = 'block';
                container.style.minHeight = 'auto';
            };
            
            container.appendChild(img);
            container.appendChild(marker);
            
            img.onclick = function(e) {
                const rect = e.target.getBoundingClientRect();
                const x = ((e.clientX - rect.left) / rect.width) * 100;
                const y = ((e.clientY - rect.top) / rect.height) * 100;
                
                document.querySelector('.coord-x').value = x.toFixed(2);
                document.querySelector('.coord-y').value = y.toFixed(2);
                
                marker.style.display = 'block';
                marker.style.left = `${x}%`;
                marker.style.top = `${y}%`;
            };
            
            // Mostrar marker se já existirem coordenadas
            const x = document.querySelector('.coord-x').value;
            const y = document.querySelector('.coord-y').value;
            if (x && y) {
                marker.style.display = 'block';
                marker.style.left = `${x}%`;
                marker.style.top = `${y}%`;
            }
        })
        .catch(error => {
            console.error('Error:', error);
            container.innerHTML = '<p class="error">Erro ao carregar a planta</p>';
            container.appendChild(marker);
        });
}