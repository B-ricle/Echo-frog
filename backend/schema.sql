CREATE TABLE problems(
    id SERIAL PRIMARY KEY,
    difficulty_level TEXT NOT NULL CHECK (difficulty_level IN ('easy', 'medium', 'hard')),
    description TEXT NOT NULL,
    sample_input TEXT NOT NULL,
    expected_output TEXT NOT NULL,
    topic TEXT NOT NULL,
    timeout_seconds NUMERIC DEFAULT 5
);

ALTER TABLE problems ADD CONSTRAINT no_dupes UNIQUE (description);

CREATE TABLE attempts(
    id SERIAL PRIMARY KEY,
    student_id TEXT NOT NULL,
    problem_id INTEGER NOT NULL REFERENCES problems(id),
    code TEXT NOT NULL,
    outcome TEXT NOT NULL CHECK (outcome IN ('passed', 'wrong_answer', 'runtime_error', 'timeout')),
    exit_code INTEGER NULL,
    duration NUMERIC NOT NULL, 
    created_at TIMESTAMP DEFAULT NOW() NOT NULL
);
 
INSERT INTO problems (difficulty_level, description, sample_input, expected_output, topic, created_at)
VALUES 
    ('easy', 'Given a sorted list and a target, return the index of the target or -1 if not found.','nums = [1, 3, 5, 7, 9, 11], target = 7','3','binary_search'),
    ('medium', 'Given a sorted list of integers (which may contain duplicates) and a target value, return the index of the first occurrence of the target. Return -1 if not present','nums = [1, 2, 2, 2, 3, 4, 5], target = 2', '1', 'binary_search'),
    ('hard', 'Given a list of distinct integers originally sorted ascending but rotated at an unknown pivot (e.g., [4,5,6,7,0,1,2]), and a target value, return its index using an O(log n) algorithm. Return -1 if not present.','nums = [4, 5, 6, 7, 0, 1, 2], target = 0','4','binary_search'),
    
    ('easy', 'Given a string s, find the first non-repeating character in it and return its 0-based index. If it does not exist, return -1.', 's = "algomaster"', '1', 'hash_map'),
    ('medium', 'Given an array of integers nums and an integer k, return the total number of continuous subarrays whose sum equals k.', 'nums = [1, 1, 1], k = 2', '2', 'hash_map'), 
    ('hard', 'Given a string s and an integer k, return the maximum length of a continuous substring that contains at most k distinct characters. If no such substring exists, return 0.', 's = "eceba", k = 2', '3', 'hash_map' ),

    ('easy','Given a non-negative integer n, return the n-th Fibonacci number using structural recursion. For example, if n = 5, the Fibonacci sequence is 0, 1, 1, 2, 3, 5, so the result is 5.', 'n = 6', '8', 'recursion'),
    ('medium','Given a non-negative integer n, return the sum of its digits using recursion. For example, if n = 1234, the result is 1 + 2 + 3 + 4 = 10.', 'n = 4729', '22', 'recursion'),
    ('hard','Given an integer n representing the number of stairs, return the number of distinct ways to reach the top if you can climb either 1 or 2 steps at a time. Use recursion. For example, if n = 3, there are 3 possible ways: 1+1+1, 1+2, and 2+1.', 'n = 5', '8', 'recursion');

