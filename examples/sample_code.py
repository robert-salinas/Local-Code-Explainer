def calculate_fibonacci(n: int) -> int:
    """Calcula el n-ésimo número de Fibonacci."""
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b

class DataProcessor:
    def __init__(self, data: list):
        self.data = data

    def get_average(self) -> float:
        if not self.data:
            return 0.0
        return sum(self.data) / len(self.data)

if __name__ == "__main__":
    print(calculate_fibonacci(10))
    processor = DataProcessor([1, 2, 3, 4, 5])
    print(processor.get_average())
