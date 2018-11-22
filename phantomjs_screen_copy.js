//zf181122.1055

var system = require('system');
var args = system.args;

console.log('Chargement de la page web');
console.log(args[1]);

var page = require('webpage').create();



page.settings.resourceTimeout = 6000; // 6 seconds
page.onResourceTimeout = function(e) {
  console.log('y a une erreur mon coco...');
  console.log(e.errorCode);   // it'll probably be 408 
  console.log(e.errorString); // it'll probably be 'Network timeout on resource'
  console.log(e.url);         // the url whose request timed out
  phantom.exit(1);
};


page.viewportSize = {
    width: 1024,
    height: 2000
    };

//page.settings.userAgent = "Phantom.js bot";
page.settings.userAgent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36";

var url = args[1];

page.open(url, function (status) {
    console.log('Page chargée');
//    page.render(args[2]+'.jpeg', {format: 'jpeg', quality: '100'} );
//    console.log('toto1...');
    page.render(args[2]+'.png');
//    console.log('toto2...');
    phantom.exit();
//    console.log('toto3...');
});



