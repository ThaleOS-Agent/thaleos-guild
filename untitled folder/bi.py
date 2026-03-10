import matplotlib.pyplot as plt

def plot_growth_chart(data):
    plt.plot(data, marker='o', linestyle='--', color='r')
    plt.title("Business Growth Projection")
    plt.xlabel("Year")
    plt.ylabel("Revenue ($M)")
    plt.show()

# Example usage:
growth_data = [5, 10, 15, 22, 30, 45]
plot_growth_chart(growth_data)