import random
from GUI import Extendedpanel
import data_store


print("수집된 사용자 데이터:")
for key, value in data_store.user_data.items():
    print(f"{key}: {value}")

food_db = {
    "쌀밥 200g": {
        "carbs": 36,
        "protein": 4,
        "fat": 0.5,
        "vigun": ["채식"],  # 채식주의 가능 여부 ('채식', '비건' 등 구분)
        "stress": ["효과낮음"],  # 스트레스 완화 효과 ('효과낮음', '효과높음' 등 구분)
        "water": 60,  # 수분 함량(% 기준)
        "quantity" : 200, #음식 양(g)
        "allergy": [],  # 알레르기 정보 (쌀밥은 알레르기가 없음)
        "tags":["아침"]
    },
    "소고기 안심 200g": {
        "carbs": 0,
        "protein": 25,
        "fat": 15,
        "vigun": ["비채식"],  # 비채식주의자만 가능
        "stress": ["효과높음"],  # 스트레스 완화 효과
        "water": 50,
        "quantity" : 200,
        "allergy": ["소고기"],
        "tags":[]# 소고기에 대한 알레르기 정보
    },
    "브로콜리 100g": {
        "carbs": 7,
        "protein": 3,
        "fat": 0.4,
        "vigun": ["비건"],  # 비건 포함 모든 채식주의 가능
        "stress": ["효과보통"],  # 스트레스 완화 효과가 보통
        "water": 90,
        "quantity" : 100,
        "allergy": [] ,
        "tags":["아침"]
    },
     "닭가슴살 150g": {
        "carbs": 0,
        "protein": 23,  # 단백질(g)
        "fat": 2,       # 지방(g)
        "vigun": ["비채식"],
        "stress": ["효과 높음"],
        "water": 70,
        "quantity" : 150,
        "allergy": [],
        "tags":["아침"]

    },
     "스파게티 150g":{
         "carbs":60,
         "protein":12,
         "fat": 14,
         "vigun": ["비채식"],
         "stress": ["효과 낮음"],
         "water": 30,
         "quantity": 150,
         "allergy" : ["밀", "우유", "쇠고기"],
         "tags":[]
     },
     "닭가슴살 샐러드 200g":{
         "carbs":10,
         "protein":25,
         "fat": 7,
         "vigun": ["비채식"],
         "stress": ["효과 중간"],
         "water": 60,
         "quantity": 200,
         "allergy" : ["닭고기"],
         "tags":["아침"]
     },
     "계란말이":{
         "carbs":2,
         "protein":10,
         "fat": 7,
         "vigun": ["비채식"],
         "stress": ["효과 중간"],
         "water": 40,
         "quantity": 100,
         "allergy" : ["알류"],
         "tags":[]
     },
     "아몬드":{
         "carbs":0,
         "protein":24,
         "fat": 1,
         "vigun": ["비건"],
         "stress": ["효과 낮음"],
         "water": 5,
         "quantity": 30,
         "allergy" : ["땅콩"],
         "tags":[]
     },
     "바나나":{
         "carbs":23,
         "protein":0.3,
         "fat": 0.2,
         "vigun": ["비건"],
         "stress": ["효과 높음"],
         "water": 74,
         "quantity": 100,
         "allergy" : [],
         "tags":[]
     },
     "사과":{
         "carbs":14,
         "protein":0.3,
         "fat": 0.2,
         "vigun": ["비건"],
         "stress": ["효과 보통"],
         "water": 86,
         "quantity": 100,
         "allergy" : [],
         "tags":[]
     }, 
     "두부 스테이크": {
        "carbs": 10,
        "protein": 15,
        "fat": 8,
        "vigun": ["채식"],
        "stress": ["효과 중간"],
        "water": 70,
        "quantity": 120,
        "allergy": ["대두"],
        "tags":[]
    },
    "연어 구이": {
        "carbs": 0,
        "protein": 25,
        "fat": 14,
        "vigun": ["비채식"],
        "stress": ["효과 높음"],
        "water": 55,
        "quantity": 150,
        "allergy": ["고등어"],
        "tags":[]
    },
    "그린 스무디": {
        "carbs": 25,
        "protein": 2,
        "fat": 1,
        "vigun": ["채식"],
        "stress": ["효과 높음"],
        "water": 90,
        "quantity": 300,
        "allergy": [],
        "tags":[]
    },
    "소고기 스테이크": {
        "carbs": 0,
        "protein": 30,
        "fat": 20,
        "vigun": ["비채식"],
        "stress": ["효과 높음"],
        "water": 50,
        "quantity": 200,
        "allergy": ["쇠고기"],
        "tags":[]
    },
    "카레라이스": {
        "carbs": 50,
        "protein": 10,
        "fat": 8,
        "vigun": ["비채식"],
        "stress": ["효과 중간"],
        "water": 65,
        "quantity": 200,
        "allergy": ["쇠고기"],
        "tags":[]
    },
    "계란 프라이": {
        "carbs": 1,
        "protein": 7,
        "fat": 6,
        "vigun": ["비채식"],
        "stress": ["효과 낮음"],
        "water": 75,
        "quantity": 50,
        "allergy": ["계란"],
        "tags":["아침"]
    },
    "오트밀 죽": {
        "carbs": 40,
        "protein": 5,
        "fat": 2,
        "vigun": ["채식"],
        "stress": ["효과 중간"],
        "water": 85,
        "quantity": 200,
        "allergy": ["밀"],
        "tags":["아침"]
    },
    "돼지고기 김치찌개": {
        "carbs": 10,
        "protein": 18,
        "fat": 12,
        "vigun": ["비채식"],
        "stress": ["효과 중간"],
        "water": 70,
        "quantity": 250,
        "allergy": ["돼지고기"],
        "tags":[]
    },
    "해물 파전": {
        "carbs": 30,
        "protein": 15,
        "fat": 10,
        "vigun": ["비채식"],
        "stress": ["효과 중간"],
        "water": 55,
        "quantity": 200,
        "allergy": ["밀", "새우", "오징어"],
        "tags":[]
    },
    "닭가슴살 구이": {
        "carbs": 0,
        "protein": 30,
        "fat": 3,
        "vigun": ["비채식"],
        "stress": ["효과 중간"],
        "water": 50,
        "quantity": 100,
        "allergy": ["닭고기"],
        "tags":[]
    },
    "바나나 스무디": {
        "carbs": 30,
        "protein": 4,
        "fat": 2,
        "vigun": ["채식"],
        "stress": ["효과 높음"],
        "water": 85,
        "quantity": 300,
        "allergy": ["우유"],
        "tags":[]
    },
    "토마토 스프": {
        "carbs": 15,
        "protein": 3,
        "fat": 5,
        "vigun": ["채식"],
        "stress": ["효과 중간"],
        "water": 90,
        "quantity": 200,
        "allergy": ["토마토"],
        "tags":["아침"]
    },
    "고등어 구이": {
        "carbs": 0,
        "protein": 22,
        "fat": 18,
        "vigun": ["비채식"],
        "stress": ["효과 높음"],
        "water": 50,
        "quantity": 150,
        "allergy": ["고등어"],
        "tags":[]
    },
    "비트 샐러드": {
        "carbs": 15,
        "protein": 2,
        "fat": 8,
        "vigun": ["채식"],
        "stress": ["효과 낮음"],
        "water": 88,
        "quantity": 150,
        "allergy": [],
        "tags":["아침"]
    },
    "연두부 샐러드": {
        "carbs": 4,
        "protein": 8,
        "fat": 4,
        "vigun": ["채식"],
        "stress": ["효과 중간"],
        "water": 85,
        "quantity": 150,
        "allergy": ["대두"],
        "tags":["아침"]
    },
    "초밥": {
        "carbs": 45,
        "protein": 12,
        "fat": 5,
        "vigun": ["비채식"],
        "stress": ["효과 중간"],
        "water": 70,
        "quantity": 200,
        "allergy": ["밀", "생선"],
        "tags":[]
    }
}



 # wx.App 객체 생성

