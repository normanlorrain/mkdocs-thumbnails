# mkdocs-thumbnails

[MkDocs](https://www.mkdocs.org/) plugin to generate thumbnails automatically.

Provides a mechanism to indicate, in Markdown, the desire for PDF files and YouTube links to have a thumbnail image, automatically generated/downloaded.

## Setup

Install the plugin using pip:

`pip install mkdocs-thumbnails`

Edit `mkdocs.yml`:  
1. Add `thumbnails` to the list of plugins.  
2. Add `markdown.extensions.attr_list` [(explained here)](https://python-markdown.github.io/extensions/attr_list/) to the list of markdown extensions:


```yaml
plugins:
  - search
  - thumbnails:
      # optional styling for the thumbnail:
      style: margin-top:5px;margin-bottom:5px;margin-right:25px  

markdown_extensions:
    - markdown.extensions.attr_list 
```
> **Note:** The extension If you have no `plugins` entry in your config file yet, you'll likely also want to add the `search` plugin. MkDocs enables it by default if there is no `plugins` entry set, but now you have to enable it explicitly.

More information about plugins in the [MkDocs documentation](http://www.mkdocs.org/user-guide/plugins/).

## Config

* `style` - This is the CSS style to be set in the thumbnail's image tag

## Usage
In the attribute list of a link, add `.pdf` or `.youtube` to turn on the thumbnail for that link:
```markdown
[My PDF file](foo.pdf){.pdf}⸱⸱
[A YouTube video link](https://youtu.be/dQw4w9WgXcQ){.youtube}⸱⸱  

```

The markdown conversion generates:
```html
<a href="foo.pdf" class="pdf" >My PDF file</a>
<br>
<a href="https://youtu.be/dQw4w9WgXcQ">A YouTube video link</a>
<br>
```

...which is converted by the plugin:
```html
<a href="foo.pdf"><img src="foo.pdf-thumb.png" class="pdf" >My PDF file</a>
<br>
<a href="https://youtu.be/dQw4w9WgXcQ"><img src="dQw4w9WgXcQ-thumb.png" class="youtube" >A YouTube video link</a>
<br>
```
Thumbnails are generated automatically.  PDF links will have the first page of the PDF in the thumbnail.  YouTube thumbnails are downloaded from Youtube via the link: `https://img.youtube.com/vi/{id}/default.jpg`

In the example above two spaces are added after each line, to force a markdown line break.


