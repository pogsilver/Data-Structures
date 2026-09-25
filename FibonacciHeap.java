/**
 * FibonacciHeap
 *
 * An implementation of Fibonacci heap over positive integers.
 *
 */

public class FibonacciHeap
{

	public HeapNode min;
	private int linkAmount;
	private int cutsAmount;
	private int nodeAmount;
	private int treeAmount;
	
	/**
	 *
	 * Constructor to initialize an empty heap.
	 * Complexity: O(1) - both worst case and amortized
	 */
	public FibonacciHeap()
	{
		this.min=null;
		this.linkAmount=0;
		this.cutsAmount=0;
		this.nodeAmount=0;
		this.treeAmount=0;
	}

	/**
	 * 
	 * pre: key > 0
	 *
	 * Insert (key,info) into the heap and return the newly generated HeapNode.
	 * Complexity: O(1) - both worst case and amortized
	 */
	public HeapNode insert(int key, String info) 
	{    
		boolean changeMin=false;
		HeapNode newNode = new HeapNode(key,info);
		
		//inserting into an empty heap
		if (this.min==null)
		{
			this.min=newNode;
			this.min.next=newNode;
			this.min.prev=newNode;
		}
		//inserting into a non-empty heap
		else
		{
			if(this.min.key>key) {
				changeMin=true;
			}
			HeapNode temp=this.min.next;
			this.min.next=newNode;
			temp.prev=newNode;
			newNode.next=temp;
			newNode.prev=this.min;
			if (changeMin) {
				this.min=newNode;
			}
		}
		this.treeAmount++;
		this.nodeAmount++;
		return newNode;
	}

	/**
	 * 
	 * Return the minimal HeapNode, null if empty.
	 * Complexity: O(1) - both worst case and amortized
	 */
	public HeapNode findMin()
	{
		return this.min;
	}

	/**
	 * 
	 * Delete the minimal item
	 * Complexity: O(n) - worst case, O(log n) - amortized
	 */
	public void deleteMin()
	{
		//deletion when tree has a single node
		if (this.nodeAmount==1)
		{
			this.min=null;
			this.treeAmount=0;
			this.nodeAmount=0;
			return;
		}
		
		//cutting the children of the deleted node and adding them as separate trees
		HeapNode min = this.min;
		while (min.child !=null)
		{
			this.cut(min.child);
		}
		
		//deleting the node
		min.prev.next=min.next;
		min.next.prev=min.prev;
		HeapNode tempRoot=min.next;
		min.next=null;
		min.prev=null;
		
		//array for successive linking
		int arrSize=this.UpperBound(this.nodeAmount);
		HeapNode[] treeArr = new HeapNode[arrSize];
		HeapNode currNode=tempRoot;
		
		//successive linking without updating root pointers
		do{
			HeapNode nextNode=currNode.next;
			HeapNode tempNode=currNode;
			int index = tempNode.rank;
			
			//successive linking of a single tree to previous trees
			while (treeArr[index]!=null)
			{
				int currKey = tempNode.key;
				int oldKey = treeArr[index].key;
				HeapNode newChild;
				HeapNode oldChild;
				HeapNode parent;
				
				//determining which of the two trees of the same rank has the smaller key and remains a root
				if (currKey<oldKey)
				{
					newChild=treeArr[index];
					oldChild=tempNode.child;
					parent = tempNode;
				}
				else {
					parent = treeArr[index];
					newChild=tempNode;
					oldChild=parent.child;				
				}
				this.linkAmount++;
				
				//update children pointers
				if (oldChild!=null)
				{
					parent.child=newChild;
					newChild.parent=parent;
					newChild.next=oldChild;
					newChild.prev=oldChild.prev;
					newChild.prev.next=newChild;
					newChild.next.prev=newChild; //update oldChild
					parent.rank++;
				}
				else {
					parent.child=newChild;
					newChild.parent=parent;
					newChild.next=newChild;
					newChild.prev=newChild;
					parent.rank++;
				}
				//updating the array for successive linking and iterators
				treeArr[index]=null;
				index++;
				tempNode=parent;
			}
			
			//updating iterators
			currNode=nextNode;
			treeArr[index]=tempNode;
		}while (currNode!=tempRoot);

		
		//updating roots pointers by passing on treeArr at most twice which is O(log n)
		int firstIndex=findNextNonNull(-1,treeArr);
		HeapNode currMin = treeArr[firstIndex];
		int i=firstIndex;
		this.treeAmount=0;
		//passing once on every entry in treeArr (while doing no work on nulls), size of array is O(log n)
		do{	
			int j=this.findNextNonNull(i, treeArr);
			treeArr[i].next=treeArr[j];
			treeArr[j].prev=treeArr[i];
			
			//updating minimum
			if(treeArr[i].key<currMin.key)
			{
				currMin=treeArr[i];
			}
			this.treeAmount++;
			i=j;
		}while(i!=firstIndex);
		this.min=currMin;
		this.nodeAmount--;
		return;

	}

