# MountainProject-DataScience
This repository stores code and files pertaining to data analytics/visualization performed on data scraped from mountainproject.com.

## Repository Organization
The file is split into 4 folders:
1) Data
2) Data Processing Notebooks
3) Data Science Notebooks
4) Figures

### Data Folder
The Data directory contains both the raw and processed data files used in our analyses.

The raw files are JSON files, and contain the exact data scraped from mountainproject.com at the beginning of January 2019. The processed data files are pickle files (.pkl) that are ready to be loaded directly into a Pandas DataFrame in python.

There are, specifically, processed data files for the following categories of information:
1) The users of mountain project (pickledPeople.pkl)
2) The routes on mountain project (pickledRoutes_unpacked.pkl)
3) The vote history of routes on mountain project (pickledVotes_unpacked.pkl)

There are corresponding JSON files for each of these files. Additionally there is an "areaData.json" file that was not used in any analyses (and thus does not have a corresponding processed pickle file).

### Data Processing Notebooks
The Data Processing Notebooks directory contains the files we used to import, process and adjust the raw JSON files (obtained by scraping mountainproject.com) into Pandas DataFrames, as well as save them as pickle files.

### Data Science Notebooks
The Data Science Notebooks directory contains the files we used to perform analyses on the data. The most successful of these include the "Mann-Whitney Test" file, the "MLR - Investigating Route Quality" file and the "Summary Statistics" file.

Additionally, there are some notebooks that I used to try and build a classifier ("Classifier", "Common People Finder") for routes that users would enjoy based on their past history of liking or disliking other routes. While no classifier was built, we were successfully able to identify the routes with the most common users for any given area.

### Figures
The Figures directory contains a few png files of figures that were produced in the Data Science Notebooks.