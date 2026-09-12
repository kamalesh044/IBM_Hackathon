"""
Rule-based AI Chatbot for Learning Intelligence Platform.
Answers student questions about their mastery, struggles, learning path,
mentor sessions, and general concept explanations.
"""

from concept_graph import CONCEPT_GRAPH, CONCEPT_ORDER

# ── Learning resources per concept ────────────────────────────────────────────

RESOURCES = {
    "Arrays/Linked Lists": {
        "visual": [
            {"type": "video", "title": "Arrays & Linked Lists Visualized", "url": "https://www.youtube.com/watch?v=RBSGKlAvoiM", "source": "CS Dojo"},
            {"type": "video", "title": "Linked List Data Structure", "url": "https://www.youtube.com/watch?v=njTh_OwMljA", "source": "HackerRank"},
            {"type": "diagram", "title": "Visual Guide to Arrays vs Linked Lists", "url": "https://visualgo.net/en/list", "source": "VisuAlgo"},
        ],
        "example-first": [
            {"type": "article", "title": "Arrays & Linked Lists with Examples", "url": "https://www.geeksforgeeks.org/data-structures/linked-list/", "source": "GeeksForGeeks"},
            {"type": "video", "title": "Linked List Explained with Code", "url": "https://www.youtube.com/watch?v=WwfhLC16bis", "source": "freeCodeCamp"},
            {"type": "practice", "title": "Array Problems on LeetCode", "url": "https://leetcode.com/tag/array/", "source": "LeetCode"},
        ],
        "practice-first": [
            {"type": "practice", "title": "Linked List Practice Problems", "url": "https://leetcode.com/tag/linked-list/", "source": "LeetCode"},
            {"type": "practice", "title": "Array Drills", "url": "https://www.hackerrank.com/domains/data-structures?filters%5Bsubdomains%5D%5B%5D=arrays", "source": "HackerRank"},
            {"type": "video", "title": "Solve Linked List Problems Fast", "url": "https://www.youtube.com/watch?v=Hj_rA0dhr2I", "source": "NeetCode"},
        ],
    },
    "Recursion": {
        "visual": [
            {"type": "video", "title": "Recursion Visualized Step by Step", "url": "https://www.youtube.com/watch?v=ngCos392W4w", "source": "Computerphile"},
            {"type": "video", "title": "What is Recursion? (Animation)", "url": "https://www.youtube.com/watch?v=mz6tAJMVmfM", "source": "CS50"},
            {"type": "diagram", "title": "Recursion Call Stack Visualizer", "url": "https://visualgo.net/en/recursion", "source": "VisuAlgo"},
        ],
        "example-first": [
            {"type": "video", "title": "Recursion with Worked Examples", "url": "https://www.youtube.com/watch?v=KEEKn7Me-ms", "source": "CS Dojo"},
            {"type": "article", "title": "Recursion — Step by Step with Examples", "url": "https://www.geeksforgeeks.org/recursion/", "source": "GeeksForGeeks"},
            {"type": "practice", "title": "Recursion Problems", "url": "https://leetcode.com/tag/recursion/", "source": "LeetCode"},
        ],
        "practice-first": [
            {"type": "practice", "title": "Recursion Drills (Easy→Hard)", "url": "https://leetcode.com/tag/recursion/", "source": "LeetCode"},
            {"type": "practice", "title": "Recursion Challenges", "url": "https://www.hackerrank.com/domains/fp?filters%5Bsubdomains%5D%5B%5D=recursion", "source": "HackerRank"},
            {"type": "video", "title": "Master Recursion Fast", "url": "https://www.youtube.com/watch?v=IJDJ0kBx2LM", "source": "NeetCode"},
        ],
    },
    "Tree Traversal": {
        "visual": [
            {"type": "video", "title": "Tree Traversals Animated (In/Pre/Post/BFS)", "url": "https://www.youtube.com/watch?v=9RHO6jU--GU", "source": "CS Dojo"},
            {"type": "diagram", "title": "Interactive Binary Tree Traversal", "url": "https://visualgo.net/en/bst", "source": "VisuAlgo"},
            {"type": "video", "title": "BFS vs DFS Visualized", "url": "https://www.youtube.com/watch?v=pcKY4hjDrxk", "source": "Michael Sambol"},
        ],
        "example-first": [
            {"type": "article", "title": "Tree Traversal with Code Examples", "url": "https://www.geeksforgeeks.org/tree-traversals-inorder-preorder-and-postorder/", "source": "GeeksForGeeks"},
            {"type": "video", "title": "DFS & BFS Explained with Examples", "url": "https://www.youtube.com/watch?v=TIbUeeksXcI", "source": "freeCodeCamp"},
            {"type": "practice", "title": "Tree Problems on LeetCode", "url": "https://leetcode.com/tag/tree/", "source": "LeetCode"},
        ],
        "practice-first": [
            {"type": "practice", "title": "Tree Traversal Practice", "url": "https://leetcode.com/tag/depth-first-search/", "source": "LeetCode"},
            {"type": "practice", "title": "BFS Problems", "url": "https://leetcode.com/tag/breadth-first-search/", "source": "LeetCode"},
            {"type": "video", "title": "Nail Tree Questions in Interviews", "url": "https://www.youtube.com/watch?v=fAAZixBzIAI", "source": "NeetCode"},
        ],
    },
    "Binary Search Trees": {
        "visual": [
            {"type": "video", "title": "Binary Search Trees Visualized", "url": "https://www.youtube.com/watch?v=pYT9F8_LFTM", "source": "CS Dojo"},
            {"type": "diagram", "title": "Interactive BST (Insert/Delete/Search)", "url": "https://visualgo.net/en/bst", "source": "VisuAlgo"},
            {"type": "video", "title": "BST Insert & Delete Animated", "url": "https://www.youtube.com/watch?v=wcIRPqTR3Kc", "source": "Michael Sambol"},
        ],
        "example-first": [
            {"type": "article", "title": "BST with Full Code Examples", "url": "https://www.geeksforgeeks.org/binary-search-tree-data-structure/", "source": "GeeksForGeeks"},
            {"type": "video", "title": "BST Insertion, Deletion, Search Explained", "url": "https://www.youtube.com/watch?v=COZK7NATh4k", "source": "Abdul Bari"},
            {"type": "practice", "title": "BST Problems on LeetCode", "url": "https://leetcode.com/tag/binary-search-tree/", "source": "LeetCode"},
        ],
        "practice-first": [
            {"type": "practice", "title": "BST Drills", "url": "https://leetcode.com/tag/binary-search-tree/", "source": "LeetCode"},
            {"type": "practice", "title": "BST Challenges", "url": "https://www.hackerrank.com/domains/data-structures?filters%5Bsubdomains%5D%5B%5D=trees", "source": "HackerRank"},
            {"type": "video", "title": "Solve BST Problems Efficiently", "url": "https://www.youtube.com/watch?v=s6ATEkipzow", "source": "NeetCode"},
        ],
    },
}

