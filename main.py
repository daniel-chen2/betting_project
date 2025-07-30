import pandas as pd
import os
import glob

# Get the current working directory
current_directory = os.getcwd()

# Define the pattern to match all CSV files in the current directory
csv_files = glob.glob(os.path.join(current_directory, "*.csv"))

# Create an empty list to store individual DataFrames
df_list = []

# Loop through each CSV file, read it into a DataFrame, and append to the list
for file in csv_files:
    df = pd.read_csv(file)
    if("MaxD" in df.keys()):
        df_list.append(df)

# Concatenate all DataFrames in the list into a single DataFrame
df = pd.concat(df_list)

totalprofit = 0
totalBets = 0
correct=0
totalGames=0

for index, row in df.iterrows():
    totalGames+=1
    averageHome = float(row['AvgH']) 
    averageDraw = float(row['AvgD']) 
    averageAway = float(row['AvgA']) 
    maxH = float(row['MaxH']) 
    maxD = float(row['MaxD']) 
    maxA = float(row['MaxA']) 

    # print(f"Index: {index}, Home Team: {row['HomeTeam']}, Away Team: {row['AwayTeam']}, Average Home: {averageHome}, Average Away: {averageAway}, Average Draw: {averageDraw}, Max: {maxInt}")
    betValue=100
    commision = 0.94
    alpha = 0.039
    probabilityAverageHome = 1/(averageHome)
    willBetHome = maxH > 1/max((probabilityAverageHome-alpha), 0.01) and maxH < 6
    homeBet=0
    if(willBetHome):
        correct += row["FTR"] == "H"
        homeBet = betValue * (maxH-1) * commision if row["FTR"] == "H" else -betValue

    probabilityAverageAway = 1/(averageAway)
    willBetAway = maxA > 1/max((probabilityAverageAway - alpha),0.01) and maxA < 6
    awayBet=0
    if(willBetAway):
        correct += row["FTR"] == "A"
        awayBet = (betValue * (maxA-1) * commision if row["FTR"] == "A" else -betValue)

    probabilityAverageDraw = 1/(averageDraw)
    willBetDraw = maxD > 1/max((probabilityAverageDraw - alpha), 0.01) and maxD < 6
    drawBet=0
    if(willBetDraw):
        correct += row["FTR"] == "D"
        drawBet = (betValue * (maxD-1) * commision if row["FTR"] == "D" else -betValue) 

    # print(f"will Bet: {willBet}")
    totalprofit += drawBet + awayBet + homeBet
    if(willBetAway or willBetHome or willBetAway): 
        print(f"Index: {index}, Home Team: {row['HomeTeam']}, Away Team: {row['AwayTeam']}, Average Home: {averageHome}, Average Away: {averageAway}, Average Draw: {averageDraw}, MaxHome: {maxH}, MaxAway: {maxA}, MaxD: {maxD}")
        totalBets+=1
        print(f"betting {betValue}, Home bet: {homeBet}, away bet: {awayBet}, draw bet: {drawBet}")
        print(f"Result: {row['FTR']}")
        print(f"total profit: {totalprofit}")
    

print(f"totalBets: {totalBets}")
print(f"accuracy: {correct/totalBets if totalBets != 0 else 0}")
print(f"value per bet: {totalprofit/totalBets if totalBets != 0 else 0}")
print(totalprofit)
print(totalGames)
