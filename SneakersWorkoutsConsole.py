import ConvertTxtToCSV as cnv
from DBOperations import DBManager

def main(dbname: str):
    db = DBManager(dbname)
    db.SetConnection()
    while True:
        print()
        print('---------SneakersWearJournalMenu-----------')
        print()
        print('1 - Add new sneaker to DB\n2 - Add new workout to DB\n3 - Add workouts from csv file to DB')
        print('4 - Print all workouts for sneaker\n5 - Delete sneaker\n6 - Delete workout\n7 - Exit')
        print()
        print('-------------------------------------------')
        key = 0
        try:
            key = int(input())
        except:
            print('Invalid input value')
        finally:
            if key == 1:
                sneakername = input('Input sneaker name: ')
                print()
                print(db.CreateNewSneaker(sneakername))
            elif key == 2:
                sneakername = input('Input sneaker name: ')
                date = input('Input date as dd.mm.yy: ')
                type = input('Input workout type (Run/Walk): ')
                distance = input('Input workout diatance in km: ')
                values = (date, type, distance)
                print()
                print(db.CreateNewWorkout(sneakername, values))
            elif key == 3:
                sneakername = input('Input file name (must match with sneakername): ')
                print()
                print(db.AddWorkoutsFromCSV(sneakername))
            elif key == 4:
                sneakername = input('Input sneaker name: ')
                print()
                print(db.PrintWorkoutsForSneaker(sneakername))
            elif key == 5:
                sneakername = input('Input sneaker name: ')
                print('Are you sure? This also will delete all workouts for selected sneaker')
                decision = input('Yes/No:')
                if decision == 'Yes':
                    print(db.DeleteSneaker(sneakername))
            elif key == 6:
                sneakername = input('Input sneaker name: ')
                date = input('Input date as dd.mm.yy: ')
                type = input('Input workout type (Run/Walk): ')
                values = (date, type)
                print('Are you sure?')
                decision = input('Yes/No:')
                if decision == 'Yes':
                    print(db.DeleteWorkout(sneakername, values)) 
            elif key == 7:
                db.CloseConnection()
                break
            else:
                print('Uncorrect command')

if __name__=="__main__":
    main('SneakersWorkouts.db')