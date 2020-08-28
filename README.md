# new.py

Python program to write new Python programs

## Description

The "new.py" program is intended to automate the creation of a program that uses argparse to handle command-line arguments.
Run with `-h|--help` for the documentation:

```
usage: new.py [-h] [-n NAME] [-e EMAIL] [-p PURPOSE] [-t] [-f] program

Create Python argparse program

positional arguments:
  program               Program name

optional arguments:
  -h, --help            show this help message and exit
  -n NAME, --name NAME  Name for docstring (default: Ken Youens-Clark)
  -e EMAIL, --email EMAIL
                        Email for docstring (default: kyclark@gmail.com)
  -p PURPOSE, --purpose PURPOSE
                        Purpose for docstring (default: Rock the Casbah)
  -t, --write_test      Create basic test.py (default: False)
  -f, --force           Overwrite existing (default: False)
```

The only required argument is the "program" name:

```
$ new.py foo.py
Done, see new script "foo.py."
```

Now you will have a program that will accept the following parameters:

```
$ ./foo.py -h
usage: foo.py [-h] [-a str] [-i int] [-f FILE] [-o] str

Rock the Casbah

positional arguments:
  str                   A positional argument

optional arguments:
  -h, --help            show this help message and exit
  -a str, --arg str     A named string argument (default: )
  -i int, --int int     A named integer argument (default: 0)
  -f FILE, --file FILE  A readable file (default: None)
  -o, --on              A boolean flag (default: False)
```

Edit the "get_args()" function to whatever your program's requirements may be.

If you run this same command again, the "foo.py" file will be detected, and you will be prompted to see if you wish to overwrite it.
Unless you answer "yes," the program will exit:

```
$ new.py foo.py
"foo.py" exists.  Overwrite? [yN] n
Will not overwrite. Bye!
```

If you do wish to overwrite the program, you can use the `-f|--force` flag:

```
$ new.py foo.py -f
Done, see new script "foo.py."
```

You can indicate the name and email address you wish to appear in the program's docstrings, or you can write a "~/.new.py" configuration file with these parameters, e.g.:

```
$ cat ~/.new.py
name=Ken Youens-Clark
email=kyclark@gmail.com
```

The `-p|--purpose` option will also become part of the program docstring/argparse documentation.
You can also add a "purpose" option to your "~/.new.py" file to override the default "Rock the Casbah" value.

Use the `-t|--test` option to create a "{prg}_test.py" file and a "Makefile":

```
$ new.py -t foo.py
Done, see new script "foo.py."
```

Now you should have the following files:

```
$ ls
Makefile	foo.py*		foo_test.py
```

You can run "make test" to execute "python3 -m pytest -xv":

```
$ make test
python3 -m pytest -xv
...
```

## See Also

I first created a version of this program for [Tiny Python Projects](http://tinypythonprojects.com/):

https://github.com/kyclark/tiny_python_projects/blob/master/bin/new.py

This version is different in that it incorporates type hints and uses structures like named tuples as records/structs to represent complex, typed objects such as the program "Args".

[Chapter 1](http://tinypythonprojects.com/#/chapters/1) of the book covers how to use "new.py" to start a new program.
The [TPP appendix](http://tinypythonprojects.com/#/chapters/23) covers argparse in greater detail.

## Author

Ken Youens-Clark <kyclark@gmail.com>
