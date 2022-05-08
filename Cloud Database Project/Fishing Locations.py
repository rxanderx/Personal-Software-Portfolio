from ast import Return
from traceback import print_list
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate("fishing-tracker-2da35-firebase-adminsdk-hp6as-62d48ca1f0.json")
firebase_admin.initialize_app(cred)
# TK ^ remove the key from the contents of the project and update the path.



db = firestore.client()
# now my client is stored to the database, and I can use the db to reference.

# db.collection('Locations').add({'location':'MontGomery Hole','temperature': 50, 'raining':True})

Running = True
while Running:
    #prompt user for action
    action = input("||To log a fishing trip, enter (1)\n||To access/modify a previous fishing log, enter (2)\n||To exit the program, enter (3)\n  : ")
    if action == '1':
        
        log_place = input("||Enter your fishing location:\n")
        confirm1 = input(f"||Is {log_place} correct? Y / N\n")

        if confirm1.upper() == "N":
            print("||Entry marked incorrect and discarded, returning you to the main selection.")
            pass

        elif confirm1.upper() == "Y":
            log_date = input("||Location confirmed. Now enter the date of your venture (format 00/00/0000):\n")
            confirm2 = input(f"||Is {log_date} correct? Y / N\n")

            if confirm2.upper() == "N":
                print("Entry marked incorrect and discarded, returning you to the main selection.")
                pass

            elif confirm2.upper() =="Y":
                user_entry = input("||Enter your best catch of the trip here. Enter NA if you were unsuccessful.\n")
                
                # the database call below is adding the doc in the locations collection
                
                db.collection('Locations').document(f'{log_place}').set({'Date':f'{log_date}','Catch':f'{user_entry}'})

                print("||Entry saved to logbook.")
                
                #TK save entry to logbook here


    elif action == '2':
        search_choice = input("||Would you like to search by fishing location, or date? (enter anything else to go back)\n")

        if search_choice.upper() == "LOCATION":

            #TK for this entry we will call and search the database by location
            log_place = input("||Enter the fishing location:\n")
            confirm1 = input(f"||Is {log_place} correct? Y / N\n")

            if confirm1.upper() == 'Y':
                doc_ref = db.collection(u'Locations').document(f'{log_place}')
                doc = doc_ref.get()
                print(doc)
                if doc.exists:
                    print(f'||Log found: {doc.to_dict()}')

                    edit_choice = input('||Would you like to edit this log? Y / N\n')
                    if edit_choice.upper() == "Y":
                        edit_choice2 = input('||Enter (1) to edit the location, (2) to edit the date, or (3) to delete this log\n')
                        
                        if edit_choice2 == '1':
                            new_loc = input('||Please enter the new location:\n')
                            #recieve and update the location
                            db.collection('Locations').document(f'{new_loc}').set({'Date':f'{doc.to_dict().get("Date")}','Catch':f'{doc.to_dict().get("Catch")}'})
                            db.collection('Locations').document(f'{log_place}').delete()
                            
                            pass

                        elif edit_choice2 == '2':
                            new_date = input("||Please enter the new date (format 00/00/0000):\n")
                            #recieve and update the date
                            db.collection('Locations').document(f'{log_place}').set({'Date':f'{new_date}','Catch':f'{doc.to_dict().get("Catch")}'})
                            pass

                        elif edit_choice2 == '3':
                            delete_check = input("||Are you sure you want to delete this log? Y/N\n")
                            if delete_check.upper() == "Y":
                                db.collection('Locations').document(f'{log_place}').delete()
                                # delete the log
                                pass                            
                        else:
                            print("||Input not recognized.")
                else:
                    print(f'No log found for {log_place}')
            

            pass




        elif search_choice.upper() == "DATE":
            #TK for this entry we will call and search the database by date
            log_date = input("||Enter the date of your venture (format 00/00/0000):\n")
            confirm1 = input(f"||Is {log_date} correct? Y / N\n")

            doc_ref = db.collection(u'Locations').where(u'Date',u'==',f'{log_date}')
            doc = doc_ref.get()
        

            if doc[0].exists:
                
                print(f'||Log(s) found: {doc[0].to_dict().get("Date")}')
                i = 0
                for each in doc:
                    print(f'({i+1}): {doc[0].id} {doc[i].to_dict().get("Catch")}')
                    i += 1

                _edit_choice = input(f'||Enter the number of the Log to edit ( 1 - {i} )\n')
                edit_choice = int(_edit_choice) - 1
                print(f'||Log number {_edit_choice} selected.')

                print(f'||{doc[int(edit_choice)].id}  {doc[int(edit_choice)].to_dict()}')
                edit_choice2 = input('||Enter (1) to edit the location, (2) to edit the date, or (3) to delete this log\n')

                if edit_choice2 == '1':
                    new_loc = input('||Please enter the new location:\n')
                    #recieve and update the location
                    db.collection('Locations').document(f'{new_loc}').set({'Date':f'{doc[int(edit_choice)].to_dict().get("Date")}','Catch':f'{doc[int(edit_choice)].to_dict().get("Catch")}'})
                    db.collection('Locations').document(f'{doc[int(edit_choice)].id}').delete()
                    
                    pass

                elif edit_choice2 == '2':
                    new_date = input("||Please enter the new date (format 00/00/0000):\n")
                    #recieve and update the date
                    db.collection('Locations').document(f'{doc[int(edit_choice)].id}').set({'Date':f'{new_date}','Catch':f'{doc.to_dict().get("Catch")}'})
                    pass

                elif edit_choice2 == '3':
                    delete_check = input("||Are you sure you want to delete this log? Y/N\n")
                    if delete_check.upper() == "Y":
                        db.collection('Locations').document(f'{doc[int(edit_choice)].id}').delete()
                        # delete the log
                        pass                            
                else:
                    print("||Input not recognized.")

            else:
                print(f'||No log of date {log_date} found')

            pass




        else:
            print("||Neither search type entered, returning you to the main selection.")

    elif action == '3':

        Running = False

    else:

        print("||Input unrecognized. ")



