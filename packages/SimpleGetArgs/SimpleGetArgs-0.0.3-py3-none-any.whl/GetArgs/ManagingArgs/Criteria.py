class ArgsCriteria:
    """Search parameters class"""

    def __init__(self):
        self.maxTweets = 0
        self.topTweets = False
        self.within = "15mi"
        self.emoji = "ignore"

    def setcounttill100(self, counttill100):
        """Set the permission to count to 100
        Parameters
        ----------
        ct100 : True or false
        """
        self.counttill100 = counttill100
        return self.counttill100

    def setprint(self, print1):
        """Set the permission to print name
        Parameters
        ----------
        print1 : True or false
        """
        self.print1 = print1
        return self.print1

    def setname(self, name):
        """Set the name of the guy you want to say hello
        Parameters
        ----------
        name : str,
        """
        self.name = name
        return self.name
