//Hero Section
var heroSwiper = new Swiper(".heroSwiper", {
    effect: "fade",
    fadeEffect: {
        crossFade: true 
    },
    speed: 1500,
    autoplay: {
        delay: 5000,
        disableOnInteraction: false,
    },

    loop: true,
});

function animateText(row) {
    const elementi = document.querySelectorAll(row);
    
    elementi.forEach(elemento => {
        const testo = elemento.innerText;
        elemento.innerHTML = ''; 

        testo.split('').forEach((lettera, indice) => {
            const span = document.createElement('span');
            span.innerHTML = lettera === ' ' ? '&nbsp;' : lettera; 
            span.style.animationDelay = `${indice * 0.04}s`; 
            elemento.appendChild(span);
        });
    });
}

animateText('.up-row');
animateText('.down-row');