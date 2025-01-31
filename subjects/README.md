## Instructions to use the testing script 

The code of each benchmark calls the function on the last line and asks the input parameters from stdin (i.e., sys.argv), as in the following snippet: 
```
if __name__ == '__main__':
  main( int(sys.argv[1]) if len(sys.argv) > 1 else 10 ) 
```

To correctly execute the test.py script, the user needs the above-mentioned code section with the function call followed by its parameters. Therefore, the snippet becomes:
`main(param)`

Once replace, you can execute the test script, specifying the name of the compiler. For example:
`python test.py numba`
