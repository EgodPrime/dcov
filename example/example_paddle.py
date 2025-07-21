import paddle

# Example usage
input = paddle.uniform([10, 2])
print(f"input={input}")
linear = paddle.nn.Linear(2, 3)
print(f"linear={linear}")
out = linear(input)
print(f"out=linear(input)={out}")
