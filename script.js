document.addEventListener('DOMContentLoaded', () => {
    const scrollIndicator = document.querySelector('.scroll-indicator');

    function updateScrollIndicator() {
        if (!scrollIndicator) return;
        
        const scrollY = window.scrollY;
        // Calcola l'altezza totale scrollabile
        const maxScroll = document.documentElement.scrollHeight - window.innerHeight;
        const threshold = 50; // Margine di tolleranza in pixel

        // Rimuoviamo tutte le classi per ripartire puliti
        scrollIndicator.classList.remove('top', 'middle', 'bottom');

        if (scrollY < threshold) {
            // Siamo in cima
            scrollIndicator.classList.add('top');
        } else if (scrollY >= maxScroll - threshold) { // Ho messo >= per sicurezza
            // Siamo in fondo
            scrollIndicator.classList.add('bottom');
        } else {
            // Siamo nel mezzo
            scrollIndicator.classList.add('middle');
        }
    }

    // Controllo iniziale al caricamento
    updateScrollIndicator();

    // Aggiorna quando si scrolla
    window.addEventListener('scroll', updateScrollIndicator);
    
    // Aggiorna se la finestra viene ridimensionata (cambia l'altezza pagina)
    window.addEventListener('resize', updateScrollIndicator);

    // Gestione Click to Copy
const emailBtn = document.getElementById('emailBtn');

if (emailBtn) {
    emailBtn.addEventListener('click', () => {
        const email = emailBtn.getAttribute('data-email');
        
        // Usa la Clipboard API moderna
        navigator.clipboard.writeText(email).then(() => {
            // 1. Salva il testo originale
            const originalText = emailBtn.innerText;
            
            // 2. Cambia testo e stile per dare feedback
            emailBtn.innerText = "EMAIL COPIED!";
            emailBtn.classList.add('success');

            // 3. Dopo 2 secondi torna come prima
            setTimeout(() => {
                emailBtn.innerText = originalText;
                emailBtn.classList.remove('success');
            }, 2000);
        }).catch(err => {
            console.error('Errore nella copia: ', err);
        });
    });
}
});