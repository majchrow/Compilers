class Memory:

    def __init__(self, table):  # memory name
        self.table = table

    def get(self, name):  # gets from memory current value of variable <name>
        return self.table[name]

    def put(self, name, value):  # puts into memory current value of variable <name>
        self.table[name] = value


class MemoryStack:

    def __init__(self):  # initialize memory stack with memory <memory>
        self.memories = [Memory({})]  # global

    def get(self, name):  # gets from memory stack current value of variable <name>
        return self.memories[-1].get(name)

    def put(self, name, value):  # inserts into memory stack variable <name> with value <value>
        self.memories[-1].put(name, value)

    def push(self):  # pushes memory <memory> onto the stack
        current_table = self.memories[-1].table
        self.memories.append(Memory(current_table))

    def pop(self):  # pops the top memory from the stack
        self.memories.pop()
