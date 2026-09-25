# Data Structures

Implementations of advanced data structures featuring an AVL Tree and a Fibonacci Heap. These structures are built to fulfill optimal theoretical time complexities for both worst-case and amortized bounds.

## 1. AVL Tree (Python)
An AVL tree implementation supporting standard operations alongside advanced features like finger searching, joining, and splitting. Each node maintains an integer key and a string value. The implementation ensures optimal asymptotic worst-case bounds dependent on the number of elements, n, in the tree. The codebase targets Python 3.13.

### Complexity & Return Specifications
*   **`search(k)`**: 
    *   Returns a tuple `(x, e)`, where `x` is a pointer to the node (or `None` if not found) and `e` is the length of the search path in edges plus 1.
    *   O(log n) worst-case.
*   **`finger_search(k)`**: 
    *   Returns a tuple `(x, e)` identical in structure to standard search, but begins searching from the maximum node.
    *   O(log n) worst-case.
*   **`insert(k, v)`**: 
    *   Returns a tuple `(x, e, promote)` where `x` points to the new node, `e` is the number of edges on the insertion path, and `promote` is the number of height changes required during balancing.
    *   O(log n) worst-case.
*   **`finger_insert(k, v)`**: 
    *   Returns a tuple `(x, e, promote)` identical in structure to standard insert, but begins from the maximum node.
    *   O(log n) worst-case.
*   **`delete(x)`**: 
    *   Deletes the given node `x` from the tree; does not return a value.
    *   O(log n) worst-case.
*   **`join(t, k, v)`**: 
    *   Joins the current tree with another tree `t` and a separating key `k`; does not return a value.
    *   O(log n) worst-case.
*   **`split(x)`**: 
    *   Returns a tuple `(t1, t2)` where `t1` contains keys smaller than `x` and `t2` contains keys larger than `x`.
    *   O(log n) worst-case.
*   **`avl_to_array()`**: 
    *   Returns a sorted array representing the dictionary's elements, where each element is a `(key, value)` tuple.
    *   O(n) worst-case.
*   **`max_node()`**: 
    *   Returns a pointer to the node with the maximum key.
    *   O(1) worst-case.
*   **`size()`**: 
    *   Returns the total number of items in the tree.
    *   O(1) worst-case.
*   **`get_root()`**: 
    *   Returns a pointer to the tree's root node.
    *   O(1) worst-case.
 
### Usage
```python
tree = AVLTree()
tree.insert(10, "value")
tree.insert(5, "another value")
node, edges = tree.search(10)
print(tree.avl_to_array())  # [(5, 'another value'), (10, 'value')]
```

## 2. Fibonacci Heap (Java)
A Fibonacci Heap implementation featuring efficiently structured amortized operations. Every node contains a natural number key and a string for information. The logic adheres strictly to asymptotic time bounds in terms of n, evaluating both worst-case and amortized scenarios. The structure is implemented using Java 21.

### Complexity & Return Specifications
*   **`insert(k, info)`**: 
    *   Returns a pointer to the created node.
    *   O(1) amortized / O(1) worst-case.
*   **`findMin()`**: 
    *   Returns the heap element with the minimum key.
    *   O(1) amortized / O(1) worst-case.
*   **`deleteMin()`**: 
    *   Deletes the minimum element from the heap; does not return a value.
    *   O(log n) amortized / O(n) worst-case.
*   **`decreaseKey(x, d)`**: 
    *   Decreases the key of node `x` by `d` and fixes the heap; does not return a value.
    *   O(1) amortized / O(n) worst-case.
*   **`delete(x)`**: 
    *   Deletes node `x` from the structure; does not return a value.
    *   O(log n) amortized / O(n) worst-case.
*   **`totalLinks()`**: 
    *   Returns the total number of tree links (connections between trees of the same rank) performed.
    *   O(1) amortized / O(1) worst-case.
*   **`totalCuts()`**: 
    *   Returns the total number of cuts (disconnecting a node from its parent) performed.
    *   O(1) amortized / O(1) worst-case.
*   **`meld(heap2)`**: 
    *   Melds the current heap with `heap2`; does not return a value.
    *   O(1) amortized / O(1) worst-case.
*   **`size()`**: 
    *   Returns the number of elements in the heap.
    *   O(1) amortized / O(1) worst-case.
*   **`numTrees()`**: 
    *   Returns the number of trees currently in the heap.
    *   O(1) amortized / O(1) worst-case.
### Usage
```java
FibonacciHeap heap = new FibonacciHeap();
FibonacciHeap.HeapNode node = heap.insert(10, "value");
heap.insert(5, "another value");
System.out.println(heap.findMin().key); // 5
```
