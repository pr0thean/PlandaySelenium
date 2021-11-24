class WebControl:
    def __init__(self,
                 class_name: str = None,
                 id: str = None,
                 tag_name: str = None,
                 css_selector: str = None
                 ):
        self.class_name = class_name
        self.id = id
        self.tag_name = tag_name
        self.css_selector = css_selector