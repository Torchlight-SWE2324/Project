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

    #sys.stdout.write("\r")  # Move cursor to the beginning of the line
    #print("Loading complete!")
    sys.stdout.write("\r" + " " * (len("Loading " + animation_chars[-1]) + 1))  # Clear the loading animation
    sys.stdout.flush()
    

if __name__ == "__main__":
    loading_animation(2)