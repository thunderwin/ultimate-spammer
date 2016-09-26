#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Variable that appears in the main menu as "popup" message
autoguipopup = ""

# Sets the popup variable if the module is absent
try:
    import pyautogui

except ImportError:
    print "[-] Import error: pyautogui."
    print "Maybe some dependencies are missing: https://github.com/asweigart/pyautogui"
    autoguipopup = "  <<< [-] Missing pyautogui module"
    raw_input("Press any key to continue...")

try:
    import sys
    import os
    import time
    import readline

    from src.EmailFunctions import *
    from src.SkypeFunctions import *

except ImportError as error:
    print "[-] Import error: " + str(error)
    raw_input("Press any key to continue...")
    sys.exit(1)

__author__ = 'Qubasa'

# Get os specific terminal command
if sys.platform.startswith('win'):
    clearCommand = 'cls'
else:
    clearCommand = 'clear'

# Add directory auto completion
readline.parse_and_bind("tab: complete")

# Check if variable is empty
def Empty(value):
    if value == "":
        raise ValueError("The Variable is empty.")


# Main gui where the spam method gets selected
def MainMenu():

    os.system(clearCommand)

    print '''
 [*] ULTIMATE SPAMMER 2.0 [*]

            .-------.
      _|~~ ~~  |_
    =(_|_______|_)=
      |:::::::::|
      |:::::::[]|
      |o=======.|
      `"""""""""`

    Creator: Qubasa
-------------------------------

1) Skype automated typing ''' + autoguipopup + '''

2) Clear your skype chat

3) Email spammer

4) Generic spammer ''' + autoguipopup + '''

99) Quit
    '''

    try:
        choice = raw_input('>> ')
        Exec_Menu(choice)

    except KeyboardInterrupt:
        os.system(clearCommand)
        DoExitMenu()

def AutoTypeTextMenu():

    # If module pyautogui is not installed function exits
    if autoguipopup != "":
        print "[-] Missing module: pyautogui."
        raw_input("Press any key to continue...")
        menu_actions['main_menu']()

    print """
        ##################################################
        #                     NOTE:                      #
        #                                                #
        #    To abort the spammer move your cursor       #
        #          to the upper left corner.             #
        #                                                #
        ##################################################

        """

    try:
        # Start Skype and print the friendlist
        InitSkype()
        friendlist = GetFriends()
        FriendMenu(friendlist)

        # Get user input
        while True:
            try:
                print 'Target number:'
                target = raw_input('>> ')
                target = int(target)

                print 'Your message to deliver:'
                msg = raw_input('>> ')
                Empty(msg)

                print 'How many times: '
                quantity = raw_input('>> ')
                quantity = int(quantity)
                print

                break

            except ValueError:
                print
                print '[-] Invalid input please try again!'
                print

        # Execute the spam function
        AutoTypeText(friendlist, target, msg, quantity)
        print "[+] Successfully send " + str(quantity) + " messages!"

    # EXCEPTION HANDLING -------------------------------------------------------------------
    except Skype4Py.SkypeError:
        print "[-] Skype raised an unexpected problem, please try again."

    except Skype4Py.SkypeAPIError:
        print "[-] Connection issues with skype. Is this program whitelisted ?"

    except KeyboardInterrupt:
        print "[+] Aborted program."

    except pyautogui.FailSafeException:
        print "[+] Aborted program."

    except Exception as er:
        print "[-] An unexpected error was raised: " + str(er)

    finally:
        raw_input("Press any key to continue...")
        menu_actions['main_menu']()


def ClearChatMenu():

    try:
        # Start Skype
        InitSkype()

        # Get user input
        choice = raw_input("Are you sure to delete ALL history ?[y/n]")

        # Clear chat
        if choice == "y":
            ClearChat()
            print "[+] Done."

    # EXCEPTION HANDLING -------------------------------------------------------------------
    except Skype4Py.SkypeError:
        print "[-] Skype raised an unexpected problem, please try again."

    except Skype4Py.SkypeAPIError:
        print "[-] Connection issues with skype. Is this program whitelisted ?"

    except Exception as er:
        print "[-] An unexpected error was raised: " + str(er)

    finally:
        raw_input("Press any key to continue...")
        menu_actions['main_menu']()


def DoExitMenu():

    try:
        # If skype is running ask if to quit process
        if skype.Client.IsRunning:

            # Get user input
            choice = raw_input("Do you wan to close skype ?[y/n]")

            # Quit skype and programm
            if choice == "y" or choice == "Y" or choice == "yes" or choice == "Yes":
                skype.Client.Shutdown()

        # WARNING: Do not use finally after an exit function
        # because the exception, SystemExit, then doesnt have any impact on the programm
        # and it doesnt quit.
        sys.exit()

    # EXCEPTION HANDLING -------------------------------------------------------------------
    except KeyboardInterrupt:
        print '[+] Aborted program.'
        raw_input("Press any key to continue...")
        menu_actions['main_menu']()

    except Exception as er:
        print "[-] An unexpected error was raised: " + str(er)
        raw_input("Press any key to continue...")
        menu_actions['main_menu']()


def Exec_Menu(choice):

    # Clear the console
    os.system(clearCommand)

    # If empty input immediately go back to main menu
    if choice == '':
        menu_actions['main_menu']()

    else:

        # Execute selected function out of dictionary
        try:
            menu_actions[choice]()

        # If given input isnt in dictionary
        except KeyError:
            print '[-] Invalid selection, please try again.'
            time.sleep(1)
            menu_actions['main_menu']()


