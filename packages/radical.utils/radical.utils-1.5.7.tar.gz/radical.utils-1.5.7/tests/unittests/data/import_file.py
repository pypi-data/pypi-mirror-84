
import time


# ------------------------------------------------------------------------------
#
def foo(bar, buz=1):

    assert bar == buz
    time.sleep(0.1)
    return True


# ------------------------------------------------------------------------------
#
class Foo(object):

    def foo(self, bar, buz=1):

        assert bar == buz
        time.sleep(0.1)
        return True


# ------------------------------------------------------------------------------

