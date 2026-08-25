import matplotlib.pyplot as plt
import numpy as np


class GraphEngine:

    def plot(self, expression):

        x = np.linspace(-10, 10, 400)

        expression = expression.replace("^", "**")

        y = eval(expression)

        plt.figure(figsize=(8, 6))

        plt.plot(x, y)

        plt.title(f"y = {expression}")

        plt.grid(True)

        plt.xlabel("x")

        plt.ylabel("y")

        plt.show()