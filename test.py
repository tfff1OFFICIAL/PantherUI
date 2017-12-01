import panther


@panther.events.subscribe('load')
def load_event():
    print("Loaded panther!")


panther.conf.height = 500
panther.conf.width = 500
panther.conf.title = "hi there"

panther.start()
