
# An implementation of AVL Tree


"""A class represnting a node in an AVL tree"""
class AVLNode(object):
	"""Constructor, you are allowed to add more fields. 
	
	@type key: int
	@param key: key of your node
	@type value: string
	@param value: data of your node
	Complexity: O(1)
	"""

	def __init__(self, key=None, value=None, virtual=False):
		self.key = key
		self.value = value
		if virtual:
			self.left = None
			self.right = None
			self.parent = None
			self.height = -1
		else:
			self.left = AVLNode(virtual=True)
			self.right = AVLNode(virtual=True)
			self.left.parent = self #added self.
			self.right.parent = self #added self.
			self.parent = None
			self.height = max(self.left.height,self.right.height) + 1 #added self.
			

	"""returns whether self is not a virtual node 

	@rtype: bool
	@returns: False if self is a virtual node, True otherwise.
	Complexity: O(1)
	"""
	def is_real_node(self):
		return self.height != -1
	
	def update_height(self):
		"""
		updates the node's height according to its children
		Complexity: O(1)
		 """
		self.height = max(self.left.height, self.right.height) + 1


"""
A class implementing an AVL tree.
"""

class AVLTree(object):

	"""
	Constructor
	root(AVLNode): the node at the root of the tree, defaults to virtual
	check_max(boolean): flag wether we need to check and update the tree's max. defaults to True
	Complexity if not check_max: O(1), used while splitting
	Complexity if check_max: O(log k), k the size of the subtree of root.
							When used, k is constant - O(1)  
	"""
	def __init__(self, root=AVLNode(virtual=True),check_max=True):
		self.root = root
		if check_max:
			self.maximal_node = self.find_max()
		else:
			self.maximal_node=self.root
		self.tree_size = 0

	"""searches for a node in the dictionary corresponding to the key (starting at the root)
        
	@type key: int
	@param key: a key to be searched
	@rtype: (AVLNode,int)
	@returns: a tuple (x,e) where x is the node corresponding to key (or None if not found),
	and e is the number of edges on the path between the starting node and ending node+1.
	Complexity: O(log n)
	"""
	def search(self, key):

		node, path_length=self.find(key)

		if node.is_real_node():
			return node, path_length
		return None, path_length

	def find(self,key):
		"""inner function to separate between searches for the purpose of searching
		and searches for the purpose of inserting

		Args:
			key (int): key to be found
		
		Returns:
			tuple(AVLNode, int): pointer to the found node if found and path length

		Complexity: O(log n)
		"""
		return self.search_subtree(self.root, key)

	def search_subtree(self,node, key):
		"""searches a subtree of the AVLtree

		Args:
			node (AVLNode): root of the subtree from which we search the given key
			key: the key of the node we wish to find

		Returns:
			tuple (AVLNode, int): the node with the given key and the length of the path to it from node
								defaults to virtual node where the key would have been if it was in the AVLTree, -1

		Complexity: O(log k), where k is the size of the subtree which its root is node, WC: O(log n)
		"""

		curr_node = node
		path_length = 1
		while curr_node.is_real_node():
			if curr_node.key == key:
				return curr_node, path_length
			if curr_node.key < key:
				curr_node = curr_node.right
			else:
				curr_node = curr_node.left
			path_length += 1

		return curr_node, path_length - 1


	"""searches for a node in the dictionary corresponding to the key, starting at the max
        
	@type key: int
	@param key: a key to be searched
	@rtype: (AVLNode,int)
	@returns: a tuple (x,e) where x is the node corresponding to key (or None if not found),
	and e is the number of edges on the path between the starting node and ending node+1.

	Complexity: O(log k), where k is the size of the minimal subtree containing both the maximun
						  and node, assuming the node exists, WC: O(log n)
	"""
	def finger_search(self, key):

		node, path_length = self.finger_find(key)
		if node.is_real_node():
			return node, path_length
		return None, path_length

	def finger_find(self,key):
		"""inner function to separate between searches for the purpose of searching
		and searches for the purpose of inserting
		Args:
			key (int): key to be found

		Returns:
			tuple(AVLNode, int): pointer to the found node if found and path length

		Complexity: O(log k), where k is the size of the minimal subtree containing both the maximun
						  and node, assuming the node exists, WC: O(log n)
		"""
		curr_node = self.maximal_node
		path_length = 0
		while curr_node.parent and key < curr_node.parent.key:
			curr_node = curr_node.parent
			path_length += 1
		node, search_length = self.search_subtree(curr_node,key)
		return node, path_length+search_length
	
	def right_rotate(self,node):
		"""takes an AVL node and rotates it right in the following way:
			node                         left
			/       					/      
			left   C   =>  				A       node
			/                               	/       
			A	rotated_subtree       rotated_subtree   C
		Args:
			node (AVLNode): the tree's node we wish to rotate around with updated heights
		Complexity: O(1)
		"""
		parent = node.parent
		left = node.left
		rotated_subtree = left.right
		node.left = rotated_subtree
		left.right = node

		if parent:
			if parent.key < node.key:
				parent.right = left
			else:
				parent.left = left
			left.parent = parent
		else:
			self.root = left
			left.parent = None
		
		node.parent = left
		rotated_subtree.parent = node

		node.update_height()
		left.update_height()


	def left_rotate(self,node):
		"""takes an AVL node and rotates it right in the following way:
			right                         node
			/       					/      
			node   C      <= 			A       right
			/                               	/       
			A	rotated_subtree       rotated_subtree   C
		Args:
			node (AVLNode): the tree's node we wish to rotate around with updated heights
		
		Complexity: O(1)
		"""
		parent = node.parent
		right = node.right
		rotated_subtree = right.left
		node.right = rotated_subtree
		right.left = node

		if parent:
			if parent.key < node.key:
				parent.right = right
			else:
				parent.left = right
			right.parent = parent
		else:
			self.root = right
			right.parent = None
		
		node.parent = right
		rotated_subtree.parent = node

		node.update_height()
		right.update_height()

	def double_right_rotate(self,node):
		"""does a double rotation to the right to handle extreme cases
		in insertion and deletion
		Args:
			node (AVLNode): the tree's node we wish to rotate around

		Complexity: O(1)
		"""
		self.left_rotate(node.left)
		self.right_rotate(node)
	
	def double_left_rotate(self,node):
		"""does a double rotation to the left to handle extreme cases
		in insertion and deletion
		Args:
			node (AVLNode): the tree's node we wish to rotate around

		Complexity: O(1)
		"""
		self.right_rotate(node.right)
		self.left_rotate(node)

	

	"""inserts a new node into the dictionary with corresponding key and value (starting at the root)

	@type key: int
	@pre: key currently does not appear in the dictionary
	@param key: key of item that is to be inserted to self
	@type val: string
	@param val: the value of the item
	@rtype: (AVLNode,int,int)
	@returns: a 3-tuple (x,e,h) where x is the new node,
	e is the number of edges on the path between the starting node and new node before rebalancing,
	and h is the number of PROMOTE cases during the AVL rebalancing

	Complexity: O(log n)
	"""
	def insert(self, key, val):
		return self.insert_by_search_func(key, val, self.find) 
		

	def insert_by_search_func(self, key, val, search_func):
		"""
		A function used by both insert and insert finger, that acts based on the search_func in how it finds the place to insert

		Args:
		key(int): the key of the new node we wish to insert
		val (string): the value of new node we wish to insert
		search_func(function): the function by which we insert the new node

		Returns:
		tuple(AVLNode, int, int): the inserted node, number of edges on the path from the start of search to the new node ,number of promotions

		Complexity: O(log n)
		 """
		
		new_node = AVLNode(key=key, value=val)
		# Handling empty tree:
		if not self.root.is_real_node():
			self.root = new_node
			self.tree_size += 1
			self.maximal_node=new_node
			return self.root, 0, 0 

		# finding the virtual node at insertion place according to the given search_func:
		node, path_length = search_func(key)
		parent = node.parent
		new_node.parent = parent
		
		if new_node.key < parent.key:
			parent.left = new_node
		else:
			parent.right = new_node

		# loop of counting promotions and balancing accordingly
		promotion_counter = 0
		flag = False
		curr_node=parent
		while curr_node and not flag:
			next_node = curr_node.parent
			action, flag = self.find_case_insertion(curr_node)
			action(curr_node)
			curr_node = next_node
			if not flag:
				promotion_counter += 1

		# update the tree fields
		self.tree_size += 1
		if self.maximal_node.key < new_node.key:
			self.maximal_node = new_node
		return new_node, path_length, promotion_counter
		
	"""inserts a new node into the dictionary with corresponding key and value, starting at the max

	@type key: int
	@pre: key currently does not appear in the dictionary
	@param key: key of item that is to be inserted to self
	@type val: string
	@param val: the value of the item
	@rtype: (AVLNode,int,int)
	@returns: a 3-tuple (x,e,h) where x is the new node,
	e is the number of edges on the path between the starting node and new node before rebalancing,
	and h is the number of PROMOTE cases during the AVL rebalancing

	Complexity: O(log n)
	"""
	def finger_insert(self, key, val):
		return self.insert_by_search_func(key, val, self.finger_find)


	def find_successor_two_children(self, node):
		""" finds the successor of a given node assuming it has two children

		Args:
			node (AVLNode): node of which we wish to find its successor 

		Returns:
			AVLNode: the successor of the given node

		Complexity: O(h), where h is the node's height. Worst case: h = log n
		"""
		curr_node = node.right
		while curr_node.left.is_real_node():
			curr_node = curr_node.left
		
		return curr_node

	"""deletes node from the dictionary

	@type node: AVLNode
	@pre: node is a real pointer to a node in self

	Complexity: O(log n)
	"""
	
	def delete(self, node):
		# checking if the given node is the root:
		change_root = False
		if node == self.root:
			change_root = True

		parent = node.parent
		# check if we need to switch the node with its successor:
		if node.left.is_real_node() and node.right.is_real_node():
			successor = self.find_successor_two_children(node)
			# handling the different options for successor placement: 
			if node.right == successor:
				successor.parent = parent
				node.parent = successor

				temp = successor.left
				successor.left = node.left
				node.left = temp
				successor.left.parent = successor

				temp = successor.right
				successor.right = node
				node.right = temp

				node.right.parent = node
				node.left.parent = node

			else:
				successor_parent = successor.parent

				temp = node.right
				node.right = successor.right
				successor.right = temp

				temp = node.left
				node.left = successor.left
				successor.left = temp

				successor.parent = parent
				node.parent = successor_parent

				node.left.parent = node
				node.right.parent = node
				successor.left.parent = successor
				successor.right.parent = successor
				successor_parent.left = node
			
			temp=node.height
			node.height=successor.height
			successor.height=temp
			# if we have changed the root during the switch, updates it. otherwise, the node had a parent whose fields are updated:
			if change_root:
				self.root = successor
			else:
				if parent.key < successor.key:
					parent.right = successor
				else:
					parent.left = successor
		# handling nodes has at most one child:
		if node.right.is_real_node():
			child = node.right
			node.left=AVLNode(virtual=True)
			node.left.parent=node
		else:
			child = node.left
			node.right=AVLNode(virtual=True)
			node.right.parent=node
		
		# deleting the node, and updating the root and various fields as needed:
		parent = node.parent
		child.parent = parent

		if parent:
			if parent.left== node:
				parent.left = child
			else:
				parent.right = child
		else:
			self.root = child
		node = AVLNode(virtual=True)

		# Rebalancing:
		flag = False
		curr_node = parent

		while curr_node and not flag:
			next_node = curr_node.parent
			action, flag = self.find_case_deletion(curr_node)
			action(curr_node)
			curr_node = next_node
		
		# updating tree fields:
		self.tree_size += -1
		self.maximal_node = self.find_max()
	
	def find_max(self):
		"""finds and returns the maximum of the tree. used to update
			the self.maximal_node 

		Returns:
			AVLNode: the maximal key node

		Complexity: O(log n)
		"""
		curr = self.root
		if not curr.is_real_node():
			return curr
		while curr.right.is_real_node():
			curr = curr.right
		return curr

			
	
	def find_case_deletion(self, parent):
		"""finds the case of deletion rebalancing we need to handle

		Args:
			node (AVLNode): The parent of the last updated node

		Returns:
			tuple (function, boolean): the function of action needed to balance the tree, flag variable to notify breaking of rebalancing

		Complexity: O(1)
		"""
		# setting the parameters according to which we rebalance: 
		left_height_dif = parent.height - parent.left.height
		right_height_dif = parent.height - parent.right.height
		height_dif = (left_height_dif, right_height_dif)

		balanced = [(1, 2), (2, 1), (1, 1)]
		demotion = [(2, 2)]
		left = [(3, 1)]
		right = [(1, 3)]
		# handling different left rotation cases:
		if height_dif in left:
			child = parent.right
			left_child_height_dif = child.height - child.left.height
			right_child_height_dif = child.height - child.right.height
			child_height_dif = (left_child_height_dif, right_child_height_dif)

			if child_height_dif == (1, 1):
				return self.left_rotate, True
			if child_height_dif ==(2,1):
				return self.left_rotate, False
			if child_height_dif ==(1,2):
				return self.double_left_rotate, False
		# handling different right rotation cases:
		if height_dif in right:
			child = parent.left
			left_child_height_dif = child.height - child.left.height
			right_child_height_dif = child.height - child.right.height
			child_height_dif = (left_child_height_dif, right_child_height_dif)

			if child_height_dif == (1, 1):
				return self.right_rotate, True
			if child_height_dif ==(1,2):
				return self.right_rotate, False
			if child_height_dif ==(2,1):
				return self.double_right_rotate, False

		# demoting as needed:
		if height_dif in demotion:
			return self.demote, False
		# no balancing needed, so returns an empty function:
		if height_dif in balanced:
			return lambda x:None, True 


	"""joins self with item and another AVLTree

	@type tree2: AVLTree 
	@param tree2: a dictionary to be joined with self
	@type key: int 
	@param key: the key separting self and tree2
	@type val: string
	@param val: the value corresponding to key
	@pre: all keys in self are smaller than key and all keys in tree2 are larger than key,
	or the opposite way

	Complexity: O(max_height - min_height + 1), where max_height is the height of 
	the higher tree and min_tree of the shorter tree, WC: O(log n)
	"""
	def join(self, tree2, key, val):
		node=AVLNode(key=key,value=val)
		self.join_by_node(tree2,node)

	def join_by_node(self,tree2,node):
		"""takes an AVLTree and an AVLNode, and joins them to self
		
		Args:
		tree2 (AVLTree): the tree we join to ourselves
		node (AVLNode): the node we join by to ourselves
		Complexity: O(max_height - min_height + 1), where max_height is the height of 
		the higher tree and min_tree of the shorter tree, WC: O(log n)
		"""
		self.tree_size += tree2.size() + 1
		key=node.key
		# handling joining into a non empty tree:
		if self.root.is_real_node():
			if key<self.root.key:
				r_tree=self
				l_tree=tree2
			else:
				r_tree=tree2
				l_tree=self
		# handling joining a non empty tree into an empty tree:
		elif tree2.root.is_real_node():
			if key<tree2.root.key:
				r_tree=tree2
				l_tree=self
			else:
				r_tree=self
				l_tree=tree2
		# handling joining two empty trees:
		else:
			self.root = node
			self.maximal_node = node
			self.tree_size = 1
			return

		# from now on, r_tree refers to the tree with keys all greater than node's key, and l_tree to the tree with all 
		# lesser keys than node's key:
		r_height=r_tree.root.height
		l_height=l_tree.root.height

		if r_tree.get_root().is_real_node():
			self.maximal_node=r_tree.max_node()
		else:
			self.maximal_node = node

		# Handling cases according to which tree is higher:

		# If the trees have the same height:
		if r_height==l_height:
			node.right=r_tree.root
			node.left=l_tree.root
			self.root=node
			node.left.parent=node
			node.right.parent=node

		# if the left tree is higher:
		if r_height<l_height:
			curr_node=l_tree.root
			while r_height<curr_node.height:
				curr_node=curr_node.right
			node.left=curr_node
			node.right=r_tree.root
			node.parent=curr_node.parent
			node.parent.right=node
			node.left.parent=node
			node.right.parent=node

			self.root=l_tree.get_root()

		# if the right tree is higher:
		if l_height<r_height:
			curr_node=r_tree.root
			while l_height<curr_node.height:
				curr_node=curr_node.left
			node.right=curr_node
			node.left=l_tree.root
			node.parent=curr_node.parent
			node.parent.left=node
			node.right.parent=node
			node.left.parent=node

			self.root=r_tree.get_root()

		# rebalancing:
		node.update_height()
		flag = False
		curr_node=node.parent
		while curr_node and not flag:
			next_node = curr_node.parent
			action, flag = self.find_case_insertion(curr_node)
			action(curr_node)
			curr_node = next_node


	"""splits the dictionary at a given node

	@type node: AVLNode
	@pre: node is in self
	@param node: the node in the dictionary to be used for the split
	@rtype: (AVLTree, AVLTree)
	@returns: a tuple (left, right), where left is an AVLTree representing the keys in the 
	dictionary smaller than node.key, and right is an AVLTree representing the keys in the 
	dictionary larger than node.key.

	Complexity: O(log n)
	"""
	def split(self, node):
		# lists to store the nodes of the final right tree and left tree relative to node's key:
		r_lst=[] 
		l_lst=[]

		# the nodes on the path from node to the root which will be used in the joining of the subtrees:
		r_mid_nodes=[]
		l_mid_nodes=[]

		# updating the pointers related to node's children and adding the children to their corresponding lists:
		right=node.right
		left=node.left
		node.right=AVLNode(virtual=True)
		node.right.parent = node
		node.left=AVLNode(virtual=True)
		node.left.parent=node
		right.parent=None
		left.parent = None
		r_lst.append(AVLTree(root=right,check_max=False))
		l_lst.append(AVLTree(root=left,check_max=False))

		# path to the root and updating the lists declared at the start and pointers of nodes:
		curr_node=node
		while curr_node.parent:
			next_node=curr_node.parent
			if next_node.left==curr_node:
				right=next_node.right
				right.parent=None
				r_lst.append(AVLTree(root=right,check_max=False))
				r_mid_nodes.append(next_node)
			else:
				left=next_node.left		
				left.parent=None
				l_lst.append(AVLTree(root=left,check_max=False))
				l_mid_nodes.append(next_node)
			next_node.right=AVLNode(virtual=True)
			next_node.right.parent=next_node
			next_node.left=AVLNode(virtual=True)
			next_node.left.parent=next_node
			curr_node.parent=None
			curr_node=next_node

		# joining back nodes and subtrees to form the needed trees:
		for i in range(1,len(r_lst)):
			r_lst[0].join_by_node(r_lst[i],r_mid_nodes[i-1])
		for i in range(1,len(l_lst)):
			l_lst[0].join_by_node(l_lst[i],l_mid_nodes[i-1])
		r_tree=r_lst[0]
		l_tree=l_lst[0]
		r_tree.maximal_node=r_tree.find_max() #to deal with check_max=False
		l_tree.maximal_node=l_tree.find_max() #to deal with check_max=False
		return l_tree,r_tree

	
	"""returns an array representing dictionary 

	@rtype: list
	@returns: a sorted list according to key of tuples (key, value) representing the data structure

	Complexity: O(n)
	"""
	def avl_to_array(self):
		return self.rec_avl_to_array(self.root, [])

	def rec_avl_to_array(self, node, lst):
		""" recursive function to go through the tree in order
		Args:
		node (AVLNode): the node we start in order walk from
		lst(list): the list to which we append the nodes in order

		Returns:
		lst (list): updated list of tuples with the node's subtree's nodes

		Complexity: O(k), where k is the size of the subtree of which node is the root, WC: O(n)
		"""
		if not node.is_real_node():
			return lst
		self.rec_avl_to_array(node.left,lst)
		lst.append((node.key,node.value))
		self.rec_avl_to_array(node.right, lst)
		return lst


	"""returns the node with the maximal key in the dictionary

	@rtype: AVLNode
	@returns: the maximal node, None if the dictionary is empty
	Complexity: O(1)
	"""

	def max_node(self):
		if self.root.is_real_node():
			return self.maximal_node
		return None

	"""returns the number of items in dictionary 

	@rtype: int
	@returns: the number of items in dictionary 

	Complexity: O(1)
	"""
	def size(self):
		# won't work properly if tree was split 
		return self.tree_size


	"""returns the root of the tree representing the dictionary

	@rtype: AVLNode
	@returns: the root, None if the dictionary is empty

	Complexity: O(1)
	"""
	def get_root(self):
		if self.root.is_real_node():
			return self.root
		return None


	def find_case_insertion(self,node):
		"""finds the case of insertion rebalancing we need to handle

		Args:
			node (AVLNode): The parent of the last updated node

		Returns:
			tuple (function, boolean): the function of action needed to balance the tree, flag variable to notify breaking of rebalancing

		Complexity: O(1)
		"""

		# setting the parameters according to which we rebalance: 
		left = node.left
		right = node.right
		left_height_dif = node.height - left.height
		right_height_dif = node.height - right.height
		node_dif = (left_height_dif,right_height_dif)

		# different cases
		balanced_height_dif = [(1, 1), (1, 2), (2, 1)]
		promote_dif = [(1, 0), (0, 1)]

		# handling right rotations:
		if node_dif == (0, 2):
			if left.height - left.right.height == 2:
				return self.right_rotate, True
			if left.height - left.left.height == 2:
				return self.double_right_rotate, True
			if left.height-left.left.height==1 and left.height-left.right.height==1:
				return self.right_rotate, False
		# handling left rotations:
		if node_dif == (2, 0):
			if right.height - right.left.height == 2:
				return self.left_rotate, True
			if right.height - right.right.height == 2:
				return self.double_left_rotate, True
			if right.height-right.right.height==1 and right.height-right.left.height==1:
				return self.left_rotate, False
		# no balancing needed, so returns an empty function:
		if node_dif in balanced_height_dif:
			return lambda x: None, True
		# promoting as needed:
		if node_dif in promote_dif:
			return self.promote, False

	
	def promote(self,node):
		"""promotes the given node

		Args:
			node (AVLNode): promotes the given node
		
		Complexity: O(1)
		"""
		node.update_height()

	def demote(self,node):
		"""promotes the given node

		Args:
			node (AVLNode): promotes the given node
		
		Complexity: O(1)
		"""
		node.update_height()










