
# What is it ?

This is a Web app which retrieve european football data from 2012 to 2019, you can select a league then visualize who the best teams are and download the data in csv format. 

Avaiable league are french Ligue 1, spanish LaLiga, italian Serie A, german Bundesliga, english Premiere League, Champions League and Europa League.



# How to use it ?
```
git clone https://github.com/clementB94/DataEngineerTools.git
cd DataEngineerTools
cd 6Evaluation
cd Projet
docker-compose up
```

Download or clone the project and type "docker-compose up" in your terminal (download Docker if required) then wait a few seconds/minutes so that the project is set up and open "http://localhost:5000/football" in your browser.  


# Reproductibility

This project is composed in multiple parts, there is the Dockerfile and Docker-compose.yml file which describe the architecture of the project, make the link between the app and the database and install required dependencies. The scrapping.py file has been used to collect europa league and champions league datas with BeautifullSoup Scrapper. The insert_db.py file insert the datas in the MongoDB Database in the start of the project. The data_to_insert folder is where we store the data until it is in the database. The Templates folder is where are stored html files to design the app. Finaly, The app.py file is where we build and run the application, we have to create roads beetween html files and pythons scripts and manipulate the data in order to display it as we wish.
