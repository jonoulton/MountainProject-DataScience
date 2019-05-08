import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def basic_route_info(routes):
    # List the grades
    simpleGradeList = ['3rd', '4th', 'Easy 5th', '5.0', '5.1', '5.2', '5.3', '5.4', '5.5', '5.6', '5.7', '5.8', '5.9', '5.10', '5.11', '5.12', '5.13', '5.14', '5.15']

    # Create a dict with all the grades as keys => The values will be the number of routes
    routesPerGrade = {}
    for i in simpleGradeList:
        routesPerGrade[i] = 0

    # Count the number of routes per grade
    for i in range(len(routes)):
        rating = routes.iloc[i]['simpleDiffRating']
        try:
            routesPerGrade[rating] = routesPerGrade[rating] + 1
        except:
            continue
    
    print("######################")
    print("## BASIC ROUTE INFO ##")
    print("######################\n")
    
    print("There are", len(routes), "routes on MountainProject.com\n")
    print("What does the breakdown look like for type of climb (e.g. Sport, Trad, Boulder)?\n")

    # Separate the respective climbing types
    trad = routes.loc[routes['trad'] == True]
    sport = routes.loc[routes['sport'] == True]
    boulder = routes.loc[routes['boulder'] == True]
    other = len(routes) - len(trad) - len(sport) - len(boulder)
    total = len(trad) + len(sport) + len(boulder)
    
    # Plot as a pie chart
    tot = len(trad) + len(sport) + len(boulder) + other
    tradLen = len(trad)/tot
    sportLen = len(sport)/tot
    boulderLen = len(boulder)/tot
    otherLen = other/tot
    explode = (0.05, 0.05, 0.05, 0.05)
    data = [tradLen, sportLen, boulderLen, otherLen]
    myLabels = ["Trad", "Sport", "Boulder", "Other"]

    fig, ax = plt.subplots(figsize=(10,6))
    ax.pie(data, explode=explode, labels=myLabels, autopct='%1.1f%%')
    ax.set_title("Relative Distribution of Route Types", fontsize=16)
    ax.axis('equal')
    plt.show()

    print("Number of Trad routes:", len(trad))
    print("Number of Sport routes:", len(sport))
    print("Number of Boulder problems:", len(boulder))
    print()
    print("Together this is", total, "climbs. This leaves *about*", len(routes)-total, "routes unaccounted for. \n'About', because some climbs are marked as multiple types (e.g. Trad and Sport). These climbs are made up of the more obscure disciples, let us consider those now.\n")

    aid = routes.loc[(routes['aid'] == True) & (routes['trad'] == False)]
    mixed = routes.loc[(routes['mixed'] == True) & (routes['trad'] == False)]
    ice = routes.loc[(routes['ice'] == True) & (routes['trad'] == False)]
    TR = routes.loc[(routes['TR'] == True) & (routes['trad'] == False) & (routes['sport'] == False) & (routes['boulder'] == False)]
    totalOther = len(aid) + len(mixed) + len(ice) + len(TR)

    print("Number of Aid routes:", len(aid))
    print("Number of Mixed routes:", len(mixed))
    print("Number of Ice routes:", len(ice))
    print("Number of Top-Rope routes:", len(TR))
    print("Together, these comprise", totalOther, "routes. \n\nThis clearly goes over our count of 188,536 routes. \nHowever, this is okay since some routes are marked as multiple types (e.g. 'Top-Rope' and 'Sport').\n")

    total = 0
    for i in range(len(routesPerGrade)):
        total = total + routesPerGrade[simpleGradeList[i]]

    print("We lump all 'roped' routes together by filtering for routes with grades such as 5.* ( Yosemite Decimal System). \nThis removes boulder problems, ice/mixed routes, and most aid-only routes.\n")
    print("Doing so demonstrates that there are", total, "routes rated with the Yosemite Decimal System (YDS).\n")
    
    print("Now we consider number of routes per grade for roped routes:")
    for i in range(len(routesPerGrade)):
        print(simpleGradeList[i], ":", routesPerGrade[simpleGradeList[i]])
    print("Total :", total)
    print()
    
    print("Great! For now, we will focus our analysis on this subset of", total, "routes.\n")


