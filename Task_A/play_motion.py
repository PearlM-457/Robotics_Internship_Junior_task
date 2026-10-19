

import numpy as np, mujoco

XML = r"C:\Users\user\unitree_rl_gym\resources\robots\g1_description\g1_29dof.xml"

model = mujoco.MjModel.from_xml_path(XML)
data = mujoco.MjData(model)
motion = np.loadtxt("motion.csv", delimiter=",")

assert motion.shape[1] == model.nq, (motion.shape[1], model.nq)

row = motion[0].copy()
row[3:7] = motion[0][[6, 3, 4, 5]]   # CSV is xyzw, MuJoCo wants wxyz
data.qpos[:] = row
mujoco.mj_forward(model, data)
print("OK, frame 0 loaded. pelvis z =", data.qpos[2])