import re
import json
from pathlib import Path
from urllib.parse import quote


class TableOfContents:
    def __init__(self, nb_path):
        nb_path = Path(nb_path)
        with nb_path.open() as file:
            nb = json.load(file)
        toc = []
        prev_level = 0
        for cell in nb["cells"]:
            if cell["cell_type"] != "markdown":
                continue
            for heading in re.finditer(
                r"^(#+)\s*(.+)$",
                "".join(cell["source"]),
                flags=re.MULTILINE,
            ):
                level, heading = len(heading.group(1)), heading.group(2)
                level_diff = level - prev_level
                prev_level = level
                ul = "<ul>" if level_diff > 0 else "</ul>"
                toc.extend(ul for _ in range(abs(level_diff)))
                anchor = quote(heading.replace(" ", "-"))
                toc.append(f'<li><a href="#{anchor}">{heading}</a></li>')
        toc.extend("</ul>" for _ in range(prev_level))
        self.toc = "\n".join(toc)
        self.path = nb_path

    def __repr__(self):
        return f"<{self.__class__.__name__} for {self.path.name!r}>"

    def _repr_html_(self):
        return self.toc
