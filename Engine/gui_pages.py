"""
-------------------------------
IMPORTS
-------------------------------
"""
import signal, json, time, os
import tkinter as tk
import multiprocessing as mp

from Engine import chessboard, gameState, audio

from Engine.GUI import gui_widgets as widgets, keyboard
from Engine.lichess import lichessInterface_new as interface


"""
-------------------------------
VARIABLES
-------------------------------
"""
eventQueue = mp.Queue()
gameQueue = mp.Queue()

eventstream = None
gamestream = None

terminated = False

eventstream_pid = None
gamestream_pid = None

app_username = "MagiChess_Bot"
"""
-------------------------------
PAGE CLASSES
-------------------------------
"""

class StartupPage(tk.Frame):
    def __init__(self, master, controller):
        tk.Frame.__init__(self, master)
        header = widgets.createLabel(self, text="MagiChess", font="times", fontsize=25, fontweight="bold")
        header.pack(padx=10, pady=10)

        #startup buttons
        signinButton = widgets.createButton(self, function=lambda: controller.show_frame(SigninPage),
                                text="Sign in to LiChess.org", bgcolor="sky blue")
        signinButton.pack(pady=10)

        exitButton = widgets.createButton(self, function=quit_program,
                                text="Exit", bgcolor="seashell3")    
        exitButton.pack()



class SigninPage(tk.Frame):
    def __init__(self, master, controller):
        tk.Frame.__init__(self, master)
        header = widgets.createLabel(self, text="Sign in to LiChess", font="times", fontsize=14, fontweight="bold")
        header.pack(padx=10, pady=10)

        """ username/password entries
        usernameLabel = widgets.createLabel(self, text="Username", font="times", fontsize=11, fontweight="normal")
        usernameLabel.pack()
        usernameEntry = widgets.createEntry(self, bgcolor="beige")
        usernameEntry.pack()

        passwordLabel = widgets.createLabel(self, text="Password", font="times", fontsize=11, fontweight="normal")
        passwordLabel.pack()
        passwordEntry = widgets.createEntry(self, bgcolor="beige", show="*")
        passwordEntry.pack()
        """

        """ buttons """
        loginButton = widgets.createButton(self, function=lambda: self.submit(controller=controller, username=app_username),
        text="Login as "+app_username, bgcolor="seashell3")
        loginButton.pack(pady=4)

        returnButton = widgets.createButton(self, function=lambda: controller.show_frame(StartupPage),
        text="Return", bgcolor="seashell3")
        returnButton.pack(pady=7)

    """ submit username/password for validation """
    def submit(self, controller, username, password=None):
        valid = 1

        # login as MagiChess_Bot
        if valid:
            controller.show_frame(MainMenuPage, user=username)

            # create and start an event stream process
            global eventstream
            eventstream = mp.Process(target = event_stream, args = (eventQueue,))
            eventstream.start()
            eventstream_pid = eventstream.pid
            print("EVENT STREAM PID: ", eventstream_pid)

        else:
            print("User not found. Invalid username/password")

        return




class MainMenuPage(tk.Frame):
    def __init__(self, master, controller):
        tk.Frame.__init__(self, master)
        
    def welcomeHeader(self, username):
        header = widgets.createLabel(self, text="Welcome to MagiChess, " + username, font="times", fontsize=14, fontweight="bold")
        header.pack(padx=10, pady=10)
        
    def menuButtons(self, controller):
        """ main menu options """
        widgets.createButton(self, function=lambda: controller.show_frame(PlayBotPage),
                                             text="Play Bot", bgcolor="sky blue").pack(pady=5)
        
        # widgets.createButton(self, function=lambda: controller.show_frame(PlayRandomPage),
        #                                      text="Seek an Opponent", bgcolor="sky blue").pack(pady=5)
        
        widgets.createButton(self, function=lambda: controller.show_frame(ChallengePage),
                                             text="Challenge a Friend", bgcolor="sky blue").pack(pady=5)
        
        widgets.createButton(self, function=lambda:controller.show_frame(ReplayGamePage),
                                                     text="Replay a Game", bgcolor="sky blue").pack(pady=5)

        widgets.createButton(self, function=quit_program,
                                             text="Exit MagiChess", bgcolor="seashell3").pack(pady=5)
        
     


