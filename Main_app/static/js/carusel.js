$(document).ready(function(){
    let timerId = setTimeout(function tick() {
        let count = Number($('.carousel-open:checked').attr('id').slice(9));
        if (count===15) {
            count = 1;
        };
        $('.control-'+count).trigger('click');
        timerId = setTimeout(tick, 3000); // (*)
    }, 3000);
});