def plot_sport_vs_trad(routes):
    
    print("Now, let us consider the distribution of trad climbs vs sport climbs")
    print()
    
    # CREATE A LIST OF ALL MP GRADES
    with open('./Data/grades.txt') as file:
        reader = file.read()
        grades = []
        tempStr = ""
        for c in reader:
            if c != '\n':
                tempStr = tempStr + c
            else:
                grades.append(tempStr)
                tempStr = ""
                
    # Separate the trad and sport routes
    trad = routes.loc[(routes['trad'] == True) & (routes['sport'] == False)]['diffRating']
    sport = routes.loc[(routes['trad'] == False) & (routes['sport'] == True)]['diffRating']
    
    # GATHER QUANTITY OF EACH ROUTE INTO PRE-DEFINED ROUTE BINS 
    tradDistro = []
    for i in grades:
        tradDistro.append(np.sum(trad == i))

    sportDistro = []
    for i in grades:
        sportDistro.append(np.sum(sport == i))

    # CONVERT MULTIPLE GRADES TO SIMPLE GRADES (e.g. 5.10-/5.10a/5.10c => 5.10)
    simpleGrades = ['3rd', '4th', 'Easy 5th', '5.0', '5.1', '5.2', '5.3', '5.4', '5.5', '5.6', '5.7', '5.8', '5.9', '5.10', '5.11', '5.12', '5.13', '5.14', '5.15']
    simpleTrad = [0] * len(simpleGrades)
    simpleSport = [0] * len(simpleGrades)
    for i in range(len(simpleGrades)):
        for j in range(len(grades)):
            if simpleGrades[i] in grades[j] and simpleGrades[i] != '5.1':
                simpleTrad[i] = simpleTrad[i] + tradDistro[j]
                simpleSport[i] = simpleSport[i] + sportDistro[j]
            elif simpleGrades[i] is '5.1' and grades[j] == '5.1':
                simpleTrad[i] = simpleTrad[i] + tradDistro[j]
                simpleSport[i] = simpleSport[i] + sportDistro[j]

    # CHANGE THESE TO ALTER GRAPH (EXPANDED VS COMPRESSED GRADES)
    tradBars = simpleTrad   # CHANGE BTW SIMPLETRAD & TRAD DISTRO
    sportBars = simpleSport # CHANGE BTW SIMPLESPORT & SPORT DISTRO
    labels = simpleGrades   # CHANGE BTW SIMPLEGRADES & GRADES

    # NORMALIZE THE DATA
    normTrad = []
    for i in tradBars:
        normTrad.append(i/np.sum(tradBars))
    normSport = []
    for i in sportBars:
        normSport.append(i/np.sum(sportBars))

    # PLOT THE FIGURE
    fig, ax = plt.subplots(figsize=(10,6))
    ind = np.arange(len(labels))
    width = 0.2
    ax.bar(ind-(width/2), normTrad, width=width, tick_label=labels, color='blue')
    ax.bar(ind+(width/2), normSport, width=width, tick_label=labels, color='grey')
    ax.set_xlabel("Grade", fontsize=14)
    ax.set_ylabel("Relative Grade Density", fontsize=14)
    ax.set_title("Sport vs Trad Grade Distribution", fontsize=16)
    ax.tick_params(axis='x', labelrotation=80, labelsize=12)
    ax.tick_params(axis='y', labelsize=12)
    ax.legend(["Trad", "Sport"], fontsize=14)

    plt.show()

