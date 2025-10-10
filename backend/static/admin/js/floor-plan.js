document.addEventListener('DOMContentLoaded', function() {
    const floorSelector = document.querySelector('.floor-plan-selector');
    const container = document.createElement('div');
    container.className = 'floor-plan-container';
    
    let marker = document.createElement('div');
    marker.className = 'location-marker';
    
    let imagePreview = document.createElement('div');
    imagePreview.className = 'floor-plan-preview';
    imagePreview.innerHTML = '<p>Clique na imagem para marcar a localização</p>';
    
    if (floorSelector) {
        floorSelector.parentElement.insertBefore(container, floorSelector.nextSibling);
        container.appendChild(imagePreview);
        container.appendChild(marker);
        
        if (floorSelector.value) {
            loadFloorPlan(floorSelector.value);
        }
        
        floorSelector.addEventListener('change', function(e) {
            if (e.target.value) {
                loadFloorPlan(e.target.value);
            } else {
                imagePreview.innerHTML = '<p>Selecione um andar para ver a planta</p>';
                marker.style.display = 'none';
            }
        });
    }
});

function loadFloorPlan(floorId) {
    if (!floorId) return;
    
    fetch(`/api/floor-plans/${floorId}/`)
        .then(response => response.json())
        .then(data => {
            const container = document.querySelector('.floor-plan-container');
            const imagePreview = container.querySelector('.floor-plan-preview');
            const marker = container.querySelector('.location-marker');
            
            // Create or update image
            let img = container.querySelector('.floor-plan-image');
            if (!img) {
                img = document.createElement('img');
                img.className = 'floor-plan-image';
                imagePreview.innerHTML = '';
                imagePreview.appendChild(img);
            }
            
            img.onload = function() {
                // Show image only after it's loaded
                img.style.display = 'block';
            };
            
            img.onerror = function() {
                imagePreview.innerHTML = '<p>Erro ao carregar a imagem</p>';
            };
            
            img.src = data.plan_image;
            
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
            
            // Show existing coordinates if they exist
            const x = document.querySelector('.coord-x').value;
            const y = document.querySelector('.coord-y').value;
            if (x && y) {
                marker.style.display = 'block';
                marker.style.left = `${x}%`;
                marker.style.top = `${y}%`;
            }
        })
        .catch(error => {
            console.error('Error loading floor plan:', error);
            const imagePreview = document.querySelector('.floor-plan-preview');
            imagePreview.innerHTML = '<p>Erro ao carregar a planta do andar</p>';
        });
}