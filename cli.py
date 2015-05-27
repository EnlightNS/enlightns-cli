# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

import click


@click.group()
def cli():
    """Helps creating the database"""
    pass

@cli.command()
def initdb():
    click.echo('Initialized the database')

@cli.command()
def dropdb():
    click.echo('Dropped the database')
