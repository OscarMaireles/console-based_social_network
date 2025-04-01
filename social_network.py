
import os


def instructions():
    #display instructions
    #-> command changed to posts to make it more coherent with other commands
    #create usser, help and exit commands added 
    print("To create a new user, write: <username> create")
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
    print(f"{username} exists?")
    return True
    
def create_user():
    #create a file named as username.txt
    #a second file can be created with username_follows.txt
    print("username file created")
    print("username follows file created")
    
def follow():
    #add username to username_follows.txt
    print("username added to your following list")
    
def unfollow():
    #delete username to username_follows.txt
    print("username deleted from your following list")
    
def write_post(message):
    #fill username.txt with post text and datetime
    print("username posted ", message)
    print("post added to user timeline")    
    
def display_timeline():
    #Displays posts in username.txt
    print("timeline displayed")
  
def display_wall():
    #Display username timeline along with followed users timelines
    print("wall displayed")
    


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
            if check_user(username) == True:
              #if user exists, check action to do
                action =  command.split()[1]
                
                if action == "create":
                    create_user()
                    
                elif action == "posts":
                    message =command.split( )[2:] 
                    message = ''.join(message)
                    write_post(message)

                elif action == "follows":
                    second_user=command.split()[2]
                    print("<username> subscribed to <username2>")
                    follow()
                    
                elif action == "unfollows":
                    second_user=command.split()[2]
                    print("<username> unsubscribed to <username2>")
                    unfollow()
                    
                elif action == "wall":
                    print("<username>'s wall")
                    display_wall()
                    
                else:
                    print("command not valid, write: help to check available commands")
            else:
                print("username not valid, check usarename or create a new one")
        
        

