Task 1:
- The sortari function sorts a singly linked list in ascending order without creating new nodes. It places the existing nodes in an array, orders them, and reconnects their next pointers. It returns the new head of the sorted list.

Task 2:
- The get_words function splits a character string into words using the delimiters " .,\n". It stores each word's address in the words array. It uses strtok until all words are extracted or number_of_words is reached.
- The sort function sorts an array of words (char** words) with qsort. It orders words by length first, then lexicographically when lengths are equal. The compare function uses strlen and strcmp.

Task 3:
- The kfib function calculates term n of a generalized k-Fibonacci sequence, in which each term is the sum of the previous k terms. It returns 0 when n is smaller than k and 1 when n equals k. Otherwise, it recursively sums kfib(n - i, k) for i from 1 to k. The result is returned in eax.

Task 4:
- The check_palindrome function checks whether a string is a palindrome by comparing characters from both ends. It returns 1 when all pairs match and 0 otherwise.
- The composite_palindrome function builds word concatenations from a list and checks which are palindromes. It keeps the longest valid palindrome or, for equal lengths, the lexicographically smallest one. It uses check_palindrome, strlen, strcmp, and strdup, and returns a duplicated result string.