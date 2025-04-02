import os
from datetime import datetime
import numpy as np
import csv


def instructions():
    #display instructions
    #-> command changed to posts to make it more coherent with other commands
    #create usser, help and exit commands added 
    print("To create a new user, write: <username> create (not valid if username exists)")
    print("To delete any user, write: <username> delete")
    print("To post, write: <username> posts <text>")
    print("To view anyone's timeline, write: <username>")
    print("To follow anyone's timeline, write: <username> follows <other_username>")
    print("To unfollow anyone's timeline, write: <username> unfollows <other_username>")
    print("To check anyone's wall, write: <username> wall")
    print("if you need help, write: help")
    print("if you want to exit, write: exit")
    print("\n notes: <username> has to be a single word")
    
def check_user(username):
    #check if username exists
    return os.path.isfile(f"./Users/{username}.csv")

def check_posts(username):
    #check if username timeline is empty
    with open(f'./Users/{username}.csv', 'r') as csvfile:
        csv_dict = [row for row in csv.DictReader(csvfile)]
        if len(csv_dict) == 0:
            return False
        else:
            return True
    
def create_user(username):
    #create a file named as username.csv
    #a second file can be created with username_follows.csv
    with open(f"./Users/{username}.csv", "w") as my_empty_csv:
        pass
    with open(f"./Users/{username}_follows.csv", 'a', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow([username])
    print(f"{username} user created")

def delete_user(username):
    #delete a file named as username.csv
    #username_follows.txt is also deleted    
    os.remove(f"./Users/{username}.csv")
    os.remove(f"./Users/{username}_follows.csv")
    print(f"{username} user deleted")
    
def follow(username, second_user):
    #add second_user to username_follows.csv
    followed=np.loadtxt(f"./Users/{username}_follows.csv",dtype=str,delimiter=';',usecols=(0,))
    #check if second_user is already in the followed list fist
    if second_user in followed:
        print(f"{second_user} already followed")
    else:
        with open(f"./Users/{username}_follows.csv", 'a', newline='') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow([second_user])
            print(f"{second_user} added to your following list")
    
def unfollow(username, second_user):
    #delete second_user in username_follows.csv    
    with open(f"./Users/{username}_follows.csv", "r") as f:
        reader = csv.reader(f)
        rows_keep = [row for row in reader if row[0] != second_user]

    #rewrite username_follows.csv
    with open(f"./Users/{username}_follows.csv", "w", newline="") as wrt:
        writer = csv.writer(wrt)
        for row in rows_keep:
            writer.writerow(row)
    print(f"{second_user} deleted from your following list")
    
def write_post(username, message):
    #fill username.txt with post text and datetime (in seconds)
    current_dateTime = datetime.now()
    print(f"{username} posted ", message)
    with open(f"./Users/{username}.csv", 'a', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow([message, int(current_dateTime.timestamp())])   
    
def display_timeline(username):
    #Displays posts in username.csv
    #first check if username.csv is empty
    if check_posts(username) == True:
        #create datetime to print the elapsed time since the creation of each post
        current_dateTime = datetime.now()
        #load posts and dates stored in username.csv
        posts=np.loadtxt(f"./Users/{username}.csv",dtype=str,delimiter=';',usecols=(0,))
        dates=np.loadtxt(f"./Users/{username}.csv",dtype=int,delimiter=';',usecols=(1,))
        timediff=int(current_dateTime.timestamp())-dates
        #print posts and times
        for i in range(len(posts)-1, -1, -1):
            if timediff[i]<60:
                print (posts[i], "\t", f"(less than a minute ago)")
            elif timediff[i]>60 and timediff[i]<3600:
                print (posts[i], "\t", f"({int(timediff[i]/60)} minutes ago)")
            elif timediff[i]>3660 and timediff[i]<3600*24:
                print (posts[i], "\t", f"({int(timediff[i]/3600)} hours ago)")
            elif timediff[i]>3660*24 and timediff[i]<3600*24*365:
                print (posts[i], "\t", f"({int(timediff[i]/(3600*24))} days ago)")
            elif timediff[i]>3660*24*365:
                print (posts[i], "\t", f"({int(timediff[i]/(3600*24*365))} years ago)")
    else:
        print("no posts added")
  
def display_wall(username):
    #Display username timeline along with followed users timelines
    posts=[]
    dates=[]
    users=[]
    #create datetime to print the elapsed time since the creation of each post
    current_dateTime = datetime.now().timestamp()
    #load usernames followed, by default, username itself exists
    followed=np.loadtxt(f"./Users/{username}_follows.csv",dtype=str,delimiter=';',usecols=(0,))
    #load all posts, dates and user corresponding to each post
    for name in followed :
        if check_posts(name) == True:
            other_posts=np.loadtxt(f"./Users/{name}.csv",dtype=str,delimiter=';',usecols=(0,))
            posts.extend(other_posts)    
            other_dates=np.loadtxt(f"./Users/{name}.csv",dtype=int,delimiter=';',usecols=(1,))
            other_dates=int(current_dateTime)-other_dates
            dates.extend(other_dates)
            users.extend([name]*len(other_posts))
        else:
            continue
        
    #sort the three lists depending on time
    dates, posts, users = zip(*sorted(zip(dates, posts, users)))
    
    #print wall posts
    for i in range(len(posts)):
            if dates[i]<60:
                print (f"{users[i]}  -  {posts[i]} \t (less than a minute ago)")
            elif dates[i]>60 and dates[i]<3600:
                print (f"{users[i]}  -  {posts[i]} \t ({int(dates[i]/60)} minutes ago)")
            elif dates[i]>3660 and dates[i]<3600*24:
                print (f"{users[i]}  -  {posts[i]} \t ({int(dates[i]/3600)} hours ago)")
            elif dates[i]>3660*24 and dates[i]<3600*24*365:
                print (f"{users[i]}  -  {posts[i]} \t ({int(dates[i]/(3600*24))} days ago)")
            elif dates[i]>3660*24*365:
                print (f"{users[i]}  -  {posts[i]} \t ({int(dates[i]/(3600*24*365))} years ago)")


if __name__ == "__main__":
    #Create a folder to store users publications
    #in case it does not exist, create
    Users_folder="./Users/"
    if not os.path.exists(Users_folder):
        os.makedirs(Users_folder)
    
    #First diplay instructions to help user
    instructions()
    
    command=""
    #Then user enters inputs until input equals to exit
    while True:
        #the user inputs a command
        command = input("Enter your command: ")
        username= command.split()[0]
        if len(command.split())==1:
            #display instructions if input equals help
            if username == "help":
                instructions()
            #stop execution
            if username == "exit":
                break;
            #display username timeline, if user exists
            else:
                if check_user(username)==True:
                    display_timeline()
                else:
                    print("username not valid, check usarename or create a new one")
        
        if len(command.split())>1:               
            action =  command.split()[1]
            #if user exists, check action to do              
            if check_user(username) == True:
                    
                if action == "posts":
                    message =command.split()[2:] 
                    message = ' '.join(message)
                    write_post(username, message)
                    
                elif action == "delete":
                    delete_user(username)

                elif action == "follows":
                    second_user=command.split()[2]
                    if check_user(second_user) == True:              
                        follow(username, second_user)
                    else:
                         print("the user to follow does not exist")
                    
                elif action == "unfollows":
                    second_user=command.split()[2]
                    if check_user(second_user) == True:                
                        unfollow(username, second_user)
                    else:
                         print("the user to unfollow does not exist")
                    
                elif action == "wall":
                    display_wall(username)
                    
                else:
                    print("command not valid, write: help to check available commands")
            else:
                if action == "create":
                    create_user(username)
                
                else:
                    print("username not valid, check usarename or create a new one")
        
        

