/*CS 316 PA3
* Authors: William Miller, Bryan Johnson
* Purpose:
*  Create a music-distributing server software using the NodeJS runtime.
*/

//needed libraries
var http = require("http"),
    url =  require('url');

var STARTPORT = 2000;
var ENDPORT = 30000;
var HOSTNAME = 'iris.cs.uky.edu';
//rate of advertisements as a percentage, ints only
var ADVERT_RATE = 33;



//Boolean, checks if an advert should be distributed.
//True if an advert should be distributed, false otherwise.
function giveAdvert() {
	//random number between 0 and 99
	var num = Math.floor(Math.random() * 100);
	//Return an advert if needed
	if(num < ADVERT_RATE) {
		//show advert
		return true;
	}
	return false;
}

function giveFile(filename) {
	
}

//Validates the URL.
//Returns false if name is not valid.
//Returns a string with the filename if name is valid.
function validateURL(fullURL) {
	var filename = fullURL.substring(fullURL.lastIndexOf('/'), fullURL.length);
	var regx1 = new RegExp("[a-zA-Z0-9_]*.mp3");
	var regx2 = new RegExp("[a-zA-Z0-9_]*.jpg");
	if(regx1.test(filename)||regx2.test(filename)) {
		return filename;
	}
	return false;
}

function start() {
	//based on/borrowed from:
	//https://stackoverflow.com/questions/4959975/generate-random-number-between-two-numbers-in-javascript
	var port = Math.floor(Math.random()*ENDPORT-STARTPORT+1)+STARTPORT;
	var server = http.createServer(function(request, response) {
		var givenURL = request.url;
		response.statusCode = 200;
		response.setHeader('Content-Type', 'text/plain');
		response.end('Hello, World!  You requested the following URL: '+givenURL+'\n');
	});

	server.listen(port, HOSTNAME, function() {
		console.log('Server running at http://'+ HOSTNAME +':'+ port +'/');
		console.log('Hello, World!');
	});
	
}
start();