def calculate_calories(food):
    carbs = food.get("carbs", 0)
    protein = food.get("protein", 0)
    fat = food.get("fat", 0)
    return (carbs * 4) + (protein * 4) + (fat * 9)

# 음식 데이터베이스에 칼로리 계산 추가
for food_name, food_info in food_db.items():
    food_info["calories"] = calculate_calories(food_info)


# 추천 식단 함수 정의
def get_recommended_meals(user_data):
    # 예측된 칼로리를 기반으로 식사별 칼로리 비율 계산
    predicted_calories = user_data.get('칼로리')

    if predicted_calories is not None:
        # 사용자가 선택한 식사 횟수에 따라 칼로리 비율 설정
        meal_plan = user_data.get("식사 횟수", "3끼")
        
        if meal_plan == "3끼":
            calories_morning = predicted_calories * 0.3
            calories_noon = predicted_calories * 0.4
            calories_dinner = predicted_calories * 0.3
        elif meal_plan == "2끼":
            calories_morning = predicted_calories * 0.4
            calories_dinner = predicted_calories * 0.6
        else:
            # 식사 횟수가 잘못된 경우에 대한 예외 처리
            print("사람은 일반적으로 2~3끼의 식사를 합니다. 먼저 식단을 추천받기 전에, 하루에 2~3끼만 먹는 습관을 들이세요.")
            return []

        # 아침 메뉴 추천
        breakfast_meals = recommend_meals(food_db, calories_morning,user_data, tag="아침")
        # 점심 또는 저녁 메뉴 추천
        if meal_plan == "3끼":
            lunch_meals = recommend_meals(food_db, calories_noon,user_data, tag="점심")
            dinner_meals = recommend_meals(food_db, calories_dinner,user_data, tag="저녁")
            return breakfast_meals + lunch_meals + dinner_meals
        else:
            dinner_meals = recommend_meals(food_db, calories_dinner,user_data, tag="저녁")
            return breakfast_meals + dinner_meals
    else:
        print("예측된 칼로리를 불러올 수 없습니다.")
        return []

