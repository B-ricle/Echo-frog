from backend.database import get_connection


def feature_computation(student_id):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT topic, AVG(attempt_count) AS avg_attempts
                FROM (SELECT p.topic, a.problem_id, COUNT(*) AS attempt_count
                FROM attempts a 
                JOIN problems p ON a.problem_id = p.id
                WHERE a.student_id = %s
                GROUP BY p.topic, a.problem_id) AS problem_counts
                GROUP BY topic;
                """,
                (student_id,)
            )

            return cursor.fetchall()

def get_all_student_ids():
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT DISTINCT student_id FROM attempts WHERE student_id LIKE 'synthetic_%';")
            return cursor.fetchall()


def build_all_features():
    student_record = get_all_student_ids()
    rows = []
    for (student_id,) in student_record:
        students_features = feature_computation(student_id)
        for topic, avg_attempts in students_features:
            rows.append((student_id, topic, avg_attempts))

    return rows

print(build_all_features())        