def plot_sport_vs_trad_simple(sport, trad):
    ratings = ['5.0', '5.1', '5.2', '5.3', '5.4', '5.5', '5.6', '5.7', '5.8', '5.9', '5.10', '5.11', '5.12', '5.13', '5.14', '5.15']

    # PLOT THE FIGURE
    fig, ax = plt.subplots(figsize=(10,6))
    ind = np.arange(len(ratings))
    width = 0.2
    ax.bar(ind-(width/2), trad, width=width, tick_label=ratings, color='blue')
    ax.bar(ind+(width/2), sport, width=width, tick_label=ratings, color='grey')
    ax.set_xlabel("Grade", fontsize=14)
    ax.set_ylabel("Relative Grade Density", fontsize=14)
    ax.set_title("Sport vs Trad Grade Distribution", fontsize=16)
    ax.tick_params(axis='x', labelrotation=80, labelsize=12)
    ax.tick_params(axis='y', labelsize=12)
    ax.legend(["Trad", "Sport"], fontsize=14)

    plt.show()
    
def routes_by_submit_date(routes):
    
    print("It may also be interesting to consider the number of climbs added to MP.com per year, as well as by year")
    
    simpleGrades = ['3rd', '4th', 'Easy 5th', '5.0', '5.1', '5.2', '5.3', '5.4', '5.5', '5.6', '5.7', '5.8', '5.9', '5.10', '5.11', '5.12', '5.13', '5.14', '5.15']
    
    routes = routes.dropna()
    # CREATE LIST OF UNIQUE SUBMISSION YEAR VALUES AND SORT THEM
    sortedYears = sorted(routes.subYear.unique())

    # GET DISCRETE NUMBER OF ROUTES ADDED IN 'X' YEAR, DIVIDED BY GRADE
    routesPerYear_Grade = [[np.sum((routes['subYear']==year) & (routes['simpleDiffRating']==grade)) for year in sortedYears] for grade in simpleGrades]

    # GET DISCRETE NUMBER OF ROUTES ADDED IN 'X' YEAR, DIVIDED BY GRADE
    routesPerYear_Grade = [[np.sum((routes['subYear']==year) & (routes['simpleDiffRating']==grade)) for grade in simpleGrades] for year in sortedYears]

    # GET DISCRETE NUMBER OF ROUTES ADDED IN 'X' YEAR ONLY (GRADE NOT CONSIDERED)
    routesPerYear_Total = [np.sum(routes['subYear']==year) for year in sortedYears]
    
    fig, ax = plt.subplots(figsize=(10,6))

    # PLOT THE DATA (X=YEARS, Y=ROUTES_PER_YEAR)
    ax.plot(sortedYears, routesPerYear_Grade)
    # ax.plot(sortedYears, routesPerYear_Total)

    # FORMAT THE GRAPH
    ax.set_title("Routes Added to MP.com per Year", fontsize=16)
    ax.set_ylabel("Number of Routes Added", fontsize=14)
    ax.set_xlabel("Year", fontsize=14)
    ax.legend(simpleGrades, loc=(1.01, 0.02), title="Legend", edgecolor='k', facecolor='lightgoldenrodyellow')
    ax.set_xticks(sortedYears)

    plt.show()
    
