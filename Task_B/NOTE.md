# Part B: G1 Walking in a Circle

## What I changed
In `deploy/deploy_mujoco/configs/g1.yaml`:
- `cmd_init: [0.5, 0, 0]`  for walking staright 
-> `cmd_init: [0.3, 0, 0.9]` which makes a circle 
tried some couple of changes and chose that 
but why ? because when i started with `cmd_init : [0.4, 0, 0.3]` it tried to make a huge egg shaped circle but went half way through then video stopped due to duration (where i decided to change the duration too )  NEEDED TUNING

- `simulation_duration` -> `70` (so one full loop fits in the run)

In `deploy_mujoco.py` I also added a 25 s pause before the simulation
starts, so I could position the camera and start screen recording.
This does not affect the robot's behavior.

## Why this produces circular motion
The policy takes a velocity command `[vx, vy, wz]` (forward speed,
sideways speed, yaw rate) expressed in the robot's own body frame. The
default command is forward only, so the robot walks in a straight line.
With a constant forward speed and a constant yaw rate, the robot keeps
turning while it moves ahead, which traces a circle of radius about
vx / wz. The robot does not track the turn command exactly (the real
loop took about 70 s and did not close perfectly), but the path is
a circle.

## What inputs does the policy receive, and where do they come from?
It receives a 47-dimensional observation, rebuilt every policy step:
- Base angular velocity (3): from the simulated IMU (`d.qvel[3:6]`)
- Projected gravity vector (3): computed from the base quaternion
  (`d.qpos[3:7]`); it tells the robot which way is down
- Velocity command (3): `cmd_init` from the config, multiplied by `cmd_scale`
- Joint positions minus default pose (12): from `d.qpos[7:]`
- Joint velocities (12): from `d.qvel[6:]`
- Previous action (12): kept from the last policy step
- Gait phase (2): sin and cos of a clock-based phase (0.8 s period)

## What does the policy output, and how does it become torque?
The policy outputs 12 values, one per leg joint (the arms and waist are
held at their default pose). Each action is turned into a target angle:

    target_dof_pos = action * action_scale + default_angles

A PD controller then computes the torque for each joint, at every
simulation step:

    tau = kp * (target_dof_pos - q) + kd * (0 - dq)

The torque is written to `d.ctrl`, and MuJoCo steps the physics. The policy
runs once every `control_decimation` simulation steps, so the PD controller
runs more often than the policy.

## Files
- `walk_circle.mp4`: screen recording of the robot walking in a circle
- `g1.yaml`: my modified config
- `deploy_mujoco.py`: the script with the added pause