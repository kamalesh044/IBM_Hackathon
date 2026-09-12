"""
Concept graph for the DS curriculum slice.
Arrays/Linked Lists → Recursion → Tree Traversal → Binary Search Trees
"""

CONCEPT_GRAPH = {
    "Arrays/Linked Lists": {
        "prerequisites": [],
        "next": ["Recursion"],
        "display_name": "Arrays & Linked Lists",
        "sub_concepts": [
            "array indexing",
            "traversal",
            "linked list nodes",
            "pointer manipulation",
            "two-pointer technique",
        ],
    },
    "Recursion": {
        "prerequisites": ["Arrays/Linked Lists"],
        "next": ["Tree Traversal"],
        "display_name": "Recursion",
        "sub_concepts": [
            "base case",
            "recursive case",
            "call stack",
            "memoization",
            "tail recursion",
        ],
    },
    "Tree Traversal": {
        "prerequisites": ["Recursion"],
        "next": ["Binary Search Trees"],
        "display_name": "Tree Traversal",
        "sub_concepts": [
            "in-order",
            "pre-order",
            "post-order",
            "BFS",
            "DFS",
        ],
    },
    "Binary Search Trees": {
        "prerequisites": ["Tree Traversal"],
        "next": [],
        "display_name": "Binary Search Trees",
        "sub_concepts": [
            "BST property",
            "insertion",
            "deletion",
            "search",
            "balancing basics",
        ],
    },
}

CONCEPT_ORDER = [
    "Arrays/Linked Lists",
    "Recursion",
    "Tree Traversal",
    "Binary Search Trees",
]
