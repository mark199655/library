# -*- coding: utf-8 -*-

"""
Author: shashial
Language: Python 2.7
Task: MVC book management system

Library book control system. Library has books and users.
Library rools:
1)There is only one entity of book in the system.
2)User is limited to three boks at the current perion of time.
3)User can hold a book for no longer than a month.

I have to develop a system, which has these functions:
1. Print list of books in the library.
2. Print list of users.
3. Give a book to a user.
4. Take a book from user.
5. Print list of user with expired books.

System has to be implemented in the MVC way.
"""

#to track book give out time
import datetime

'''
hardcoded initial 'database' 
'''
#list of books
bookz = ['book1', 'book2', 'book3', 'book4', 'book5', 'book6', 'book7', 'book8', 'book9', 'book10', 'book11']
#list of users
userz = ['user1', 'user2', 'user3', 'user4']
#dictionaries with corresponded users, dates and books
user1 = {'book12':'2016-11-15', 'book13':'2016-10-14'}
user2 = {}
user3 = {'book14':'2016-11-15'}
user4 = {'book15':'2016-11-15', 'book16':'2016-10-14', 'book17':'2016-10-14'}

class Model():
  """
  model is called by controller and calls view
  model looks after overall logic, every action is done with model involved
  """
  def get_books(self):
    """
    get books list
    """
    books = []
    for book in bookz:
      books.append(book)
    return books

  def get_users(self):
    """
    get user list
    """
    users = []
    for user in userz:
      users.append(user)
    return users

  def take_book(self, uname, book):
    """
    take a book from library: 
    1.Check if user exists
    2.Check users ammount of books taken
    3.Check if book in library
    4.Give a book:remove from library, add it to user
    """

    #check if user exists
    users = main_model.get_users()
    if uname in users:
      main_view.print_found(uname)
    else:
      main_view.print_not_found(uname)

    #check users ammout of books taken
    if (len(eval(uname))) >=3:
      main_view.print_book_limit()

    #check if a book in library
    books = main_model.get_books()
    if book in books:
      main_view.print_found(book)
    else:
      main_view.print_not_found(book)

    #give a book to a user, add date
    bookz.remove(book)
    eval(uname)[book] = str(datetime.datetime.now().date())

    #print success message
    main_view.print_book_taken(uname, book)

  def give_book(self, uname, book):
    """
    give a book to a user
    1)check if the user exists
    2)check if the user has the book
    3)take a book from user, add it to the library
    """
    #check if user exists
    users = main_model.get_users()
    if uname in users:
      main_view.print_found(uname)
    else:
      main_view.print_not_found(uname)

    #check if the user has the book
    user_books = []
    for i,k in eval(uname).iteritems():
      user_books.append(i)
    if book in user_books:
      main_view.print_found(book)
    else:
      main_view.print_not_found(book)

    #take a book from user, add it to the library
    eval(uname).pop(book)
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
    for user in userz:
      for i,k in eval(user).iteritems():
        book_time = datetime.datetime.strptime(k, "%Y-%m-%d").date()
        #if the book is expired(differens is more than 31 days) then add user to naughty list
        if (abs(now-book_time).days) > 31:
          ex_users.append(user)
    #user must be unique
    ex_users = set(ex_users)
    #print list of user with at least 1 expired book
    main_view.print_users(ex_users)

class View():
  """
  View is used to create all the output of a programm
  """
  def print_CLI(self):
    print('you wanna play my lil library game, %username%?\n0. Menu\n1. Books available\n2. Users available\n3. Take a book \n4. Return a book \n5. List users with expired books\n6. Exit\n')

  def print_books(self, books):
    print('\nBooks available:\n')
    for i in books:
      print(i)
    print('\n')

  def print_users(self, users):
    print('\nUsers available:\n')
    for i in users:
      print(i)
    print(' ')

  def print_requirements(self):
    print('\nIn order to take or return a book, you have to tell me your username and a book title:\n')

  def print_found(self, entity):
    print('\n{} found!').format(entity)

  def print_not_found(self, entity):
    print('\nNo {}, sorry!\n').format(entity)
    main_control.handler(main_control.wait())

  def print_book_taken(self, user, book):
    print('\n{} was successfully taken by {}\n').format(book, user)

  def print_book_returned(self, user, book):
    print('\n{} was successfully returned by {}\n').format(book, user)

  def print_book_limit(self):
    print('User has reached book limit, sorry!\n')
    main_control.handler(main_control.wait())

class Controller():
  """
  controller is used to pass all user input from view to model
  """
  def wait(self):
    """
    wait for a numeric input from a user
    """
    while True:
      try:
        action_num = int(raw_input('Choose your action(number only):'))
        break
      except ValueError:
        print("NUMBERS, do you speak it?")
    return action_num

  def handler(self, action_num):
    """
    this method handles user input: it desides which actions to do in case of different situations
    """
    if action_num == 0:
      main_view.print_CLI()
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
      exit()

    #and pass control to controller again, untill user press exit.
    main_control.handler(main_control.wait())



#initialize objects
main_view = View()
main_control = Controller()
main_model = Model()

#main: pass control to the controller
main_control.handler(0)

'''
user_books = []
for i,k in eval(uname).iteritems():
user_books.append(i)
'''