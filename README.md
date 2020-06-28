# `podspec_builder`
#### WORK IN PROGRESS

Sick of having to constantly maintain your `.podspec` files? Ever been ready for a release, and realize that you forgot to bump the version on your `.podspec` file? This command line tool is intended to alleveiate some fo the pain points faced when publishing a library via [CocoaPods](https://cocoapods.org). In fact, with this tool you can remvoe the entire `.podspec` file fromo your project all together!

`podspec_builder` will autodetect the required Podspec files that need to be generated, detect dependencies, construct a dependency graph, generate your `.podspec` files, and push in the proper order for consumption.

Currently supported:
- [x] [xcodegen](https://github.com/yonaskolb/XcodeGen) - leverages `project.yml`
- [ ] [SwiftPM](https://github.com/apple/swift-package-manager)

TODO:
- [ ] Adjust project structure to follow standard
- [ ] Abstract podspec information into readable csv
- [ ] Auto detect third party dependencies and versions
- [ ] Add support for SwiftPM (swift package dump-package)
- [ ] CI Integration
- [ ] Unit test coverage

## Usage
```python
 usage: podspec_builder.py [-h] [-u] [-l] version

 positional arguments:
   version

 optional arguments:
   -h, --help    show this help message and exit
   -u, --upload  Determines if the newly built Podspec files should be pushed.
   -l, --local   Generate the podspec files and store them in the project
                 directory. NOTE: You are unable to push if this option is set.
```