ymaps.ready(init);
var myMap, 
    myPlacemark;

function init(){ 
    myMap = new ymaps.Map("map", {
        center: [32.94048411, 14.57042561],
        zoom: 2
    }); 

    myPlacemark = new ymaps.Placemark([61.6987, 99.5054], {
        hintContent: 'Россия'
    });
    myMap.geoObjects.add(myPlacemark);
    
    myPlacemark = new ymaps.Placemark([64.5199,26.2830], {
        hintContent: 'Финляндия'
    });
    myMap.geoObjects.add(myPlacemark);
    
    myPlacemark = new ymaps.Placemark([39.4959,-98.9900], {
        hintContent: 'США'
    });
    myMap.geoObjects.add(myPlacemark);
    
    myPlacemark = new ymaps.Placemark([48.4636,31.6860], {
        hintContent: 'Украина'
    });
    myMap.geoObjects.add(myPlacemark);
    
    myPlacemark = new ymaps.Placemark([40.3877,-3.5574], {
        hintContent: 'Испания'
    });
    myMap.geoObjects.add(myPlacemark);
    
    myPlacemark = new ymaps.Placemark([43.5292,12.1620], {
        hintContent: 'Италия'
    });
    myMap.geoObjects.add(myPlacemark);
}