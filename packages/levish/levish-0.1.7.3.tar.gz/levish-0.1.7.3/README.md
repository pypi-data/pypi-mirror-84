![header](media/header.png)

# levish: Create your own Shell

## Installation

Install levish using pip:

```txt
pip install levish
```

## Getting started

Using levish is very easy. We start by importing the 'Shell' class and creating a new Shell object.

```python
from levish import Shell

sh = Shell("MyShell")
```

After that we can create our first command. We do that by first creating a function that takes one parameter called 'args'. Then we can add the function to our Shell object using the add_command() method. This method takes 3 arguments: 'cmd', 'func' & 'description' (optional). The 'cmd' parameter takes a string that we later have to type, to execute our function. The 'func' takes the name of the function that we want to execute. And well, 'description' is the description.

```python
def cmd_hello(args):
    print("hello!)

sh.add_command("hello", hello, description="this command prints hello!")
```

Now we just need to run our shell. We do that by executing the run() function of our Shell object.

### Complete code

```python
from levish import Shell

sh = Shell("MyShell")

def cmd_hello(args):
    print("hello!")

sh.add_command("hello", hello, description="this command prints hello!")

sh.run()
```

### Output

```txt
[>] hello
hello!
```
