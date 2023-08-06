import numpy as np
def z(l,k,sort=True,reverse=True):
    '''
    Implementation of arXiv:1905.13729
    For l,k two set of same dimensions (or k with an extra dimension)
    return a builded array z, such that
     sum( z )=0
     sum( z**3)=0
    '''
    l=list(l)
    k=list(k)
    #Build vector-like solutions x,y
    if len(l)==len(k) :
        x=np.array( [l[0]]+k+[-l[0]]+[-i for i in k ])
        y=np.array( [0,0] +l        +[-i for i in l ])
    else:
        x=np.array( [0]+k+[-i for i in k ] )
        y=np.array( l+[k[0]]+[0]+[-i for i in l ]+[-k[0]])
    xfac=0
    yfac=0
    # Build not trivial solution
    zz=(x*y**2).sum()*x-(x**2*y).sum()*y
    if sort:
        zz=sorted( zz ,key=abs, reverse=reverse ) 
    return np.array(zz)

free=z
