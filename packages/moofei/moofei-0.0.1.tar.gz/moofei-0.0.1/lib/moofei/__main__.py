import os, sys
print('moofei', sys.argv)
print(os.getcwd())
#也可以将pkg作为一个Package执行：python -m pkg

if len(sys.argv)>2:
    if sys.argv[1]==":find":
        from ._find import main
        main(cmd=":find")
exit(0)
