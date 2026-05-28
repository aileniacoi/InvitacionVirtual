// Countdown to October 3, 2026
const weddingDate = new Date('October 3, 2026 18:00:00').getTime();

function updateCountdown() {
    const now = new Date().getTime();
    const distance = weddingDate - now;

    // Calculate time units
    const days = Math.floor(distance / (1000 * 60 * 60 * 24));
    const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
    const seconds = Math.floor((distance % (1000 * 60)) / 1000);

    // Update the DOM
    document.getElementById('days').textContent = days;
    document.getElementById('hours').textContent = hours;
    document.getElementById('minutes').textContent = minutes;
    document.getElementById('seconds').textContent = seconds;

    // If countdown is finished
    if (distance < 0) {
        document.getElementById('countdown').innerHTML = '<h2 class="cursive">¡Es hoy! ¡Nos casamos!</h2>';
    }
}

// Update countdown every second
updateCountdown();
setInterval(updateCountdown, 1000);