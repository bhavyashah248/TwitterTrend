def get_jaccard(a,b):
    a=a.split()
    b=b.split()
    union = list(set(a+b))
    intersection = list(set(a) - (set(a)-set(b)))
#    print "Union - %s" % union
#    print "Intersection - %s" % intersection
    jaccard_coeff = float(len(intersection))/len(union)
#    print "Jaccard Coefficient is = %f " % jaccard_coeff
    return jaccard_coeff

if __name__ == '__main__':
    a = 'NEW Fujifilm 16MP 5x'
    b = 'NEW Fujifilm 16MP'
    a=a.lower()
    b=b.lower()
    jaccard(a,b)