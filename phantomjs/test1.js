console.log('Chargement de la page web');
var page = require('webpage').create();
var url = 'http://fr.wikipedia.org/';
page.open(url, function (status) {
  console.log('Page chargée');
  page.render('wikipedia.org.png');
  phantom.exit();
});