	/**
	 * 
	 * pre: treeArr has a non null value somewhere
	 * 
	 * return first index that is cyclically after i so that treeArr[index]!=null. 
	 * Complexity: O(log n) - worst case
	 */
	public int findNextNonNull(int i, HeapNode[] treeArr)
	{
		int index=i+1;
		//cyclic array
		index=index%treeArr.length;
		//skipping nulls
		while (treeArr[index]==null) {
			index++;
			//cyclic array
			index=index%treeArr.length;
		}
		return index;
	}
	
	/**
	 * 
	 * pre: n>=1
	 * 
	 * bounding from above maximal rank of root in heap of size n. 
	 * Complexity: O(log n) - worst case
	 */
	public int UpperBound(int n)
	{
		int count=1;
		//computes log2 approximation
		while (n>1) {
			n=n/2;
			count++;
		}
		
		//an upper bound for rank of tree in fibonacci heap
		return count*2;
	}
	/**
	 * 
	 * pre: 0<diff<x.key
	 * 
	 * Decrease the key of x by diff and fix the heap. 
	 * Complexity: O(n) - worst case, O(1) - amortized
	 */
	public void decreaseKey(HeapNode x, int diff) 
	{    
		//updating key
		x.key=x.key-diff;
		//checks if heap structure still legal
		if(x.parent!=null)
		{
			HeapNode parent = x.parent;
			if (x.parent.key>x.key)
			{
				this.cut(x);
				//cascading cuts
				while (parent.mark)
				{
					HeapNode currNode = parent;
					parent=currNode.parent;
					this.cut(currNode);
				}
				//marking last parent if needed
				if (parent.parent!=null)
				{
					parent.mark=true;
				}	
			}
		}
		//updating min if needed
		if (this.min.key>x.key)
		{
			this.min=x;
		}
		return;
	}
	
	
	/**
	 * 
	 * pre: x.parent!=null
	 * 
	 * Cuts x from its parent and adds to roots and updates his mark and all relevant pointers. 
	 * Complexity: O(1) - both worst case and amortized
	 */
	public void cut(HeapNode x)
	{
		HeapNode parent = x.parent;
		//parent has one child
		if (x.next==x) {
			parent.child=null;
			parent.rank=0;
			x.parent=null;
			x.prev=null;
			x.next=null;
		}
		//parent has multiple children
		else {
			parent.child=x.next;
			x.next.prev=x.prev;
			x.prev.next=x.next;
			x.prev=null;
			x.next=null;
			parent.rank--;
			x.parent=null;
		}
		//adds x between min and his next as a root
		HeapNode temp=this.min.next;
		this.min.next=x;
		temp.prev=x;
		x.next=temp;
		x.prev=this.min;
		x.mark=false;
		this.cutsAmount++;
		this.treeAmount++;
		return;
	}
	/**
	 * 
	 * Delete the x from the heap.
	 * Complexity: O(n) -  worst case, O(log n) - amortized
	 */
	public void delete(HeapNode x) 
	{    
		//calls delete min if x is the minimum
		if(x==this.min) {
			this.deleteMin();
			return;
		}
		HeapNode parent=x.parent;
		//cuts deleted node from its parent
		if (parent!=null) {
			this.cut(x);
			//cascading cuts
			while (parent.mark)
			{
				HeapNode currNode = parent;
				parent=currNode.parent;
				this.cut(currNode);
			}
			//updating last parent mark if needed
			if (parent.parent!=null)
			{
				parent.mark=true;
			}	
		}
		//adding deleted node's children as separate trees
		while (x.child !=null)
		{
			this.cut(x.child);
		}
		
		//deleting the node
		HeapNode prev=x.prev;
		HeapNode next=x.next;
		prev.next=next;
		next.prev=prev;
		x.next=null;
		x.prev=null;
		this.nodeAmount--;
		this.treeAmount--;
		return;
	}


