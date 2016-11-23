#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Script Name   : library_mvc_v1.py
# Author        : shashial
# Description   : Book management system using MVC + SOLID

import datetime

#hardcoded initial 'database' 
#list of books at the library
bookz = ['book1', 'book2', 'book3', 'book4', 'book5', 'book6', 'book7', 'book8', 'book9', 'book10', 'book11']
#list of users and corresponding books
userz = {
'user1':{'book12':'2016-11-15', 'book13':'2016-10-14'},
'user2':{},
'user3':{'book14':'2016-11-15'},
'user4':{'book15':'2016-11-15', 'book16':'2016-10-14', 'book17':'2016-10-14'}
}

class Model:
  """
  model is called by controller and calls view
  model looks after overall logic, every action is done with model involved
  """
  def __init__(self):
    self.book_limit = 3
  def get_books(self):
    """get list of books"""
    return [book for book in bookz]

  def get_users(self):
    """get list of users"""
    return [user for user, books in userz.iteritems()]

  def user_exists(self, uname):
    """checks if user exists"""
    users = main_model.get_users()
    if uname in users:
      main_view.print_found(uname)
    else:
      main_view.print_not_found(uname)

  def book_in_library(self, book):
    """checks if a book in the library"""
    books = main_model.get_books()
    if book in books:
      main_view.print_found(book)
    else:
      main_view.print_not_found(book) 

  def book_in_user(self, uname, book):
    """check if the user has the book"""
    user_books = []
    for i,k in userz[uname].iteritems():
      user_books.append(i)
    if book in user_books:
      main_view.print_found(book)
    else:
      main_view.print_not_found(book)

  def take_book(self, uname, book):
    """take a book from library"""
    #check if user exists
    main_model.user_exists(uname)

    #check users ammout of books taken
    if (len(userz[uname])) >= main_model.book_limit:
      main_view.print_book_limit()

    #check if book in library
    main_model.book_in_library(book)

    #give a book to a user, add date
    bookz.remove(book)
    userz[uname][book] = str(datetime.datetime.now().date())

    #print success message
    main_view.print_book_taken(uname, book)

  def give_book(self, uname, book):
    """give a book to a user"""
    #check if the user exists
    main_model.user_exists(uname)

    #check if the user has the book
    main_model.book_in_user(uname, book)

    #take a book from user, add it to the library
    userz[uname].pop(book)
    bookz.append(book)

    #print success message
    main_view.print_book_returned(uname, book)


  def give_expired_list(self):
    """
    Print list of the users with expired books.
    Current realisation assumes, that there are 31 days in every month.
    """
    ex_users = []
    #get current date
    now = datetime.datetime.now().date()

    #check date for every book
    for i, k in userz.iteritems():
      for j, b in k.iteritems():
        book_time = datetime.datetime.strptime(b, "%Y-%m-%d").date()
        #if the book is expired(differens is more than 31 days) then add user to naughty list
        if (abs(now-book_time).days) > 31:
          ex_users.append(i)
    #user must be unique
    ex_users = set(ex_users)
    #print list of user with at least 1 expired book
    main_view.print_users(ex_users)

  def file_input(self, fname):
    pass

  def array_input(self, ):
    pass

class View:
  """iew is used to create all the output of a programm"""
  def __init__(self):
    self.cli_menu = ("Menu", "Books available", "Users available", "Take a book", "Return a book", "List users with expired books", "Credits", "Exit")
  
  def print_cli(self):
    counter = 0;
    print("\n")
    for i in range(0, len(main_view.cli_menu)):
      print(str(counter)+'. '+main_view.cli_menu[i])
      counter+=1
    print("\n")

  def print_books(self, books):
    print('\nBooks available:\n')
    for i in books:
      print(i)
    print('\n')

  def print_users(self, users):
    print('\nUsers match criteria:\n')
    for i in users:
      print(i)
    print(' ')

  def print_requirements(self):
    print('\nIn order to take or return a book, you have to tell me your username and a book title:\n')

  def print_found(self, entity):
    print('\n{} found!'.format(entity))

  def print_not_found(self, entity):
    print('\nNo {}, sorry!\n'.format(entity))
    main_control.handler(main_control.wait())

  def print_book_taken(self, user, book):
    print('\n{} was successfully taken by {}\n'.format(book, user))

  def print_book_returned(self, user, book):
    print('\n{} was successfully returned by {}\n'.format(book, user))

  def print_book_limit(self):
    print('User has reached book limit, sorry!\n')
    main_control.handler(main_control.wait())

  def print_credits(self):
    print("\n")
    print("+----------------------------------------------------------------------------+")
    print("|                                   Library v2                               |")
    print("+----------------------------------------------------------------------------+")
    print("|                              Developed by shashial.                        |")
    print("|                             Pattern:MVC using SOLID                        |")
    print("+----------------------------------------------------------------------------+")
    print("\n")

  def print_input_menu(self):
    print('\nPlease, choose input source:')
    print('0. Show instructions again')
    print('1. File_1')
    print('2. File_2')
    print('3. Buildin DB')


class Controller:
  """controller is used to pass all user input from view to model"""
  def wait(self):
    """wait for a numeric input from a user"""
    while True:
      try:
        action_num = int(raw_input('Choose your action(number only):'))
        break
      except ValueError:
        print("NUMBERS, do you speak it?")
      except EOFError:
        print("\n\nYou should exit properly next time, %username%\n")
        exit()
    return action_num

  def handler(self, action_num):
    """handles user input in the main menu"""
    if action_num == 0:
      main_view.print_cli()
    elif action_num == 1:
      main_view.print_books(main_model.get_books())
    elif action_num == 2:
      main_view.print_users(main_model.get_users())
    elif action_num == 3:
      main_view.print_requirements()
      uname = raw_input('Your username: ')
      book = raw_input('Book: ')
      main_model.take_book(uname, book)
    elif action_num == 4:
      main_view.print_requirements()
      uname = raw_input('Your username: ')
      book = raw_input('Book: ')
      main_model.give_book(uname, book)
    elif action_num == 5:
      main_model.give_expired_list()
    elif action_num == 6:
      main_view.print_credits()
    elif action_num == 7:
      exit()

    #and pass control to controller again, untill user press exit.
    main_control.handler(main_control.wait())

  def input_handler(self, input_num):
    """handles user input in the input menu"""
    if input_num == 0:
      main_view.print_input_menu()
    if input_num == 1:
      main_control.handler(0)
    elif input_num == 2:
      main_control.handler(0)
    elif input_num == 3:
      main_control.handler(0)
    main_control.input_handler(main_control.wait())


#initialize objects
main_view = View()
main_control = Controller()
main_model = Model()

#main: pass control to the controller
main_view.print_credits()
main_control.input_handler(0)