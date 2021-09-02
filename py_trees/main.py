import py_trees

if __name__ == '__main__':

    root = py_trees.composites.Selector("Unit found?")
    friend = py_trees.composites.Sequence("Is Friend?")
    not_friend = py_trees.composites.Sequence("Is Not friend?")

    replunish = py_trees.behaviours.Success(name="Replunish")
    attack = py_trees.behaviours.Success(name="Attack")

    move = py_trees.behaviours.Success(name="Move")

    not_friend.add_children([replunish, attack])
    friend.add_children([move])
    root.add_children([friend, not_friend])

    behaviour_tree = py_trees.trees.BehaviourTree(
        root=root
    )
    print(py_trees.display.unicode_tree(root=root))
    behaviour_tree.setup(timeout=15)

    def print_tree(tree):
        print(py_trees.display.unicode_tree(root=tree.root, show_status=True))

    try:
        behaviour_tree.tick(post_tick_handler=print_tree)
    except KeyboardInterrupt:
        behaviour_tree.interrupt()
