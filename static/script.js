window.addEventListener('DOMContentLoaded', () => {
  const canvas = document.getElementById('vulnerabilityChart');
  if (!canvas) return;

  // Canvas'taki data-* attribute'larını okuyalım
  const safeCount = parseInt(canvas.dataset.safeCount, 10) || 0;
  const vulnerableCount = parseInt(canvas.dataset.vulnerableCount, 10) || 0;

  const ctx = canvas.getContext('2d');
  new Chart(ctx, {
    type: 'pie',
    data: {
      labels: ['Safe', 'Vulnerable'],
      datasets: [{
        data: [safeCount, vulnerableCount],
        backgroundColor: ['#28a745', '#dc3545']
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: 'bottom'
        }
      }
    }
  });
});
