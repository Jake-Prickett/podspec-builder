 #!/usr/bin/env python
"""
 Objects.py

 Intent:
      - Simplify the process of generating .podspec files
      - Easily generate and push to Private Pod Repo
      - No longer required to keep as part of Repo

 Jake Prickett - May 2020
"""

class Target:
    """
    Target of Pod to generate
    """
    def __init__(self, name, version, category="", dependencies=None):
        self.name = name
        self.version = version
        self.category = category
        if dependencies is None:
            dependencies = []
        self.dependencies = dependencies

    def add_dependency(self, dependency):
        """
        Add a dependency directly to a Target
        """
        self.dependencies.append(dependency)

    def as_podspec(self):
        """
        Podspec representation of the Target. Including name, version,
        dependencies, etc.
        """
        print('\n')
        print('Building Podspec for %s' % self.name)
        print('-----------------------------------------------------------')

        podspec = "Pod::Spec.new do |s|\n\n"
        podspec += "    s.name = '%s'\n" % self.name
        podspec += "    s.version = '%s'\n" % self.version
        podspec += "    s.summary = 'REPLACEME.'\n"
        podspec += "    s.homepage = 'REPLACEME'\n"
        podspec += "    s.license = 'REPLACEME'\n"
        podspec += "    s.author = 'REPLACEME'\n\n"

        podspec += "    s.documentation_url = 'REPLACEME'\n\n"

        podspec += "    s.swift_version = '5.0'\n"
        podspec += "    s.ios.deployment_target = '11.0'\n"

        podspec += "\n" if len(self.dependencies) > 0 else ""

        for dep in self.dependencies:
            podspec += dep.as_podspec()

        podspec += "\n"
        podspec += "    s.source = { :git => 'REPLACEME', :tag => s.version.to_s }\n"
        podspec += "    s.source_files = 'REPLACEME'\n" % (self.category, self.name)

        podspec += "\nend"
        return podspec

class InternalDependency(Target):
    """
    Internal dependency representation (Another Project Target)
    """
    def __init__(self, name, version="s.version.to_s"):
        Target.__init__(self, name, version)

    def as_podspec(self):
        return "    s.dependency '%s', %s\n" % (self.name, self.version)

class ThirdPartyDependency(Target):
    """
    Third party dependency such as gRPC-Swift, JWTDecode, etc.
    """
    def __init__(self, name, version):
        Target.__init__(self, name, version)

    def as_podspec(self):
        return "    s.dependency '%s', '%s'\n" % (self.name, self.version)
