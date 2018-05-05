# EZSpot


EZSpot - the spot management tool help you to use AWS EC2 spot instances easily. 

## Features

1. Start workload as multi spot fleets
    - If some of fleets can not start, the whole workload will rollback.
    - Rollback will clean all resources which create by EZSpot.
    - Support all AWS regions, including BJS and ZHY in China.
2. Stop workload by terminate all spot fleets behind by workload tag.
3. Auto associate EIP to all workload spot instance and manage EIP lifecycle.
4. Log file output under '~/.ezspot/log'.
5. Can get spot fleet run time and cost by status command.
6. Can run workload by normal mode (spot fleets) or persistent (spot instances with block duration) or on-demand (on-demand ec2 instances).
7. Clean all resources created by EZSpot in the history. (Since we already have rollback feature, this command would be only used when some untracked error happened).

## Quick Start

First, instance this library
```bash
$ sudo pip install ezspot
```

Second, config your aws AKSK
```bash
$ aws configure
```

If you are the first time to use AWS Spot Fleet, you need to open your console and get a AWS service role for spot fleet.

Then, run
```bash
$ ezspot start
```

Run stop to close your workload
```bash
$ ezspot stop
```

Run status to check workload status, including cost and time (Only support normal mode)
```bash
$ ezspot status
```

Run clean to clean aws console useless resources (Created by EZSpot) if nessary
```bash
$ ezspot clean
```

You can also try more config setting by write it under '~/.ezspot/config' or in command
```text
[default]
wld_instance_type = [ c4.large , c4.xlarge ]
...
```

You can see the examples folder for more cases.

Because we are still working on this project, you can contact us [david.wang@finishy.cn](mailto:david.wang@finishy.cn)

## Docs

[config](CONFIG.md)

## TODO

- [ ] Fixed public IP and private IP
- [ ] Support ELB and other config for instances

## Version

0.0.6
