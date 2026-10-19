# Robotics_Internship_Junior_task
Trying simulation tools (Ultimate Bots Studio, Mujoco) to learn robot motion

# Part A: Human Motion to Robot (Unitree G1)

## What this is
A 5-second motion for the Unitree G1 generated in UltimateBots Studio,
exported as a LAFAN CSV, and played back in MuJoCo and rendered to MP4.

## Files
- `motion.csv`: LAFAN motion file (150 frames, 30 fps, 36 columns)
- `motion.mp4`: rendered result
- `prompt.txt`: input used in UltimateBots Studio (suggested prompt in the studio)
- `render_motion.py`: loads the G1, plays the motion, saves the video
- `inspect_g1.py`: prints the model's `nq` and joint names
- `read_csv.py`: checks the CSV shape and quaternion norms

## How to reproduce
1. Clone Unitree RL Gym: https://github.com/unitreerobotics/unitree_rl_gym
2. Install dependencies:
   `pip install mujoco numpy imageio imageio-ffmpeg`
3. Run from this folder, passing the path to your copy of the G1 model:
   `python render_motion.py path\to\unitree_rl_gym\resources\robots\g1_description\g1_29dof.xml`
4. `motion.mp4` is written next to the script.

## How I determined what the CSV columns represent
- The file has 150 rows and 36 columns. 36 = 7 + 29, which matches
  `model.nq` of `g1_29dof.xml` (a free-floating base plus 29 joints).
- Columns 0-2: root position. Column 2 is about 0.78 m, a plausible pelvis height.
- Columns 3-6: root orientation quaternion. Row norms are about 1.0, and the
  order is (x, y, z, w), so it is reordered to MuJoCo's (w, x, y, z).
- Columns 7-35: the 29 joint angles, in the same order as the joint list
  printed by `inspect_g1.py`.
- 150 frames for a 5 s clip gives 30 fps.
- Check: setting frame 0 as `qpos` gave a correct standing pose.