# 식단 추천 함수
def recommend_meals(food_db, calorie_limit,user_data, tag=None):
    recommended_foods = []
    food_db_copy = food_db.copy()
    current_total_calories = 0
    current_total_water = 0

    if user_data.get("성별") == "남성":
        recommended_water_intake = 3.7 * 1000  #mL 단위로 변환
    else:
        recommended_water_intake = 2.7 * 1000 

    # 사용자 수분 섭취량 가져오기
    user_water_intake = user_data.get("물 섭취량", "1L 미만")
    if user_water_intake == "1L 미만":
        user_water_intake_ml = 500  #평균값
    elif user_water_intake == "1~2L":
        user_water_intake_ml = 1500
    elif user_water_intake == "2~3L":
        user_water_intake_ml = 2500
    else:
        user_water_intake_ml = 3000

    #식단에서 필요한 추가 수분량 계산
    remaining_water_intake = recommended_water_intake - user_water_intake_ml
    
    #알레르기 정보 받아오기
    meal_allergy = user_data.get("알레르기", []) if user_data else []
    
    #스트레스 여부 받아오기
    stress_level = user_data.get("스트레스 여부")
    if stress_level == "스트레스를 거의 받지 않음":
        stress_weight = 0
    elif stress_level == "약간 스트레스를 받음":
        stress_weight = 1
    elif stress_level == "자주 스트레스를 받음":
        stress_weight = 2
    elif stress_level == "항상 스트레스를 받음":
        stress_weight = 3
    #"스트레스를 거의 받지 않음", "약간 스트레스를 받음", "자주 스트레스를 받음","항상 스트레스를 받음"
    
    for _ in range(3):
        weights = []
        for name, details in food_db_copy.items():
            base_weight = 1

            #태그에 따른 기본 가중치 설정 (식사 시간에 맞는 태그에 가중치 추가)
            if tag and tag in details.get("tags", []):
                base_weight += 2

            #스트레스 수준에 따라 스트레스 효과가 있는 음식 가중치 추가
            if stress_level != "스트레스를 거의 받지 않음":
                if "효과높음" in details.get("stress", []):
                    base_weight += stress_weight  #스트레스가 높을수록 더 높은 가중치를 부여
                elif "효과보통" in details.get("stress", []):
                    base_weight += stress_weight // 2  #스트레스가 중간일 경우 약간의 가중치를 부여

            weights.append(base_weight)

        
        while True: #반복적으로 메뉴를 무작위로 선택하되 칼로리 제한을 넘지 않도록 함
            # 무작위로 음식 선택 (가중치 기반)
            selected_food_name = random.choices(list(food_db_copy.keys()), weights=weights, k=1)[0]
            selected_food_details = food_db_copy[selected_food_name]

            # 선택한 음식의 칼로리와 수분 함량 가져오기
            selected_food_calories = selected_food_details.get("calories", 0)
            selected_food_water = selected_food_details.get("water", 0)  # 수분 함량 (mL)
            quantity = selected_food_details.get("quantity", 0)  # 음식의 총 무게 (g)

            # 음식 알레르기
            food_allergies = selected_food_details.get("allergy", [])
            has_allergy = any(allergen in meal_allergy for allergen in food_allergies)

            # 수분 양 계산
            selected_food_water_final = quantity * (selected_food_water / 100)

            # 칼로리, 알레르기 및 수분 제한을 넘지 않으면 추천 리스트에 추가
            if (current_total_calories + selected_food_calories <= calorie_limit) and \
               (current_total_water + selected_food_water_final <= remaining_water_intake) and \
               not has_allergy:
                recommended_foods.append((selected_food_name, selected_food_details))
                current_total_calories += selected_food_calories
                current_total_water += selected_food_water_final

                # 선택된 메뉴를 food_db_copy에서 제거
                del food_db_copy[selected_food_name]

                # 다음 메뉴를 선택하러 가기 위해 반복문 종료
                break
            else:
                # 선택된 음식이 칼로리 또는 수분 제한을 초과하거나 알레르기가 있는 경우 다시 선택
                continue
            
    return recommended_foods
            
# 예시로 식단 추천을 호출
if __name__ == "__main__":
    from data_store import user_data
    
    recommended_meals = get_recommended_meals(user_data)
    for meal in recommended_meals:
        print(f"추천 메뉴: {meal[0]}, 칼로리: {meal[1]['calories']} kcal")
       