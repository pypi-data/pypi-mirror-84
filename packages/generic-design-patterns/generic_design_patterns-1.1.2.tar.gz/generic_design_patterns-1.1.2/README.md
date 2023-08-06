# Python Generic Design Patterns

[![PyPI-Status](https://img.shields.io/pypi/v/generic-design-patterns.svg)](https://pypi.org/project/generic-design-patterns/)
[![PyPI-Versions](https://img.shields.io/pypi/pyversions/generic-design-patterns.svg)](https://pypi.org/project/generic-design-patterns/)
[![GitHub issues](https://img.shields.io/github/issues/ShadowCodeCz/generic_design_patterns)](https://github.com/ShadowCodeCz/generic_design_patterns/issues)
[![Build Status](https://travis-ci.com/ShadowCodeCz/generic_design_patterns.svg?branch=master)](https://travis-ci.com/ShadowCodeCz/generic_design_patterns)
[![GitHub license](https://img.shields.io/github/license/ShadowCodeCz/generic_design_patterns)](https://github.com/ShadowCodeCz/generic_design_patterns/blob/master/LICENSE)

Python package implements design patterns in generic way. Its can be used in a wide range of projects.
Some of these patterns are slightly improved for efficient use in real-world projects.

## Installation 
```python
pip install generic-design-patterns 
``` 

## Overview

### Implemented Patterns
* [Chain of responsibility](#chain-of-responsibility)

* [Event Provider](#event-provider)

* [Specification](#specification)

### Other parts of package
* [Plugin](#plugin)

## Chain Of Responsibility
The purpose of this text is not to explain the principles of chain of responsibility. For example, source describing CoR is [refactoring.guru].
This package implements node of chain as plugin. For more information about plugin in this package visit [plugin chapter](#plugin).


### How it works in few steps
1. User create chain node plugin

2. User set collectors which collect all chain nodes (plugins)

3. User call build function


### Chain Node
Chain node have to inherit from  `gdp.chain.ChainNodePlugin`, which inherit form `yapsy.IPlugin.IPlugin`. 

Each node of chain have to implement these methods:
* `check()` - It detects that the request is handleable by the node. The method has to return bool value.

* `handle()` - It is performing method which processes the request. It returns result. 

* `description()` - It returns string or any other class which describes the node/plugin.

All nodes/plugins (in one chain) have to implement `check()` and `handle()` with same arguments.    

### Examples
Here is a short minimum example. It implements chain nodes for pseudo handling different text formats.

![Chain of responsibility example][chain_example]

#### TXT Node Plugin
```python
import generic_design_patterns as gdp

class TxtChainPlugin(gdp.chain.ChainNodePlugin):
    answer = "txt successfully handled"

    def check(self, input_string):
        return "txt" == input_string.strip()

    def handle(self, input_string):
        return self.answer

    def description(self):
        return "txt"
``` 

#### JSON Node Plugin
```python
import generic_design_patterns as gdp

class JsonChainPlugin(gdp.chain.ChainNodePlugin):
    answer = "json successfully handled"

    def check(self, input_string):
        return "json" == input_string.strip()

    def handle(self, input_string):
        return self.answer

    def description(self):
        return "json"
``` 

#### Build chain
```python
import generic_design_patterns as gdp

collectors = [gdp.plugin.SubclassPluginCollector(gdp.chain.ChainNodePlugin)]
chain = gdp.chain.build(collectors)
``` 
This example uses `gdp.plugin.SubclassPluginCollector`. This package implements more plugin collectors, which are described in part [plugin collectors](#collectors).


#### Handle request by chain
```python
for request in ["txt", "json", "yaml"]:
    result = chain.handle(request)
    print(result)
``` 

```python
>>> txt successfully handled
>>> json successfully handled
>>> None
``` 

#### Get description of chain nodes
The chain is dynamically build by collected plugins. Generally we do not know which nodes chain will contain (before build). 
However assembled chain should offer information about its nodes. It other words chain should describe which request is able handle.
This feature cover chain method `description()`.

```python
descriptions = chain.description()
print(descriptions)
``` 
```python
>>> ["txt", "json"]
``` 


Input value _yaml_ has not handler in the chain. In that case return value is `None`.

## Event Provider
This standard implementation of publisher-subscriber design pattern. There are not any improvements. Note that current implementation is only for single thread/process usage. 

### How it works
* Main part is event provider, which store subscriptions. On the basis of subscriptions provider directs notifications to right subscribers. 

* Subscribers can register at provider.

* Publishers can send notification via provider.

### Examples
The code shows minimum example. Note:
* The subscriber has to implement `update()` method. The package contains `AdvancedSubscriber` class which add methods for subscribe and unsubscribe itself.

* The publisher is created only for this example. Important is line where `notify()` method is called. 

* The example shows how to make subscription. It has to part string `message` and `subscriber` object.

* Use notification class from this package or your custom class which should inherit from it. The most import is that notification has to contain message attribute.

```python
import generic_design_patterns as gdp

dummy_message = "dummy message"

class DummySubscriber(gdp.event.Subscriber):
    def __init__(self):
        self.notification = None

    def update(self, notification):
        print(notification.message)

class DummyPublisher:
    def __init__(self, provider):
        self.provider = provider
    
    def publish(self):
        dummy_notification = gdp.event.Notification(dummy_message)
        self.provider.notify(dummy_notification)

provider = gdp.event.Provider()

subscriber = DummySubscriber()
provider.subscribe(dummy_message, subscriber)

publisher = DummyPublisher(provider)
publisher.publish()

print(subscriber.notification.message)
``` 

```python
>>> dummy message
``` 

## Specification
The purpose of this text is not to explain the principles of specification pattern. For detail information visit [wiki - specification pattern]. 

However it is useful to describe the most important aspects of this pattern:
* This pattern encapsulates condition to class.

* This pattern enables compose condition together and create more complex conditions. All this without losing readability and clarity. In other words, it allows to avoid an endless cascade of if-else cascades or some very long condition.

* This pattern allows to create the composite conditions dynamically.

### Examples
The example is intended to demonstrate the creation of a complex condition.

First of all define list to work with.
```python
alphabet_list = ["Alpha", "Bravo", "Charlie", "Delta", "Echo", "Foxtrot", "Golf", "Hotel"]
```

Now define rules for selecting items:
* Select items its index is lower or equal to 2 and not start with char "b" (case insensitive).

* Select items its index is higher than 2 and it contains "e" or "a" but not both.  (case insensitive)

#### Create single conditions by specification pattern
```python
import generic_design_patterns as gdp

class ContainChar(gdp.specification.Condition):
    required_char = ""

    def is_satisfied(self, index, item):
        return self.required_char in item.lower()


class ContainCharA(ContainChar):
    required_char = "a"


class ContainCharE(ContainChar):
    required_char = "e"


class IsIndexHigherThanTwo(gdp.specification.Condition):
    def is_satisfied(self, index, item):
        return index > 2

class FirstCharIsB(gdp.specification.Condition):
    def is_satisfied(self, index, item):
        return item[0].lower() == "b"
```
Note that input arguments of method `is_satisfied()`, it depends only on the user's requirements. But it is necessary that the arguments of all conditions are the same.

#### Put single conditions together
```python
condition = (~IndexHigherThanTwo() & ~FirstCharIsB())  
condition |= (IndexHigherThanTwo() & (ContainCharA() ^ ContainCharE()))
``` 

#### Apply condition
Iterate over the list and filter items which meet condition.
```python
for index, item in enumerate(alphabet_list):
    if condition(index, item):
        print(item)
``` 

```python
>>> Alpha
>>> Charlie
>>> Echo
>>> Hotel
``` 

## Plugin 
Here is not implement some plugin system. Plugin module only encapsulates existing systems 
and makes it easier to use. Current version of the package uses plugin only for [chain of responsibility](#chain-of-responsibility).

### Collectors
In the context of this package, plugin can be average class or [Yapsy] plugin. For more information about Yapsy plugin system visit [Yapsy documentation] pages.

Collectors are intended for find plugin and make it accessible. This package contains three basic plugin collectors:
* `gdp.plugin.YapsyPluginCollector`
* `gdp.plugin.YapsyRegExPluginCollector`
* `gdp.plugin.SubclassPluginCollector`

All examples in this chapter follow the example in chapter [chain of responsibility](#chain-of-responsibility).

#### YapsyPluginCollector
In the default setting, this collector find standard [Yapsy] plugins by `.yapsy-plugin` info file.

Assume this directory structure:
```
+- plugins/
   +- toml.py
   +- toml.yapsy-plugin
   +- yaml.py
   +- yaml.yapsy-plugin
``` 

#####  toml.py
```python
import generic_design_patterns as gdp


class TomlChainPlugin(gdp.chain.ChainNodePlugin):
    answer = "toml successfully handled"

    def check(self, input_string):
        return "toml" == input_string.strip()

    def handle(self, input_string):
        return self.answer

    def description(self):
        return "toml"
``` 

#####  toml.yapsy-plugin
```
[Core]
Name = toml
Module = toml

[Documentation]
Author = ShadowCodeCz
Version = 0.1
Description = Test Toml Plugin
``` 

Toml and Yaml plugins are similar. 

##### Collector construction
```python
import generic_design_patterns as gdp

collector = gdp.plugin.YapsyPluginCollector(["./plugins"])
``` 
If you are experienced with [Yapsy], you can use attribute `plugin_manager` of `gdp.plugin.YapsyPluginCollector` class. It is instance of `yapsy.PluginManager.PluginManager`. 

#### YapsyRegExPluginCollector
This collector is child of `YapsyPluginCollector`, which bring some improvements:
* plugins are located in destination by regular expression
* `.yapsy-plugin` are not required

Assume this directory structure which is similar to previous one only without `.yapsy-plugin`. Contents of `.py` file are same.
```
+- plugins/
   +- t_plugin_toml.py
   +- t_plugin_yaml.py
``` 

##### Collector construction
```python
import generic_design_patterns as gdp

collector = gdp.plugin.YapsyRegExPluginCollector(["./plugins"], "t_plugin_.+.py$")
```
Be careful about regular expression. Especially about ending symbol `$`. It will find also `.pyc` files without `$` at the end of re. It will causes problems. 

#### SubclassPluginCollector
It is collecting all child of selected class. The example of usage the collector `SubclassPluginCollector` is in [chain of responsibility](#chain-of-responsibility) chapter.


[chain_example]: https://raw.githubusercontent.com/ShadowCodeCz/generic_design_patterns/184f910ff25711fc03e458cb66bf18346c900995/img/chain_example.svg "Chain of responsibility example"
[chain_of_plugins_design]: img/chain_plugin_design.svg "Chain of plugins design"
[refactoring.guru]: https://refactoring.guru/design-patterns/chain-of-responsibility
[Yapsy]: https://pypi.org/project/Yapsy/
[Yapsy documentation]: http://yapsy.sourceforge.net/
[wiki - specification pattern]: https://en.wikipedia.org/wiki/Specification_pattern