# ── Concept explanations ───────────────────────────────────────────────────────

CONCEPT_EXPLAIN = {
    "Arrays/Linked Lists": (
        "Arrays store elements in contiguous memory — fast random access (O(1)) but slow insert/delete. "
        "Linked Lists use nodes with pointers — fast insert/delete (O(1)) but slow access (O(n)). "
        "Key sub-topics: array indexing, traversal, pointer manipulation, two-pointer technique."
    ),
    "Recursion": (
        "Recursion is when a function calls itself to solve a smaller version of the same problem. "
        "Every recursive function needs: (1) a base case that stops the recursion, and "
        "(2) a recursive case that moves toward the base case. "
        "The call stack tracks each function call. Watch out for infinite loops — always define your base case first!"
    ),
    "Tree Traversal": (
        "Tree traversal means visiting every node in a tree in a specific order. "
        "In-order (Left→Root→Right) gives sorted output for BSTs. "
        "Pre-order (Root→Left→Right) is used for copying trees. "
        "Post-order (Left→Right→Root) is used for deletion. "
        "BFS uses a queue to visit level by level. DFS uses recursion or a stack to go deep first."
    ),
    "Binary Search Trees": (
        "A BST is a binary tree where every left child is smaller than its parent, "
        "and every right child is larger. This property makes search, insert, and delete O(log n) on average. "
        "Key operations: insert (always at a leaf), search (go left if smaller, right if larger), "
        "delete (3 cases: leaf, one child, two children). Unbalanced trees degrade to O(n)."
    ),
}

