l=[]
r=[1,11]
l.append(lambda n: n in range(*r))
r=[15, 111]
print(l[0](1))  # False because range hadn't been called until this line


l=[]
r=[1,11]
rr=range(*r)
l.append(lambda n: n in rr)
r=[15, 111]
rr=range(*r)
print(l[0](1))  # Still False because the data where rr points to got updated

l=[]
r=(1,11)
rr=range(*r)
l.append(lambda n: n in rr)
r=(15, 111)
rr=range(*r)
print(l[0](1))  # Still False because the data where rr points to got updated
