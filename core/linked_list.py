
from functools import reduce


# https://stackoverflow.com/questions/280243/python-linked-list#280284
cons   = lambda el, lst: (el, lst)
mklist = lambda *args: reduce(lambda lst, el: cons(el, lst), reversed(args), None)
car = lambda lst: lst[0] if lst else lst
cdr = lambda lst: lst[1] if lst else lst
nth = lambda n, lst: nth(n-1, cdr(lst)) if n > 0 else car(lst)
length  = lambda lst, count=0: length(cdr(lst), count+1) if lst else count
begin   = lambda *args: args[-1]
display = lambda lst: begin(print("%s " % car(lst)), display(cdr(lst))) if lst else print("()")
