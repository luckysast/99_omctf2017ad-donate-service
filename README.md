Donation service

This is repo for donation service for OmCTF-2017

Used:
	- Flask (+extensions)
	- MongoDB (donations db)
	- Collections:
		- 1
		- 2
		- 3
		- constants

Endpoints:
	/donation/				 							- index page - referrer to donations/credits
		---
	/donation/credits/							- submit form for credits
	/donation/credits/history 			- show all donats (#, cardNumber(placeholdered), name, summ)
	/donation/credits/info?id=... 	- detailed information about donation by unique id (with another parameter)
		---
	/donation/karma									- submit form for karma points (affect on bg color of one field)
		---
	/donation/flags									- submit form   		-- deprecated

Models:
	Flags: --deprecated
		- flag
		- date

	Credit:
		- uid				uuid3 (need to solve this)
		- name
		- number		-valid
		- expired		-valid
		- ccv				
		- email			
		- comment		-flag stored here
		- date			

	Karma:
		- value
		- date
		we store abs min and max in separate Mongo Document to calc bg color


	Successfull donations flushes messages with link to detailed info
	
	After donation user get unique id to see own donations
	id generated using card info (in base app - number + name)		

----------------------

	Queries:

	Get last donations flags (+pagination)
	Get top donations credit aggregated by name (name, total donat!) +pagination
	Get last donations credit, not aggregated (date, names, donat, comment* modified by ***) +pagination
	Get full info about all donats thru secret info (names, number, ccv)* with no links (or hidden)
	karma - query to sum of all donats, get min and get max/

