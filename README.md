# EZSpot


EZSpot - the spot management tool help you to use AWS EC2 spot instance easily. 

## Features

1. Start workload as multi spot fleets
    - If some of fleets can not start, the whole workload will rollback.
    - Rollback will clean all resources which create by EZSpot.
    - Support all AWS regions, including BJS and ZHY in China.
2. Stop workload by terminate all spot fleets behind by workload tag.
3. Auto associate EIP to all workload spot instance and manage EIP lifecycle.
4. Log file output under '~/.ezspot/log'

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
$ ezspot start -p ${aws_profile} -r ${aws_region}
```

After it start competelt, you can try more config setting by write it under '~/.ezspot/config'
```text
[default]
wld_instance_type = [ c4.large , c4.xlarge ]
...
```

You can see the examples folder for more cases.

Because we are still working on this project, you can contact us [david.wang@finishy.cn](mailto:david.wang@finishy.cn)

## Version

0.0.3

## Bugs

- Now, if you config your aws profile and other aws config in '~/.ezspot/config', it will not work.
