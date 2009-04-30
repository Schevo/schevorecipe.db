"""Database management zc.buildout recipe for Schevo."""

# Copyright (c) 2009 ElevenCraft Inc.
# See LICENSE.txt for details.

import os
import subprocess

import zc.buildout


class Recipe(object):
    """Database management recipe.

    As a precaution, databases are never deleted when the recipe is
    altered or uninstalled.

    This recipe supports the following options:

    schevoscript
        The name of the 'schevo' script installed in the bin directory by
        a Schevo egg.  Default: 'schevo'.

    location
        (Required) The path to the database file, relative to the root of the
        buildout.  No default.

    app
        (One of 'app' or 'schema' is required.)  The top-level package name of
        the app whose schema should be used to create the database.
        No default.

    schema
        (One of 'app' or 'schema' is required.)  The package name of the
        schema to be used to create the database.  No default.

    schemaversion
        The schema version to use when creating the database.
        Default: latest version available.

    sample
        Set to True if the database should be populated with sample data upon
        creation.  Default: False.

    recreate
        Set to True if the database should be deleted whenever the buildout
        is run.  Useful for development.  Default: False.
    """

    def __init__(self, buildout, name, options):
        self.name = name
        self.schevoscript = os.path.abspath(os.path.join(
            buildout['buildout']['bin-directory'],
            options.get('schevoscript', 'schevo'),
            ))
        self.location = os.path.abspath(os.path.join(
            buildout['buildout']['directory'],
            options['location'],
            ))
        self.location_parent = os.path.dirname(self.location)
        self.app = options.get('app', None)
        self.schema = options.get('schema', None)
        if self.app is None and self.schema is None:
            raise zc.buildout.UserError(
                'One of "app" or "schema" must be given for %s' % name)
        self.schemaversion = options.get('schemaversion', None)
        if self.schemaversion is not None:
            self.schemaversion = int(self.schemaversion)
        self.sample = options.get('sample', False)
        self.recreate = options.get('recreate', False)

    def install(self):
        """Called when installing a part or when part config changes."""
        # Only create a database if recreate is True.
        if os.path.exists(self.location) and not self.recreate:
            print 'Not creating database %s (exists at %s)' % (
                self.name,
                self.location,
                )
        else:
            self._make_parent_dir()
            # Build the command.
            cmdline = [self.schevoscript, 'db', 'create']
            if self.app is not None:
                cmdline += ['--app=%s' % self.app]
            else:
                cmdline += ['--schema=%s' % self.schema]
            if self.schemaversion is not None:
                cmdline += ['--version=%i' % self.schemaversion]
            if self.sample:
                cmdline += ['--sample']
            if self.recreate:
                cmdline += ['--delete']
            cmdline += [self.location]
            # Call the command.
            print 'Calling %s' % ' '.join(cmdline)
            retcode = subprocess.call(cmdline)
            if retcode != 0:
                raise zc.buildout.UserError('Failed to create database.')
            print 'Created database.'
        # Keep databases around: Do not uninstall anything!
        return []

    def update(self):
        """Called when buildout is run again with no part config changes."""
        # Do the same thing as install for now.
        return self.install()

    def _make_parent_dir(self):
        """Make parent directory of database location."""
        if not os.path.exists(self.location_parent):
            os.makedirs(self.location_parent)
