library = "torch"
import importlib.util
from pathlib import Path

import dcov

spec = importlib.util.find_spec(library)
origin = spec.origin
print(f"source is {origin}")

code = r'''
import numpy as np
from scipy.optimize import root

class KeplerSolver:
    """
    This class provides solutions to Kepler's Equation using the scipy library.
    """

    def __init__(self, e, n=1):
        """
        Initializes the KeplerSolver with the eccentricity (e) and mean motion (n).
        """
        self.e = e  # Eccentricity of the orbit
        self.n = n  # Mean motion, defaults to 1 rad/day for simplicity

        # Validate the eccentricity
        if not (0 <= e < 1):
            raise ValueError("Eccentricity must be between 0 and 1.")

        # Validate the mean motion
        if n <= 0:
            raise ValueError("Mean motion must be greater than 0.")

    def kepler_equation(self, E, M):
        """
        Defines the Kepler's Equation.
        """
        return E - self.e * np.sin(E) - M

    def solve_kepler(self, M0, tol=1e-8):
        """
        Solves Kepler's Equation for the eccentric anomaly (E) given the mean anomaly (M0).
        """
        # Use scipy.optimize.root to find the solution
        sol = root(self.kepler_equation, M0, args=(M0,), tol=tol)

        if not sol.success:
            raise ValueError("Failed to converge to a solution.")

        return sol.x[0]

    def calculate_true_anomaly(self, E):
        """
        Calculates the true anomaly (v) from the eccentric anomaly (E).
        """
        return 2 * np.arctan2(np.sqrt(1+self.e)*np.sin(E/2), np.sqrt(1-self.e)*np.cos(E/2))

    def calculate_new_moon_dates(self, start_day, days=30):
        """
        Calculates the new Moon dates for a given number of days from the start day.
        """
        new_moons = []
        M0 = 0  # Start with mean anomaly at zero for the first new moon

        for day in range(start_day, start_day + days):
            if day % self.n == 0:  # New moon occurs when mean anomaly completes a full rotation
                E = self.solve_kepler(M0)
                v = self.calculate_true_anomaly(E)
                new_moons.append((day, E, v))
                M0 += 2 * np.pi  # Increment the mean anomaly by 2π for the next new moon

        return new_moons

def main():
    # Test with predefined values
    e = 0.25  # Example eccentricity
    n = 1  # Example mean motion (days^-1)
    start_day = 0  # Example start day

    solver = KeplerSolver(e=e, n=n)
    new_moons = solver.calculate_new_moon_dates(start_day=start_day, days=60)  # Calculate for 60 days

    print("New Moon Dates (Day, Eccentric Anomaly, True Anomaly):")
    for moon in new_moons:
        print(moon)

if __name__ == "__main__":
    main()
'''
with dcov.LoaderWrapper() as loader:
    loader.add_source(Path(origin).resolve())
    exec(code)
    print(f"final cov={dcov.count_bits_py()}")
