class Trunk:
	def __init__(self, prev=None, str=None):
		self.prev = prev
		self.str = str

def showTrunks(p):
	if p is None:
		return
	showTrunks(p.prev)
	print(p.str, end='')


def printTree(root, prev, isLeft):
	if root is None:
		return

	prev_str = '	'
	trunk = Trunk(prev, prev_str)
	printTree(root.right, trunk, True)

	if prev is None:
		trunk.str = '———'
	elif isLeft:
		trunk.str = '.———'
		prev_str = '   |'
	else:
		trunk.str = '`———'
		prev.str = prev_str

	showTrunks(trunk)
	print(' ' + root.star_info.display_name)
	if prev:
		prev.str = prev_str
	trunk.str = '   |'
	printTree(root.left, trunk, False)
    