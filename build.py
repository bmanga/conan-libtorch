#!/usr/bin/env python
# -*- coding: utf-8 -*-


from bincrafters import build_template_default
import os

if __name__ == "__main__":
    os.environ["CONAN_REMOTES"]="https://api.bintray.com/conan/conan-community/conan"

    builder = build_template_default.get_builder()

    builder.run()
