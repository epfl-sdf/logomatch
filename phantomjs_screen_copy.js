//zf181113.1238

var system = require('system');
var args = system.args;

console.log('Chargement de la page web');
console.log(args[1]);

var page = require('webpage').create();

page.viewportSize = {
    width: 1024,
    height: 3000
    };

page.settings.userAgent = "Phantom.js bot";

var url = args[1];

page.open(url, function (status) {
    console.log('Page chargée');
    page.render(args[2]+'.png');
    phantom.exit();
});



