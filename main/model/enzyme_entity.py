class EnzymeEntity:
    e_name = None
    top_site = None
    bottom_site = None
    link = None

    def __init__(self, e_name, top_site, bottom_site, link):
        self.e_name = e_name
        self.top_site = top_site
        self.bottom_site = bottom_site
        self.link = link

    def get_e_name(self):
        return self.e_name

    def get_top_site(self):
        return self.top_site

    def __str__(self):
        return 'e_name: {}, top_site: {}'.format(self.e_name, self.top_site)
