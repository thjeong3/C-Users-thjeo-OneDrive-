from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import mean_squared_error
import pandas as pd

# 초기 데이터 생성
data = {
    '체중': [70, 60, 80, 82, 50, 65, 72, 80,54,51,78,90,68,60,63],
    '신장': [175, 160, 180, 190, 155, 165, 178, 182,164,162,175,188,171,169,173],
    '나이': [25, 30, 22, 40, 55, 18, 25, 43,33,47,23,35,31,22,56],
    '성별': ['남성', '여성', '남성', '남성', '여성', '여성', '남성', '남성','여성','여성','남성','남성','남성','여성','남성'],
    '운동 횟수': [2, 1, 4, 4, 1, 4, 3, 1,1,1,2,2,1,2,1], #0~4
    '다이어트 목표': [0, 0, 2, 1, 2, 2, 0, 2,0,0,1,2,2,2,2],
    '음주 빈도' : [0, 0, 500, 750, 500, 0, 350, 1200,1300,263,800,740,827,350,350],
    '운동 강도' : [4, 1, 4, 4, 2, 3, 4, 4, 2, 1, 3, 4, 2, 1, 1], #0~4
    '권장 칼로리': []
}
# 성별 컬럼 인코딩 (문자형 데이터를 숫자형으로 변환)
label_encoder = LabelEncoder()
data['성별'] = label_encoder.fit_transform(data['성별'])  # '남성' -> 1, '여성' -> 0


# 권장 칼로리 계산 함수
def calculate_recommended_calories(weight, height, age, gender, exercise_frequency,drink_volume, goal, exercise_strength ):
    # 기초 대사량 계산 (Harris-Benedict 방정식 사용)
    if gender == 1:  # 남성
        bmr = 66 + (13.75 * weight) + (5 * height) - (6.75 * age)
    else:  # 여성
        bmr = 655 + (9.56 * weight) + (1.85 * height) - (4.68 * age)
        
    # 근육 증진이 목표인 경우, bmr에 1.2배 적용
    if goal == 1:  # 근육 증진
        bmr *= 1.2

    # 운동 빈도에 따른 활동 지수
    if exercise_frequency >= 5:
        activity_multiplier = 1.725
    elif exercise_frequency >= 3:
        activity_multiplier = 1.55
    elif exercise_frequency >= 1:
        activity_multiplier = 1.375
    else:
        activity_multiplier = 1.2

    # 다이어트 목표에 따른 추가 조정
    if goal == 0:  # 체중 감량
        calorie_adjustment = -500
    elif goal == 1:  # 근육 증진
        calorie_adjustment = 400
    else:  # 현상 유지
        calorie_adjustment = 0
        

    # 최종 권장 칼로리 계산
    recommended_calories = bmr * activity_multiplier + calorie_adjustment
    
    #나이에 따른 칼로리 계산
    if age <=24:
        recommended_calories += 200
    elif age >=41:
        recommended_calories -= 200
        
     #음주에 따른 칼로리 조정
    if drink_volume > 1.0:  # 주당 1000ml 이상의 음주
        recommended_calories -= 70  # 권장 칼로리 70 감소
    elif drink_volume > 0.5:  # 주당 500~1000ml 사이의 음주
        recommended_calories -= 30  # 권장 칼로리 30 감소
        
    # 운동 빈도가 낮은 경우 타이트한 식단 조정
    if exercise_strength <= 1:
        recommended_calories -= 100
    elif exercise_strength == 4:
        recommended_calories +=400
        
    if recommended_calories < 1400:
        recommended_calories = 1400
    
    return recommended_calories / 1000.0

def convert_drink_volume_to_liters(drink_volume):
    return drink_volume / 1000.0

# 초기 권장 칼로리 값 계산 후 데이터에 추가
for i in range(len(data['체중'])):
    weight = data['체중'][i]
    height = data['신장'][i]
    age = data['나이'][i]
    gender = data['성별'][i]
    exercise_frequency = data['운동 횟수'][i]
    goal = data['다이어트 목표'][i]
    drink_volume = data['음주 빈도'][i]
    exercise_strength = data['운동 강도'][i]
    data['권장 칼로리'].append(calculate_recommended_calories(weight, height, age, gender, exercise_frequency, goal,drink_volume,exercise_strength))
    

#특징 스케일러
global scaler
scaler = StandardScaler()
#모델 학습
def train_model(data, iterations=5):
    df = pd.DataFrame(data)
    
    for i in range(iterations):
        #특징과 목표 설정
        features = df[['체중', '신장', '나이', '성별', '운동 횟수', '다이어트 목표','음주 빈도','운동 강도']]
        target = df['권장 칼로리']

        #데이터 분할
        features_train, features_test, target_train, target_test = train_test_split(features, target, test_size=0.2, random_state=42)

        #특성 스케일링
        features_train_scaled = scaler.fit_transform(features_train)
        features_test_scaled = scaler.transform(features_test)

        #모델 학습-선형 회귀 모델
        model = LinearRegression()
        model.fit(features_train_scaled, target_train)

        #예측 및 평가
        target_pred = model.predict(features_test_scaled)
        mse = mean_squared_error(target_test, target_pred)
        print(f"Iteration {i+1}: Mean Squared Error: {mse:.4f}")

        #새로운 데이터 추가-체중,신장,나이,성별,운동 횟수, 다이어트 목표, 음주 빈도, 운동 강도
        new_user = pd.DataFrame([
            [75, 182, 28, 1, 4, 1,0/1000,4],
            [60, 170, 35, 0, 2, 0,500/1000,3],
            [90, 185, 45, 1, 3, 2,1250/1000,3],
            [52, 164, 27, 1, 3, 2,350/1000,2],
            [60, 172, 17, 1, 3, 1,0/1000,3]
        ], columns=['체중', '신장', '나이', '성별', '운동 횟수', '다이어트 목표','음주 빈도','운동 강도'])

        #새로 추가할 데이터의 권장 칼로리 예측
        new_user_scaled = scaler.transform(new_user)
        predicted_calories = model.predict(new_user_scaled)

        #예측된 칼로리 값을 데이터프레임에 추가
        new_user['권장 칼로리'] = predicted_calories

        #기존 데이터프레임에 새 데이터 추가
        df = pd.concat([df, new_user], ignore_index=True)
    
    return model

# 모델 학습 및 반복 학습 결과 출력
model = train_model(data, iterations=10)

# 칼로리 예측 함수
def predict_calories(user_data):
    # user_data는 딕셔너리 형태로 가정합니다.
    weight = user_data.get('체중', 0)
    height = user_data.get('신장', 0)
    age = user_data.get('나이', 0)
    gender = 1 if user_data.get('성별', '남성') == '남성' else 0
    exercise_frequency = user_data.get('운동 횟수', 0)
    goal = user_data.get('다이어트 목표', 0)
    drink_volume = user_data.get('음주 빈도',0)
    exercise_strength = user_data.get('운동 강도',0)
    
    drink_volume_l = convert_drink_volume_to_liters(drink_volume)
    # 예측을 위해 데이터프레임으로 변환
    new_user_df = pd.DataFrame([[weight, height, age, gender, exercise_frequency,goal,drink_volume_l,exercise_strength]], 
                               columns=['체중', '신장', '나이', '성별', '운동 횟수', '다이어트 목표','음주 빈도','운동 강도'])

    # 데이터 스케일링
    new_user_scaled = scaler.transform(new_user_df)

    # 모델을 사용하여 예측
    predicted_calories = model.predict(new_user_scaled)
    
    
    return predicted_calories[0]