console.log('Chargement de la page web');
var page = require('webpage').create();
page.viewportSize = {
    width: 1024,
    height: 768
    };
page.settings.userAgent = "Phantom.js bot";
var url = 'http://cib.epfl.ch//';
page.open(url, function (status) {
    console.log('Page chargée');
    page.render('copyscreen.png');
    phantom.exit();
});
