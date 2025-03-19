import data_store
import random
import exercise_db

exercise_db = exercise_db.exercise_db

user_data = data_store.user_data

def recommend_exercises(user_data, exercise_db):
    # 운동 횟수와 강도 가져오기
    exercise_count = user_data.get("운동 횟수",3)
    exercise_intensity = user_data.get("운동 강도","낮음")
    
    recommended_exercises = []

    for _ in range(exercise_count):
        # 운동 강도에 따른 가중치 설정
        weights = []
        for name, details in exercise_db.items():
            if details['intensity'] == exercise_intensity:
                weights.append(3)  # 높은 가중치
            elif exercise_intensity == "낮음" and details['intensity'] == "중간":
                weights.append(1)  # 낮은 가중치
            elif exercise_intensity == "중간" and details['intensity'] == "높음":
                weights.append(1)  # 낮은 가중치
            else:
                weights.append(0)  # 제외할 운동

        # 운동을 무작위로 선택
        selected_exercise = random.choices(list(exercise_db.keys()), weights=weights, k=1)[0]
        recommended_exercises.append(selected_exercise)

    return recommended_exercises