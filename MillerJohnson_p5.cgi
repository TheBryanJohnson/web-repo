#!/usr/bin/ruby

#Authors: William Miller, Bryan Johnson
#Purpose: FanXelk2.0, a web service that displays sports statistics using Ruby. 

#Set up json and cgi
require "json"
require "cgi"
cgi = CGI.new
print cgi.header


#Display the html form
def display_form()
	start_html()
	begin	
		sports = JSON.parse(open("Sports.json").read)
		
	rescue
		puts "<h3> Sports.json is missing or bad! </h3>"
		end_html()
		return
	end

	puts "
	<form action='MillerJohnson_p5.cgi' method='get'>
		Title:
		<select name='title'>
			<option value = "">Select...</option>"
	begin
		sports['sport'].each do |sport|
			#puts '<option value=>' + sport['title'] + '</option>'
			tmp = sport['title'].gsub(' ', '_')
			#puts '<option value=>' + tmp + '</option>'
			if(tmp!="")
				puts '<option value=' + tmp + '>' + sport['title'] + '</option>'
			end
		end
	
		puts "
		<select>
		&nbsp;&nbsp;&nbsp;
		Results:
		<select name='results'>
			<option value = "">Select...</option>"
		sports['sport'].each do |sport|
			#resKeys = sport['results'].keys
			#puts '<option value="a">' + sport['title'] + '</option>'
			sport['results'].each do |res|
				puts '<option value=' + res[0] + '>' + res[0] + '</option>'
			end
		end	
	
		puts "
		</select>
		&nbsp;&nbsp;&nbsp;
		Search Term:
		<select name='searchTerm'>
			<option value = "">Select...</option>"
		allTerms = []
		termDupe = false
		sports['sport'].each do |sport|
			sport['searchterms'].each do |term1|
				#puts '<option value=' + term1 + '>' + term1 + '</option>'
				termDupe = false
				allTerms.each do |term2|
					if(term1==term2)
						termDupe = true
					end
				end
				if(!termDupe)
					allTerms.push(term1)
					puts '<option value=' + term1 + '>' + term1 + '</option>'
				end
			end
		end
	
		puts "
		</select>
		&nbsp;&nbsp;&nbsp;
		<input type='submit' value='Submit'>
		</form>"
	rescue
		puts "</select></form><h3> JSON file not properly formatted! </h3>"
		end_html()
		return
	end
end

#Process the form, checking for validity and printing off the requested
#record
def process_form(cgi) 
	start_html()

	title = cgi["title"]
	results = cgi["results"]
	searchTerm = cgi["searchTerm"]
	
	
	#Fix the input fields: they will come in with _'s instead of spaces
	title = title.gsub('_', ' ')
	results = results.gsub('_', ' ')
	searchTerm = searchTerm.gsub('_', ' ')

	#Start from scratch for security
	sports = JSON.parse(open('Sports.json').read)
	titleFailed = true

	sports["sport"].each do |sport|
		if sport['title'] == title
			titleFailed = false
			sport["results"].each do |key, fileName|
				if(key == results)
					showResults(fileName, searchTerm)
					end_html()
					return
				end
			end

		end

	end

	if titleFailed
		puts "<p> Title not found, please use the HTML form! </p>"
	else 
		puts "<p> Results not found! Try a different season. </p>"	
	end

	end_html()
end

#Show results for requestsd filename and searchterm
def showResults(fName, sTerm)
	begin
		allData = JSON.parse(open(fName).read)
	rescue
		puts "<h3> JSON file missing or incorrect! </h3>"
		end_html()
		return
	end

	puts "<h3>"
	begin
		allData['comments'].each do |line|
			puts line 
		end
	rescue
		puts "JSON file missing comments!"
		end_html()
		return
	end
	puts "</h3>"

	wincount = 0
	begin
		allData['games'].each do |game|
			puts "~~~~~~~~~~~~~<br>"
			keys = game.keys
			for i in 0..keys.length-1
				cont = keys[i] + ": " + game[keys[i]]
				if(sTerm == keys[i])
					puts "<b>" + cont + "</b>"
				else
					puts "<p>" + cont + "</p>"
				end
				#update win counter
				if(keys[i] == "WinorLose" && game[keys[i]] == "W")
					wincount+=1
				end
			end
		end
		puts "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~<br>"
		puts "Wins: #{wincount} out of #{allData['games'].length} <br>"
		puts "Avg Winrate: #{wincount*100/allData['games'].length}%"
	rescue
		puts "<h3> JSON file missing games! </h3>"
		end_html()
		return
	end
	end_html()
end



#HTML header
def start_html() 
	puts "
	<html>
	<head>
		<title>Sports!</title>
	</head>
	<body>
		<h1>FanXelk2.0</h1>
		<p>Disclaimer: A particular sport may not have information for a selected season.</p>
		<p>Disclaimer2: If a particular search term is not found, it will be ignored.</p>
	"
end

#HTML closing tags
def end_html()
	puts "
	</body>
	</html>
	"
end


#if the cgi file is requested with title and results params,
#process it. Otherwise, show the form.
if (cgi["title"] != "") && (cgi["results"] != "") 
	process_form(cgi)
else 
	display_form()
end
