# Visualizing-NYC-Neighborhood

CSCI-GA.3033-005 - Big Data Application Development

A. TEAM MEMBERS:

1. Daffney Deepa Viswanath
2. Aneri Dalal
3. Rong Feng

B. DATASETS: 

1. NYC Citywide Annualized Calendar Sales - https://data.cityofnewyork.us/City-Government/NYC-Citywide-Annualized-Calendar-Sales-Update/w2pb-icbu 

2. 311 Service Requests from 2010 to Present - https://data.cityofnewyork.us/Social-Services/311-Service-Requests-from-2010-to-Present/7ahn-ypff 
	
3. GreatSchools School Ratings - (Data scrapped from website using bot) https://www.greatschools.org

C. FOLDER DETAILS:

1. data_ingest
	- contains the Scala Code for preprocessing the datasets. 

2. etl_code
	- code for cleaning and parsing each of the dataset. 

3. profiling_code
	- Code for profiling each of the dataset.

4.app_code
	- code for combining all the dataset into one data frame and visualizing it

5. screenshots
	- Contains all screenshots of visualization.

D. PROCESS TO RUN:
 
1. data_ingest

	- read each text file in directory for steps to ingest data
	- GreatSchools data must be scraped from website using GreatSchools_scraper.py

*****************************************************************************************
*****************************************************************************************

2. etl_code

	- 311_clean.spark
		- uses csv file from https://data.cityofnewyork.us/Social-Services/311-Service-Requests-from-2010-to-Present/7ahn-ypff
		- outputs text files with cleaned data
	- GreatSchools_clean.spark 
		- uses csv file from scraper 
		- outputs parquet file with cleaned data
	- NYC_Prop_Sale_clean.spark
		- uses csv file from https://data.cityofnewyork.us/City-Government/NYC-Citywide-Annualized-Calendar-Sales-Update/w2pb-icbu
		- outputs csv file with cleaned data

*****************************************************************************************
*****************************************************************************************

3. profiling_code

	- run each code in directory to see profiling information about the datasets

*****************************************************************************************
*****************************************************************************************

4. app_code

	- run All_Datasets_Processing_Joining.spark first
		- uses output files from cleaning section
		- processes code to produce score/value
		- outputs parquet files with joined data
	- make_map.py
		- python code to create maps
	- Valuing NYC Neighborhoods.ipynb

*****************************************************************************************
*****************************************************************************************

5. screenshots

	- map with 0 weight school ratings and 100 weight 311 ratings
	- map with 50 weight school ratings and 50 weight 311 ratings
	- map with 100 weight school ratings and 0 weight 311 ratings
	- summary graphs of each dataset grouped by borough

