import random 
from backend.database import get_connection
from datetime import datetime, timedelta
from collections import defaultdict

SYNTHETIC_CODE = "# synthetic code"

PROFILES = {
    "synthetic_student_a":{
        "binary_search": {
            "attempts_range": (1, 2),
            "duration_range": (0.2, 0.5),
            "Failure_outcome": ["wrong_answer"],
        },

        "recursion": {
            "attempts_range": (5,7),
            "duration_range":(1.0, 3.0),
            "Failure_outcome": ["wrong_answer", "wrong_answer", "runtime_error"]
        },

        "hash_map": {
            "attempts_range": (2,3),
            "duration_range": (0.4, 1.0),
            "Failure_outcome":["wrong_answer"]
        }
    },

    "synthetic_student_b": {
        "binary_search": {
            "attempts_range": (2,4),
            "duration_range": (0.2, 0.5 ),
            "Failure_outcome": ["wrong_answer"]
        },
        "recursion": {
            "attempts_range": (1,2),
            "duration_range": (0.2, 0.7),
            "Failure_outcome": ["wrong_answer"]
        },
        "hash_map": {
            "attempts_range": (5,8),
            "duration_range": (1.5, 3.5),
            "Failure_outcome": ["wrong_answer", "wrong_answer" , "runtime_error"]
        },
    },
    "synthetic_student_c": {
        "binary_search":{
            "attempts_range": (3,5),
            "duration_range":(0.5, 2.5),
            "Failure_outcome": ["wrong_answer", "wrong_answer", "wrong_answer"]
        },
        "recursion":{
            "attempts_range": (3,5),
            "duration_range": (0.5, 3.0),
            "Failure_outcome": ["wrong_answer", "wrong_answer", "wrong_answer"]
        },
        "hash_map":{
            "attempts_range": (3,5),
            "duration_range": (0.5, 2.5),
            "Failure_outcome": ["wrong_answer", "wrong_answer", "wrong_answer"]
        }
    },
    "synthetic_student_d": {
            "binary_search":{
                "attempts_range": (1,2),
                "duration_range":(0.2, 0.8),
                "Failure_outcome": ["wrong_answer"]
            },
            "recursion":{
                 "attempts_range": (1,2),
                 "duration_range":(0.2, 0.8),
                 "Failure_outcome": ["wrong_answer"]
            },
            "hash_map":{
                 "attempts_range": (1,2),
                 "duration_range":(0.2, 0.9),
                 "Failure_outcome": ["wrong_answer", "wrong_answer"]
            }
    },
    "synthetic_student_e": {
        "binary_search":{
            "attempts_range": (4,10),
            "duration_range":(1.0, 5.0),
            "Failure_outcome": ["wrong_answer", "runtime_error"]
        },
        "recursion":{
                "attempts_range": (4,12),
                "duration_range":(1.0, 6.0),
                "Failure_outcome": ["wrong_answer", "runtime_error"]
        },
        "hash_map":{
                "attempts_range": (4,10),
                "duration_range":(1.2, 5.0),
                "Failure_outcome": ["wrong_answer", "runtime_error"]
        }
    }

}

def caller() -> dict:
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT id, topic, difficulty_level FROM problems")
            result = cursor.fetchall()

    problems_by_topic = defaultdict(list)

    for problem_id, topic, difficulty in result:
        problems_by_topic[topic].append((problem_id, difficulty))


    return dict(problems_by_topic)

print(caller())

def generate_attempts_for(student_id, topic, problem_id, profile, start_time):

    # total attempts of the range
    low, high = profile["attempts_range"]
    total_attempts = random.randint(low, high)

    duration_low , duration_high = profile["duration_range"]
    
    rows = []
    outcome = None
    exit_code = None

    for i in range(total_attempts):
        attempt_start = start_time + timedelta(minutes=i *5)
        duration = random.uniform(duration_low, duration_high)
        is_last = (i == total_attempts -1)

        if is_last:
            outcome = 'passed' 
            
        else:
            outcome = random.choice(profile["Failure_outcome"])

        if outcome in ('passed', 'wrong_answer'):
            exit_code = 0
        elif outcome == 'runtime_error':
            exit_code = 1
        else:
            exit_code = None
        
        rows.append((exit_code, outcome, duration, attempt_start))

        
        
    
    return rows

def build_all_attempts():
    problems_by_topic = caller()
    start_time = datetime.now() - timedelta(days=30)
    all_rows = []
    for student_id, student_profile in PROFILES.items():
        for topic, profile in student_profile.items():
            for problem_id, difficulty in problems_by_topic[topic]:
                rows= generate_attempts_for(student_id, topic, problem_id, profile, start_time)
                for exit_code, outcome, duration, attempt_start in rows:
                    all_rows.append((student_id, problem_id, SYNTHETIC_CODE, outcome, exit_code, duration, attempt_start))
                start_time += timedelta(days= 1)

    return all_rows

print(build_all_attempts())
print(len(build_all_attempts()))


def insert_all_attempts(rows):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.executemany(
                """
                INSERT INTO attempts(student_id, problem_id, code, outcome, exit_code, duration, created_at)
                VALUES(%s, %s, %s, %s, %s, %s, %s) 
                """,
                rows)

insert_all_attempts(build_all_attempts())


test_profile = {
    "attempts_range": (5,7),
    "duration_range": (0.5, 1.0),
    "Failure_outcome": ["wrong_answer", "runtime_error", "timeout"]
}

print(generate_attempts_for("synthetic_a", "recursion", 7, test_profile, datetime.now() - timedelta(days= 7)))

