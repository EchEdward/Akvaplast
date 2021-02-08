ymaps.ready(init);

let myMap;
let static_dir = '';
//'static/icon/'+strike+'.png'
// /lightning_server/

let address = 'Минский р-н, д. Боровая, 3, АБК, к. 42'; 



function init () {
    // Параметры карты можно задать в конструкторе.
    myMap = new ymaps.Map(
        // ID DOM-элемента, в который будет добавлена карта.
        'map',
        // Параметры карты.
        {
            // Географические координаты центра отображаемой карты.
            center: [53.966732, 27.650771],
            // Масштаб.
            zoom: 14,
            //Тип покрытия карты: "Гибрид".
            type:"yandex#map"
        }, {
            // Поиск по организациям.
            autoFitToViewport: 'always',
            searchControlProvider: 'yandex#search',
            // Убираем ссылку открыть в яндекс картах
            suppressMapOpenBlock: true,
        }
    );
    
    myMap.container.fitToViewport()
    // Удалим с карты «Ползунок масштаба».
    myMap.controls.remove('geolocationControl');
    // Удалим с карты «Поиск по карте».
    myMap.controls.remove('searchControl');
    // Удалим с карты «Пробки».
    myMap.controls.remove('trafficControl');
    // Удалим с карты кнопу расширения
    myMap.controls.remove("fullscreenControl");

    myMap.geoObjects.add(Address());


};

function Address(){
    let placemark = new ymaps.Placemark(
        [53.966732, 27.650771], {
            'hintContent': address,
            'balloonContent': 'Время работы: Пн-Пт, с 9 до 18'
        }, {
            'preset': 'islands#redDotIcon'
        }
    );
    return placemark;
};


