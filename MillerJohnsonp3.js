/*CS 316 PA3
* Authors: William Miller, Bryan Johnson
* Purpose:
*  Create a music-distributing server software using the NodeJS runtime.
*/

//needed libraries
var http = require("http"),
	   require('url');

var STARTPORT = 2000;
var ENDPORT = 30000;
var HOSTNAME = 'iris.cs.uky.edu';
//rate of advertisements as a percentage, ints only
var ADVERT_RATE = 33;
//MP3 filenames
var mp3s = [];
//JPG filenames
var jpgs = [];



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
//Returns true if name is valid, but isn't recognized.
//Returns a string with the filename if the name is valid and recognized.
function validateURL(fullURL) {
	var filename = fullURL.substring(fullURL.lastIndexOf('/'), fullURL.length);
	allFiles = mp3s.concat(jpgs);	
}

function start() {
	//based on/borrowed from:
	//https://stackoverflow.com/questions/4959975/generate-random-number-between-two-numbers-in-javascript
	var port = Math.floor(Math.random()*ENDPORT-STARTPORT+1)+STARTPORT;
	http.createServer(function(request, response) {
		var givenURL = request.url;
		
	}
	
}
