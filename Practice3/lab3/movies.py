movies = [
    {"name": "Usual Suspects", "imdb": 7.0, "category": "Thriller"},
    {"name": "Hitman", "imdb": 6.3, "category": "Action"},
    {"name": "Dark Knight", "imdb": 9.0, "category": "Adventure"},
    {"name": "The Help", "imdb": 8.0, "category": "Drama"},
    {"name": "The Choice", "imdb": 6.2, "category": "Romance"},
    {"name": "Colonia", "imdb": 7.4, "category": "Romance"},
    {"name": "Love", "imdb": 6.0, "category": "Romance"},
    {"name": "Bride Wars", "imdb": 5.4, "category": "Romance"},
    {"name": "AlphaJet", "imdb": 3.2, "category": "War"},
    {"name": "Ringing Crime", "imdb": 4.0, "category": "Crime"},
    {"name": "Joking muck", "imdb": 7.2, "category": "Comedy"},
    {"name": "What is the name", "imdb": 9.2, "category": "Suspense"},
    {"name": "Detective", "imdb": 7.0, "category": "Suspense"},
    {"name": "Exam", "imdb": 4.2, "category": "Thriller"},
    {"name": "We Two", "imdb": 7.2, "category": "Romance"},
]


# Task 1
def is_high_rated(movie):
    return movie["imdb"] > 5.5


# Task 2
def high_rated_movies(movie_list):
    return [movie for movie in movie_list if is_high_rated(movie)]


# Task 3
def movies_by_category(movie_list, category):
    return [movie for movie in movie_list
            if movie["category"].lower() == category.lower()]


# Task 4
def average_imdb(movie_list):
    if not movie_list:
        return 0
    return sum(movie["imdb"] for movie in movie_list) / len(movie_list)


# Task 5
def category_average(movie_list, category):
    selected_movies = movies_by_category(movie_list, category)
    return average_imdb(selected_movies)


if __name__ == "__main__":
    print(is_high_rated(movies[0]))
    print(high_rated_movies(movies))
    print(movies_by_category(movies, "Romance"))
    print("All-movie average:", average_imdb(movies))
    print("Romance average:", category_average(movies, "Romance"))

words = ["cat", "apple", "book", "python", "sun"]


def long_words(words):
    result = [word for word in words if len(word) > 4]
    return result

print(long_words(words))

class Book:
    def __init__ (self, title, author, pages):
        self.title = title
        self.author = author
        self.pages = pages

    def show_info(self):
        print(self.title, self.author, self.pages)

    def is_long(self):
        if self.pages > 300:
            return True
        else:
            return False
    

p1 = Book("Beethoven", "B", "400")
p2 = Book("C++", "Alima", "200")

p1.show_info()
print(p1.is_long())