""" main menu pages """
class PlayBotPage(tk.Frame):
    def __init__(self, master, controller):
        tk.Frame.__init__(self, master)
        header = widgets.createLabel(self, text="Play a Bot", font="times", fontsize=14, fontweight="bold")
        header.pack(padx=10, pady=10)
        
        #return to main menu
        returnButton = widgets.createButton(self, function=lambda: controller.show_frame(MainMenuPage),
                                            text="Return to Main Menu", bgcolor="sky blue")
        returnButton.pack()


""" play random page (currently not implemented) """
class PlayRandomPage(tk.Frame):
    def __init__(self, master, controller):
        tk.Frame.__init__(self, master)
        header = widgets.createLabel(self, text="Seeking Opponent...", font="times", fontsize=14, fontweight="bold")
        header.pack(padx=10, pady=10)
        
        #return to main menu
        returnButton = widgets.createButton(self, function=lambda: controller.show_frame(MainMenuPage),
                                            text="Return to Main Menu", bgcolor="sky blue")
        returnButton.pack()
        
    def seekOpponent(self):
        """
        send request to LiChess server to seek an opponent
        """
        
        return

""" challenge opponent page """        
class ChallengePage(tk.Frame):
    def __init__(self, master, controller):
        tk.Frame.__init__(self, master)
        header = widgets.createLabel(self, text="Search Opponent Name", font="times", fontsize=14, fontweight="bold")
        header.pack(padx=10, pady=10)

        # name input
        usernameEntry = keyboard.KeyboardEntry(self) 
        usernameEntry.pack(pady=10)

         # provide options for starting color
        userColor = tk.StringVar(value="1")
        widgets.createRadioButton(self, "Random", userColor, "random").pack()
        widgets.createRadioButton(self, "White", userColor, "white").pack()
        widgets.createRadioButton(self, "Black", userColor, "black").pack()

        # challenge button
        challengeButton = widgets.createButton(self, function=lambda: self.challenge(controller, userColor.get(), usernameEntry.get()),
                                                text="Challenge", bgcolor="sky blue")
        challengeButton.pack(pady=10)

        # return to main menu
        returnButton = widgets.createButton(self, function=lambda: controller.show_frame(MainMenuPage),
                                            text="Return to Main Menu", bgcolor="sky blue")
        returnButton.pack(pady=10)

    """ challenge user """
    def challenge(self, controller, userColor, username=""):

        print(userColor)
        if username == "":
            print("User not found")
        else:

            # challenge user and set gameid
            gameid = interface.challenge_user(username, color=userColor)

            if not gameid:
                print("Unable to complete challenge")
            else:

                interface.change_gameid(gameid)

                # used to cancel challenge request after 10 seconds
                time_out = int(time.time()) + 10

                # wait until challenger accepts or declines challenge
                accepted = False
                declined = False
                while not accepted and not declined:
                    try:

                        # grab event and check if game start has occurred
                        event = eventQueue.get_nowait()
                        if event["type"] == "gameStart":
                            if event["game"]["id"] == gameid:
                                print("game accepted")
                                accepted = True

                        # check if challenge has been declined
                        elif event["type"] == "challengeDeclined":
                            declined = True

                        # cancel challenge after 10 seconds
                        elif time.time() > time_out:
                            declined = True
                            interface.challenge_cancel(gameid)

                    except:
                        pass

                if accepted:
                    ingame(username, controller)
                if declined:
                    controller.show_frame(ChallengeDeniedPage)
        return


