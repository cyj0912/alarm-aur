# Arch Linux Repository for Jetson Nano

The script pulls NVIDIA's deb repo and generate PKGBUILDs based on the Debian packages.

Note that the Xorg video driver that NVIDIA provides only works with Xorg 1.19, hence the following AUR packages are recommended:
```
yay xorg-server1.19-git
yay xf86-input-libinput-git
```
