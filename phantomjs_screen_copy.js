//zf181113.1334

var system = require('system');
var args = system.args;

console.log('Chargement de la page web');
console.log(args[1]);

var page = require('webpage').create();



page.settings.resourceTimeout = 2000; // 2 seconds
page.onResourceTimeout = function(e) {
  console.log(e.errorCode);   // it'll probably be 408 
  console.log(e.errorString); // it'll probably be 'Network timeout on resource'
  console.log(e.url);         // the url whose request timed out
  phantom.exit(1);
};


page.viewportSize = {
    width: 1024,
    height: 3000
    };

page.settings.userAgent = "Phantom.js bot";

var url = args[1];

page.open(url, function (status) {
    console.log('Page chargée');
//    page.render(args[2]+'.jpeg', {format: 'jpeg', quality: '100'} );
    page.render(args[2]+'.png');
    phantom.exit();
});



