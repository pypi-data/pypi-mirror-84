# altair_morberg



## Install

`pip install altair_morberg`

## How to use

```python
#hide_output
import altair as alt
import altair_morberg.core as morberg

alt.themes.register("morberg_theme", morberg.theme)
alt.themes.enable("morberg_theme")
```

Here is one chart using this theme:

![Example graph using altair_morberg theme](visualization.png "Scatterplot graph")

[More examples](https://morberg.github.io/altair_morberg/examples.html) using this theme are available in [the documentation](https://morberg.github.io/altair_morberg/).
