# sparsest-solution-underdetermined-linear-system
optimize norm with underdetermined system equality constraint

## problem statement

```
Minimize ||x||_p
Given Ax=b
where   x \in R^n
        A \in R^{m \times n}
        b \in R^m
        p \in R_+
```

## algorithm

### unconstrained optimization (L_p norm, p > 1)

```
Let z \in R^{n-m} be an arbitrary vector.
Represent the solution of Ax=b by x = A* z + b* // see boyd convex optimization
The problem becomes minimizing ||A*z + b*||_p
```

### linear programming (L_1 norm)

```
Let y \in R^{n} with 2 additional constraints
y \geq x and y \geq -x
Let u = [x, y] \in R^{2n}, the feasible set is a polyhydron.
Minimize y, get y = |x|_1
```

## results

### L2 norm sparsity

![norm2](https://raw.githubusercontent.com/khanhhhh/sparse-uls/main/assets/norm2.png)

### L1 norm sparsity

![norm1](https://raw.githubusercontent.com/khanhhhh/sparse-uls/main/assets/norm1.png)

## Packaging

```bash
rm -rf dist/*
python setup.py sdist bdist_wheel
twine upload dist/*
```


## Useful links

- https://pypi.org/project/sparse-uls/

- https://web.stanford.edu/~boyd/cvxbook/bv_cvxbook.pdf (page 682)

- https://packaging.python.org/tutorials/packaging-projects/

- https://dzone.com/articles/executable-package-pip-install
