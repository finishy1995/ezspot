# EZSpot


EZSpot - the spot management tool help you to use AWS EC2 spot instance easily. 

## Features

1. Start workload as multi spot fleets
2. Stop workload by terminate all spot fleets behind
3. Auto associate EIP to all workload spot instance and manage EIP lifecycle

## Quick Start

First, instance this library
```bash
$ sudo pip install ezspot
```

Second, config your aws AKSK
```bash
$ aws configure --profile ${your_profile_name}
```

If you are the first time to use AWS Spot Fleet, you need to open your console and get a AWS service role for spot fleet.

Then, run
```bash
$ ezspot start
```

After it start competelt, you can try more config setting by write it under '~/.ezspot/config'
```text
[default]
wld_instance_type = [ c4.large , c4.xlarge ]
```

Because we are still working on this project, you can contact us [david.wang@finishy.cn](mailto:david.wang@finishy.cn)

## Version

0.0.2
