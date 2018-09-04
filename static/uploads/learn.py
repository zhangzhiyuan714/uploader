
#-*-coding:utf-8-*-
from multiprocessing import Manager,Process,Pool,cpu_count
import time

CPU_COUNT = cpu_count()
def foo(d,i):
    time.sleep(1)
    print "-"
    d['a{}'.format(i)] = 1
    print i
if __name__ == '__main__':
    md = Manager().dict({'name':'zzy'})
    print CPU_COUNT
    pool_obj = Pool(CPU_COUNT)
    for i in xrange(50):
    	p = pool_obj.apply_async(func=foo,args=(md,i,))
    	
    
    pool_obj.close()
    pool_obj.join()

    time.sleep(1)
    print md