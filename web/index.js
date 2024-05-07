var express = require('express');
var expressHbs =  require('express-handlebars');
var app = express();
var path = require('path');
var axios = require('axios');

app.engine('.hbs', expressHbs.engine({ extname: '.hbs', defaultLayout: "main"}));

// view engine setup
app.set('views', path.join(__dirname, 'resources', 'views'));
app.set('view engine', 'hbs');

app.get('/', function (req, res) {
axios
  .get("http://api_service:8000/products")
  .then((response) => {
  res.render('search', {
    data: response.data,
  });
})
.catch((err) => console.log(err));
})

app.get('/search', function (req, res) {
  axios
  .get(`http://api_service:8000/search?title=${req.query.title}`)
  .then((response) => {
    res.render('search', {
      data: response.data,
    });
  })
  .catch((err) => console.log(err));
});


app.listen(3000, function () {
  console.log('Example app listening on port 3000!');
});