---
title: Exceptions
tags: 
  - name: Exceptions - Python Docs
    link: https://docs.python.org/3/tutorial/errors.html
  - name: Python Exceptions @RealPython
    link: https://realpython.com/python-exceptions/
  - name: Exception hierarchy
    link: https://docs.python.org/3/library/exceptions.html#exception-hierarchy
  - name: Classes
    link: /python/exceptions
  - name: EAFP
    link: https://realpython.com/python-lbyl-vs-eafp
  - name: Assertions
    link: /python/assertion
---
## Exceptions

### Page Contents

- [Overview](#overview)
- [The Exception Handling Process](#the-exception-handling-process)
- [An Unhandled Exception](#an-unhandled-exception)
- [Why and How to Handle](#why-and-how-to-handle)
- [Example: Input Validation](#example-input-validation)
- [The Exception Hierarchy](#the-exception-hierarchy)
- [What Exceptions to Catch?](#what-exceptions-to-catch)
- [Some Common Exception Types](#some-common-exception-types)
- [Example: Catching Different Exception Types](#example-catching-different-exception-types)
- [Raising Exceptions Programmatically](#raising-exceptions-programmatically)
- [Defining Your Own Exceptions](#defining-your-own-exceptions)
- [Tracebacks](#tracebacks)
- [Pattern: Exception to Break or Continue an Outer Loop](#pattern-exception-to-break-or-continue-an-outer-loop)
- [Write Exceptions as JSON](#write-exceptions-as-json)
- [EAFP](#eafp)

### Overview

Exceptions are used to handle situations that are not the _normal_ flow of our code. Exceptions are errors which are detected and  _thrown_ at runtime.  This is different to syntactic errors; i.e. where the code itself is structurally or syntactically not valid.

When an exception is _thrown_, there are basically two things we can do.

1. We can write code to _catch_ and handle the exception. This might mean gracefully dealing with a situation, allowing the program to then continue.
1. We can not bother writing any such code; the exception will cause our program to terminate with an error.

### The Exception Handling Process

1. **An exception is _raised_ by a line of code.**
  - E.g. when we do something bad, like... \
    -> Trying to divide by 0. \
    -> Capturing user input, not validating its type, and then always assuming the user has entered, say, an integer value. \
    -> Trying to write to a read-only file. \
    -> Trying to obtain a dictionary value with a non-existent key.
  - We can also programmatically raise our own exceptions.  We'll get to that later.

1. **Optionally handle the exception.**
  - I.e. do something to gracefully deal with the exception, allowing the program to continue.
  - Or, leave the exception unhandled, resulting in the program terminating.

### An Unhandled Exception

What happens if an exception is thrown and you don't handle it?  Here's an example...

```python
numerator = 10
denominator = 0

print(numerator / denominator)
print("You won't see this.")
```

Here's the output of trying to divide by 0:

```text
Traceback (most recent call last):
  File "c:\Users\djl\localdev\Python\Advent-of-Code\src\snippets\snippet.py", line 4, in <module>
    print(numerator / denominator)
ZeroDivisionError: division by zero
```

We can see that the program has terminated prematurely on the line where we try to divide a number by 0. The program never executes the last line. 

A `ZeroDivisionError` was thrown.  And we see the `Traceback` - the context in which in the exception was generated.

Here's another example:

```python
bad_number = "Darren"
good_number = 10

print(bad_number + good_number)
print("You won't see this.")
```

And here's the output of trying to handle a string as if it were a number:

```text
Traceback (most recent call last):
  File "c:\Users\djl\localdev\Python\Advent-of-Code\src\snippets\snippet.py", line 4, in <module>     
    print(bad_number + good_number)
TypeError: can only concatenate str (not "int") to str
```

Again, we can see that the program has terminated due to this exception being thrown.  This time we get an exception of type `TypeError`.  And once again, we see the `Traceback`.

### Why and How to Handle

There's a few reasons why we might want to _handle_ an exception:

1. To prevent the program terminating with nothing more than a `stacktrace`.
1. To handle a situation, but then allow the program to continue.
1. To provide the user with information that is useful and appropriate.
1. To hide stacktrace information that may be unhelpful, confusing, or reveal implementation details that may pose a security concern.

To explicitly handle exceptions, We use the **try-except block**, which is a construct that appears in many programming languages. (E.g. in Java, it's called _try-catch_).

The general structure is:

```python
try:
  # normal execution flow
except some_exception as some_err:
  # code to execute only if "some_exception" is caught.
  # this might include some helpful messaging to the user
except some_other_exception as some_err:
  # code to execute only if "some_other_exception" is caught
  # this might include some helpful messaging to the user
finally:
  # an optional block that we execute whether an exception is caught or not
```

So, we:
- Wrap the code that _could_ throw an exception in the `try:` block.
- Create an `except` block for each exception type that we may want to explicitly handle. The code will fall through to each successive `except` clause, until a matching exception is found.  
- We can optionally name our caught exception with the `as some_name` construct.  This allows us to interrogate the exception in more detail, within the `except` block.
- An optional `finally` block is for any code that we may want to exception after any exception handling has taken place, or even if there was no exception.

### Example: Input Validation

```python
print("Welcome to the number sorter!")
ready_to_quit = False
numbers_list = []

while not ready_to_quit:
    print("Enter some numbers, one entry at a time. Press Q to sort and Quit.")
    userEntered = input("> ").upper()
    if (userEntered == "Q"):
        break
    else:
        try:
            num_entered = int(userEntered)
        except ValueError:
            # Instead of the program terminating with a ValueError,
            # we allow the program to continue looping and provide the user with a helpful message
            print("Not a number! Try again.")
        else:
            print("You entered", userEntered)
            numbers_list.append(num_entered)
        finally:
            print("Done with this try-catch iteration.", userEntered)
              
print("Size of list: {0}".format(len(numbers_list)))
numbers_list.sort()
print(",".join(str(num) for num in numbers_list))
```

This code:

- Uses an infinite loop to capture input.  We break out of the loop if the user enters `q`.
- Whenever the user enters a value (other than `q`), the code attempts to convert the input to an integer number.  It does this in `try-except` block. If the value entered can be parsed as an integer, the code continues happily to the next iteration.
- If the user enters invalid data (i.e. not a number), then Python _throws_ a `ValueError`, which we handle in the code by displaying an appropriate message.

Let's try it out with valid input:

```text
Welcome to the number sorter!
Enter some numbers, one entry at a time. Press Q to sort and Quit.
> 15
You entered 15
Done with this try-catch iteration. 15
Enter some numbers, one entry at a time. Press Q to sort and Quit.
> 5
You entered 5
Done with this try-catch iteration. 5
Enter some numbers, one entry at a time. Press Q to sort and Quit.
> 4
You entered 4
Done with this try-catch iteration. 4
Enter some numbers, one entry at a time. Press Q to sort and Quit.
> 9
You entered 9
Done with this try-catch iteration. 9
Enter some numbers, one entry at a time. Press Q to sort and Quit.
> q
Size of list: 4
4,5,9,15
```

Now let's give it bad input, to test our `except` block:

```text
Welcome to the number sorter!
Enter some numbers, one entry at a time. Press Q to sort and Quit.
> 15
You entered 15
Done with this try-catch iteration. 15
Enter some numbers, one entry at a time. Press Q to sort and Quit.
> 5
You entered 5
Done with this try-catch iteration. 5
Enter some numbers, one entry at a time. Press Q to sort and Quit.
> 4
You entered 4
Done with this try-catch iteration. 4
Enter some numbers, one entry at a time. Press Q to sort and Quit.
> foo
Not a number! Try again.
Done with this try-catch iteration. FOO
Enter some numbers, one entry at a time. Press Q to sort and Quit.
> 10
You entered 10
Done with this try-catch iteration. 10
Enter some numbers, one entry at a time. Press Q to sort and Quit.
> q
Size of list: 4
4,5,10,15
```

### The Exception Hierarchy

Before we describe which exception types you should be handling in your code, let's first look at the [exception hierarchy](https://docs.python.org/3/library/exceptions.html#exception-hierarchy){:target="_blank"}. I.e. the class hierarchy for all built-in exception types defined in the standard Python library:

```text
BaseException
 +-- SystemExit
 +-- KeyboardInterrupt
 +-- GeneratorExit
 +-- Exception
      +-- StopIteration
      +-- StopAsyncIteration
      +-- ArithmeticError
      |    +-- FloatingPointError
      |    +-- OverflowError
      |    +-- ZeroDivisionError
      +-- AssertionError
      +-- AttributeError
      +-- BufferError
      +-- EOFError
      +-- ImportError
      |    +-- ModuleNotFoundError
      +-- LookupError
      |    +-- IndexError
      |    +-- KeyError
      +-- MemoryError
      +-- NameError
      |    +-- UnboundLocalError
      +-- OSError
      |    +-- BlockingIOError
      |    +-- ChildProcessError
      |    +-- ConnectionError
      |    |    +-- BrokenPipeError
      |    |    +-- ConnectionAbortedError
      |    |    +-- ConnectionRefusedError
      |    |    +-- ConnectionResetError
      |    +-- FileExistsError
      |    +-- FileNotFoundError
      |    +-- InterruptedError
      |    +-- IsADirectoryError
      |    +-- NotADirectoryError
      |    +-- PermissionError
      |    +-- ProcessLookupError
      |    +-- TimeoutError
      +-- ReferenceError
      +-- RuntimeError
      |    +-- NotImplementedError
      |    +-- RecursionError
      +-- SyntaxError
      |    +-- IndentationError
      |         +-- TabError
      +-- SystemError
      +-- TypeError
      +-- ValueError
      |    +-- UnicodeError
      |         +-- UnicodeDecodeError
      |         +-- UnicodeEncodeError
      |         +-- UnicodeTranslateError
      +-- Warning
           +-- DeprecationWarning
           +-- PendingDeprecationWarning
           +-- RuntimeWarning
           +-- SyntaxWarning
           +-- UserWarning
           +-- FutureWarning
           +-- ImportWarning
           +-- UnicodeWarning
           +-- BytesWarning
           +-- EncodingWarning
           +-- ResourceWarning
```

What does this mean?  Well, it means that exceptions are hierarchical, and that all these built-in exception types are ultimately descendents of the parent class, `BaseException`.  

For example:
- `ZeroDivisionError` inherits from `ArithmeticError`, which inherits from `Exception`, which inherits from `BaseException`.
- `KeyError` inherits from `LookupError`, which inherits from `Exception`, which inherits from `BaseException`.

In fact, you can take any class in Python, and view it's inheritance hierarchy with the `mro()` method.  For example:

```text
>>> KeyError.mro()
[<class 'KeyError'>, <class 'LookupError'>, <class 'Exception'>, <class 'BaseException'>, <class 'object'>]
>>> ValueError.mro()
[<class 'ValueError'>, <class 'Exception'>, <class 'BaseException'>, <class 'object'>]
```

### What Exceptions to Catch?

Here's the most important rule: **always specify an exception type!**  Never have an empty `except`. Why?  Because then your `except` block will catch **all** types of exceptions that can be thrown.  And you'll see from the hierarchy above that this includes the likes of `KeyboardInterrupt`, which are inherited from `BaseException`.

Take a look at this example:

```python
from random import randrange

def main():
    number = randrange(100)
    while True:     # loop until user guesses
        try:
            guess = int(input("Guess the number? Quit with Ctrl-C if you get bored: "))
        except Exception:     # Better than catching empty, since this would even catch KeyboardInterrupt!
            continue
        
        if guess == number:
            print("You win!")
            break   # exit the loop

if __name__ == "__main__":
    main()
```

This program picks a random number between 0 and 99, prompts the user for input, and only exits if the user guesses correctly.

But what if the user gets bored and wants to quit?  Here I aborted after four attempts:

```text
Guess the number? Quit with Ctrl-C if you get bored: 50
Guess the number? Quit with Ctrl-C if you get bored: 30
Guess the number? Quit with Ctrl-C if you get bored: 25
Guess the number? Quit with Ctrl-C if you get bored: 10
Guess the number? Quit with Ctrl-C if you get bored: Traceback (most recent call last):
  File "f:\Users\Darren\localdev\Python\Basic-Scripts\src\Exceptions\empty_except.py", line 16, in <module>
    main()
  File "f:\Users\Darren\localdev\Python\Basic-Scripts\src\Exceptions\empty_except.py", line 7, in main
    guess = int(input("Guess the number? Quit with Ctrl-C if you get bored: "))
KeyboardInterrupt
```

If we press Ctrl-C, this causes a `KeyboardInterrupt` to be raised.  Our code catches `Exception`, but **does not catch** `KeybaordInterrupt`.  Note from the exception hierarchy that `KeyboardInterrupt` does not descend from `Exception`. Instead, `KeyboardException` inherits directly from `BaseException`. And we're not catching `BaseException`.

But what happens if we just catch **everything**?  We can do this by having an _empty_ `except` block, like this:

```python
from random import randrange

def main():
    number = randrange(100)
    while True:     # loop until user guesses
        try:
            guess = int(input("Guess the number? Quit with Ctrl-C if you get bored: "))
        except:     # THIS IS BAD!!  It even catches KeyboardInterrupt
            continue
        
        if guess == number:
            print("You win!")
            break   # exit the loop

if __name__ == "__main__":
    main()
```

The above program cannot be terminated.  Pressing Ctrl-C does nothing, because the resulting `KeyboardException` is caught by our empty `except` block, and then the code simply continues with the infinite `while` loop.

My advice:

- Always catch _something_.  Don't leave the `except` empty.
- Catching `Exception` is better than nothing.  It doesn't catch `SystemExit`, `KeyboardInterrupt` or `GeneratorExit`.  It will catch all other built-in Python exceptions.
- Ideally, be a bit more specific. If you know what exceptions are likely, then try to handle them with a bit more specificity.  Some of the most common exception types you'll want to explicitly handle are:
  - `ValueError` - for handling inappropriate input
  - `IndexError` - for when the code attempts to reference an object using an index that is out of range
  - `KeyError` - when we try to reference a key that doesn't exist (e.g. in a dict lookup)
  - `StopIteration` - for when there are no more values to iterate over
- You can always follow your _specific_ exceptions with a more generic `catch Exception`.

### Some Common Exception Types

Here are some of the more common exception types, and what they mean:

|Exception|Description|
|---------|-----------|
|ValueError|Often thrown when the input value is of the wrong type or bad|
|IndexError|When we attempt an out-of-range lookup; e.g. using at index beyond the end of a list|
|KeyError|When a key lookup fails; e.g. attempting to retrieve a value from a dict using a key that doesn't exist|
|StopIteration|When we have no more values to iterate over|

### Example: Catching Different Exception Types

```python
from sys import stderr

person = {
    "Firstname": "Bob",
    "Role": "Trader",
    "ID": 123
}
try:
    last_name = person["Lastname"]  # lookup a key that doesn't exist
    print("Lastname: ", last_name)
except KeyError as error:
    print("No last name!")
    print(f"Error of type: {type(error).__name__} with message: {error}")
except Exception as error:
    print("Unknown error!")
    print(f"{error!r}", file=stderr)

```

And when we run it:

```text
No last name!
Error of type: KeyError with message: 'Lastname'
```

### Raising Exceptions Programmatically

It is possible to raise an exception ourselves, programmatically. Here's an example of when we might want to do this:

```python
""" Find the median of any iterable.
Program aborts with an IndexError if the supplied iterable is empty. """
def median(iterable):
    items = sorted(iterable)
    
    # Odd e.g. 1, 4, 5, 6, 9: median index = 4 // 2 = 2
    # Even e.g. 1, 4, 5, 6, 9, 10: median index = 5 // 2 = 2
    median_index = (len(items) - 1) // 2    # integer division
    if len(items) % 2 != 0:
        return items[median_index]
    
    return (items[median_index] + items[median_index+1]) / 2.0
 
def test(iterable):
    print(f"Using {iterable}...")
    print(median(iterable))

numbers = [1, 4, 5, 6, 9]
test(numbers)

numbers = []
test(numbers)
```

Here we've created a function that determines the median from any supplied iterable (e.g. list) of numbers. It calculates the median as follows:

- Sort the supplied values in numerical order.
- Determines the number of values in the list. Subtract one from this number, and then divide by 2, ignoring any remainder. Store this as our index.
  - E.g. if we have 6 numbers, then we divide 5 by 2, to get 2.
  - E.g. if we have 5 numbers, then we divide 4 by 2, to get 2.
- If the total number of values was odd, then we return the value at the index calculated. This is the median.
- If the total number of values was even, then we need to return the value in between the value at our index, and the subsequent value.

We test the function using two lists: the first has some numbers, but the second list is empty.  This is the result:

```text
Using [1, 4, 5, 6, 9]...
5
Using []...
Traceback (most recent call last):
  File "c:\Users\djl\localdev\Python\Advent-of-Code\src\snippets\snippet.py", line 23, in <module>   
    test(numbers)
  File "c:\Users\djl\localdev\Python\Advent-of-Code\src\snippets\snippet.py", line 17, in test       
    print(median(iterable))
  File "c:\Users\djl\localdev\Python\Advent-of-Code\src\snippets\snippet.py", line 13, in median     
    return (items[median_index] + items[median_index+1]) / 2.0
IndexError: list index out of range
```

We can see that when we supply the first list, our code has no trouble calculating the median.  But when we supply an empty list, an uncaught `IndexError` is thrown. This happens because when we try to reference `items[median_index]` in our `median()` function, the `items` list is empty, so the index tries to reference a value that doesn't exist.  Doh!  

Furthermore, this error isn't very useful to anyone else running our code. **It would be much more helpful if our code generated a more useful exception in this scenario.**

As an improvement, we can choose to **throw an exception programmatically**, if our function is given an empty list:

```python
""" Find the median of any iterable.
Explicitly handle empty iterable use case by raising a ValueError,
otherwise we'll see an IndexError raised by the implementation. """
def median(iterable):
    items = sorted(iterable)
    if len(items) == 0:
        raise ValueError("median() arg was empty sequence")
    
    # Odd e.g. 1, 4, 5, 6, 9: median index = 4 // 2 = 2
    # Even e.g. 1, 4, 5, 6, 9, 10: median index = 5 // 2 = 2
    median_index = (len(items) - 1) // 2    # integer division
    if len(items) % 2 != 0:
        return items[median_index]
    
    return (items[median_index] + items[median_index+1]) / 2.0
 
def test(iterable):
    print(f"Using {iterable}...")
    print(median(iterable))

numbers = [1, 4, 5, 6, 9]
test(numbers)

numbers = []
test(numbers)
```

The only difference was the addition of a test to see `if` the list was empty, and the explicit code to throw a more appropriate `ValueError`, if the list is indeed empty. A `ValueError` is a good choice for an exception we should throw, if the value received by a function is not appropriate.

Now when we run it:

```text
Using [1, 4, 5, 6, 9]...
5
Using []...
Traceback (most recent call last):
  File "c:\Users\djl\localdev\Python\Advent-of-Code\src\snippets\snippet.py", line 25, in <module>   
    test(numbers)
  File "c:\Users\djl\localdev\Python\Advent-of-Code\src\snippets\snippet.py", line 19, in test       
    print(median(iterable))
  File "c:\Users\djl\localdev\Python\Advent-of-Code\src\snippets\snippet.py", line 7, in median      
    raise ValueError("median() arg was empty sequence")
ValueError: median() arg was empty sequence
```

This is a bit better. When we pass an empty list, the code now shows a more appropriate `ValueError`, and also has a message payload in the `Exception`, which is printed when the exception is thrown.

Unfortunately, we still get a messy stacktrace.  So one more improvement we can make it is to actually _handle_ the `ValueError`, when it is thrown. I.e.

```python
""" Find the median of any iterable.
Explicitly handle empty iterable use case by raising a ValueError,
otherwise we'll see an IndexError raised by the implementation. """
def median(iterable):
    items = sorted(iterable)
    if len(items) == 0:
        raise ValueError("median() arg was empty sequence")
    
    # Odd e.g. 1, 4, 5, 6, 9: median index = 4 // 2 = 2
    # Even e.g. 1, 4, 5, 6, 9, 10: median index = 5 // 2 = 2
    median_index = (len(items) - 1) // 2    # integer division
    if len(items) % 2 != 0:
        return items[median_index]
    
    return (items[median_index] + items[median_index+1]) / 2.0
 
def test(iterable):
    try:
        print(f"Using {iterable}...")
        print(median(iterable))
    except ValueError as err:
        print(f"Error of type: {type(err).__name__} with message: {err}")

numbers = [1, 4, 5, 6, 9]
test(numbers)

numbers = []
test(numbers)
```

The only change here was that the lines in our `test()` function have now been wrapped with a `try-except` block.

When we run our code:

```text
Using [1, 4, 5, 6, 9]...
5
Using []...
Error of type: ValueError with message: median() arg was empty sequence
```

You can see that the output is much less messy.  
- The first list works fine, as expected.
- The second list results in a `ValueError`, which is caught.  The code then prints the error message in a friendly way.

### Defining Your Own Exceptions

In most cases, it is not necessary to implement your own exception types.  But there are times when it can be useful to create user-defined exceptions.  For example, when we want our own exception to hide obscure implementation details.

To make your own exception type, simply `extend Exception`.

Time for an example. Let's create a function that determines inclination based on two values: horizontal distance, and vertical distance.  I.e. the angle relative to the horizontal.

Remember _SOH CAH TOA_ from school?  Here, we're getting the angle using the tangent of opposite over adjacent.

<img src="{{'/assets/images/sohcahtoa.png' | relative_url }}" alt="SOHCAHTOA" width="740" />

```python
import math

def inclination(dx, dy):
    """ Get the angle of an incline, given horizontal distance dx 
    and vertical distance, dy. """
    
    return round(math.degrees(math.atan(dy/dx)), 1)

def test():
    print("Inclination:", inclination(3, 5))
    print("Inclination: ", inclination(0, 5))
 
if __name__ == "__main__":
    test()
```

This is what happens when we run it:

```text
Inclination: 59.0
Traceback (most recent call last):
  File "c:\Users\djl\localdev\Python\Advent-of-Code\src\snippets\snippet.py", line 14, in <module>    
    test()
  File "c:\Users\djl\localdev\Python\Advent-of-Code\src\snippets\snippet.py", line 11, in test        
    print("Inclination: ", inclination(0, 5))
  File "c:\Users\djl\localdev\Python\Advent-of-Code\src\snippets\snippet.py", line 7, in inclination  
    return round(math.degrees(math.atan(dy/dx)), 1)
ZeroDivisionError: division by zero
```

It's pretty obvious to us what has gone wrong here.  But it won't be obvious to someone using our function. We've got a messy stacktrace, and an zero division error.

The first improvement we can make is to create a user-defined exception:

```python
import math

class InclinationError(Exception):
    """ User-defined exception with no implementation """
    pass

def inclination(dx, dy):
    """ Get the angle of an incline, given horizontal distance dx 
    and vertical distance, dy. """

    try:
        return round(math.degrees(math.atan(dy/dx)), 1)
    except ZeroDivisionError as e:
        # if dx is 0, let's convert to our custom InclinationError
        raise InclinationError("Slope cannot be vertical") from e

def test():
    try:
        print("Inclination:", inclination(3, 5))
        print("Inclination: ", inclination(0, 5))
    except InclinationError as err:
        print(f"Error of type: {type(err).__name__} with message: {err}")
 
if __name__ == "__main__":
    test()
```

Let's run it again...

```text
Inclination: 59.0
Error of type: InclinationError with message: Slope cannot be vertical
```

So much nicer!  And we didn't even have to write any exception code!  All we had to do was `extend` the `Exception` base class!  This is a simple and easy way to provide more meaningful errors in your code.

But we can improve this a lot!  Firstly, it would be nice if our `InclinationError` knew about the parameters that had been used, so that we can report them in the error.  Secondly, it would be nice if the `InclinationError` formatted its own output, rather than having to use:

```python
    print(f"Error of type: {type(err).__name__} with message: {err}")
```

Well, this is all easy to do.  First:

- We'll include the parameters to the `inclination()` method in our `InclinationError` constructor. Note that the first argument supplied to the constructor should always be a descriptive message for the error, as described in [PEP352](https://peps.python.org/pep-0352/){:target="_blank"}.
- Secondly, we'll add a `__str__()` method to our `InclinationError`, in order to format the error message in a friendly way.

Here's the updated code:

```python
import math
 
class InclinationError(Exception):
    """ User-defined exception that is raised when we can't determine the inclination.
    Args:
        msg - the error message to be included
        other_args - any other args we want to pass to the exception
    """
       
    def __str__(self) -> str:
        """ A friendly error message that includes any args """   
        return f"InclinationError: {self.args[0]}. Args were: {self.args[1:]}"
 
def inclination(dx, dy):
    """ Get the angle of an incline, given horizontal distance dx 
    and vertical distance, dy. """

    try:
        return round(math.degrees(math.atan(dy/dx)), 1)
    except ZeroDivisionError as e:
        # if dx is 0, let's convert to our custom InclinationError
        raise InclinationError("Slope cannot be vertical", dx, dy) from e

def test():
    try:
        print("Inclination:", inclination(3, 5))
        print("Inclination: ", inclination(0, 5))
    except InclinationError as err:
        print(err)
 
if __name__ == "__main__":
    test()
```

Now when we run the code, the output looks like this:

```text
Inclination: 59.0
InclinationError: Slope cannot be vertical. Args were: (0, 5)
```

### Tracebacks

Tracebacks are always printed when an _unhandled exception_ is thrown, causing a program to terminate.

But we can also interrogate a traceback programmatically, i.e. when handling an exception.  This can be useful for diagnostics.  Since Python3, all exceptions include a `__traceback__` attribute, which includes a reference to the traceback object associated with that exception.  To interrogate the traceback object, we need to have imported the traceback module.
Useful functions from the traceback module include:

- `print_exc()` - prints the exception and stack trace
- `format_exc()` - returns the exception and stack trace as a str

As an example, let's use the `InclinationError` from the previous example.  Recall that when we ran this code, the output was:

```text
Inclination: 59.0
InclinationError: Slope cannot be vertical. Args were: (0, 5)
```

But what if want the full stacktrace of our handled exception?  Easy... We can just add two lines:

- The `import` statement
- The `traceback.format_exc()` call.

Here's the updated code:

```python
import math
import traceback
 
class InclinationError(Exception):
    """ User-defined exception that is raised when we can't determine the inclination.
    Args:
        msg - the error message to be included
        other_args - any other args we want to pass to the exception
    """
       
    def __str__(self) -> str:
        """ A friendly error message that includes any args """        
        return f"InclinationError: {self.args[0]}. Args were: {self.args[1:]}"
 
def inclination(dx, dy):
    """ Get the angle of an incline, given horizontal distance dx 
    and vertical distance, dy. """

    try:
        return round(math.degrees(math.atan(dy/dx)), 1)
    except ZeroDivisionError as e:
        # if dx is 0, let's convert to our custom InclinationError
        raise InclinationError("Slope cannot be vertical", dx, dy) from e

def test():
    try:
        print("Inclination:", inclination(3, 5))
        print("Inclination: ", inclination(0, 5))
    except InclinationError as err:
        print(err)
        print("Error details:", traceback.format_exc())  # Show the full stacktrace

if __name__ == "__main__":
    test()
```

And now the output looks like this:

```text
Inclination: 59.0
InclinationError: Slope cannot be vertical. Args were: (0, 5)
Error details: Traceback (most recent call last):
  File "f:\Users\Darren\localdev\Python\Advent-of-Code\src\snippets\scratch.py", line 22, in inclination
    return round(math.degrees(math.atan(dy/dx)), 1)
ZeroDivisionError: division by zero

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "f:\Users\Darren\localdev\Python\Advent-of-Code\src\snippets\scratch.py", line 30, in test
    print("Inclination: ", inclination(0, 5))
  File "f:\Users\Darren\localdev\Python\Advent-of-Code\src\snippets\scratch.py", line 25, in inclination
    raise InclinationError("Slope cannot be vertical", dx, dy) from e
InclinationError: InclinationError: Slope cannot be vertical. Args were: (0, 5)
```

The `traceback` shows us that the original exception was a `ZeroDivisionError`, which was caught and then resulted in an `InclinationError`. 

An interesting point to note is that the original exception was available as the _cause_ of the handled exception. This is possible because Python automatically links the _causing_ exception to the _caused_ exception, through a procss called _implicit chaining_.  You can always refer to the _cause_ Exception explicitly, by using the `__context__` attribute of the handled exception. So, for example, if we wanted to know the original exception, but we didn't want to print the full stack trace, we could change our final `try-except` block to look like this:

```python
def test():
    try:
        print("Inclination:", inclination(3, 5))
        print("Inclination: ", inclination(0, 5))
    except InclinationError as err:
        print(err)
        print("The cause was:", err.__context__) 
```

And now the output of running our program looks like this:

```text
Inclination: 59.0
InclinationError: Slope cannot be vertical. Args were: (0, 5)
The cause was: division by zero
```

### Pattern: Exception to Break or Continue an Outer Loop

Sometimes we want to exit an outer loop based on something happening in an inner loop. Many languages provide a syntax for doing this, but Python does not.

Fear not, for here I describe a way to break out of an outer loop using exceptions!

```python
good_things = []

for thing in things:
    try:
        for subthing in thing:
            if is_good(subthing):
                good_things.append(thing)
                raise StopIteration()
    except StopIteration:
        # Continue the outer loop
        continue
```

In our snippet, when a particular condition is met, we raise a `StopIteration()` exception to cause the outer loop to continue to `continue`. Alternatively, we could use this approach to `break` the outer loop.

### Write Exceptions as JSON

Here's some code that can be used to write an exception as JSON.

```python
import traceback
import json
import os
 
SCRIPT_DIR = os.path.dirname(__file__)  # path where this file lives
MY_APP = "dump_errs"

def report(ex):
    """ Convert the exception to a dict """
    data = {}
    data['message'] = f"{ex}"
    data['serviceContext'] = {'service': MY_APP}
    
    return data

def dump_report(errors_report):
    """ Export this dict as a json file """
    file_name = os.path.join(SCRIPT_DIR, "exceptionsTest.json")
    with open(file_name, "a") as f:
        json.dump(errors_report, f)
             
def simulate_error():
    errors_report = {}  # store all errors in a dict
    error_counter = 0   # increment each time we catch an exception
   
    try:
        undefined_method()
    except Exception as e:
        error_counter += 1
        print("Exception was: ", e)    # just get the exception heading
        print(traceback.format_exc())   # print traceback from here
        errors_report[error_counter] = report(traceback.format_exc())
 
    try:
        x = a/2
    except Exception as e:
        error_counter += 1
        print("Exception was: ", e)    # just get the exception heading
        print(traceback.format_exc())   # print traceback from here
        errors_report[error_counter] = report(traceback.format_exc())
 
    try:
        x = 2/0
    except Exception as e:
        error_counter += 1
        print("Exception was: ", e)    # just get the exception heading
        print(traceback.format_exc())   # print traceback from here
        errors_report[error_counter] = report(traceback.format_exc())
 
    try:
        import non_existent_library
    except Exception as e:
        error_counter += 1
        print("Exception was: ", e)    # just get the exception heading
        print(traceback.format_exc())   # print traceback from here
        errors_report[error_counter] = report(traceback.format_exc())
    
    dump_report(errors_report)
 
if __name__ == '__main__':
    simulate_error()
```

The code generates a bunch of exceptions, and catches them all. For each exception caught, we call the `report()` function against the exception's stacktrace, to store the error and its stacktrace as a dictionary.  Finally, we call `dump_report()` to dump our dictionary of dictionaries as a JSON file.

The output file looks like this:

```json
{
    "1": {
        "message": "Traceback (most recent call last):\n  File \"c:\\Users\\djl\\localdev\\Python\\Advent-of-Code\\src\\snippets\\snippet.py\", line 27, in simulate_error\n    undefined_method()\nNameError: name 'undefined_method' is not defined\n",
        "serviceContext": {
            "service": "dump_errs"
        }
    },
    "2": {
        "message": "Traceback (most recent call last):\n  File \"c:\\Users\\djl\\localdev\\Python\\Advent-of-Code\\src\\snippets\\snippet.py\", line 35, in simulate_error\n    x = a/2\nNameError: name 'a' is not defined\n",
        "serviceContext": {
            "service": "dump_errs"
        }
    },
    "3": {
        "message": "Traceback (most recent call last):\n  File \"c:\\Users\\djl\\localdev\\Python\\Advent-of-Code\\src\\snippets\\snippet.py\", line 43, in simulate_error\n    x = 2/0\nZeroDivisionError: division by zero\n",
        "serviceContext": {
            "service": "dump_errs"
        }
    },
    "4": {
        "message": "Traceback (most recent call last):\n  File \"c:\\Users\\djl\\localdev\\Python\\Advent-of-Code\\src\\snippets\\snippet.py\", line 51, in simulate_error\n    import non_existent_library\nModuleNotFoundError: No module named 'non_existent_library'\n",
        "serviceContext": {
            "service": "dump_errs"
        }
    }
}
```

### EAFP

**Easier to Ask Forgiveness Than Permission** is a Python philosophy. (It contrasts from the _Look Before You Leap_ strategy.) EAFP advocates not validating all possible conditions before executing code, but rather: catching exceptions when they occur. The rationale is that the developer does not expend significant effort in trying to prevent every error condition that may occur. But instead, simply handle errors when they do. Thus, this strategy favours happy path coding, but explicitly handles errors.

For example, when opening a file: rather than checking if the file exists and is of the right type, instead, simply catch an OSError if it occurs.
