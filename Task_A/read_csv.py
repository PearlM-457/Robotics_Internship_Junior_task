import numpy as np
data = np.loadtxt("motion.csv", delimiter=",")
print(data.shape)             # expect (~150, 36) for 5 s at 30 fps
print(data[0, :7])            # root z should be ~0.7-0.8 m (pelvis height)
print(np.linalg.norm(data[:, 3:7], axis=1)[:5])   # should be ~1.0 if these are a quaternion