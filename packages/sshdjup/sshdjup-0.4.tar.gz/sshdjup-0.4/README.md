# sshdjup
![PyPI](https://img.shields.io/pypi/v/sshdjup?color=yellow) <span style="margin-left: 2em">![GitHub last commit](https://img.shields.io/github/last-commit/YarikRevich/sshdjup?logo=GitHub)</span>

---


<h2><center>What it for?</center></h2>
<br/>

<div style="font-size:24px">This library was developed to make files upgrade more easier and to make update process more automated.</div> 

<br/>
<font size=5px>
Concised information:
<br/>
<br/>
<br/>



- ***Helps you to concentrate on coding.***
<br/>
- ***Economies you time.***
<br/>
- ***Automates ugdates through ssh.***
</font>

---

<h2><center>How to use?</center></h2>
<br/>

<font size=5px>
Firstly run such command to install pypi package:

```text
$ pip3 install sshdjup
```


<br/>

Create ```SSHFile``` and write available commands from 
[```COMMANDS.md```](./COMMANDS.md).

It is important to write such variables in ```SSHFile```.

```
HOST=111.222.333.444      #write your own host
USERNAME=root             #write your own username
PORT=22                   #it is optional variable default is 22
PASSWORD=12345678         #write your own password to the machine
```

<br/>
To run it you have to be located in the directory with SSHFile to test run such command:

```
$ python3 -m sshdjup --ping
```

<br/>

If  the output is:

```
$ python3 -m sshdjup --ping
[output] pong
```
run possible commands using such commands as:

```
$ python3 -m sshdjup --help
```

<br/>

*The number of commands is increasing and will be extended in the upcomming ```new versions```*
<br/>

> The master is YarikRevich
> Communicate via mail yariksvitlitskiy81@gmail.com
</font>