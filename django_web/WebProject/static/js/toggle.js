document.addEventListener('DOMContentLoaded', (event) => {
    const currentMode = localStorage.getItem('theme') || 'light';
    if (currentMode === 'dark') {
        document.body.classList.add('dark-mode');
    }

    const toggleButton = document.getElementById('mode-toggle');
    toggleButton.addEventListener('click', () => {
        document.body.classList.toggle('dark-mode');
        let theme = 'light';
        if (document.body.classList.contains('dark-mode')) {
            theme = 'dark';
        }
        localStorage.setItem('theme', theme);
    });
});

$(document).ready(function() {
    // Check the initial state of the monitoring
    $.getJSON('/ai/get_monitoring_state/', function(data) {
        updateButtonState(data.is_active);
    });

    // Toggle the monitoring state on button click
    $('#toggle-monitoring-button').click(function() {
        $.getJSON('/ai/toggle_monitoring/', function(data) {
            updateButtonState(data.is_active);
        });
    });
});

    function toggleRealTimeMonitoring() {
        // Esta función se llamará cuando se haga clic en el botón
        $.getJSON('/ai/toggle_monitoring/', function(data) {
            updateButtonState(data.is_active);
        });
    }

    
    function updateButtonState(isActive) {
        if (isActive) {
            $('#toggle-monitoring-button').text('Stop Real-Time Monitoring')
                .removeClass('inactive')
                .addClass('active');
            $('#monitoring-indicator').removeClass('inactive').addClass('active');
        } else {
            $('#toggle-monitoring-button').text('Start Real-Time Monitoring')
                .removeClass('active')
                .addClass('inactive');
            $('#monitoring-indicator').removeClass('active').addClass('inactive');
        }
    }

    




$(document).ready(function() {
    // Check the initial state of the monitoring
    $.getJSON('/ai/get_monitoring_state/', function(data) {
        updateButtonState(data.is_active);
    });

    // Toggle the monitoring state on button click
    $('#toggle-monitoring-button').click(toggleRealTimeMonitoring);
});