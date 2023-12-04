(function () {
    const sliders = [...document.querySelectorAll('.esp_body')];
    const buttonNext = document.querySelector('#next');
    const buttonBefore = document.querySelector('#before');
    let value;

    buttonNext.addEventListener('click', () => {
        changePosition(1);
    });
    buttonBefore.addEventListener('click', () => {
        changePosition(-1);
    });

    const changePosition = (add) => {
        const currentEsp = document.querySelector('.esp_body--show').dataset.id;
        value = Number(currentEsp);
        value+= add;

        if(value === sliders.length+1 || value === 0){
            value = value === 0? sliders.length  : 1;
        }
        sliders[Number(currentEsp)-1].classList.remove('esp_body--show');
        sliders[value-1].classList.add('esp_body--show');
    }



})();