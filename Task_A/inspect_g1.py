import mujoco

path = r"C:\Users\user\unitree_rl_gym\resources\robots\g1_description\g1_29dof.xml"
model = mujoco.MjModel.from_xml_path(path)

print("nq:", model.nq)
for i in range(model.njnt):
    print(i, model.joint(i).name)
