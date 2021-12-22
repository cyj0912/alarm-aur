# Arch Linux Repository for Jetson Nano

The script pulls NVIDIA's deb repo and generate PKGBUILDs based on the Debian packages.

Note that the Xorg video driver that NVIDIA provides only works with Xorg 1.19, hence the following AUR packages are recommended:
```
yay xorg-server1.19-git
yay xf86-input-libinput-git
```

# Notes

## Boot information on Jetson Nano 2GB's default SD image

https://docs.nvidia.com/jetson/l4t/index.html#page/Tegra%20Linux%20Driver%20Package%20Development%20Guide/uboot_guide.html

CBoot then U-Boot
Default U-Boot script will run kernel specified under /boot/extlinux/extlinux.conf

## Other Notes

/usr/lib/libv4l2.so needs to be fixed.

Symlinks with SONAME are automatically created by ldconfig.
