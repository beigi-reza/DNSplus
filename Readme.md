# DIG++
**CHECK DNS PROPAGATION**

 **`DIG++`** provides a free DNS propagation application to check Domain Name System records against a selected list of DNS servers in multiple regions worldwide. Perform a quick DNS propagation lookup for any hostname or domain, and check DNS data collected from all available DNS Servers to confirm that the DNS records are fully propagated.

`dig++` is a network administration Application for querying the Domain Name System (DNS).


This Application Use dig  Command Line Tools.

This program is available by default in Linux, but for Windows you need to install the Bind program.

## Install dig on linux 

Red Hat / CentOs
```bash
dnf install bind-utils
```

Debian / Ubuntu
```bash
apt install dnsutils
```

Windows 

[How to Install Dig on Windows](https://phoenixnap.com/kb/dig-windows)


## Run 
To run this program, you need Python version 3 or later

```
./dig++.py
```

>After the first run, select the `check` option once so that the DNS status of the servers is checked and the active servers are identified.

