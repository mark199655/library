#!/usr/bin/env python

# Script Name   : library_mvc_v1.py
# Author        : shashial
# Description   : Book management system using MVC + SOLID

import datetime
import pickle
import json

#hardcoded initial 'database' 
#list of books at the library
db_books = ['book14', 'book88', 'book3', 'book4', 'book5', 'book6', 'book7', 'book8', 'book9', 'book10', 'book1']
#list of users and corresponding books
db_users = {
'user1':{'book12':'2016-11-15', 'book13':'2016-10-14'},
'user2':{},
'user3':{'book14':'2016-11-15'},
'user4':{'book15':'2016-11-15', 'book16':'2016-10-14', 'book17':'2016-10-14'}
}

class ModelInput(object):
  """parent class for all input, defines source and destination"""
  def __init__(self, users, books):
    self.users = users
    self.books = books

class ModelInputPickle(ModelInput):
  def input(self, f_uname, f_bname):
    ''' use pickle file as input '''
    while True:
      try:
        users_file = open(f_uname, 'rb')
        books_file = open(f_bname, 'rb')
        break
      except IOError:
        print('No such file, please, try again')
        main_control.input_handler(main_control.wait())

    users = pickle.load(users_file)
    books = pickle.load(books_file)

    users_file.close()
    books_file.close()

    return (users, books)

class ModelInputJson(ModelInput): 
  def input(self, f_uname, f_bname):
    """ use json file as input """
    while True:
      try:
        users_file = open(f_uname)
        books_file = open(f_bname)
        break
      except IOError:
        print('No such file, please, try again')
        main_control.input_handler(main_control.wait())

    users = json.load(users_file)
    books = json.load(books_file)

    users_file.close()
    books_file.close() 

    return (users, books)

class ModelInputDB(ModelInput):
  """ use database as input """
  def input(self, db_users, db_books):
    return (db_users, db_books)

class ModelInputSourse(object):
  """ interraction with data """
  def input(self, num):
    """ input interface """
    if num == 1:
      model_pickle_input = ModelInputPickle('users_1.txt', 'books_1.txt')
      self.users, self.books = (model_pickle_input.input(model_pickle_input.users, model_pickle_input.books))
    if num == 2:
      model_json_input = ModelInputJson('users_2.txt', 'books_2.txt')
      self.users, self.books = (model_json_input.input(model_json_input.users, model_json_input.books))
    if num == 3:
      model_input_db = ModelInputDB(db_users, db_books)
      self.users, self.books = (model_input_db.input(model_input_db.users, model_input_db.books))

  def ret(self):
    """returns loaded data"""
    return(self.users, self.books)

class Model:
  """
  model is called by controller and calls view
  model looks after overall logic, every action is done with model involved
  """
  def __init__(self):
    self.book_limit = 3

  def get_books(self):
    """get list of books"""
    return [book for book in main_input.ret()[1]]

  def get_users(self):
    """get list of users"""
    return [user for user in main_input.ret()[0]]


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
    for i,k in main_input.ret()[0][uname].iteritems():
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
    if (len(main_input.ret()[0][uname])) >= main_model.book_limit:
      main_view.print_book_limit()

    #check if book in library
    main_model.book_in_library(book)

    #give a book to a user, add date
    main_input.ret()[1].remove(book)
    main_input.ret()[0][uname][book] = str(datetime.datetime.now().date())

    #print success message
    main_view.print_book_taken(uname, book)

  def give_book(self, uname, book):
    """give a book to a user"""
    #check if the user exists
    main_model.user_exists(uname)

    #check if the user has the book
    main_model.book_in_user(uname, book)

    #take a book from user, add it to the library
    main_input.ret()[0][uname].pop(book)
    main_input.ret()[1].append(book)

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
    for i, k in main_input.ret()[0].iteritems():
      for j, b in k.iteritems():
        book_time = datetime.datetime.strptime(b, "%Y-%m-%d").date()
        #if the book is expired(differens is more than 31 days) then add user to naughty list
        if (abs(now-book_time).days) > 31:
          ex_users.append(i)
    #user must be unique
    ex_users = set(ex_users)
    #print list of user with at least 1 expired book
    main_view.print_users(ex_users)



class View:
  """iew is used to create all the output of a programm"""
  def __init__(self):
    self.cli_menu = ("Menu", "Books available", "Users available", "Take a book", "Return a book", "List users with expired books", "Choose Database", "About", "Exit")
    self.input_menu = ("Show instructions", "File_1(pickle)", "File_2(json)", "Buildin 'database'(list)", "Exit")
  
  def print_cli(self, menu):
    counter = 0;
    print("\n")
    for i in range(0, len(menu)):
      print(str(counter)+'. '+menu[i])
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

  def print_about(self):
    """prints 'about' """
    print("\n")
    print("+----------------------------------------------------------------------------+")
    print("|                                   Library v2                               |")
    print("+----------------------------------------------------------------------------+")
    print("|                              Developed by shashial.                        |")
    print("|                             Pattern:MVC using SOLID                        |")
    print("+----------------------------------------------------------------------------+")
    print("\n")


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
      except KeyboardInterrupt:
        print("\n\nYou should exit properly next time, %username%\n")
        exit()        
    return action_num

  def handler(self, action_num):
    """handles user input in the main menu"""
    if action_num == 0:
      main_view.print_cli(main_view.cli_menu)
    elif action_num == 1:
      main_view.print_books(main_model.get_books())
    elif action_num == 2:
      main_view.print_users(main_model.get_users())
    elif action_num == 3:
      main_view.print_requirements()
      uname = raw_input('Your username: ')
      book = raw_input('Book title: ')
      main_model.take_book(uname, book)
    elif action_num == 4:
      main_view.print_requirements()
      uname = raw_input('Your username: ')
      book = raw_input('Book title: ')
      main_model.give_book(uname, book)
    elif action_num == 5:
      main_model.give_expired_list()
    elif action_num == 6:
      main_control.input_handler(0)
    elif action_num == 7:
      main_view.print_about()
    elif action_num == 8:
      exit()
    #and pass control to controller again, untill user press exit.
    main_control.handler(main_control.wait())

  def input_handler(self, input_num):
    """handles user input in the input menu"""
    if input_num == 0:
      main_view.print_cli(main_view.input_menu)
    if input_num == 1:
      main_input.input(1)
      main_control.handler(0)
    elif input_num == 2:
      main_input.input(2)
      main_control.handler(0)
    elif input_num == 3:
      main_input.input(3)
      main_control.handler(0)
    elif input_num == 4:
      exit()
    main_control.input_handler(main_control.wait())


#initialize objects
main_view = View()
main_control = Controller()
main_model = Model()
main_input = ModelInputSourse()

#main: pass control to the controller
main_view.print_about()
main_control.input_handler(0)