class ChallengeDeniedPage(tk.Frame):
    def __init__(self, master, controller):
        tk.Frame.__init__(self, master)
        header = widgets.createLabel(self, text="Challenge has been declined or timed out (10s)", font="times", fontsize=14, fontweight="bold")
        header.pack(padx=10, pady=10)

        returnButton = widgets.createButton(self, function=lambda: controller.show_frame(ChallengePage),
                                             text="Return", bgcolor="sky blue")
        returnButton.pack(pady=10)


""" replay game page """
class ReplayGamePage(tk.Frame):
    def __init__(self, master, controller):
        tk.Frame.__init__(self, master)
        header = widgets.createLabel(self, text="Want to replay a game? Input the Game ID", font="times", fontsize=14, fontweight="bold")
        header.pack(padx=10, pady=10)

        # game id entry box
        idEntry = keyboard.KeyboardEntry(self)
        idEntry.pack(pady=10)

        widgets.createButton(self, function=lambda: self.replay(controller, idEntry.get()), 
                            text="Replay with Gameid", bgcolor="sky blue").pack(pady=10)
        widgets.createButton(self, function=lambda: controller.show_frame(PreviousGamesPage),
                            text="View your previous games", bgcolor="sky blue").pack(pady=10)
        
        returnButton = widgets.createButton(self, function=lambda: controller.show_frame(MainMenuPage),
                                                text="Return", bgcolor="sky blue")
        returnButton.pack(pady=10)

    def replay(self, controller, gameid):
        return

""" list previous games  """
class PreviousGamesPage(tk.Frame):
    def __init__(self, master, controller):
        tk.Frame.__init__(self, master)

        # create frame for scrollbar
        sb_frame = tk.Frame(self)
        sb = widgets.createScrollbar(sb_frame)
        sb_frame.pack()

        # find past 25 games (completed), put them in listbox, and put listbox in scrollbar
        games = interface.get_all_games()
        gamelist = widgets.createListbox(sb_frame, width=100, yscrollcommand=sb.set)
        sb.config(command=gamelist.yview)
        sb.pack(side='right', fill='y')
        # make an entry for each game
        for game in games:
            # get date and time of game
            date_object = time.gmtime(int(game['time'])/1000.)
            date = time.strftime('%m/%d/%Y %H:%M', date_object)

            gamelist.insert('end', game["gameid"]+" ~ White: "+game["white"]+" ~ Black: "+game["black"]+" ~ Date: "+date)
        gamelist.pack(pady=10)

        widgets.createButton(self, function=lambda: self.replay(controller, gamelist.get(gamelist.curselection())), 
                            text="Replay your previous game", bgcolor="sky blue").pack(pady=10)

        # widgets.createButton(self, function=lambda: self.refresh(controller), text="Refresh", bgcolor="gray").pack(pady=10)

        returnButton = widgets.createButton(self, function=lambda: controller.show_frame(ReplayGamePage),
                                                text="Return", bgcolor="sky blue")
        returnButton.pack(pady=10)
        

    def replay(self, controller, entry):
        gameid = entry.split(" ~ ")[0]
        white = entry.split(" ~ ")[1].split(": ")[1]
        black = entry.split(" ~ ")[2].split(": ")[1]
        if white == app_username:
            user_color = 'w'
            opp_name = black
        elif black == app_username:
            user_color = 'b'
            opp_name = white

        response = interface.create_gamestream(gameid)
        lines = response.iter_lines()
        #iterate through the response message
        for line in lines:

            if line:
                event = json.loads(line.decode('utf-8'))
                moves = event["state"]["moves"]
                print(moves.split(" "))
        
        gamestate = gameState.GameState(replay=True, gameQueue=moves.split(" "), replay_user_color=user_color)
        chessboard.init_chessboard(opp_name, gamestate)

    def refresh(self, controller):

        # self.games = interface.get_all_games()
        # self.gamelist = widgets.createListbox(sb_frame, width=100, yscrollcommand=sb.set)
        # sb.config(command=gamelist.yview)
        # sb.pack(side='right', fill='y')
        pass


