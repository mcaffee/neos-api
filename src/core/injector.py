import inject


def configure_injector():
    """
    Configure DI for the project.
    """
    def configure(binder: inject.Binder):
        pass
        # binder.bind(UserRepository, UserModelRepository())

    inject.configure_once(config=configure)
