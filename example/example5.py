library = "scipy"
import importlib.util
from pathlib import Path

import dcov

spec = importlib.util.find_spec(library)
origin = spec.origin
print(f"source is {origin}")

code = r'''
import numpy as np
from scipy.optimize import root_scalar
from scipy.stats import linregress


# Function to calculate the roots of a quadratic equation
def calculate_quadratic_roots(coefficients):
    """
    Calculate the roots of a quadratic equation using `scipy.optimize.root_scalar`.
    
    Args:
    coefficients (tuple): A tuple (a, b, c) containing the coefficients of the quadratic equation ax^2 + bx + c = 0.
    
    Returns:
    tuple: A tuple containing the two roots of the quadratic equation.
    """
    a, b, c = coefficients

    if a == 0:
        raise ValueError("Coefficient 'a' cannot be zero for a quadratic equation.")
    
    def quadratic_function(x):
        return a * x**2 + b * x + c

    root1 = root_scalar(quadratic_function, bracket=[-100, 100]).root
    root2 = root_scalar(quadratic_function, bracket=[-100, -10], x0=-10, fprime=lambda x: 2*a*x + b).root

    return root1, root2

class SimpleLinearRegression:
    """
    A class to perform simple linear regression using `scipy.stats.linregress`.
    """
    def __init__(self):
        self.coefficients = None
        self.intercept = None

    def fit(self, x, y):
        """
        Fit the regression model to the data.
        
        Args:
        x (array-like): The independent variable.
        y (array-like): The dependent variable.
        """
        slope, intercept, _, _, _ = linregress(x, y)
        self.coefficients = slope
        self.intercept = intercept

    def predict(self, x):
        """
        Predict the dependent variable for a given value of the independent variable.
        
        Args:
        x (array-like): The independent variable.
        
        Returns:
        array-like: The predicted dependent variable.
        """
        return self.coefficients * x + self.intercept

    def get_coefficients(self):
        """
        Get the regression coefficients (slope and intercept).
        
        Returns:
        tuple: A tuple containing the slope and intercept.
        """
        return self.coefficients, self.intercept


def main():
    # Task 1: Calculate the roots of a quadratic equation with coefficients a = 2, b = 5, and c = 2
    try:
        quadratic_coefficients = (2, 5, 2)
        roots = calculate_quadratic_roots(quadratic_coefficients)
        print(f"Task 1: Roots of the quadratic equation ax^2 + bx + c = 0 are: {roots}")
    except ValueError as e:
        print(f"Task 1: Error: {e}")

    # Task 2: Perform simple linear regression on a predefined dataset and calculate the coefficients of the regression line
    x = np.array([1, 2, 3, 4, 5])
    y = np.array([2, 4, 5, 4, 5])
    linear_regression = SimpleLinearRegression()
    linear_regression.fit(x, y)
    coefficients = linear_regression.get_coefficients()
    print(f"Task 2: Coefficients of the regression line: slope = {coefficients[0]}, intercept = {coefficients[1]}")

    # Task 3: Use the regression model to predict the values for a given set of input data
    new_x = np.array([6, 7, 8])
    predictions = linear_regression.predict(new_x)
    print(f"Task 3: Predicted values for input data {new_x} are: {predictions}")


if __name__ == "__main__":
    main()
'''
dcov.open_bitmap_py()
dcov.clear_bitmap_py()
with dcov.LoaderWrapper("edge") as loader:
    loader.add_source(origin)
    exec(code)
    print(f"final cov={dcov.count_bits_py()}")
