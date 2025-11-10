# A Simple Counter Tool for Markdown

**Motivation:** I use Pandoc markdown for almost all my academic writing.
 Pandoc is a great tool. My main complaint is that it doesn’t natively support counters.

This is usually not a problem when latex/PDF is the only output format I need. However, sometimes I need HTML and docx outputs as well. And I feel really sorry for asking students to manually edit/check the docx files,  just to match the numbered references in PDF...


## Syntax

`counter` is designed to be a simple pre-processor for Markdown.
 Here’s the basic syntax:

- Use `` `c <pre:zz>` `` to register a counter with ID `pre:zz`.
   This counter belongs to the kind `pre`.
- Counters of the same kind are numbered sequentially, starting from 1.
  - If there’s no `:` in the counter ID, it goes into a default group.
- Use ``#pre:id`` for cross-references.
   It’ll be replaced by that counter’s number.

## Example

**Input:**

````md
# Intro
A numbered equation:
$$ y = x^2 \tag{#eq:main}$$
`c eq:main`
Another eq:
$$ y = x^3 \tag{#eq:3}$$
`c eq:3`

Cross-ref: Equation (#eq:3) is good.

`c thm:main`
**Theorem #thm:main.**
This theorem is plain.

# Model
`c thm:main2`
**Theorem #thm:main2.**
Another theorem.
````

**Output:**

```md
# Intro
A numbered equation:
$$ y = x^2 \tag{1}$$
Another eq:
$$ y = x^3 \tag{2}$$

Cross-ref: Equation (2) is good.

**Theorem 1.**
This theorem is plain.

# Model
**Theorem 2.**
Another theorem.⏎
```

PDF pic:

<img width="404" height="219" alt="image" src="https://github.com/user-attachments/assets/2bf9d3d1-0c52-4955-a521-90d0a17f0a19" />



## Design Notes
- I use `#thm:main` instead of `@thm:main` for cross-reference, as pandoc already abuses `@` for both citeproc and example lists.
- The syntax `` `c eq:zz` `` is inspired by knitr, which uses `` `r x=2` `` for evaluating inline R code.
- Since I was/am a LaTeX user, many design choices were probably influenced by amsthm.
- I do not care about clickable  hyperlinks.

## Implementation Notes

The implementation should be trivial. Just walk through the text files,
find all snippets of the pattern `` `c <id>`  ``, compute their counter values, and does a simple find-and-replace.

With the help of LLM, I wrote two
implementations in Go:
`counter.go` and `counterN.go`.
The only difference is that in `counterN.go`, the counter values will be appended by section/chapter numbers.

- My implementation of `counterN.go` is very ad-hoc and non-robust: just count how many lines start with `# ` before each ID.

Since most of the go code was written by LLM, I’m not sharing it here. 
Any modern LLM should be able to generate the code for you given the above description.
