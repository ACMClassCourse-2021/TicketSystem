import os
import json
import subprocess
from filecmp import cmp as fcmp

data_dir='data'
compile_script='build.sh'
run_script='run.sh'
clean_script='clean.sh'

def printRet(detail=True):
    def decorator(func):
        def wrapper(*args, **kw):
            if detail:
                print("\033[36m{}\033[0m".format('call: {}'.format(func.__name__)))
            ret,val=func(*args, **kw)
            if val!='':
                if ret==0:
                    print("\033[37m{}\033[0m".format(val))
                else:
                    print("\033[31m{}\033[0m".format('ret code: '+str(ret)))
                    print("\033[37m{}\033[0m".format(val))
                    quit()
        return wrapper
    return decorator

@printRet(True)
def compile_project():
    return subprocess.getstatusoutput('sh {}'.format(compile_script))

@printRet(False)
def run(input_path):
    return subprocess.getstatusoutput('sh {} <{} > tmp.out'.format(run_script,input_path))

@printRet(False)
def clean():
    subprocess.getstatusoutput('rm tmp.out')
    return subprocess.getstatusoutput('sh {}'.format(clean_script))

def main():
    if not os.path.exists(data_dir):
        print("\033[31m{}\033[0m".format('data set not find!'))
        exit(127)
    with open('{}/config.json'.format(data_dir),'r')as f:
        testInfo=json.load(f)
    compile_project()
    errorCase=[]
    for info in testInfo:
        fail_point=None
        print('test for {}'.format(info['name']))
        for point in info['point']:
            file_path='{}/{}/{}'.format(data_dir,info['name'],point)
            if os.path.exists(file_path+'.in') and os.path.exists(file_path+'.out'):
                run(file_path+'.in')
                try:
                    result=fcmp(file_path+'.out','tmp.out')
                except:
                    result=False
                if not result:
                    errorCase.append((info['name']))
                    fail_point=point
                    break
            else:
                print("\033[31m{}\033[0m".format('data set is broken at {}!'.format(file_path)))
                exit(127)
        clean()
        if fail_point==None:
            print("\033[36m{}\033[0m".format('success in {}'.format(info['name'])))
        else:
            print("\033[31m{}\033[0m".format('case {} fail at {}'.format(info['name'],fail_point)))
    print("\033[36m{}\033[0m".format('pass case {}/{}'.format(len(errorCase),len(testInfo))))

if __name__=='__main__':
    main()

