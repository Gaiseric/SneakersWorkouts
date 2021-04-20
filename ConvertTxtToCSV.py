import csv
 
def ConvertTxtToCSV(filename):
    workouts = []
    textfile = filename + ".txt"
    csvfile = filename + ".csv"
    try:
        with open(textfile, "r") as file:
            for line in file:
                lst = line.split(" ")
                if lst[0] == "\n":
                    continue
                elif lst[0] == "Ходьба" or lst[0] == "Бег":
                    if lst[0] == "Ходьба":
                        tmp = "Walk"
                    elif lst[0] == "Бег":
                        tmp = "Run"
                        row = {"Data": lst[1][0:-1], "Type": tmp, "Distance": lst[2]}                        
                        workouts.append(row)
        with open(csvfile, "w", newline="") as file:
            columns = ["Data", "Type", "Distance"]
            writer = csv.DictWriter(file, fieldnames=columns)
            writer.writeheader()
            writer.writerows(workouts)
        return 'Convertations was successfull'
    except Exception as e:
        return e