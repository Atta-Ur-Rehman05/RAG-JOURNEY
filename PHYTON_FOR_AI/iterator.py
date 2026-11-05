

# this file contains the stuffs related to iterator

# what is iterator?
# An iterator is an object that allows you to traverse through all the elements of a collection,
#  such as a list or a tuple, one at a time. In Python, an iterator is any object 
# that implements the `__iter__()` and `__next__()` methods. The `__iter__()` method returns the iterator object itself, and the `__next__()` method 
# returns the next value from the collection. When there are no more items to return, `__next__()` raises a `StopIteration` exception.


students = ["Alice", "Bob", "Charlie"]

iterator = iter(students)

print(next(iterator))  # Output: Alice
print(next(iterator))  # Output: Bob
print(next(iterator))  # Output: Charlie

# print them using a for loop

for student in students:
    print(student)  # Output: Alice, Bob, Charlie

    # for loop vs iterator
    
    """"
    the difference between a for loop and an iterator is that a for loop is a high-level construct that abstracts away the details of iteration,
    while an iterator is a low-level object that provides a way to traverse through a collection of items.
      A for loop automatically creates an iterator for the collection and handles the StopIteration exception when the end of the collection is reached, 
    while an iterator requires you to manually call the next() function to retrieve each item and handle the StopIteration exception yourself.

    what problems does each solve? is

 loop is useful when you want to iterate over a collection of items in a simple and concise way, without having to worry about the details of iteration.
while an iterator is useful when you want more control over the iteration process, such as when you need to pause and resume iteration, or when you want to create your own custom iteration behavior.

where does each fit in the bigger picture of programming? a for loop is a common construct in many programming languages, and is often used to iterate over collections of data.
while an iterator is a more advanced concept that is often used in functional programming and other programming paradigms that require more control over the iteration process.
    """



# creating a custom iterator

class MyIterator:
    def __init__(self, data):
        self.data = data
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.index < len(self.data):
            result = self.data[self.index]
            self.index += 1
            return result
        else:
            raise StopIteration


    # using the custom iterator

    my_iterator = MyIterator(["Alice", "Bob", "Charlie"])

    for student in my_iterator:
        print(student)  # Output: Alice, Bob, Charlie




class oddnumberiterator:
    def __init__(self, max):
        self.max = max
        self.num = 1

    def __iter__(self):
        return self

    def __next__(self):
        if self.num > self.max:
            raise StopIteration
        else:
            result = self.num
            self.num += 2
            return result


    odd = oddnumberiterator(10)

    for num in odd:
        print(num)  # Output: 1, 3, 5, 7, 9