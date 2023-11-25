# UOCIS322 - Project 6 Brevets, but with RESTful API and MongoEngine now


# Descriptions


## Application


This project involves the development of hosting a website that allows user input for the duration of a bike ride, and brevet locations in terms of distance. In return for such information, the program will automatically fill in the brevet times that should be put in place based on the standards given. The program relies heavily on JQuery, Python, JavaScript, HTML, MongoEngine and Docker for testing in a more controlled enviorment. Now, however the program is improved by providing the ability to save a race and the associated table using a submit button, and the ability to display the last submitted table using the display button. The tables are saved and served via MongoEngine through an API.



## Algorithm


In this project we take information from the user using JQuery in the html file and send it to our main python file called flask_brevets.py that then parses the information as needed as well as handles the webpage directing. From there flask_brevets sends a request to acp_times.py that handles ensuring the validity of the entries, as well as determing how much time should be allocated to the open and close times of the given brevet and sends such information back to flask_brevets.py. After that flask_brevets.py uses json to send the information back over to the html file that then formats and redirects the information to the webpage to fill in the boxes associated with the opening and closing time brevets. Beyond all this when the submit button is clicked all of the associated information on the page is stored using the API which utlizes MongoEngine to store all of the information in the flask app using a route case and jquery, then the page is cleared of all entries. When a user clicks on the display button, provided they have submitted at least one entry, the most recent entry is then fetched on the flask app from the API (which uses MongoEngine) and returned to the table via json. 



# Instructions For Use


## Docker Compose
To run docker compose for this application first ascertain that you are in the correct directory, specifically the one that contains the Docker-compose file. From there proceed to make your Docker image by executing the command:


docker-compose up --build



Supposing everything went smoothly, your web application should now be up and running. 



## Web App



In the web application there are three main important fields to fill:


* The first is the distance of the brevet which you can select from the Distance selector. You may select from the provided options of 200, 300, 400, 600, 1000.


* The second is the date and time selector for the start of your brevet labeled as "Begins at". There you may select the proper day, month, year, and time that you wish for your brevet to begin.


* The third field to fill in is where you wish to place your control brevets in the race. You may choose to either type in the miles or kilometers field and rest assured that no matter which you choose all else will be filled in. After you type in your control brevet distance the rest of the row should fill in aside from the location which you may set. However, if you enter an invalid number according to ACP, then no automatic entries will appear until you correct it.

* Beyond this there are two possible buttons for the user to click. The first button is called submit and will effectively save and clear the given table of all relevant information pertaining to the brevets. The second button is called display and will return the last saved table of relevant information pertaining to the brevets.




# Authors

Michal Young, Ram Durairajan. Updated by Ali Hassani. Completed by Ellison Schilling.

## Contact Address

ellisons@uoregon.edu

