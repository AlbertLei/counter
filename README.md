# Counter --- a preprocessor for markdown
**Motivation:** I use pandoc markdown for almost all my academic writing.
My main complaint is that pandoc's ast doesn't natively support counters.

This is not a problem when latex/pdf is the only  format I need. 
However, sometimes I do need docx format output as well. 
And I feel really sorry for asking students to manually edit/check the docx files,
just to match the numbered cross-refs in pdf.

The [pandoc-crossref filter](https://github.com/lierdakil/pandoc-crossref) solves about 90% of my problems,
but it's not flexible enough for me. For example, it does not support amsthm-style crossrefs.

## Syntax of `counter`
`counter` is a pre-processor for markdown.
Here’s the basic syntax:

- Use `##pre:zz` to register a counter with ID `pre:zz`.
   This counter belongs to the kind `pre`.
  - For the ease of parse, a legit `id` value must (i) begin and end with an alphanumeric and (ii) be composed of alphanumeric, ":", "-" and "_".
- Counters of the same kind are numbered sequentially, starting from 1.
  - If there’s no `:` in the counter ID, it goes into a default kind.
- Use `#pre:id` for cross-references.

## Example usage

**Input:**

```markdown
**Theorem ##thm:main.**
This theorem is plain.

**Theorem ##thm:main2.**
Another theorem.

**Proposition ##prp:main2.**
This is a corollary of theorem #thm:main.

See Theorem #thm:main2 as well.

Below is table #tbl:1.

::: c
Table ##tbl:1: This is a plain table

![](table.pdf)
:::


## Figure

Below is figure #fig:1.


::: c
![](figure.pdf)

Figure ##fig:1: This is a figure.
:::


```



**Output:**

```markdown
**Theorem [1]{#thm:main}.**
This theorem is plain.

**Theorem [2]{#thm:main2}.**
Another theorem.

**Proposition [1]{#prp:main2}.**
This is a corollary of theorem [1](#thm:main).

See Theorem [2](#thm:main2) as well.

Below is table [1](#tbl:1).

::: c
Table [1]{#tbl:1}: This is a plain table

![](table.pdf)
:::


## Figure

Below is figure [1](#fig:1).

::: c
![](figure.pdf)

Figure [1]{#fig:1}: This is a figure.
:::
```


## Remarks
- I use `#thm:main` instead of `@thm:main` for cross-reference, as pandoc already abuses `@` for both citeproc and example lists.
- This preprocessor does not work inside equations, and i still use the pandoc cross-ref filter for equation and section crossrefs.


## Implementation
The implementation should be trivial. Just walk through the text files,
find all counter ids, compute their counter values, and does multiple find-and-replace.

Any modern LLM today should be able to generate the code for you given the above description.
I use golang to build an executable.
Since most of the go code was written by LLM, I’m not sharing it here.
