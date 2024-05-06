var express = require('express');
var expressHbs =  require('express-handlebars');
var app = express();
var path = require('path');

var data = require('./products.json');

app.engine('.hbs', expressHbs.engine({ extname: '.hbs', defaultLayout: "main"}));

// view engine setup
app.set('views', path.join(__dirname, 'resources', 'views'));
app.set('view engine', 'hbs');

app.get('/', function (req, res) {
  res.render('search', { 
      data: data,
  });
})

app.get('/search', function (req, res) {
  var title = req.query.title;
  var data = data?.filter(function (item) {
    return item.title.toLowerCase().indexOf(title.toLowerCase()) !== -1
  });
  res.render('search', {
    title: data
  });
})

app.listen(3000, function () {
  console.log('Example app listening on port 3000!');
});