from Controller.benford_analysis import analyze_benford_law
import matplotlib.pyplot as plt

def main():
    # Analyze election results using Benford's Law
    plot, chi_square = analyze_benford_law()
    
    print(f"Chi-square test statistic: {chi_square:.2f}")
    print("Wyższe wartości chi-square wskazują na większe odchylenie od rozkładu Benforda")
    
    # Save the plot
    plot.savefig('benford_analysis.png')
    plt.close()

if __name__ == "__main__":
    main()
