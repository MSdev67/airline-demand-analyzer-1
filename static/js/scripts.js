$(document).ready(function() {
    // Sample chart data
    const demandData = {
        x: ['Jan', 'Feb', 'Mar', 'Apr', 'May'],
        y: [1200, 1900, 1500, 2200, 1800],
        type: 'line',
        line: {color: '#4cc9f0'}
    };
    
    Plotly.newPlot('demandChart', [demandData], {
        title: 'Flight Demand Trend',
        paper_bgcolor: 'rgba(0,0,0,0)',
        plot_bgcolor: 'rgba(0,0,0,0)',
        font: {color: 'white'}
    });

    const routeData = {
        y: ['SYD-MEL', 'MEL-BNE', 'SYD-BNE', 'PER-SYD', 'MEL-PER'],
        x: [450, 380, 320, 280, 210],
        type: 'bar',
        orientation: 'h'
    };
    
    Plotly.newPlot('routeChart', [routeData], {
        title: 'Top Routes',
        paper_bgcolor: 'rgba(0,0,0,0)',
        plot_bgcolor: 'rgba(0,0,0,0)',
        font: {color: 'white'}
    });

    // AI Assistant
    $('#aiAssistantBtn').click(function() {
        $('.ai-assistant-panel').toggleClass('show');
    });
    
    $('#closeAssistantBtn').click(function() {
        $('.ai-assistant-panel').removeClass('show');
    });
    
    $('#sendAiPromptBtn, #aiPromptInput').keypress(function(e) {
        if (e.which === 13) sendPrompt();
    });
    
    function sendPrompt() {
        const prompt = $('#aiPromptInput').val().trim();
        if (!prompt) return;
        
        $('#aiMessages').append(`<div class="ai-message user">${prompt}</div>`);
        $('#aiPromptInput').val('');
        
        $.post('/ai-assistant', {prompt: prompt}, function(response) {
            $('#aiMessages').append(`<div class="ai-message bot"><i class="fas fa-robot"></i> ${response.response}</div>`);
        }).fail(function() {
            $('#aiMessages').append('<div class="ai-message bot">Error connecting to assistant</div>');
        });
    }
});