# ── Chatbot intent matching ────────────────────────────────────────────────────

def _match_concept(text: str) -> str | None:
    text = text.lower()
    if "array" in text or "linked list" in text or "linked" in text:
        return "Arrays/Linked Lists"
    if "recursion" in text or "recursive" in text or "base case" in text:
        return "Recursion"
    if "tree traversal" in text or "traversal" in text or "bfs" in text or "dfs" in text or "inorder" in text or "preorder" in text:
        return "Tree Traversal"
    if "binary search tree" in text or "bst" in text or "insertion" in text or "deletion" in text:
        return "Binary Search Trees"
    return None


def chat(message: str, student: dict | None) -> dict:
    """
    Process a chat message and return a response + optional resources.
    student: full student dict from db (or None if no student selected).
    """
    msg = message.lower().strip()
    name = student["name"].split()[0] if student else "there"
    style = student.get("learning_style", "visual-first") if student else "visual-first"
    mastery = student.get("mastery_scores", {}) if student else {}

    # ── Greetings ──
    if any(w in msg for w in ["hello", "hi", "hey", "start", "help"]):
        return {
            "reply": (
                f"👋 Hi {name}! I'm your AI learning assistant. I can help you with:\n\n"
                "• **What am I struggling with?**\n"
                "• **Explain Recursion / Arrays / Trees / BST**\n"
                "• **What should I study next?**\n"
                "• **Show me videos for Recursion**\n"
                "• **What is my risk level?**\n"
                "• **Why do I keep failing on base case?**\n\n"
                "Ask me anything! 🎓"
            ),
            "resources": [],
        }

    # ── Show resources / videos ──
    if any(w in msg for w in ["video", "resource", "show me", "watch", "visuali", "diagram", "learn", "how to learn", "material"]):
        concept = _match_concept(msg)
        if not concept:
            # Pick their weakest concept
            if mastery:
                concept = min(mastery, key=lambda c: mastery.get(c, 100))
            else:
                concept = "Recursion"
        resources = RESOURCES.get(concept, {}).get(style, RESOURCES[concept]["visual"])
        return {
            "reply": (
                f"📚 Here are **{style}** learning resources for **{concept}**:\n\n"
                f"These are matched to your learning style. Click any link to open it!"
            ),
            "resources": resources,
            "concept": concept,
        }

    # ── Concept explanation ──
    if any(w in msg for w in ["explain", "what is", "what are", "tell me about", "how does", "understand", "confused"]):
        concept = _match_concept(msg)
        if concept:
            explanation = CONCEPT_EXPLAIN[concept]
            resources = RESOURCES[concept].get(style, RESOURCES[concept]["visual"])[:2]
            return {
                "reply": f"📖 **{concept}**\n\n{explanation}",
                "resources": resources,
                "concept": concept,
            }

    # ── Struggle / weakness ──
    if any(w in msg for w in ["struggle", "weak", "fail", "bad at", "problem", "issue", "error", "wrong", "stuck"]):
        if student:
            weak = [(c, s) for c, s in mastery.items() if s < 60]
            weak.sort(key=lambda x: x[1])
            if weak:
                worst = weak[0]
                concept = worst[0]
                score = worst[1]
                resources = RESOURCES.get(concept, {}).get(style, [])[:2]
                attempts_data = [a for a in student.get("attempt_history", []) if a.get("concept") == concept]
                error_tags = []
                if attempts_data:
                    for a in attempts_data:
                        error_tags.extend(a.get("error_tags", []))
                error_str = ", ".join(set(error_tags)) if error_tags else "general understanding"
                return {
                    "reply": (
                        f"📊 Your biggest struggle is **{concept}** (mastery: {score}%).\n\n"
                        f"Recurring problem areas: **{error_str}**.\n\n"
                        f"I've picked resources matched to your **{style}** style to help you fix this! 👇"
                    ),
                    "resources": resources,
                    "concept": concept,
                }
        return {
            "reply": "Select a student first so I can analyse your specific struggles! 👆",
            "resources": [],
        }

    # ── What to study next ──
    if any(w in msg for w in ["next", "study next", "what should i", "what to do", "recommend", "suggestion", "plan"]):
        if student:
            next_concept = None
            for c in CONCEPT_ORDER:
                if mastery.get(c, 0) < 80:
                    prereqs = CONCEPT_GRAPH[c]["prerequisites"]
                    if all(mastery.get(p, 0) >= 60 for p in prereqs):
                        next_concept = c
                        break
            if next_concept:
                resources = RESOURCES.get(next_concept, {}).get(style, [])[:2]
                return {
                    "reply": (
                        f"🎯 You should study **{next_concept}** next!\n\n"
                        f"Your current mastery is **{mastery.get(next_concept, 0)}%** — "
                        f"aim for 80%+ to unlock the next topic.\n\n"
                        f"I've picked **{style}** resources for you 👇"
                    ),
                    "resources": resources,
                    "concept": next_concept,
                }
            return {
                "reply": "🎉 Amazing! You've mastered all concepts (≥80% mastery). Keep practicing to stay sharp!",
                "resources": [],
            }
        return {
            "reply": "Select a student first so I can give you a personalised recommendation! 👆",
            "resources": [],
        }

    # ── Risk level ──
    if any(w in msg for w in ["risk", "danger", "at risk", "prediction", "how am i doing", "performance"]):
        if student:
            scores = list(mastery.values())
            avg = round(sum(scores) / len(scores), 1) if scores else 0
            weak = [c for c, s in mastery.items() if s < 60]
            return {
                "reply": (
                    f"📈 **{name}'s Performance Summary:**\n\n"
                    f"Average mastery: **{avg}%**\n"
                    f"Concepts below 60%: **{', '.join(weak) if weak else 'None — great work!'}**\n\n"
                    f"{'⚠️ You have weak concepts that need attention.' if weak else '✅ You are on track!'}"
                ),
                "resources": [],
            }

    # ── Mentor / intervention ──
    if any(w in msg for w in ["mentor", "intervention", "session", "teacher", "help me", "tutor"]):
        if student:
            weak = [c for c, s in mastery.items() if s < 50]
            if weak:
                return {
                    "reply": (
                        f"🧑‍🏫 Based on your performance, a mentor session would help most with: **{', '.join(weak)}**.\n\n"
                        f"Go to the **Mentor Intervention** section on this page and click "
                        f"**'Request Mentor Intervention Now'** to schedule a session automatically!"
                    ),
                    "resources": [],
                }
            return {
                "reply": "✅ Your mastery levels look good! Mentor intervention is not urgently needed right now.",
                "resources": [],
            }

    # ── Specific error tags ──
    concept = _match_concept(msg)
    if concept:
        explanation = CONCEPT_EXPLAIN[concept]
        resources = RESOURCES[concept].get(style, RESOURCES[concept]["visual"])[:2]
        return {
            "reply": f"📖 **{concept}**\n\n{explanation}",
            "resources": resources,
            "concept": concept,
        }

    # ── Fallback ──
    return {
        "reply": (
            f"🤔 I didn't quite understand that, {name}. Try asking:\n\n"
            "• *\"What am I struggling with?\"*\n"
            "• *\"Show me videos for Recursion\"*\n"
            "• *\"Explain Binary Search Trees\"*\n"
            "• *\"What should I study next?\"*\n"
            "• *\"What is my risk level?\"*"
        ),
        "resources": [],
    }
