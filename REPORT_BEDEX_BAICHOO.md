BÉDEX Antoine

BAICHOO Esteban

# Report - Stable Mariage Algorithm

## How to use the source files

Source files use the YAML syntax. It is an alternative to XML / JSON.

Here's an example of a source file (this is a very short example with 2 elements per group):

```yaml
group1_serenading: True
group1:
  - name: "A"
    rank:
      1: "Beta"
      2: "Alpha"
    nmax: 1
  - name: "B"
    rank:
      1: "Alpha"
      2: "Beta"
    nmax: 1

group2:
  - name: "Alpha"
    rank:
      1: "A"
      2: "B"
    nmax: 1

  - name: "Beta"
    rank:
      1: "B"
      2: "A"
    nmax: 1
```

Now, let's understand how it works:

- We have a `group1_serenading` boolean which indicates:
  - That group 1 will be doing the serenade if `True`
  - That group 2 will be doing the serenade if `False`
- A `group1`, which is a list of elements (new element begin with `-`). Each element contains:
  - A `name` for the element
  - A `rank` containing a `key`/`value` dictionary:
    - A `key` represents the rank of an element of the other group
    - A `value` represents the name of an element of the other group
  - A `nmax` which is equal to the maximum number of accepted elements from the other group (only relevant when the element is serenaded)

## How to use the script

You have to pass an argument to the script (which is named `sma.py`), as in the following example:

```bash
python sma.py sources.yml
```

Here, `sources.yml` is a source file like we saw earlier.

## How we implemented the algorithm

We used 2 concrete classes and 1 abstract class. The abstract class (`__Parent_Serenade`) contain generic attributes and methods for both `Serenader` and `Serenaded` class.

