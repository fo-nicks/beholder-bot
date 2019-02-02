import sys

# Alternative to `print()` that will work within an infinite loop
def out(obj):
    sys.stdout.write('\n' + str(obj) + '\n')
    sys.stdout.flush()