"""   
-------------------------------
FUNCTIONS
-------------------------------
"""

""" ingame: runs while user is currently in a game
    params:
        challengerName: name of player that user is playing
    return:
"""
def ingame(challengerName, controller):

    # create a game stream
    global gamestream
    gamestream = mp.Process(target=game_stream, args=(gameQueue,))
    gamestream.start()
    gamestream_pid = gamestream.pid
    print("GAME STREAM PID: ", gamestream_pid)

    # create a game state
    gamestate = gameState.GameState(gameQueue=gameQueue)

    # start chessboard game window and wait until chessboard window is closed
    chessboard.init_chessboard(challengerName, gamestate)




""" event_stream: seperate process for event stream
    params:
        eventQueue: responses from LiChess event stream will be placed in queue
    return:
"""
def event_stream(eventQueue):
    
    iterator = 0

    # run in background
    while not terminated:
        try:
            time.sleep(3)
            # api call to start an event stream
            response = interface.create_eventstream()
            lines = response.iter_lines()

            # iterate through the response message
            for line in lines:
                # place response events in control queue
                if line:
                    event = json.loads(line.decode('utf-8'))
                    eventQueue.put_nowait(event)
                else:
                    eventQueue.put_nowait({"type": "ping"})
            

        except:
            pass
    return



""" game_stream: seperate process for game stream
    params:
    return:
"""
def game_stream(gameQueue):

    # save initial state
    response = interface.create_gamestream()
    lines = response.iter_lines()
    initialState = json.loads(next(lines).decode('utf-8'))

    # run in background
    while not terminated:
        time.sleep(3)
        response = interface.create_gamestream()
        lines = response.iter_lines()
    
        #iterate through the response message
        for line in lines:

            if line:
                event = json.loads(line.decode('utf-8'))
                gameQueue.put_nowait(event)
 
    return


""" used for testing purposes """
def test():

    # create and start an event stream process
    global eventstream
    eventstream = mp.Process(target = event_stream, args = (eventQueue,))
    eventstream.start()
    print("EVENT STREAM PID: ", eventstream.pid)

    gameid = interface.challenge_user('wayli2')

    if not gameid:
        print("Unable to complete challenge")
    else:

        interface.change_gameid(gameid)

        # wait until challenger accepts or declines challenge
        accepted = False
        while not accepted:
            try:
                event = eventQueue.get_nowait()
                if event["type"] == "gameStart":
                    if event["game"]["id"] == gameid:
                        print("game accepted")
                        accepted = True

                if event["type"] == "challengeDeclined":
                    print("Challenge declined by: ", "username")
                    break
            except:
                pass

        if accepted:
            ingame("username", None)



""" quit_program: terminates all processes and closes window
    params:
    return:
"""
def quit_program():
    chessboard.terminate_pygame()
    
    global terminated
    terminated = True
    if eventstream != None:
        terminate_eventstream()
    if gamestream != None:
        terminate_gamestream()

    print("Quit Program")
    exit()

def terminate_gamestream():
    global gamestream
    if gamestream != None:
        while not gameQueue.empty():
            gameQueue.get()
        gamestream.terminate()
        gamestream.join()
        print("TERMINATED GAME STREAM")
        gamestream = None

def terminate_eventstream():
    global eventstream
    while not eventQueue.empty():
        eventQueue.get()
    eventstream.terminate()
    eventstream.join()
    print("TERMINATED EVENT STREAM")
    eventstream = None


"""
signal_handler: maps keyboard interrupt to terminate event/game streams
"""
def signal_handler(sig, frame):
    global eventstream_pid
    global gamestream_pid
    print("signal handler")
    if eventstream_pid != None:
        os.kill(eventstream_pid, 9)
        print("Event Stream Terminated")
    if gamestream_pid != None:
        os.kill(gamestream_pid, 9)
        print("Game Stream Terminated")

    exit()

signal.signal(signal.SIGINT, signal_handler)