#!/usr/bin/env python
"""
 podmanager.py

 Intent:
      - Parses project.yml used for generating .xcodeproj
      - Generates an ordered array of Pods to be created/pushed
      - Pushes Pods to remote if specified

 Jake Prickett - May 2020
"""

import os
import yaml
from flatten import flatten
from objects import Target
from objects import InternalDependency
from objects import ThirdPartyDependency

class PodManager:

    pods = []
    sorted_dependency_pods = []

    def __init__(self, directory, version, should_publish):
        self.directory = directory
        self.version = version
        self.should_publish = should_publish

    def write(self, pod, contents):
        print("    Writing to %s/%s.podspec " % (self.directory, pod))
        f = open("%s/%s.podspec" % (self.directory, pod), "w")
        f.write(contents)
        f.close

    def publish(self, pod_name):
        print("    Publishing %s.podspec" % (pod_name))
        os.system('pod trunk push --allow-warnings --skip-import-validation %s/%s.podspec' % (self.directory, pod_name))

    def detect_pods(self):
        pods = {}
        test = {}

        # Process project.yml file and create required Pods

        with open('project.yml', "r") as file:
            project = yaml.full_load(file)

            for name, info in project['targets'].items():
                # We don't want podspecs for Test targets
                if 'Test' in name:
                    continue

                category = info['templateAttributes']['layer']

                if 'dependencies' in info:
                    test[name] = [dependencies['target'] for dependencies in info['dependencies']]
                    deps = [InternalDependency(dependencies['target']) for dependencies in info['dependencies']]
                else:
                    deps = []
            
                target = Target(name, self.version, category, deps)

                # Manually adding 3rd party libraries
                #    - Think of a better way to handle this (JP)

                pods[target.name] = target

            self.pods = pods
            self.sorted_dependency_pods = flatten(test)
    
    def go(self):
        if len(self.sorted_dependency_pods) == 0:
            print("ERROR: Must call detect_pods before executing.")
            exit()

        # Create .podspec files and publish
        for name in self.sorted_dependency_pods:
            target = self.pods[name]
            self.write(target.name, target.as_podspec())
            if self.should_publish:
                self.publish(target.name)
            else:
                print("    Skipping Publishing...")
