import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from .Results import getResults

def get_first_digit(number):
    """Extract the first digit of a number."""
    try:
        return int(str(abs(float(number))).strip('0.')[0])
    except (ValueError, IndexError):
        return None

def calculate_benford_distribution(data):
    """Calculate the actual distribution of first digits and compare with Benford's Law."""
    # Theoretical Benford's Law distribution
    benford = [np.log10(1 + 1/d) * 100 for d in range(1, 10)]
    
    # Calculate actual distribution
    first_digits = [get_first_digit(x) for x in data if x > 0]
    first_digits = [d for d in first_digits if d is not None]    
    if not first_digits:
        raise ValueError("Brak odpowiednich danych do analizy")
        
    digit_counts = pd.Series(first_digits).value_counts().sort_index()
    actual_distribution = (digit_counts / len(first_digits) * 100)
    
    return benford, actual_distribution.values

def analyze_benford_law(election_level="województwa", type="procentowe"):
    """Analyze election results using Benford's Law."""
    try:
        # Get election results
        _, results = getResults(0, election_level, type)
        
        # Combine all numerical values for analysis
        all_values = []
        for column in results.columns:
            values = results[column].dropna().values
            all_values.extend([v for v in values if isinstance(v, (int, float))])
        
        if not all_values:
            raise ValueError("Nie znaleziono danych liczbowych do analizy")
        
        # Calculate distributions
        benford_dist, actual_dist = calculate_benford_distribution(all_values)
        
        # Create visualization
        plt.figure(figsize=(10, 6))
        digits = range(1, 10)
        
        plt.bar([x - 0.2 for x in digits], benford_dist, width=0.4, 
                label="Rozkład Benforda", color='blue', alpha=0.5)
        plt.bar([x + 0.2 for x in digits], actual_dist, width=0.4, 
                label="Rozkład rzeczywisty", color='red', alpha=0.5)
        
        plt.xlabel('Pierwsza cyfra')
        plt.ylabel('Częstość (%)')
        plt.title(f'Analiza rozkładu Benforda - {election_level}')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.xticks(digits)
        
        # Calculate chi-square test statistic
        expected = np.array(benford_dist) * len(all_values) / 100
        observed = np.array(actual_dist) * len(all_values) / 100
        chi_square = np.sum((observed - expected) ** 2 / expected)
        
        return plt, chi_square
        
    except Exception as e:
        plt.close()  # Clean up any open figures
        raise ValueError(f"Błąd podczas analizy: {str(e)}")
