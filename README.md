# PythonFileReaderTemplate

Template for a custom Python-based file reader that hooks into *OVITO* and can easily be shared with other users.

This repository contains a template for creating your own [Python file reader](https://docs.ovito.org/python/introduction/custom_modifiers.html) !!WRONG LINK!!, which can be installed into *OVITO Pro* or the [`ovito`](https://pypi.org/project/ovito/) Python module using *pip*.

## Getting Started

1. Click the "Use this template" button to create your own repository based on this template.
2. Rename `src/FileReaderName` to reflect the name of your modifier.
3. Implement your [file reader](https://docs.ovito.org/python/introduction/custom_modifiers.html#advanced-interface) !!WRONG LINK!! in [`src/FileReaderName/__init__.py`](src/FileReaderName/__init__.py). Fill in the predefined functions as needed. More details on this method can be found in the [OVITO Python docs](https://www.ovito.org/docs/current/python/introduction/custom_modifiers.html#writing-custom-modifiers-advanced-interface) !!WRONG LINK!!. 
4. Fill in the [`pyproject.toml`](pyproject.toml) file. Fields that need to be replaced with your information are enclosed in descriptive `[[field]]` tags. Please make sure to include ovito>=3.9 as a dependency. Depending on your needs, you can add additional fields to the `pyproject.toml` file. Information can be found [here](https://setuptools.pypa.io/en/latest/userguide/index.html).
5. Fill in the [`README_Template.md`](README_Template.md) file. Again, the `[[fields]]` placeholders should guide you. Feel free to add other sections like "Images", "Citation", or "References" as needed.
6. Add meaningful examples and data sample files to the `Examples` directory to help others understand the use of your modifier.
7. Pick a license for your project and replace the current (MIT) [`LICENSE`](LICENSE) file with your license. If you keep the MIT license, please update the name and year in the current file.
8. Once you're done, rename `README_Template.md` to `README.md`, replacing this file.
