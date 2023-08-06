# pyflies-psychopy

Generator for [PsychoPy](https://www.psychopy.org/) experiments from
[pyFlies](https://github.com/pyflies/pyflies) models.

When this project is installed you will have a textX registered generator that
can generate PsychoPy experiment from pyFlies models (`.pf` files). You can
verify that generator is available by:

```
textx list-generators
```

and you can generate PsychoPy experiment by:

```
textx generate <your pyflies model.pf> --target psychopy --overwrite
```

For the details see [running generators
section](https://pyflies.github.io/pyflies/latest/generators/) of pyFlies
documentation.


# Credits

Initial project layout generated with `textx startproject`.
