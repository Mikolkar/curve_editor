def de_casteljau(x, y, w, t):
    n = len(x) - 1
    W = [[0 for _ in range(n + 1)] for _ in range(n + 1)]

    for i in range(n + 1):
        W[i][0] = (x[i] * w[i], y[i] * w[i], w[i])

    for j in range(1, n + 1):
        for i in range(n - j + 1):
            W[i][j] = (
                (1 - t) * W[i][j - 1][0] + t * W[i + 1][j - 1][0],
                (1 - t) * W[i][j - 1][1] + t * W[i + 1][j - 1][1],
                (1 - t) * W[i][j - 1][2] + t * W[i + 1][j - 1][2],
            )

    return (W[0][n][0] / W[0][n][2], W[0][n][1] / W[0][n][2])
