## Configuration

Configuration is stored inside `.license-sh.json` in the root of the project.

It can be generated interactively with `license-sh config` command or modified when running with `-i, --interactivity` 
flag.

Example:
```
{
  "ignored_packages": {
    "python_pipenv": [ 
      "PyInquirer==1.0.0",
      "setuptools==3.4.5"
    ],
    "npm": [],
    "maven": [],
    "yarn": []
  },
  "whitelist": [
    "MIT"
  ],
  "overridden_packages": {
    "python_pipenv": {
      "hamcrest-core==1.3": {
        "license": "MIT",
        "licenseText": "License text",
        "reason": "This is reason for this override"
      }
    }
  }

```

* ### Ignore packages
```
  "ignored_packages": {
    "python_pipenv": [
      "PyInquirer==1.0.0",
      "setuptools==3.4.5"
    ],
    "npm": [],
    "maven": [],
    "yarn": []
  }
```
You can ignore specific packages if it's license is unknown or you have some reason hat you don't what to see it as an error.

Format:
"{PACKAGE_NAME}=={PACKAGE_VERSION}"  --- To ignore specific version of the package RECOMMENDED 

"{PACKAGE_NAME}" --- To ignore every version of this specific package


* ### Whitelist
```
  "whitelist": [
    "MIT"
  ]
```
Whitelist is a list of green licenses that shouldn't throw an error if found.

* ### Override packages
```
   "overridden_packages": {
    "python_pipenv": {
      "hamcrest-core==1.3": {
        "license": "MIT",
        "licenseText": "License text",
        "reason": "This is reason for this override"
      }
    }
  }
```
You can override specific package license and license text.

Format:

 * Key
"{PACKAGE_NAME}=={PACKAGE_VERSION}"  --- To override specific package version RECOMMENDED 

"{PACKAGE_NAME}" --- To override every version of this package

 * Value
 ```
 {
  "license": {OVERRIDE_LICENSE_NAME},
  "licenseText": {OVERRIDE_LICENSE_TEXT},
  "reason": {OVERRIDE_LICENSE_REASON}
}
 ```
License text is only used if `--dependencies` flag is used
