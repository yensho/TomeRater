class User(object):
    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.books = {}

    def get_email(self):
        return self.email

    def change_email(self, address):
        self.email = address
        print("User {name} email address has been updated to: {email}".format(name=self.name, email=self.email))

    def __repr__(self):
        return "User {name}, email: {email}, books read: {books}".format(name=self.name, email=self.email, books=len(self.books.keys()))

    def __eq__(self, other_user):
        return self.name == other_user.name and self.email == other_user.email

    def read_book(self, book, rating=None):
        self.books[book] = rating

    def get_average_rating(self):
        return sum(self.books.values())/len(self.books.values())

class Book(object):
    def __init__(self, title, isbn):
        self.title = title
        self.isbn = isbn
        self.ratings = []

    def get_title(self):
        return self.title

    def get_isbn(self):
        return self.isbn

    def set_isbn(self, new):
        self.isbn = new
        print("ISBN for book {book} has been updated.".format(book=self.title))

    def add_rating(self, rating):
        if rating is not None and 0 <= rating <= 4:
            self.ratings.append(rating)
        else:
            print("Invalid Rating")

    def __eq__(self, other):
        return self.title == other.title and self.isbn == other.isbn

    def get_average_rating(self):
        return sum(self.ratings)/len(self.ratings)

    def __hash__(self):
        return hash((self.title, self.isbn))

class Fiction(Book):
    def __init__(self, title, author, isbn):
        super().__init__(title, isbn)
        self.author = author

    def get_author(self):
        return self.author

    def __repr__(self):
        return "{title} by {author}".format(title=self.title, author=self.author)

class Non_Fiction(Book):
    def __init__(self, title, subject, level, isbn):
        super().__init__(title, isbn)
        self.subject = subject
        self.level = level

    def get_subject(self):
        return self.subject

    def get_level(self):
        return self.level

    def __repr__(self):
        return "{title}, a {level} manual on {subject}".format(title=self.title, level=self.level, subject=self.subject)

class TomeRater(object):
    def __init__(self):
        self.users = {}
        self.books = {}

    def create_book(self, title, isbn):
        return Book(title, isbn)

    def create_novel(self, title, author, isbn):
        return Fiction(title, author, isbn)

    def create_non_fiction(self, title, subject, level, isbn):
        return Non_Fiction(title, subject, level, isbn)

    def add_book_to_user(self, book, email, rating=None):
        try:
            user = self.users[email]
        except KeyError:
            user = None
        #user = getattr(self.users, email, None)
        if user is None:
            print("No user with email {email}".format(email=email))
        else:
            user.read_book(book, rating)
            book.add_rating(rating)
            if hasattr(self.books, str((book.title, book.isbn))):
                self.books[book] += 1
            else:
                self.books[book] = 1

    def add_user(self, name, email, user_books=None):
        user = User(name, email)
        self.users[email] = user
        if user_books is not None:
            for book in user_books:
                self.add_book_to_user(book, user.email)

    def print_catalog(self):
        for book in self.books.keys():
            print(book)

    def print_users(self):
        for user in self.users.values():
            print(user)

    def most_read_book(self):
        return max(self.books.keys(), key=lambda x: self.users[x])

    def highest_rated_book(self):
        return max(self.books.keys(), key=lambda x: self.books[x].get_average_rating())

    def most_positive_user(self):
        return max(self.users.values(), key=lambda x: x.get_average_rating())
