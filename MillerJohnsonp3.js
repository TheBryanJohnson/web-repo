/*CS 316 PA3
* Authors: William Miller, Bryan Johnson
* Purpose:
*  Create a music-distributing server software using the NodeJS runtime.
*/

//needed libraries
var http = require("http"),
    url =  require('url');
const fs = require('fs');

var STARTPORT = 6660;
var ENDPORT = 6660;
var HOSTNAME = 'iris.cs.engr.uky.edu';
//rate of advertisements as a percentage, ints only
var ADVERT_RATE = 33;



//Boolean, checks if an advert should be distributed.
//True if an advert should be distributed, false otherwise.
function giveAdvert() {
	//random number between 0 and 99
	var num = Math.floor(Math.random() * 100);
	console.log(num);
	//Return an advert if needed
	if(num < ADVERT_RATE) {
		//show advert
		return true;
	}
	return false;
}

function giveFile(filename, response) {
	if(fs.existsSync('./'+filename)) {
		if (giveAdvert()) {
			fs.readFile('./advert.jpg', (err, data) => {
				response.statusCode = 200;
				response.setHeader('Content-disposition', 'attachment; filename=advert.jpg');
				response.end(data);
	
			});
		}
		else {
			fs.readFile('./'+filename, (err, data) => {
			
				if (err) {
					//console.log("setheaderErr");
					response.statusCode = 403;
					response.setHeader('Content-Type', 'text/html');
					response.end("<h3>Unidentified error in reading file</h3>");
				}
				else {
					//serve file
					response.statusCode = 200;
					//mp3
					if(filename.substring(filename.length-1, filename.length) == "3") {
						//console.log("setHeaderMP3");
						response.setHeader('Content-Type', 'audio/mpeg3');
						response.end(data, 'binary');
					}
					//jpg
					else {
						//console.log("setHeaderJPG");
						//response.setHeader('Content-Type', 'image/jpeg');
						//response.end(data, 'binary');
						response.setHeader('Content-disposition', 'attachment; filename='+filename);
						response.end(data);
					}
				}
			});
		}
	}
	else {
		//console.log("setHeader404");
		response.setHeader('Content-Type', 'text/html');
		response.end("<h3>File doesn't exist!</h3>");
	}
}

//Validates the URL.
//Returns false if name is not valid.
//Returns a string with the filename if name is valid.
function validateFilename(fileName) {
	var regx1 = new RegExp("[0-9a-zA-z_]+.mp3$");
	var regx2 = new RegExp("[0-9a-zA-z_]+.jpg$");
	console.log("a request for ["+fileName+"] was made");
	if(regx1.test(fileName)||regx2.test(fileName)) {
		return fileName;
	}
	//console.log(fileName+" comes up as false");
	return false;
}

function start() {
	//random port based on/borrowed from:
	//https://stackoverflow.com/questions/4959975/generate-random-number-between-two-numbers-in-javascript
	var port;
	if(STARTPORT == ENDPORT) port = STARTPORT;
	else port = Math.floor(Math.random()*ENDPORT-STARTPORT+1)+STARTPORT;
	var server = http.createServer(function(request, response) {
		var givenURL = request.url;
		//substring out the /
		givenURL = givenURL.substring(1, givenURL.length);
		fileName = validateFilename(givenURL);
		if(fileName === false) {
			//console.log("setHeaderBadName");
			response.statusCode = 403;
			response.setHeader('Content-Type', 'text/html;');
			response.end("<h3>Invalid file name!</h3>");
		}
		else {
			giveFile(fileName, response);
		}
	});

	server.listen(port, HOSTNAME, function() {
		console.log('Server running at http://'+ HOSTNAME +':'+ port +'/');
	});
	
}
start();
