import time
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

print("Hello.")
time.sleep(1)
print("Are you ready?")
time.sleep(1)
print("Press Enter to continue")
input("Press Enter to continue...")
print("preparing...")
time.sleep(5)

# 1. Load the image
img = mpimg.imread("Luke Charles.jpg")

# 2. Display the image
plt.imshow(img)
plt.show()

