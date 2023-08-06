zsv.ticker
~~~~~~~~~~

``zsv.ticker`` enables flexible and idiomatic regular execution of
tasks::

    from zsv.ticker import Ticker

    ticker = Ticker()
    ticker.start(5)

    while ticker.tick():
        execute_task()

``Ticker`` aims to be more idiomatic and easy to use than a time calculation and
sleep call, and further enables the instantaneous termination of a waiting
task::

    import signal
    from time import sleep
    from zsv.ticker import Ticker

    ticker = Ticker()
    ticker.start(5)

    def abort(signum, frame):
        ticker.stop()

    signal.signal(signal.SIGINT, abort)

    while ticker.tick():
        print("tick")
        sleep(2)
        print("tock")


The above script wraps a `stop` call in a signal handler registered to SIGINT:
hitting Ctrl+C after the script prints "tick" but before it prints "tock"
will yield a final "tock" before it terminates.
