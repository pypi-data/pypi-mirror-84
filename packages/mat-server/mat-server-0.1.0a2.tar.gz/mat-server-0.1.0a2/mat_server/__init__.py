from mat_server.app import AppContainer

container = AppContainer()
cli = container.create_cli()

if __name__ == '__main__':
    cli()
