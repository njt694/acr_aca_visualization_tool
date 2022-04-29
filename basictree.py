"""A Tree class to build the phylogenetic tree in build_phylo.py"""
class Tree:
    def __init__(self, val=None, depth=0, parent=None):
        self.val = val
        self.depth = depth
        self.children = []
        self.parent = parent
        #if parent is not None:
        #    self.all_members = self.parent.all_members[depth].append(self.val)
        #else:
        #    self.all_members = [[self.val],[],[],[],[],[],[]]

    def is_root(self):
        if self.depth == 0 and self.parent is None:
            return True
        return False

    def is_empty(self):
        if self.val is None:
            return True
        return False

    def has_children(self):
        if len(self.children) > 0:
            return True
        return False

    def add_child(self, val):
        child = Tree(val, self.depth+1, self)
        self.children.append(child)
        #self.all_members[self.depth+1].append(val)

    def get_children_values(self):
        vals = []
        for child in self.children:
            vals.append(child.val)
        return vals

    def get_parent_val(self):
        if self.is_root():
            return None
        return self.parent.val

    def search(self, val):
        if self.val == val:
            return self
        else:
            if self.has_children():
                for child in self.children:
                    result = child.search(val)
                    if result is not None:
                        return result
            else:
                result = None
            return result

    def to_string_newick(self):
        newick_string = ""
        stack = []
        if self.has_children():
            stack.append(str(self.val))
            newick_string += '('
            children_strings = []
            for child in self.children:
                children_strings.append(child.to_string_newick())
            for child_string in children_strings:
                newick_string += child_string
                newick_string += ','
            newick_string = newick_string[:-1]
            newick_string += ')' + str(self.val)
        else:
            newick_string += str(self.val)
        if self.is_root():
            return newick_string + ';'
        else:
            return newick_string

"""
    def get_root(self):
        me = self
        parent = self.parent
        while not me.is_root():
            me = self.parent
            parent = me.parent
        return me

    def val_in_tree(self, val, depth=None):
        if depth is not None:
            if val in self.all_members[depth]:
                return True
            else:
                return False
        else:
            flag = False
            for level in self.all_members:
                if val in level:
                    flag = True
            return flag

    def get_val_in_tree(self, val, depth=None):
        if not self.val_in_tree(val):
            print("Error: Value is not in the tree")
            return
        else:
            if depth is not None:

            else:
"""

"""
# main
test = Tree(1)
test.add_child(2)
test.add_child(3)
test.add_child(4)
two = test.children[0]
three = test.children[1]
four = test.children[2]
two.add_child(5)
two.add_child(6)
two.add_child(7)
six = two.children[1]
six.add_child(11)
six.add_child(12)
three.add_child(8)
three.add_child(9)
nine = three.children[1]
nine.add_child(13)
four.add_child(10)
print(test.to_string_newick())

for i in range(1,15):
    res = test.search(i)
    if res is not None:
        print(res.val)
    else:
        print(res)
"""