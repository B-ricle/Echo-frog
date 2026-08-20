from backend.database import get_connection
from classifier.synthetic_data import GROUND_TRUTH

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

def truth_building():
    built_student_features = build_all_features()
    label = []
    for(student_id, topic, avg_attempts, ) in built_student_features:
        student_label = GROUND_TRUTH[(student_id, topic)]
        label.append((student_id, topic, avg_attempts, student_label))
        
    return label

def build_training_data():
    training_data_truth_value = truth_building()
    # x is avg_attempts
    training_data_x = []
    # y is truth label ex. True/False
    training_data_y = []

    for(student_id, topic, avg_attempts, student_label) in training_data_truth_value:
        training_data_x.append([float(avg_attempts)])
        training_data_y.append(student_label)

    return training_data_x, training_data_y
    
print(build_training_data())


            


