#!/usr/bin/env python3
import requests
import re
import os
import subprocess

repo_overview = 'https://repo.download.nvidia.com/jetson/'

r = requests.get(repo_overview)
src = str(r.content)
i_until = src.find('<a name="Jetpack 4.5">')
src = src[:i_until]
debs = re.findall(r'https:\/\/repo\S+?deb', src)

pkg_list = []
prev_name = ''
for deb_url in debs:
    tag = None
    if 'jetson/t210' in deb_url:
        tag = 't210'
    if 'jetson/common' in deb_url:
        tag = 'common'
    if not tag:
        continue

    last = deb_url.rfind('/')
    deb_name = deb_url[last+1:]
    name, ver, arch = deb_name.split('_')
    arch = arch[:-4]
    if arch == 'arm64':
        arch = 'aarch64'
    t = (name, ver, arch, tag, deb_url)
    if name == prev_name:
        pkg_list.pop()
    prev_name = name
    pkg_list.append(t)

print(pkg_list)

name_set = set()
for t in pkg_list:
    name_set.add(t[0])

cwd = os.getcwd()
for name, ver, arch, tag, deb_url in pkg_list:
    last = deb_url.rfind('/')
    deb_name = deb_url[last+1:]

    os.chdir(cwd)
    os.system(f'mkdir -p {name}')
    os.chdir(cwd + '/' + name)

    if not os.path.isfile('control'):
        os.system(f'wget -nc {deb_url}')
        os.system(f'bsdtar -xf {deb_name}')
        os.system(f'tar xvf control.tar*')

    pkgdesc = ''
    depends = ''
    with open('control') as f:
        fls = f.read().splitlines()
        for fl in fls:
            if fl.startswith('Description: '):
                pkgdesc = fl[13:]
            elif fl.startswith('Depends:'):
                colon_i = fl.find(':')
                deps = fl[colon_i+1:].strip()
                deps = deps.split(',')
                for dep in deps:
                    dep = dep.strip()
                    i_space = dep.find(' ')
                    dep_name = dep[:i_space]
                    if dep_name in name_set:
                        dep_ver = dep[i_space:]
                        dep_ver = dep_ver.replace(' ', '').replace('(', '').replace(')','').replace('-', '_')
                        depends += f"'{dep_name}{dep_ver}' "

    checksum = subprocess.check_output(f'sha256sum -b {deb_name}', cwd=os.getcwd(), shell=True, text=True)
    checksum = checksum.split()[0]

    ver_ = ver.replace('-', '_')
    head = f"""pkgname={name}
pkgver={ver_}
pkgrel=1
pkgdesc='{pkgdesc}'
arch=({arch})
url='https://repo.download.nvidia.com/jetson/'
license=('custom')
depends=({depends})
source=('{deb_url}')
sha256sums=('{checksum}')
"""
    
    tail = """
prepare() {
  mkdir -p root
  tar xvf data.tar* -C root
}

package() {
  cp -a root/. $pkgdir/

  # On Arch, /lib is symlink to /usr/lib
  if test -d $pkgdir/lib; then
    cp -a $pkgdir/lib/. $pkgdir/usr/lib/
    rm -rf $pkgdir/lib
  fi

  # On Arch, sbin is a symlink to bin
  if test -d $pkgdir/usr/sbin; then
    cp -a $pkgdir/usr/sbin/. $pkgdir/usr/bin/
    rm -rf $pkgdir/usr/sbin
  fi

  # Arch on ARM doesn't use multilib
  if test -d $pkgdir/lib/aarch64-linux-gnu; then
    cp -a $pkgdir/lib/aarch64-linux-gnu/. $pkgdir/lib/
    rm -rf $pkgdir/lib/aarch64-linux-gnu
  fi
  if test -d $pkgdir/usr/lib/aarch64-linux-gnu; then
    cp -a $pkgdir/usr/lib/aarch64-linux-gnu/. $pkgdir/usr/lib/
    rm -rf $pkgdir/usr/lib/aarch64-linux-gnu
  fi
}
"""
    if not os.path.isfile('TAIL'):
        with open('TAIL', 'w') as f:
            f.write(tail)
    else:
        with open('TAIL') as f:
            tail = f.read()

    print(head)
    with open('PKGBUILD', 'w') as f:
        f.write(head)
        f.write(tail)
