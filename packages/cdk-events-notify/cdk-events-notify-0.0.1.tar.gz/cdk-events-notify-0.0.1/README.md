[![NPM version](https://badge.fury.io/js/cdk-events-notify.svg)](https://badge.fury.io/js/cdk-events-notify)
[![PyPI version](https://badge.fury.io/py/cdk-events-notify.svg)](https://badge.fury.io/py/cdk-events-notify)
![Release](https://github.com/guan840912/cdk-s3bucket/workflows/Release/badge.svg)

![Downloads](https://img.shields.io/badge/-DOWNLOADS:-brightgreen?color=gray)
![npm](https://img.shields.io/npm/dt/cdk-events-notify?label=npm&color=orange)
![PyPI](https://img.shields.io/pypi/dm/cdk-events-notify?label=pypi&color=blue)

# cdk-events-notify

cdk-events-notify is an AWS CDK construct library that provides you know who login in your aws console.

## Welcome to contribute another event notify case you want.

### Now support

* Line Notify

## Usage

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import aws_cdk.core as cdk
from cdk_events_notify import EeventNotify

app = cdk.App()
stack = cdk.Stack(app, "integ-stack", env=env)
EeventNotify(stack, "LineEeventNotify", line_notify_token=process.env.LINE_NOTIFY_TOKEN)
```

### To deploy

```bash
cdk deploy
```

### To destroy

```bash
cdk destroy
```

## :clap:  Supporters

[![Stargazers repo roster for @guan840912/cdk-events-notify](https://reporoster.com/stars/guan840912/cdk-events-notify)](https://github.com/guan840912/cdk-events-notify/stargazers)
[![Forkers repo roster for @guan840912/cdk-events-notify](https://reporoster.com/forks/guan840912/cdk-events-notify)](https://github.com/guan840912/cdk-events-notify/network/members)
