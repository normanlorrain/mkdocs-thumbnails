# mkdocs-thumbnails

An mkdocs plugin to generate thumbnails automatically.

Provides a mechanism to indicate, in Markdown, the desire for PDF/YouTube links to have a thumbnail image, automatically generated/downloaded.

## Setup

Install the plugin using pip:

`pip install mkdocs-thumbnails`

Activate the plugin in `mkdocs.yml`:
```yaml
plugins:
  - search
  - thumbnails:
      # optional styling for the thumbnail:
      style: margin-top:5px;margin-bottom:5px;margin-right:25px  
```

> **Note:** If you have no `plugins` entry in your config file yet, you'll likely also want to add the `search` plugin. MkDocs enables it by default if there is no `plugins` entry set, but now you have to enable it explicitly.

More information about plugins in the [MkDocs documentation][mkdocs-plugins].

## Config

* `style` - This is the CSS style to be set in the thumbnail's image tag

[mkdocs-plugins]: http://www.mkdocs.org/user-guide/plugins/

