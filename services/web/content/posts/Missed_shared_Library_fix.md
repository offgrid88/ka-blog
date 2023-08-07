title: Missing shared Library problem fix [Archlinux]
date: 2023-07-11 





```
: cannot open shared object file: No such file or directory
```

If you are using Linux it's common that you have faced this problem, especially when you are using arch Linux or any similar distro. 

And the solution is easy, so easy that you can make a script that solve it whenever you face it , but we won't be doing that. 
I will show you how to fix it and how to avoid it. This article is not related to any distro, but I am using archlinux on my machine and it should work on yours. 

***The solution***

First identify which library you are missing with the exact version in my case  I am missing icu so I went to the archlinux packages archive and downloaded the zst file
https://archive.archlinux.org/packages/i/icu/
and then decompressed it


```
tar --use-compress-program=unzstd -xvf archive.tar.zst
```

After that switch to root user 

```
su - root
```

then you will find a usr directory cd into it 

```
cd usr/
```

copy the whole content of the directory into your main usr directory 

```
cp -r * /usr/
```

and you are done 
try running the application that caused you this problem and it should work

***Mitigation***

to avoid this error in the future just the solution I have is for archlinux but you could find other tutorials to do it on other distro. 

You need to stop the package manager in our case **pacman** from updating the library to a newer version. 

so you need to access this file using your best text editor I use nvim you use whatever vi,vim or nano

```
sudo nvim /etc/pacman.conf
```

look for 

```
IgnorePkg   = 
```

and add the package you want to stop from updating (in our case icu)

```
IgnorePkg   = icu
```

***Last note***
One last note, if you installed the package manually you don't need to change anything as pacman won't be able to update it. you need the mitigation steps for other packages.