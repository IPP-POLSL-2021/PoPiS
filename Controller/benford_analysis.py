import pandas as pd
import numpy as np
import plotly.graph_objects as go
from .Results import getResults
from scipy import stats

def perform_ks_test(actual_dist, benford_dist):
    """
    Perform Kolmogorov-Smirnov test to compare actual distribution with Benford's Law.

    Args:
    actual_dist (array-like): The observed distribution of first digits.
    benford_dist (array-like): The expected Benford's Law distribution.

    Returns:
    tuple: KS statistic and p-value
    """
    # Normalize distributions to create cumulative distribution functions
    actual_cdf = np.cumsum(actual_dist) / np.sum(actual_dist)
    benford_cdf = np.cumsum(benford_dist) / np.sum(benford_dist)

    # Perform Kolmogorov-Smirnov test
    ks_statistic, p_value = stats.ks_2samp(actual_cdf, benford_cdf)

    return ks_statistic, p_value

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
            all_values.extend(
                [v for v in values if isinstance(v, (int, float))])

        if not all_values:
            raise ValueError("Nie znaleziono danych liczbowych do analizy")

        # Calculate distributions
        benford_dist, actual_dist = calculate_benford_distribution(all_values)

        # Create visualization using Plotly
        digits = range(1, 10)

        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=digits, y=benford_dist,
            name="Rozkład Benforda",
            marker_color='blue', opacity=0.5
        ))
        fig.add_trace(go.Bar(
            x=digits, y=actual_dist,
            name="Rozkład rzeczywisty",
            marker_color='red', opacity=0.5
        ))

        fig.update_layout(
            title=f'Analiza rozkładu Benforda - {election_level}',
            xaxis_title='Pierwsza cyfra',
            yaxis_title='Częstość (%)',
            barmode='group',
            template='plotly_white'
        )

        # Calculate chi-square test statistic
        expected = np.array(benford_dist) * len(all_values) / 100
        observed = np.array(actual_dist) * len(all_values) / 100
        chi_square = np.sum((observed - expected) ** 2 / expected)

        # Calculate KS statistic and p-value
        ks_statistic, p_value = perform_ks_test(actual_dist, benford_dist)

        return fig, chi_square, ks_statistic, p_value

    except Exception as e:
        raise ValueError(f"Błąd podczas analizy: {str(e)}")
