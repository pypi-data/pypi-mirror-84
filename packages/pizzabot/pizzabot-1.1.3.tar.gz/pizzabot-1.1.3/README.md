# Pizzabot

Slice is working on a robot that delivers pizza. To instruct Pizzabot on how to deliver pizzas to all the houses in a neighborhood, give it a input string like this :P
```sh
$ pizzabot "5x5 (1, 3) (4,4)"
NNNEDEENED
```
# Dependencies

* Python 3.7 or later

# Installation

```sh
$ pip3 install pizzabot
```
# Build and test from source

```sh
$ git clone https://github.com/lightatzero/pizzabot.git
$ cd pizzabot
$ pip3 install -e ./
$ ./scripts/run_tests
```
If you want to isolate in docker
```sh
$ ./scripts/build 
$ docker run --rm --name pizzabot pizzabotimage
```
