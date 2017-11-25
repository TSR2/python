def bubo(ta):
    for i in range(len(a)-1,0,-1):
        for j in range(i):
            if ta[j]>ta[j+1]:
                ta[j],ta[j+1]=ta[j+1],ta[j]
            print(ta)
a=[2,3,1,8,9,3,2,10,15]
bubo(a)
