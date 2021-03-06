import math

"""
basic l-system "library"/framework
designed to be used by logorator generators

https://en.wikipedia.org/wiki/L-system

Joel Carlbark 2012
"""

class LSys:
    def __init__(self, axiom, rules, iterations):
        self.stack = []
        self.verts = []
        self.axiom = axiom
        self.rules = rules
        self.iters = int(iterations)
        self.commands = self.evolve(self.iters, axiom, rules)


    def produce_command(self, axiom, rules):
        """
        Produce a new command string from the
        axiom string and the rules applied to it
        """
        command = ""
        for i in axiom:
            command = command + rules.get(i, i)
        return command


    def evolve(self, n, axiom, rules):
        """
        Recursively apply the rules to the result of a produced
        command string
        """
        if n == 0:
            return axiom
        else:
            return self.evolve(n-1, self.produce_command(axiom, rules), rules)


    def parse_command(self, state, cmd, forward_func = None):
        """
        Parse a single command/character in the state
        Supported commands: F (forward), B (forward), + (left), - (right),
            [ (push state), ] (pop state)
        """
        s = None
        if cmd == "F" or cmd == "B":
            if forward_func == None:
                s = self.forward(state)
            else:
                s = forward_func(state)
        elif cmd == "+":
            s = self.left(state)
        elif cmd == "-":
            s = self.right(state)
        elif cmd == "[":
            s = self.push(state)
        elif cmd == "]":
            s = self.pop(state)
        else:
            s = state
        return s


    def parse(self, state, commands, forward_func = None):
        """
        Parse the whole string of commands in the state

        @func an optional function that takes the state and a command,
            handles the command and return the resulting state.
        """
        self.verts = []
        new_state = state
        for command in commands:
            new_state = self.parse_command(new_state, command, forward_func)
        #print("verts: " + str(self.verts))
        return new_state


    def left(self, state):
        """
        Turn left d degrees.
        """
        return {"x":state.get("x"),
                "y":state.get("y"),
                "a":(state.get("a") - state.get("d")),
                "d":(state.get("d", math.radians(90))),
                "s":state.get("s", 10)}


    def right(self, state):
        """
        Turn right d degrees
        """
        return {"x":state.get("x"),
                "y":state.get("y"),
                "a":(state.get("a") + state.get("d")),
                "d":(state.get("d", math.radians(90))),
                "s":state.get("s", 10)}


    def forward(self, state):
        """
        Move forward s pixels.
        """
        d = state.get("d", math.radians(90))
        s = state.get("s", 10)
        a = state.get("a")
        x = (state.get("x") + (s * math.cos(a)))
        y = (state.get("y") + (s * math.sin(a)))
        #line(state.get("x"), state.get("y"), x, y)
        self.verts.append(state.get("x"))
        self.verts.append(state.get("y"))
        self.verts.append(x)
        self.verts.append(y)
        
        return {"x":x,
                "y":y,
                "a":a,
                "s":s,
                "d":d}


    def pop(self, state):
        """
        Pop a state from the stack
        """
        return self.stack.pop()


    def push(self, state):
        """
        Push the state onto the stack
        """
        self.stack.append(state)
        return state

