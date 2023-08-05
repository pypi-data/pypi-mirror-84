class Version:
    major = 0
    minor = 5
    patch = 0

    alpha_build = False
    beta_build = False
    developer_build = False

    def __str__(self):
        _human_readable_version = f"{self.major}.{self.minor}.{self.patch}"
        if self.alpha_build:
            _human_readable_version += ".alpha"

        if self.beta_build:
            _human_readable_version += ".beta"

        if self.developer_build:
            _human_readable_version += ".developer-build"

        return _human_readable_version
