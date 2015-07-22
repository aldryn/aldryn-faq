# -*- coding: utf-8 -*-
from django.shortcuts import _get_queryset

from .exceptions import OldCategoryFormatUsed


def get_category_from_slug(queryset, slug, pk=None, language=None):
    """
    Given a category queryset, lookup a category that matches
    the given slug and pk if available.
    If no pk is available or match is found by combining
    slug and pk into one string, then raise OldCategoryFormatUsed exception.
    """
    if pk:
        category = get_or_none(
            queryset,
            pk=pk,
            translations__slug=slug
        )

        if category:
            return category
        else:
            slug = '{}-{}'.format(pk, slug)

    category = get_or_none(queryset, translations__slug=slug)

    if category:
        new_url = category.get_absolute_url(
            language=language,
            slug=slug
        )
        error = OldCategoryFormatUsed(
            category_slug=slug,
            new_url_format=new_url
        )
        raise error
    return category


def get_or_none(klass, *args, **kwargs):
    queryset = _get_queryset(klass)

    try:
        return queryset.get(*args, **kwargs)
    except queryset.model.DoesNotExist:
        return None
