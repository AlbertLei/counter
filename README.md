# About
Most (all?) markdown variants lack support for registering counters.

I use the following syntax to register counters and crossref them.
- Use `##thm:foo` to register a counter with ID `thm:foo`.
  This counter belongs to the kind `thm`.
- Counters of the same kind are numbered sequentially, starting from 1.
  - If there’s no `:` in the counter ID, it belongs to a default kind.
- Use `@thm:foo` for cross-references.

## Example
The following contents:

<table>
<tr>
<th>before.md</th>
<th>after.md</th>
</tr>
<tr>
<td>

```md
##thm:main
**Theorem @thm:main.**
This theorem is plain.

##thm:main2
**Theorem @thm:main2.**
Another theorem.

One more test: @thm:main2

##prp:main2
**Proposition @prp:main2.**
This is a corollary of theorem @thm:main.

See Theorem @thm:main2 as well.

## Figure
Below is figure @fig:1.

##fig:1
::: c
![](figure.pdf)

Figure @fig:1: This is a figure.
:::
```

</td>
<td>

```md
<EMPTYLINE>
**Theorem 1.**
This theorem is plain.

<EMPTYLINE>
**Theorem 2.**
Another theorem.

One more test: 2

<EMPTYLINE>
**Proposition 1.**
This is a corollary of theorem 1.

See Theorem 2 as well.

## Figure
Below is figure 1.

<EMPTYLINE>
::: c
![](figure.pdf)

Figure 1: This is a figure.
:::
```

</td>
</tr>
</table>


## Remarks
- I hesitated between using `#id` or `@id` for cross-references.
  I chose  `@thm:main` because if there is a typo in reference id,
  it will usually be caught by pandoc citeproc.

- For cross-ref equations, use `\label{eq:id}` and `@eq:id`, respectively.

## Implementation
The implementation is trivial. Just walk through the text files,
find all counter ids, compute their counter values, and does multiple find-and-replace.

A python implementation is provided. See `counter.py` and `counter-eq.py`