def quality_analysis(routes):
    
    # Introduction
    print("Are routes on MP.com generally high or low quality?")
    print("We determine this by considering the average rating of routes on MP.com")
    print()
    
    # Average quality of all routes together
    print("The average rating of all routes on MP.com is:", round(np.mean(routes['avgQualityRating']),2))
    print()
    
    # Quality of routes by grade
    # List the grades
    simpleGradeList = ['3rd', '4th', 'Easy 5th', '5.0', '5.1', '5.2', '5.3', '5.4', '5.5', '5.6', '5.7', '5.8', '5.9', '5.10', '5.11', '5.12', '5.13', '5.14', '5.15']

    # Create a dict with all the grades as keys => The values will be the number of routes
    byGrade = {}
    for i in simpleGradeList:
        byGrade[i] = [0, 0]

    # Calculate the average difficulty of routes per grade
    for i in range(len(routes)):
        route = routes.iloc[i]
        grade = route['simpleDiffRating']
        avgRating = route['avgQualityRating']
        try:
            byGrade[grade][0] = byGrade[grade][0] + 1
            byGrade[grade][1] = byGrade[grade][1] + avgRating
            
            # For Calculating a running average
            # byGrade[grade][1] = (byGrade[grade][1]*(byGrade[grade][0]-1) + routes.iloc[i]['avgQualityRating'])/byGrade[grade][0]

        except:
            continue
    for i in byGrade:
        byGrade[i][1] = byGrade[i][1]/byGrade[i][0]
    
    # Print out the results in text form
    print("What about by the average rating of each grade? Are some grades considered better than others?")
    print()

    pointsToPlot = []
    for i in range(len(byGrade)):
        print(simpleGradeList[i], ":", round(byGrade[simpleGradeList[i]][1],2))
        pointsToPlot.append(byGrade[simpleGradeList[i]][1])
                
    # Plot up route difficulty grade vs avg quality rating
    fig, ax = plt.subplots(figsize=(10,6))

    ax.plot(pointsToPlot, marker='.', linestyle='', color='cyan', markersize=16, markeredgecolor='blue')

    ax.set_title("Average Quality Rating by Grade", fontsize=16)
    ax.set_xlabel("Route Difficulty Rating", fontsize=14)
    ax.set_ylabel("Avgerage Rating", fontsize=14)
    ax.set_ylim(0,4)
    ax.set_xticks(np.arange(len(pointsToPlot)))
    ax.set_xticklabels(simpleGradeList, rotation=50)

    plt.show()
    
def get_best_worst(routes):
    
#     Introduction
    print("Of the 180,000+ routes on MP.com, there is only one route that holds the title of 'Best Route'. \nWhich route is it?\n")
    print("We determine this by first filtering the 'routes' dataframe to only include routes with a 4/4 star rating, \nand then sorting these routes by the number of quality votes. The route with the most votes with a 4/4 rating \nis deemed the 'Best Route' on MountainProject.com.\n")
    
    
    print("#################")
    print("## BEST ROUTES ##")
    print("#################\n")
    
    bestRoutes = routes.loc[routes['avgQualityRating'] == 4.0].sort_values(by='numQualityVotes', ascending=False)[:10]
    print("***")
    print("The Best Route on MountainProject.com is...", bestRoutes.iloc[0]['name'], bestRoutes.iloc[0]['diffRating'], "!")
    print("The link to", bestRoutes.iloc[0]['name'], "is here:", bestRoutes.index[0])
    print("***\n")
    
    print("There are some notable runner-ups (you may have heard of some of them) they are:")
    for i in range(1, len(bestRoutes)):
        print(i+1, ":", bestRoutes.iloc[i]['name'], bestRoutes.iloc[i]['diffRating'], "---", bestRoutes.index[i])
    print("---\n")
    
    print("##################")
    print("## WORST ROUTES ##")
    print("##################\n")
    
    print("It follows that we should also find the worst route on MP.com! \n\nTo do so, we follow the same procedure, but only include routes with a 0/4 average rating. \nThe route with the most votes with a 0/4 rating will be awarded the prestigious title of 'Worst Route'.\n")
    
    worstRoutes = routes.loc[routes['avgQualityRating'] == 0.0].sort_values(by='numQualityVotes', ascending=False)[:5]
    print("***")
    print("The Worst Route on MountainProject.com is...", worstRoutes.iloc[0]['name'], worstRoutes.iloc[0]['diffRating'], "!")
    print("The link to", worstRoutes.iloc[0]['name'], "is here:", worstRoutes.index[0])
    print("***\n")
    
    print("For obvious reasons, the worst routes have significantly fewer rating votes from users than do the top routes. \nSuch choss-fests aren't for the faint of heart! However, this does mean that our classification of the 'Worst Route' \nis probably not representative (since the dataset for votes on crappy routes is quite small).\n")
    print("For those disturbed folks who are so inclined to seek out the worst routes, here is a list of the runner-ups:")
    for i in range(1, len(worstRoutes)):
        print(i+1, ":", worstRoutes.iloc[i]['name'], worstRoutes.iloc[i]['diffRating'], "---", worstRoutes.index[i])
    print("---\n")

