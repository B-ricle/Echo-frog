CREATE TABLE problems(
    id SERIAL PRIMARY KEY,
    difficulty_level TEXT NOT NULL CHECK (difficulty_level IN ('easy', 'medium', 'hard')),
    description TEXT NOT NULL,
    sample_input TEXT NOT NULL,
    expected_output TEXT NOT NULL,
    topic TEXT NOT NULL,
    timeout_seconds NUMERIC DEFAULT 5
);

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
 
INSERT INTO problems (difficulty_level, description, sample_input, expected_output, topic)
VALUES 
    ('easy', 'Given a sorted list and a target, return the index of the target or -1 if not found.','nums = [1, 3, 5, 7, 9, 11], target = 7','3','binary_search'),
    ('medium', 'Given a sorted list of integers (which may contain duplicates) and a target value, return the index of the first occurrence of the target. Return -1 if not present','nums = [1, 2, 2, 2, 3, 4, 5], target = 2', '1', 'binary_search'),
    ('hard', 'Given a list of distinct integers originally sorted ascending but rotated at an unknown pivot (e.g., [4,5,6,7,0,1,2]), and a target value, return its index using an O(log n) algorithm. Return -1 if not present.','nums = [4, 5, 6, 7, 0, 1, 2], target = 0','4','binary_search');