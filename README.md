xiter
=====

`xiter` is a small library that aims to combine object-oriented syntax with
functional-style behavior into concise, readable and intent-declarative code.

It exposes `xiter()`, which can wrap any `iterable` object to feature:
* Lazily-applied transformations (`map`, `filter`, etc), plus common utilities
  such as `sum`, `all`, `count` and others.
  
* Chainable methods, which allow to clearly express series of transformations.

* Easy modification of data flow by simply commenting out or rearranging calls

* An early idea of semi-automatic parallelism in `map()`.

I plan to further improve the library, specially the last item.

The [xiter-euler](https://github.com/slezica/xiter-euler "xiter-euler") repository contains solutions to some of the project euler
problems using `xiter`. You can check them out if you want examples.

