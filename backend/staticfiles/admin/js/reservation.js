document.addEventListener('DOMContentLoaded', function() {
    const buildingSelect = document.querySelector('.building-selector');
    const floorSelect = document.querySelector('.floor-selector');
    const spaceSelect = document.querySelector('.space-selector');
    const container = document.createElement('div');
    container.className = 'floor-plan-container';
    
    // Remover container existente se houver
    const existingContainer = document.querySelector('.floor-plan-container');
    if (existingContainer) {
        existingContainer.remove();
    }
    
    let marker = document.createElement('div');
    marker.className = 'location-marker';
    
    // Adicionar container após o select do floor
    if (floorSelect) {
        floorSelect.parentElement.insertBefore(container, floorSelect.nextSibling);
        container.appendChild(marker);
    }
    
    // Handle building selection
    if (buildingSelect) {
        buildingSelect.addEventListener('change', function(e) {
            const buildingId = e.target.value;
            updateFloorSelect(buildingId);
            clearSpaceSelect();
            container.innerHTML = '<p>Selecione um andar para ver a planta</p>';
            container.appendChild(marker);
        });
    }
    
    // Handle floor selection
    if (floorSelect) {
        floorSelect.addEventListener('change', function(e) {
            const floorId = e.target.value;
            updateSpaceSelect(floorId);
            if (floorId) {
                loadFloorPlan(floorId);
            } else {
                container.innerHTML = '<p>Selecione um andar para ver a planta</p>';
                container.appendChild(marker);
            }
        });
    }
    
    // Handle recurring reservation toggle
    const isRecurringCheck = document.querySelector('#id_is_recurring');
    const dayOfWeekField = document.querySelector('#id_day_of_week').closest('.form-row');
    const recurrenceEndDateField = document.querySelector('#id_recurrence_end_date').closest('.form-row');
    const startDateTimeField = document.querySelector('#id_start_datetime_0').closest('.form-row');
    const endDateTimeField = document.querySelector('#id_end_datetime_0').closest('.form-row');
    const startTimeField = document.querySelector('#id_start_time').closest('.form-row');
    const endTimeField = document.querySelector('#id_end_time').closest('.form-row');

    // Initially hide recurring-specific fields
    dayOfWeekField.style.display = 'none';
    recurrenceEndDateField.style.display = 'none';
    startTimeField.style.display = 'none';
    endTimeField.style.display = 'none';

    if (isRecurringCheck) {
        isRecurringCheck.addEventListener('change', function(e) {
            if (e.target.checked) {
                // Show recurring fields
                dayOfWeekField.style.display = 'block';
                recurrenceEndDateField.style.display = 'block';
                startTimeField.style.display = 'block';
                endTimeField.style.display = 'block';
                // Hide datetime fields
                startDateTimeField.style.display = 'none';
                endDateTimeField.style.display = 'none';
            } else {
                // Hide recurring fields
                dayOfWeekField.style.display = 'none';
                recurrenceEndDateField.style.display = 'none';
                startTimeField.style.display = 'none';
                endTimeField.style.display = 'none';
                // Show datetime fields
                startDateTimeField.style.display = 'block';
                endDateTimeField.style.display = 'block';
            }
        });
    }

    // Format date inputs
    const dateInputs = document.querySelectorAll('input[type="text"][id$="_0"]');
    dateInputs.forEach(input => {
        input.setAttribute('placeholder', 'dd/mm/yyyy');
        input.addEventListener('change', function(e) {
            const date = e.target.value;
            if (date) {
                try {
                    const parts = date.split('/');
                    if (parts.length === 3) {
                        const formattedDate = `${parts[2]}-${parts[1]}-${parts[0]}`;
                        e.target.value = formattedDate;
                    }
                } catch (error) {
                    console.error('Error formatting date:', error);
                }
            }
        });
    });
});

// Update floor and space selects to fix duplicate options
function updateFloorSelect(buildingId) {
    const floorSelect = document.querySelector('.floor-selector');
    floorSelect.innerHTML = '<option value="">---------</option>';
    
    if (buildingId) {
        fetch(`/api/buildings/${buildingId}/floors/`)
            .then(response => response.json())
            .then(data => {
                // Clear existing options first
                floorSelect.innerHTML = '<option value="">---------</option>';
                // Add new options
                data.forEach(floor => {
                    const option = new Option(floor.name, floor.id);
                    floorSelect.add(option);
                });
            });
    }
}

