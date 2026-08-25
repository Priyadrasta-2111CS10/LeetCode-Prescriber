export const mockOverall = {
  totalAttempts: 612,
  acceptedAttempts: 341,
  uniqueProblemsSolved: 226,
  acceptanceRate: 55.7,
  streakDays: 12,
};

// Matches DifficultyStatsResponse's real shape.
export const mockDifficulty = [
  { difficulty: "Easy", totalAttempts: 151, acceptedAttempts: 118, uniqueProblemsSolved: 118, acceptanceRate: 78.2 },
  { difficulty: "Medium", totalAttempts: 183, acceptedAttempts: 94, uniqueProblemsSolved: 94, acceptanceRate: 51.4 },
  { difficulty: "Hard", totalAttempts: 64, acceptedAttempts: 14, uniqueProblemsSolved: 14, acceptanceRate: 21.9 },
];

export const mockTopics = [
  { topic: "Dynamic Programming", totalAttempts: 41, acceptanceRate: 24.4 },
  { topic: "Backtracking", totalAttempts: 22, acceptanceRate: 31.8 },
  { topic: "Graph", totalAttempts: 33, acceptanceRate: 36.4 },
  { topic: "Bit Manipulation", totalAttempts: 14, acceptanceRate: 42.9 },
  { topic: "Greedy", totalAttempts: 28, acceptanceRate: 46.4 },
  { topic: "Sliding Window", totalAttempts: 19, acceptanceRate: 57.9 },
  { topic: "Binary Search", totalAttempts: 25, acceptanceRate: 64.0 },
  { topic: "Two Pointers", totalAttempts: 31, acceptanceRate: 71.0 },
  { topic: "Hash Table", totalAttempts: 54, acceptanceRate: 79.6 },
  { topic: "Array", totalAttempts: 88, acceptanceRate: 84.1 },
];

export const mockRecentSubmissions = [
  { title: "Course Schedule II", status: "Accepted", topic: "Graph", when: "14m ago" },
  { title: "Word Break", status: "Wrong Answer", topic: "Dynamic Programming", when: "1h ago" },
  { title: "Subsets II", status: "Accepted", topic: "Backtracking", when: "1h ago" },
  { title: "Minimum Window Substring", status: "Time Limit Exceeded", topic: "Sliding Window", when: "3h ago" },
  { title: "Merge Intervals", status: "Accepted", topic: "Array", when: "5h ago" },
];

export const mockPrescription = [
  {
    topic: "Dynamic Programming",
    acceptanceRate: 24.4,
    reason:
      "Lowest acceptance rate with sufficient attempt volume — foundational patterns aren't sticking yet.",
    problems: [
      { title: "House Robber", difficulty: "Medium" },
      { title: "Coin Change", difficulty: "Medium" },
      { title: "Longest Increasing Subsequence", difficulty: "Medium" },
    ],
  },
  {
    topic: "Backtracking",
    acceptanceRate: 31.8,
    reason: "Frequent timeouts suggest pruning logic, not the recursion itself, is the gap.",
    problems: [
      { title: "Combination Sum", difficulty: "Medium" },
      { title: "Palindrome Partitioning", difficulty: "Medium" },
    ],
  },
];
