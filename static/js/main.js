document.addEventListener("DOMContentLoaded", function() {
    // Überprüfe, ob das Canvas-Element existiert
    const canvas = document.getElementById('portfolioChart');
    if (canvas) {
        // Diese Variablen sollten als globale JavaScript-Variablen über ein separates Script in deinem Template gesetzt werden.
        // Zum Beispiel: window.chart_labels und window.chart_data
        const labels = window.chart_labels || [];
        const data = window.chart_data || [];
        const ctx = canvas.getContext('2d');
        const portfolioChart = new Chart(ctx, {
            type: 'pie',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Portfolio in EUR',
                    data: data,
                    backgroundColor: [
                        'rgba(255, 99, 132, 0.2)',
                        'rgba(54, 162, 235, 0.2)',
                        'rgba(255, 206, 86, 0.2)',
                        'rgba(75, 192, 192, 0.2)',
                        'rgba(153, 102, 255, 0.2)',
                        'rgba(255, 159, 64, 0.2)'
                    ],
                    borderColor: [
                        'rgba(255, 99, 132, 1)',
                        'rgba(54, 162, 235, 1)',
                        'rgba(255, 206, 86, 1)',
                        'rgba(75, 192, 192, 1)',
                        'rgba(153, 102, 255, 1)',
                        'rgba(255, 159, 64, 1)'
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true
            }
        });
    }
});
