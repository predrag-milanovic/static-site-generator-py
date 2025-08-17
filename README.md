# static-site-generator-py

## About

This project is a lightweight Python static site generator (SSG) that transforms Markdown files into a deployable website. It processes content from `/content`, injects it into templates, and outputs optimized HTML to `/public`. Static assets are copied over to ensure the site is fully functional and ready for preview with a simple local server.

To serve the contents of the public directory change directories to the public directory and use Python's built-in [HTTP server](https://docs.python.org/3/library/http.server.html#command-line-interface):

```bash
cd public                       
python3 -m http.server 8888 &   
```

The `&` detaches the process to the background.
Run `fg` to brig it back, then `Ctrl+C`. 

## Features

- Converts Markdown content into HTML pages.
- Uses a customizable HTML template for consistent styling.
- Automatically copies static assets (CSS, images, etc.).
- Outputs ready-to-serve files into the `/public` directory.
- Supports local preview via Python’s built-in HTTP server.

## References

A quick reference for all the HTML and Markdown syntax you'll need for a project like this:

- [HTML Element Reference](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements)
- [MarkdowGuide.org](https://www.markdownguide.org/cheat-sheet/)

To get really good at using regex, use [regexr](regexr.com) for interactive regex testing.
It breaks down each part of the pattern and explains what it does.