def FriendMenu(friendlist):

    # Print a list out of all skype friends
    for index in friendlist:
        if friendlist[index][2] == '':
            x = 0
        else:
            x = 2
        print str(index) + ') ' + friendlist[index][x] + ' : ' + friendlist[index][1]
        print

def EmailSpammerMenu():
    choice = 0

    # server_dictionary[index][name][dnsname][port]
    server_dictionary = {

        1: ['Gmail', 'smtp.gmail.com', 587],
        2: ['Gmx', 'mail.gmx.net', 465],
        3: ['Icloudmail', 'smtp.mail.me.com', 587],
        4: ['Mail.de', 'smtp.mail.de', 587],
        5: ['Outlook', 'smtp-mail.outlook.com', 587],
        6: ['Yahoomail', 'smtp.mail.yahoo.com', 465],
        7: ['Web.de', 'smtp.web.de', 587],
        8: ['Sxmail', 'smtp.sxmail.de', 587]
    }

    try:
        # Prints an enumbered list of all supported mail server
        for index in range(len(server_dictionary)):
            print str(index + 1) + ") " + server_dictionary[index + 1][0]
        print

        # Get user input
        while True:
            try:
                print "Choose server:"
                choice = raw_input(">> ")
                print

                choice = int(choice)
                server = server_dictionary[choice][1]
                port = server_dictionary[choice][2]

                break

            except ValueError:
                print
                print '[-] Invalid input please try again!'
                print

            except KeyError:
                print
                print '[-] Invalid selection please try again!'
                print

        # Get more user input
        while True:
            try:
                print 'Your Email:'
                username = raw_input('>> ')
                Empty(username)

                print 'Your Password:'
                password = raw_input('>> ')
                Empty(password)

                print 'Target email:'
                targetemail = raw_input('>> ')
                Empty(targetemail)

                print 'Who send this email (From:) ?'
                fromemail = raw_input('>> ')
                Empty(fromemail)

                print 'Subject of this email:'
                subject = raw_input('>> ')
                Empty(subject)

                print 'Your message to deliver:'
                msg = raw_input('>> ')
                Empty(msg)

                print 'How many times: '
                quantity = raw_input('>> ')
                quantity = int(quantity)
                print

                break

            except ValueError:
                print
                print '[-] Invalid input please try again!'
                print

        # Execute spamming function
        EmailSpammer(server, port, username, password, targetemail, fromemail, subject, msg, quantity)
        print '[+] Sucessfully send ' + str(quantity) + " messages to " + targetemail + "."

    # EXCEPTION HANDLING -------------------------------------------------------------------
    except smtplib.SMTPAuthenticationError:
        if server_dictionary[choice][0] == "Gmail":
            print "In Gmail you have to whitelist apps connecting to your account:"
            print "https://www.google.com/settings/security/lesssecureapps"
        else:
            print "[-] Log in credentials are wrong or your email security settings are kicking in."

    except smtplib.SMTPConnectError:
        print "[-] Couldn't connect to server."

    except smtplib.SMTPRecipientsRefused:
        print "[-] Target doesnt exist."

    except Exception as er:
        print "[-] An unexpected error was raised: " + str(er)

    finally:
        raw_input("Press any key to continue...")
        menu_actions['main_menu']()


def GenericSpammerMenu():

    # If module pyautogui is not installed function exits
    if autoguipopup != "":
        print "[-] Missing module: pyautogui"
        raw_input("Press any key to continue...")
        menu_actions['main_menu']()

    try:
        # Get user input
        while True:
            try:

                print 'Your message to deliver:'
                msg = raw_input('>> ')
                Empty(msg)

                print 'How many times: '
                quantity = raw_input('>> ')
                quantity = int(quantity)
                print

                break

            except ValueError:
                print
                print '[-] Invalid input please try again!'
                print

        print """
        ##################################################
        #                     NOTE:                      #
        #                                                #
        #    To abort the programm move your cursor      #
        #          to the upper left corner.             #
        #                                                #
        ##################################################

        """
        print "Please focus your cursor in the targeted chat window"
        raw_input("Press enter to start spamming in 5 seconds...")
        print "Start in:"

        print 5
        time.sleep(1)
        print 4
        time.sleep(1)
        print 3
        time.sleep(1)
        print 2
        time.sleep(1)
        print 1
        time.sleep(1)

        # Execute spam function
        genericSpammer(quantity, msg)
        print "[+] Succesfully send " + str(quantity) + " messages."

    # EXCEPTION HANDLING -------------------------------------------------------------------
    except pyautogui.FailSafeException:
        print "[+] Aborted program."

    except KeyboardInterrupt:
        print "[+] Aborted program."

    except Exception as er:
        print "[-] An unexpected error was raised: " + str(er)

    finally:
        raw_input("Press any key to continue...")
        menu_actions['main_menu']()

# Dictionary of menu entrys
menu_actions = {
    'main_menu': MainMenu,
    '1': AutoTypeTextMenu,
    '2': ClearChatMenu,
    '3': EmailSpammerMenu,
    '4': GenericSpammerMenu,
    '99': DoExitMenu,
}

# Display main menu if file gets executed
if __name__ == '__main__':
    menu_actions['main_menu']()
