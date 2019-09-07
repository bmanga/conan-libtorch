#!/usr/bin/env python
# -*- coding: utf-8 -*-


from bincrafters import build_template_default

if __name__ == "__main__":
    config_url = "https://github.com/bincrafters/conan-config.git"

    builder = build_template_default.get_builder()

    builder.run()
