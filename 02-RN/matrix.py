class Matrix:
    def __init__(self, val):
        if isinstance(val[0], list):
            self.val = val
            self.d = len(val), len(val[0])
        else:
            self.val = [val]
            self.d = 1, len(val)

    def __getitem__(self, key):
        return self.val[key]

    def __iter__(self):
        return (Matrix([row]) for row in self.val)

    def __add__(self, other):
        if isinstance(other, list):
            other = Matrix(other)

        if self.d != other.d:
            raise Exception(
                f"Tentando somar matrizes incompativeis ({self.d} != {other.d})"
            )

        M3 = []
        for i in range(self.d[0]):
            M3.append([self[i][j] + other[i][j] for j in range(self.d[1])])
        return Matrix(M3)

    def __radd__(self, other):
        if isinstance(other, list):
            other = Matrix(other)
            return other + self

    def __sub__(self, other):
        if self.d != other.d:
            raise Exception(
                f"Tentando somar matrizes incompativeis ({self.d} != {other.d})"
            )

        M3 = []
        for i in range(self.d[0]):
            M3.append([self[i][j] - other[i][j] for j in range(self.d[1])])
        return Matrix(M3)

    def __rsub__(self, other):
        if isinstance(other, list):
            other = Matrix(other)
            return other - self

    def __mul__(self, other):
        if isinstance(other, Matrix):
            if self.d[1] != other.d[0]:
                raise Exception(
                    f"Tentando multiplicar matrizes incompativeis ({self.d[1]} != {other.d[0]})"
                )

            d3 = self.d[0], other.d[1]
            M3 = []
            for i in range(d3[0]):
                linha = []
                for j in range(d3[1]):
                    # print(f"c[{i}][{j}] = " + " + ".join([f"A[{i}][{k}] * B[{k}][{j}]" for k in range(d1[1])]))
                    linha.append(
                        sum([self[i][k] * other[k][j] for k in range(self.d[1])])
                    )
                M3.append(linha)
            return Matrix(M3)
        elif isinstance(other, (int, float)):
            return Matrix([[item * other for item in linha] for linha in self.val])

    def __rmul__(self, other):
        if isinstance(other, (int, float)):
            return self * other

    def __eq__(self, other):
        if self.d != other.d:
            return False

        for i in range(self.d[0]):
            for j in range(self.d[1]):
                if self[i][j] != other[i][j]:
                    return False
        return True

    def __str__(self):
        lens = [[len(str(i)) for i in line] for line in self.val]

        max_values = [max(column) for column in zip(*lens)]
        w = sum(max_values) + len(max_values)
        top_border = "┌ " + " " * w + "┐"
        bot_border = "└ " + " " * w + "┘"

        rows = []
        for i in range(self.d[0]):
            row_str = (
                "│ "
                + " ".join(
                    f"{self.val[i][j]:>{max_values[j]}}" for j in range(self.d[1])
                )
                + " │"
            )
            rows.append(row_str)

        return "\n".join([top_border] + rows + [bot_border])

    def transposta(self):
        return Matrix(
            [[self[i][j] for i in range(self.d[0])] for j in range(self.d[1])]
        )

    def grand_sum(self):
        return sum(sum(col) for col in self.val)

    def aplicar_a_todos(self, fn):
        return Matrix([[fn(i) for i in line] for line in self.val])

    def elementwise_mul(self, other):
        if self.d != other.d:
            raise Exception(
                f"Tentando somar matrizes incompativeis ({self.d} != {other.d})"
            )

        M3 = []
        for i in range(self.d[0]):
            M3.append([self[i][j] * other[i][j] for j in range(self.d[1])])
        return Matrix(M3)


if __name__ == "__main__":
    A = Matrix([[1, 2, 3], [1, 2, 3], [4, 5, 6]])
    B = Matrix(
        [
            [10, 11],
            [20, 21],
            [30, 31],
        ]
    )

    assert A * B == Matrix([[140, 146], [140, 146], [320, 335]])

    print(B.transposta())

    print(2 * A)