function updateSpaceSelect(floorId) {
    const spaceSelect = document.querySelector('.space-selector');
    spaceSelect.innerHTML = '<option value="">---------</option>';
    
    if (floorId) {
        fetch(`/api/floors/${floorId}/spaces/`)
            .then(response => response.json())
            .then(data => {
                // Clear existing options first
                spaceSelect.innerHTML = '<option value="">---------</option>';
                // Add new options
                data.forEach(space => {
                    const option = new Option(space.name, space.id);
                    option.dataset.x = space.location_x;
                    option.dataset.y = space.location_y;
                    spaceSelect.add(option);
                });
                
                // Add hover events
                spaceSelect.querySelectorAll('option').forEach(option => {
                    if (option.value) {
                        option.addEventListener('mouseover', () => {
                            if (option.dataset.x && option.dataset.y) {
                                showSpaceLocation(option.dataset.x, option.dataset.y);
                            }
                        });
                        option.addEventListener('mouseout', hideSpaceLocation);
                    }
                });

                // Add change event to show selected space location
                spaceSelect.addEventListener('change', function(e) {
                    const selectedOption = this.options[this.selectedIndex];
                    if (selectedOption.value) {
                        const x = selectedOption.dataset.x;
                        const y = selectedOption.dataset.y;
                        if (x && y) {
                            const marker = document.querySelector('.location-marker');
                            if (marker) {
                                marker.style.display = 'block';
                                marker.style.left = `${x}%`;
                                marker.style.top = `${y}%`;
                                marker.style.backgroundColor = 'red';
                                marker.style.zIndex = '1000';
                            }
                        }
                    } else {
                        hideSpaceLocation();
                    }
                });
            });
    }
}

// Atualizar a função showSpaceLocation para manter a cor vermelha
function showSpaceLocation(x, y) {
    const marker = document.querySelector('.location-marker');
    if (marker) {
        marker.style.display = 'block';
        marker.style.left = `${x}%`;
        marker.style.top = `${y}%`;
        marker.style.backgroundColor = 'red';
        marker.style.zIndex = '1000';
    }
}

function hideSpaceLocation() {
    const marker = document.querySelector('.location-marker');
    const spaceSelect = document.querySelector('.space-selector');
    if (marker && (!spaceSelect || !spaceSelect.value)) {
        marker.style.display = 'none';
    }
}

function clearSpaceSelect() {
    const spaceSelect = document.querySelector('.space-selector');
    spaceSelect.innerHTML = '<option value="">---------</option>';
}

function loadFloorPlan(floorId) {
    if (!floorId) return;
    
    const container = document.querySelector('.floor-plan-container');
    if (!container) return;
    
    const marker = container.querySelector('.location-marker');
    container.innerHTML = '<div class="loading">Carregando planta...</div>';
    container.appendChild(marker);
    
    fetch(`/api/floor-plans/${floorId}/`)
        .then(response => response.json())
        .then(data => {
            container.innerHTML = '';
            
            const img = document.createElement('img');
            img.className = 'floor-plan-image';
            img.style.display = 'none';
            
            img.src = data.plan_image || data.plan_image_url;
            
            img.onload = function() {
                img.style.display = 'block';
                container.style.minHeight = 'auto';
            };
            
            container.appendChild(img);
            container.appendChild(marker);
            
            // Carregar espaços deste andar para mostrar marcadores
            return fetch(`/api/floors/${floorId}/spaces/`);
        })
        .then(response => response.json())
        .then(spaces => {
            spaces.forEach(space => {
                const spaceMarker = document.createElement('div');
                spaceMarker.className = 'space-marker';
                spaceMarker.style.left = `${space.location_x}%`;
                spaceMarker.style.top = `${space.location_y}%`;
                spaceMarker.setAttribute('data-space-id', space.id);
                container.appendChild(spaceMarker);
            });
            
            // Adicionar eventos de hover nas opções do select
            const spaceSelect = document.querySelector('.space-selector');
            spaceSelect.querySelectorAll('option').forEach(option => {
                if (option.value) {
                    option.addEventListener('mouseover', () => {
                        highlightSpace(option.value);
                    });
                    option.addEventListener('mouseout', () => {
                        unhighlightSpaces();
                    });
                }
            });
        })
        .catch(error => {
            console.error('Error:', error);
            container.innerHTML = '<p class="error">Erro ao carregar a planta</p>';
            container.appendChild(marker);
        });
}

function highlightSpace(spaceId) {
    const markers = document.querySelectorAll('.space-marker');
    markers.forEach(marker => {
        if (marker.getAttribute('data-space-id') === spaceId) {
            marker.style.display = 'block';
            marker.style.backgroundColor = 'red';
        } else {
            marker.style.display = 'none';
        }
    });
}

function unhighlightSpaces() {
    const markers = document.querySelectorAll('.space-marker');
    markers.forEach(marker => {
        marker.style.display = 'block';
        marker.style.backgroundColor = 'blue';
    });
}

function clearFloorPlan() {
    const container = document.querySelector('.floor-plan-container');
    const preview = container.querySelector('.floor-plan-preview');
    preview.innerHTML = '<p>Selecione um andar para ver a planta</p>';
    
    // Remove all space markers
    container.querySelectorAll('.space-marker').forEach(marker => marker.remove());
}