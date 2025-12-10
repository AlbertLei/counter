# Counter --- a preprocessor for markdown
**Motivation:** I use pandoc markdown for almost all my academic writing.
My main complaint is that pandoc's ast doesn't natively support counters.

This is not a problem when latex/pdf is the only  format I need.
However, sometimes I do need docx format output as well.
And I feel really sorry for asking students to manually edit/check the docx files,
just to match the numbered cross-refs in pdf.

## Syntax
`counter` is a pre-processor for markdown.
Here’s the basic syntax:

- Use `__#thm:zz__` to register a counter with ID `thm:zz`.
  This counter belongs to the kind `thm`.
- Counters of the same kind are numbered sequentially, starting from 1.
  - If there’s no `:` in the counter ID, it belongs to a default kind.
- Use `@thm:id` for cross-references.


For cross-ref equations, use `\label{eq:id}` and `@eq:id`, respectively.


## Remarks
- I hesitated between using `#thm:main` or `@thm:main`.
  I finally chose  `@thm:main` because if there is a typo in reference id,
  it will be caught by pandoc citeproc.


## Implementation
The implementation is trivial. Just walk through the text files,
find all counter ids, compute their counter values, and does multiple find-and-replace.

My python implementation is provided. See `counter.py` and `counter-eq.py`
