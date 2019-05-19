def random_int_arr(shape, upto=20):
    mat = np.random.rand(*shape)
    for i in range(shape[0]):
        for j in range(shape[1]):
            mat[i, j] *= upto
    return mat.astype("int64")


def main():
    f = open("input.txt", "r")
    a = []
    for line in f.readlines():
        a.append([int(x) for x in line.split()])
    a = np.array(a, dtype='int64')

    # to find inverse
    # a = np.concatenate((a, np.eye(a.shape[0], a.shape[0], dtype="int64")), axis=1)

    full_gauss(a)


if __name__ == "__main__":
    main()
