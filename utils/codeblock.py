class Codeblock:
    def __init__(self, title, extra_title = "", description = ""):
        self.title = title
        self.description = description
        self.footer = ""
        self.extra_title = extra_title
        
        if self.extra_title != "":
            self.extra_title = f" {self.extra_title}"

    def set_footer(self, footer):   self.footer = footer
    def generate_title(self):       return f"```ini\n[ {self.title} ]{self.extra_title}```"
    def generate_description(self): return f"```asciidoc\n{self.description}```"
    def generate_footer(self):      return f"```ini\n# {self.footer}```"
    
    def __str__(self):
        if self.description == "":
            return self.generate_title()
        elif self.description != "" and self.footer == "":
            return self.generate_title() + self.generate_description()
        elif self.title == "" and self.footer == "":
            return self.generate_title() + self.generate_description()
        else:
            return self.generate_title() + self.generate_description() + self.generate_footer()