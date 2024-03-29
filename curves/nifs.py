class NIFS3:
    def __init__(self, x, y):
        # varaiables to create spline
        self.x = x
        self.y = y
        self.n = len(x)
        self.nl = self.n - 1
        self.moments = self.cal_moments()

    def h(self, k):
        return self.x[k] - self.x[k - 1]

    # returning moments
    def cal_moments(self):
        # creating lists for q, u and moments
        q = [0]
        u = [0]
        moments = [0 for _ in range(self.n)]

        def λ(k):
            return self.h(k) / (self.h(k) + self.h(k + 1))

        def p(k):
            return λ(k) * q[k - 1] + 2

        def d(k):
            return 6 * dQt(self.x[k - 1 : k + 2], self.y[k - 1 : k + 2])

        # difference quotient
        def dQt(x, y):
            if len(y) == 1:
                return y[0]
            return (dQt(x[1:], y[1:]) - dQt(x[1:], y[:-1])) / (x[-1] - x[0])

        for k in range(1, self.n - 1):
            q.append((λ(k) - 1) / p(k))
            u.append((d(k) - λ(k) * u[k - 1]) / p(k))

        moments[self.nl - 1] = u[self.nl - 1]
        k = self.nl - 2
        while k >= 0:
            moments[k] = u[k] + q[k] * moments[k + 1]
            k -= 1
        return moments

    def s(self, x, M):
        x_k = self.x
        for k in range(1, self.n):
            if self.x[k - 1] <= x < self.x[k]:
                return (
                    1 / 6 * M[k - 1] * (x_k[k] - x) ** 3
                    + 1 / 6 * M[k] * (x - x_k[k - 1]) ** 3
                    + (self.y[k - 1] - 1 / 6 * M[k - 1] * self.h(k) ** 2) * (x_k[k] - x)
                    + (self.y[k] - 1 / 6 * M[k] * self.h(k) ** 2) * (x - x_k[k - 1])
                ) / self.h(k)

    def result(self):
        M = self.moments
        return lambda x: self.s(x, M)
