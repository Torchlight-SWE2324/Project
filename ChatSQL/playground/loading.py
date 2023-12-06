import sys
import time

def loading_animation(n):
    animation_chars = "|/-\\"
    start_time = time.time()

    while time.time() - start_time < n:
        for char in animation_chars:
            sys.stdout.write("\r" + "Loading " + char)
            sys.stdout.flush()
            time.sleep(0.1)

    sys.stdout.write("\r")  # Move cursor to the beginning of the line
    print("Loading complete!")

# Example usage with duration of 5 seconds
loading_animation(2)
