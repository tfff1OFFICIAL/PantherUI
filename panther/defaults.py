def default_event_parse(dt):
    import panther
    for event in panther.events:
        if event.name == "quit":
            print("PANTHER: quitting...")
            event.auto_handle()  # execute the subscriber who wants to clean up their code before we exit
            exit(0)  # quit

        event.auto_handle()
        #print(f"Handled event: {event}")


def default_window_config_update(key, value):
    """
    update the Window in _widgets._PantherApp
    :param dt:
    :return: None
    """
    import panther

    panther._window.apply_conf(key, value)


def default_run():
    """
    DEPRECATED!! - using kivy built-ins already
    The default run function
    :return: None
    """
    import panther

    print("PANTHER: default run executing...")

    panther.events.execute('load')

    dt = 0

    while True:
        # process events
        if panther.events:
            for event in panther.events:
                if event.name == "quit":
                    print("quitting...")
                    event.auto_handle()  # execute the subscriber who wants to clean up their code before we exit
                    exit(0)  # quit

                event.auto_handle()
                print(f"Handled event: {event}")

        if panther.timer:
            dt = panther.timer.time()
            panther.timer.reset()

        panther.events.execute('update', dt)

        # draw the screen
        if panther.canvas:
            # call user-specified drawing function
            panther.canvas.clear()
            panther.events.execute('draw')
            #panther.draw_screen()
