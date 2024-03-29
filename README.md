# 深度相机D435在gazebo中的仿真软件包

本软件包基于`ros2 humble`

## 依赖

1. [realsense_gazebo_plugin](https://github.com/hellototoro/realsense_gazebo_plugin)

2. [realsense-ros](https://github.com/IntelRealSense/realsense-ros)

## 编译

```bash
colcon build --symlink-install --packages-up-to depth_camera_gazebo
```

## 运行

```bash
ros2 launch depth_camera_gazebo depth_camera.launch.py
```
