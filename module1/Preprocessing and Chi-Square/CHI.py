def ChiSquareTest(arg1, arg2, arg3):
    FeatureSet = arg1
    countList1 = arg2
    countList2 = arg3
    a = 0
    b = 0

    ChiValueDocA = {}
    ChiValueDocB = {}

    for i in countList1.keys():
        a = a + countList1[i]
    for j in countList2.keys():
        b = b + countList2[j]

    N = a + b  # Total no. of instances (constant)
    P = a  # Number of instances of document1(constant)

    for eachFeature in FeatureSet:
        if (eachFeature in countList1.keys()):

            A = countList1[eachFeature]  # count of occurrence of X in document1
            B = 0

        else:
            B = countList2[eachFeature]  # count of occurrence of X in document1
            A = 0

        M = A + B  # count of occurrence of X in both documents
        chi2 = float((N * (((A * N) - (M * P)) ** 2)) / ((P * M) * (N - P) * (N - M)))

        if (A == 0):

            ChiValueDocB[eachFeature] = chi2

        else:

            ChiValueDocA[eachFeature] = chi2

    return ChiValueDocA, ChiValueDocB

if __name__=="__main__":
    pass