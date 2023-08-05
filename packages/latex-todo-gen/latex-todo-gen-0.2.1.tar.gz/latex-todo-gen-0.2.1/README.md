# latex-todo-gen

Extract all TODOs and FIXMEs from LaTeX project.

## Usage

```
usage: latex-todo-gen [-h] [--directories DIRECTORIES] [--files FILES]
                      [--keywords KEYWORDS] [--outfile OUTFILE]
                      [--description DESCRIPTION] [--footer FOOTER]

Extract TODOs from TeX files.

optional arguments:
  -h, --help            show this help message and exit
  --directories DIRECTORIES, -d DIRECTORIES
                        comma separated list of directories
  --files FILES, -f FILES
                        comma separated list of files
  --keywords KEYWORDS, -k KEYWORDS
                        comma separated list of keywords
  --outfile OUTFILE, -o OUTFILE
                        output file
  --description DESCRIPTION
                        set output file description
  --footer FOOTER       set output file footer

For more information, see https://gitlab.com/matyashorky/latex-todo-gen.
```

Multiple output files supported:

- Markdown (`.md`). This is a default.
- LaTeX (`.tex`).
- PDF (`.pdf`). Generates `.tex` file and converts it using the `latex` package.

## Examples
```bash
# Use default settings
latex-todo-gen

# Set custom keywords
latex-todo-gen -k "REVIEW,FIXME,TODO,NOTE"

# Set description and output file to PDF
latex-todo-gen --description "This file is generated on every commit." -o "WIP.pdf"

# Set sources
latex-todo-gen -d "src,settings" -f "main.tex"
```

## Contributing

**PRs are welcome.** I'm currently looking for:

- pre-commit: I haven't been able to make it work, it seemed not to be able to locate the python script.
- Load setup from config file. Maybe `.todo-gen.yaml`?
- Universal TODO generator. This has proven to be much more universal program: you can just swap latex' `%` with python's `#` and you've got python-todo-gen. I'm probably migrate it sometime, but for now, it's just latex.
- Multiple lines below the keyword: `# TODO3` would append three lines instead of one
