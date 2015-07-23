# -*- coding: utf-8 -*-


class OldCategoryFormatUsed(Exception):
    """
    This exception is raised then we detect
    that the old url format for categories is being used.
    Once raised, this exception is handled by the view to redirect to the new
    url format.
    """
    def __init__(self, category_slug, new_url_format):
        self.category_slug = category_slug
        self.new_url_format = new_url_format
