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

U-boot resizes at offset `0x2c0800` inside the SPI flash, there is a dtb appended to its end. (`u-boot.bin` is a copy of `u-boot-dtb.bin` for the `p3450-0000_defconfig` mainline build of u-boot.)

`sudo dd if=u-boot.bin of=/dev/mtd0 bs=512 conv=notrunc seek=5636`

Directly running this command to replace stock u-boot failed. The new u-boot couldn't pass boot-image validation.

## Other Notes

/usr/lib/libv4l2.so needs to be fixed.

Symlinks with SONAME are automatically created by ldconfig.
