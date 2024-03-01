import time
import sys

def print_dots():
    for _ in range(3):
        sys.stdout.write('.')
        time.sleep(1)
    sys.stdout.flush()
    sys.stdout.write('\b\b\b   \r')  # Move the cursor back to delete the dots
    sys.stdout.flush()

# Example usage:
print("Printing dots:")
while True:
    print_dots()
