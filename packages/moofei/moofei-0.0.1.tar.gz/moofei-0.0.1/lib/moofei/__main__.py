import os, sys
print('moofei', sys.argv)
print(os.getcwd())
#Ҳ���Խ�pkg��Ϊһ��Packageִ�У�python -m pkg

if len(sys.argv)>2:
    if sys.argv[1]==":find":
        from ._find import main
        main(cmd=":find")
exit(0)
