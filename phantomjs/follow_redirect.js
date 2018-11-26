function renderPage(url, imagepath) {
  var page = require('webpage').create();
  var redirectURL = null;

  page.onResourceReceived = function(resource) {
    if (url == resource.url && resource.redirectURL) {
      redirectURL = resource.redirectURL;
    }
  };

  page.viewportSize = {
      width: 1024,
      height: 3000
      };

  page.settings.userAgent = "Phantom.js bot";

  page.open(url, function(status) {
    if (redirectURL) {
      console.log('Redirection');
      renderPage(redirectURL, imagepath);
    } else if (status == 'success') {
      console.log('Loaded page ' + url + '   saving into ' + imagepath);
      page.render(imagepath);
      phantom.exit();      
      // ...
    } else {
      console.log('Error loading page ' + url);
      c
    }
  });
}


var system = require('system');
var args = system.args;

console.log('Chargement de la page web');
console.log(args[1]);

var url = 'http://'+args[1];
var imagepath = args[1]+'.png';
renderPage(url, imagepath);