# Function to reduce the ratings to 5.0-5.15 from a python list (NOT a Pandas Dataframe)
def reduceRatings(ratingList):  
    ratings = ['5.0', '5.1', '5.2', '5.3', '5.4', '5.5', '5.6', '5.7', '5.8', '5.9', '5.10', '5.11', '5.12', '5.13', '5.14', '5.15']
    newList = []
    for i in range(len(ratingList)):
        if ratingList[i] in ratings:
            newList.append(ratingList[i])
    return sorted(newList)

# Function to reduce the ratings to 5.0-5.15 from a Dataframe with other data
def reduceRatingsDF(df):  
    ratings = ['5.0', '5.1', '5.2', '5.3', '5.4', '5.5', '5.6', '5.7', '5.8', '5.9', '5.10', '5.11', '5.12', '5.13', '5.14', '5.15']
    newList = []
    i = 0
    while i < len(df):
        try:
            if df.iloc[i]['simpleDiffRating'] in ratings:
                i = i+1
                continue
            else:
                df = df.drop(df.index[i])
            print(i/len(df), end='\r')
        except:
            break

    return df

# Function to get the densitry of route ratings
def countRatings(ratingList, density=False):
    ratings = ['5.0', '5.1', '5.2', '5.3', '5.4', '5.5', '5.6', '5.7', '5.8', '5.9', '5.10', '5.11', '5.12', '5.13', '5.14', '5.15']
    ratingsDict = {}
    for i in ratings:
        ratingsDict[i] = 0
    for i in ratingList:
        ratingsDict[i] = ratingsDict[i]+1
    if density:
        for i in ratings:
            ratingsDict[i] = ratingsDict[i]/len(ratingList)
    return ratingsDict

def avg_quality_by_grade(routes):
    ratings = ['5.0', '5.1', '5.2', '5.3', '5.4', '5.5', '5.6', '5.7', '5.8', '5.9', '5.10', '5.11', '5.12', '5.13', '5.14', '5.15']

    # Create a dict with all the grades as keys => The values will be the number of routes
    byGrade = {}
    for i in ratings:
        byGrade[i] = [0, 0]

    # Calculate the average difficulty of routes per grade
    for i in range(len(routes)):
        route = routes.iloc[i]
        grade = route['simpleDiffRating']
        avgRating = route['avgQualityRating']
        try:
            byGrade[grade][0] = byGrade[grade][0] + 1
            byGrade[grade][1] = byGrade[grade][1] + avgRating

        except:
            continue
    for i in byGrade:
        try:
            byGrade[i][1] = byGrade[i][1]/byGrade[i][0]
        except:
            continue
            
    lst = range(0,16)
    retDict = {}
    for i in range(len(lst)):
        retDict[lst[i]] = byGrade[ratings[i]]
    return retDict

def avg_quality_by_votes(routes):
    # Create a dict with all the votes as keys => The values will be the number of routes
    byVotes = {}
    for i in routes['numQualityVotes']:
        byVotes[i] = [0, 0]

    # Calculate the average difficulty of routes per number of votes
    for i in range(len(routes)):
        route = routes.iloc[i]
        votes = route['numQualityVotes']
        avgRating = route['avgQualityRating']
        try:
            byVotes[votes][0] = byVotes[votes][0] + 1
            byVotes[votes][1] = byVotes[votes][1] + avgRating
        except:
            continue
    for i in byVotes:
        try:
            byVotes[i][1] = byVotes[i][1]/byVotes[i][0]
        except:
            continue
    return byVotes

def findAvgRating(routes):
    ratings = []
    for i in range(len(routes)):
        ratings.append(routes.iloc[i]['avgQualityRating'])
    return np.mean(ratings)

def convertDiff(rating):
    ratings = ['5.0', '5.1', '5.2', '5.3', '5.4', '5.5', '5.6', '5.7', '5.8', '5.9', '5.10', '5.11', '5.12', '5.13', '5.14', '5.15']
    validRatings = {}
    count = 0
    for i in ratings:
        validRatings[i] = count
        count = count + 1
    if rating in validRatings:
        return validRatings[rating]
    else:
        return None
