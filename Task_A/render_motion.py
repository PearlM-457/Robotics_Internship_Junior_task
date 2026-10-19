from pathlib import Path
import sys 
import numpy as np
import mujoco
import imageio

DEFAULT_XML = r"C:\Users\user\unitree_rl_gym\resources\robots\g1_description\g1_29dof.xml"
XML = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_XML
HERE = Path(__file__).parent
CSV = HERE / "motion.csv"
FPS = 30

model = mujoco.MjModel.from_xml_path(XML)
model.vis.global_.offwidth = 1280
model.vis.global_.offheight = 720
data = mujoco.MjData(model)
motion = np.loadtxt(CSV, delimiter=",")
assert motion.shape[1] == model.nq, (motion.shape[1], model.nq)

renderer = mujoco.Renderer(model, height=720, width=1280)

# camera that follows the robot
cam = mujoco.MjvCamera()
cam.distance = 3.0
cam.azimuth = 135
cam.elevation = -15

frames = []
for i, row in enumerate(motion):
    qpos = row.copy()
    qpos[3:7] = row[[6, 3, 4, 5]]      # xyzw -> wxyz
    data.qpos[:] = qpos
    mujoco.mj_forward(model, data)

    cam.lookat[:] = data.qpos[:3]      # keep camera on the pelvis
    renderer.update_scene(data, camera=cam)
    frames.append(renderer.render())

imageio.mimsave(HERE / "motion.mp4", frames, fps=FPS)
print(f"Saved motion.mp4 with {len(frames)} frames")