	/**
	 * 
	 * Return the total number of links.
	 * Complexity: O(1) - both worst case and amortized
	 */
	public int totalLinks()
	{
		return this.linkAmount;
	}


	/**
	 * 
	 * Return the total number of cuts.
	 * Complexity: O(1) - both worst case and amortized
	 */
	public int totalCuts()
	{
		return this.cutsAmount;
	}


	/**
	 * 
	 * Meld the heap with heap2
	 * Complexity: O(1) - both worst case and amortized
	 */
	public void meld(FibonacciHeap heap2)
	{
		//updating cuts and links amounts
		this.cutsAmount=this.cutsAmount+heap2.totalCuts();
		this.linkAmount=this.linkAmount+heap2.totalLinks();
		
		//handling one of the heaps being empty
		if(heap2.size()==0) {
			return;
		}
		if (this.size()==0) {
			this.min=heap2.findMin();
			this.treeAmount=heap2.numTrees();
			this.nodeAmount=heap2.size();
			return;
		}
		
		//handling one of heaps having only one tree
		if (heap2.numTrees()==1)
		{
			HeapNode prev=this.min.prev;
			HeapNode min2=heap2.findMin();
			prev.next=min2;
			min2.prev=prev;
			this.min.prev=min2;
			min2.next=this.min;
			if (this.min.key>min2.key)
			{
				this.min=min2;
			}
			this.treeAmount=this.treeAmount+heap2.numTrees();
			this.nodeAmount=this.nodeAmount+heap2.size();
			return;
		}
		if (this.numTrees()==1)
		{
			HeapNode min2=heap2.findMin();
			HeapNode prev2=min2.prev;
			prev2.next=this.min;
			this.min.prev=prev2;
			this.min.next=min2;
			min2.prev=this.min;
			if (this.min.key>min2.key)
			{
				this.min=min2;
			}
			this.treeAmount=this.treeAmount+heap2.numTrees();
			this.nodeAmount=this.nodeAmount+heap2.size();
			return;
		}
		
		//handling rest of the cases
		HeapNode min2 = heap2.findMin();
		HeapNode min = this.min;
		HeapNode prev2 = min2.prev;
		HeapNode prev = min.prev;
		prev.next=min2;
		min2.prev=prev;
		prev2.next=min;
		min.prev=prev2;
		if (this.min.key>min2.key)
		{
			this.min=min2;
		}
		this.treeAmount=this.treeAmount+heap2.numTrees();
		this.nodeAmount=this.nodeAmount+heap2.size();
		return; 		
	}

	/**
	 * 
	 * Return the number of elements in the heap
	 * Complexity: O(1) - both worst case and amortized  
	 */
	public int size()
	{
		return this.nodeAmount; 
	}


	/**
	 * 
	 * Return the number of trees in the heap.
	 * Complexity: O(1) - both worst case and amortized
	 */
	public int numTrees()
	{
		return this.treeAmount;
	}
	
	

	/**
	 * Class implementing a node in a Fibonacci Heap.
	 *  
	 */
	public static class HeapNode{
		public int key;
		public String info;
		public HeapNode child;
		public HeapNode next;
		public HeapNode prev;
		public HeapNode parent;
		public int rank;
		public boolean mark;
		
		public HeapNode(int key, String info) {
			this.key=key;
			this.info=info;
			this.child=null;
			this.next=null;
			this.prev=null;
			this.parent=null;
			this.rank=0;
			this.mark=false;
		}
	}
}
