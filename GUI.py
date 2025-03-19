import wx
import webbrowser
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from threading import Thread
from 건강정보뉴스크롤링기능구현 import get_articles
import data_store
from exercise_db import exercise_db
import random


class MyApp(wx.App):
    def OnInit(self):
        frame = MainFrame(None, title="Health Assistant", size=(800, 600))
        frame.SetMaxSize((600, 600))  # 창 크기 고정
        frame.SetMinSize((600, 600))  # 창 크기 고정
        frame.Show()
        #frame.SetScrollbar(wx.VERTICAL,0,6,50)
        return True

class MainFrame(wx.Frame):
    def __init__(self, *args, **kw):
        super(MainFrame, self).__init__(*args, **kw)
        
        self.user_data = {}
        
        self.scroll_panel = wx.ScrolledWindow(self, style=wx.VSCROLL)
        self.scroll_panel.SetScrollRate(5, 5)

        # 페이지 전환을 위한 패널 생성
        self.panel0 = InputPanel(self)#성별
        self.panel1 = ResultPanel1(self)#키와 몸무게, 나이
        self.panel2 = ResultPanel2(self)#일일 활동 수준, 운동 빈도, 수면 시간
        self.panel3 = ResultPanel3(self)#식사 횟수, 음주 빈도, 채식 지향(비건 여부 등)
        self.panel4 = ResultPanel4(self)#다이어트 목표:체중 감량, 근육 증가, 건강 유지
        self.panel5 = ResultPanel5(self)#평소 습관:물 섭취량, 스트레스 수준, 흡연 및 음주 여부
        self.panel6 = ResultPanel6(self)#알레르기 여부
        self.result_comfirm = ResultConfirm(self) #결과 다시 묻기
        self.article_panel = ArticlePanel(self) #기사 표시 패널
        self.extended_panel = Extendedpanel(self) 
        self.mealrecommand_panel = MealRecommendationPanel(self)
        self.exerciserecommand_panel = ExerciseRecommendationPanel(self)
        
        # 초기에는 panel0만 보이게 설정
        self.panel1.Hide()
        self.panel2.Hide()
        self.panel3.Hide()
        self.panel4.Hide()
        self.panel5.Hide()
        self.panel6.Hide()
        self.result_comfirm.Hide()
        self.extended_panel.Hide()
        self.mealrecommand_panel.Hide()
        self.exerciserecommand_panel.Hide()

        # 수직 레이아웃 설정
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.panel0, 1, wx.EXPAND)
        self.sizer.Add(self.panel1, 1, wx.EXPAND)
        self.sizer.Add(self.panel2, 1, wx.EXPAND)
        self.sizer.Add(self.panel3, 1, wx.EXPAND)
        self.sizer.Add(self.panel4, 1, wx.EXPAND)
        self.sizer.Add(self.panel5, 1, wx.EXPAND)
        self.sizer.Add(self.panel6, 1, wx.EXPAND)
        self.sizer.Add(self.result_comfirm, 1, wx.EXPAND)
        self.sizer.Add(self.extended_panel, 1,wx.EXPAND)
        self.sizer.Add(self.article_panel, 1, wx.EXPAND | wx.ALL, 10)
        self.sizer.Add(self.mealrecommand_panel, 1, wx.EXPAND)
        self.sizer.Add(self.exerciserecommand_panel,1, wx.EXPAND)
        self.SetSizer(self.sizer)

    def switch_to_panel1(self):
        """Panel0에서 Panel1로 전환"""
        self.panel0.Hide()
        self.panel1.Show()
        self.Layout()
        
    def switch_to_panel2(self):
        """Panel1에서 Panel2로 전환"""
        self.panel1.Hide()
        self.panel2.Show()
        self.Layout()
        
    def switch_to_panel3(self):
        """Panel2에서 Panel3로 전환"""
        self.panel2.Hide()
        self.panel3.Show()
        self.Layout()
        
    def switch_to_panel4(self):
        """Panel2에서 Panel3로 전환"""
        self.panel3.Hide()
        self.panel4.Show()
        self.Layout()
    
    def switch_to_panel5(self):
        """Panel2에서 Panel3로 전환"""
        self.panel4.Hide()
        self.panel5.Show()
        self.Layout()
        
    def switch_to_panel6(self):
        """Panel2에서 Panel3로 전환"""
        self.panel5.Hide()
        self.panel6.Show()
        self.Layout()
        
    def switch_to_resultcomfirm(self):
        """Panel2에서 Panel3로 전환"""
        self.panel6.Hide()
        self.result_comfirm.update_confirmation(self.user_data)
        self.result_comfirm.Show()
        self.Layout()
    
    def switch_to_extendedpanel(self):
        self.result_comfirm.Hide()
        self.extended_panel.Show()
        self.Layout()
        
    def switch_to_mealrecommandpanel(self):
        self.extended_panel.Hide()
        self.mealrecommand_panel.Show()
        self.article_panel.Hide()
        self.Layout()
    
    def switch_to_exercisepanel(self):
        self.mealrecommand_panel.Hide()
        self.exerciserecommand_panel.Show()
        self.Layout()
        
    def switch_to_firstpanel(self):
        self.exerciserecommand_panel.Hide()
        self.panel0.Show()
        self.article_panel.Show()
        self.Layout()
        
    def on_paint(self, event):
        # 페인트 이벤트 처리기
        dc = wx.PaintDC(self)
        img = self.background_image.ConvertToImage()
        img = img.Scale(self.GetSize().GetWidth(), self.GetSize().GetHeight(), wx.IMAGE_QUALITY_HIGH)
        scaled_bitmap = wx.Bitmap(img)
        dc.DrawBitmap(scaled_bitmap, 0, 0, True)
        
class InputPanel(wx.Panel):
    def __init__(self, parent):
        
        super(InputPanel, self).__init__(parent)
        
        # 폰트 설정
        font = wx.Font(10, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Segoe UI")
        
        # 배경 이미지 설정
        self.background_image = wx.Bitmap("C:/Users/thjeo/OneDrive/바탕 화면/졸프작품/background.jpg", wx.BITMAP_TYPE_JPEG)  # InputPanel용 배경 이미지

        # 배경 이미지를 그리는 이벤트 바인딩
        self.Bind(wx.EVT_PAINT, self.on_paint)
        
        # 성별 입력 버튼
        self.txt1=wx.StaticText(self, label = '당신은 남성인가요, 여성인가요?', pos=(100,20))

        self.rb1 = wx.RadioButton(self,-1,label= '남성',pos=(50,40),name = '성별',style = wx.RB_GROUP)
        self.rb2 = wx.RadioButton(self,-1,label= '여성',pos=(50,60),name = '성별')
        
        # '다음' 버튼
        next_button = wx.Button(self, label="다음", pos=(120, 100))
        next_button.Bind(wx.EVT_BUTTON, self.on_next)
        next_button.SetFont(font)
        
        self.txt1.SetFont(font)
        self.rb1.SetFont(font)
        self.rb2.SetFont(font)

    def on_next(self, event):
        """다음 페이지로 이동"""
        # 부모 프레임의 switch_to_panel2 메서드를 호출하여 패널 전환
        if self.rb1.GetValue():
            self.GetParent().user_data['성별'] = "남성"
        elif self.rb2.GetValue():
            self.GetParent().user_data['성별'] = "여성"
        else:
            self.GetParent().user_data['성별'] = "미정"
        self.GetParent().switch_to_panel1()
        
    def on_paint(self, event):
        # 페인트 이벤트 처리기
        dc = wx.PaintDC(self)
        img = self.background_image.ConvertToImage()
        img = img.Scale(self.GetSize().GetWidth(), self.GetSize().GetHeight(), wx.IMAGE_QUALITY_HIGH)
        scaled_bitmap = wx.Bitmap(img)
        dc.DrawBitmap(scaled_bitmap, 0, 0, True)
        
class ResultPanel1(wx.Panel):
    def __init__(self, parent):
        super(ResultPanel1, self).__init__(parent)
        
        self.background_image = wx.Bitmap("C:/Users/thjeo/OneDrive/바탕 화면/졸프작품/background.jpg", wx.BITMAP_TYPE_JPEG)  # InputPanel용 배경 이미지
        self.Bind(wx.EVT_PAINT, self.on_paint)
        
        #키와 체중
        wx.StaticText(self, label="몸무게 (kg):", pos=(20, 20))
        self.weight_input = wx.TextCtrl(self, pos=(120, 20))

        wx.StaticText(self, label="키 (cm):", pos=(20, 60))
        self.height_input = wx.TextCtrl(self, pos=(120, 60))

        wx.StaticText(self, label="나이  (age):", pos=(20, 100))
        self.age_input = wx.TextCtrl(self, pos=(120, 100))
        
        # '다음' 버튼
        next_button = wx.Button(self, label="Next", pos=(120, 200))
        next_button.Bind(wx.EVT_BUTTON, self.on_next)
    
    def on_paint(self, event):
        # 페인트 이벤트 처리기
        dc = wx.PaintDC(self)
        img = self.background_image.ConvertToImage()
        img = img.Scale(self.GetSize().GetWidth(), self.GetSize().GetHeight(), wx.IMAGE_QUALITY_HIGH)
        scaled_bitmap = wx.Bitmap(img)
        dc.DrawBitmap(scaled_bitmap, 0, 0, True)
        
    # 입력된 값이 숫자인지 확인
    def on_next(self, event):
        weight = self.weight_input.GetValue()
        height = self.height_input.GetValue()
        age = self.age_input.GetValue()
        if weight.isdigit() and height.isdigit() and age.isdigit():
        # 부모 프레임의 switch_to_panel3 메서드를 호출하여 패널 전환
            weight = self.weight_input.GetValue()
            height = self.height_input.GetValue()
            self.GetParent().user_data['체중'] = weight if weight else "미정"
            self.GetParent().user_data['신장'] = height if height else "미정"
            self.GetParent().switch_to_panel2()
        else:
        # 숫자가 아닐 경우 경고 메시지 표시
            dlg = wx.MessageDialog(None, '숫자가 아닙니다.', '숫자로 입력해주세요.', wx.OK | wx.CANCEL)
            dlg.ShowModal()
            dlg.Destroy()
            
#일일 활동 수준, 운동 빈도, 수면 시간
class ResultPanel2(wx.Panel):
    def __init__(self, parent):
        super(ResultPanel2, self).__init__(parent)
        self.background_image = wx.Bitmap("C:/Users/thjeo/OneDrive/바탕 화면/졸프작품/background.jpg", wx.BITMAP_TYPE_JPEG)  # InputPanel용 배경 이미지
        self.Bind(wx.EVT_PAINT, self.on_paint)
        
        self.txt1=wx.StaticText(self, label = '당신은 일주일에 운동을 얼마나 합니까?', pos=(20,20))
        self.exercise_frequency = ["1~2회", "3~4회", "5~6회", "매일"]
        self.rb_exercise_frequency = wx.RadioBox(self, label="", pos=(20, 40), choices=self.exercise_frequency, style=wx.RA_SPECIFY_ROWS)
        
        self.txt2=wx.StaticText(self, label = '당신은 평균적으로 어느 강도로 운동을 합니까?', pos=(20,160))
        self.exercise_intensity = ["가벼운 활동 (산책 등)", "보통 활동 (일상적인 움직임)", "활동적 (가벼운 달리기)", "매우 활동적 (강도 높은 운동이나 육체 노동)"]
        self.rb_exercise_intensity = wx.RadioBox(self, label="", pos=(20, 180), choices=self.exercise_intensity, style=wx.RA_SPECIFY_ROWS)
        
        next_button = wx.Button(self, label="Next", pos=(120, 300))
        next_button.Bind(wx.EVT_BUTTON, self.on_next)
        
    def on_paint(self, event):
        # 페인트 이벤트 처리기
        dc = wx.PaintDC(self)
        img = self.background_image.ConvertToImage()
        img = img.Scale(self.GetSize().GetWidth(), self.GetSize().GetHeight(), wx.IMAGE_QUALITY_HIGH)
        scaled_bitmap = wx.Bitmap(img)
        dc.DrawBitmap(scaled_bitmap, 0, 0, True)
        
    def on_next(self, event):
        exercise_frequency = self.rb_exercise_frequency.GetStringSelection()
        exercise_intensity = self.rb_exercise_intensity.GetStringSelection()
        
        if exercise_frequency == "1~2회":
            exercise_frequency_value = 1
        elif exercise_frequency == "3~4회":
            exercise_frequency_value = 2
        elif exercise_frequency == "5~6회":
            exercise_frequency_value = 3
        elif exercise_frequency == "매일":
            exercise_frequency_value = 4
        else:
            exercise_frequency_value = 0  # 기본값 (선택되지 않았을 때)

    # 운동 강도를 수치로 매핑
        if exercise_intensity == "가벼운 활동 (산책 등)":
            exercise_intensity_value = 1
        elif exercise_intensity == "보통 활동 (일상적인 움직임)":
            exercise_intensity_value = 2
        elif exercise_intensity == "활동적 (가벼운 달리기)":
            exercise_intensity_value = 3
        elif exercise_intensity == "매우 활동적 (강도 높은 운동이나 육체 노동)":
            exercise_intensity_value = 4
        else:
            exercise_intensity_value = 0  # 기본값 (선택되지 않았을 때)
    
        
        # 부모 프레임의 user_data 딕셔너리에 값 저장
        self.GetParent().user_data['운동 횟수'] = exercise_frequency_value
        self.GetParent().user_data['운동 강도'] = exercise_intensity_value
        self.GetParent().switch_to_panel3()
        # 되돌아가기 버튼 (선택 사항)
        #back_button = wx.Button(self, label="Back", pos=(100, 200))
        #back_button.Bind(wx.EVT_BUTTON, self.on_back)

    def on_back(self, event):
        """이전 페이지로 돌아가기"""
        self.GetParent().panel2.Hide()
        self.GetParent().panel0.Show()
        self.GetParent().Layout()   
        
#식사 횟수, 음주 빈도, 채식 지향(비건 여부 등)
class ResultPanel3(wx.Panel):
    def __init__(self, parent):
        super(ResultPanel3, self).__init__(parent)
        self.background_image = wx.Bitmap("C:/Users/thjeo/OneDrive/바탕 화면/졸프작품/background.jpg", wx.BITMAP_TYPE_JPEG)  # InputPanel용 배경 이미지
        self.Bind(wx.EVT_PAINT, self.on_paint)
        
        self.txt1=wx.StaticText(self, label = '당신은 하루에 평균적으로 끼니를 몇 번 먹습니까?', pos=(20,20))
        self.food_frequency = ["1끼 이하", "2끼", "3끼", "4끼 이상"]
        self.rb_food_frequency = wx.RadioBox(self, label="", pos=(20, 40), choices=self.food_frequency, style=wx.RA_SPECIFY_ROWS)
        
        self.txt2=wx.StaticText(self, label = '당신은 일주일에 평균 몇 회 정도의 음주를 합니까?', pos=(20,160))
        self.alcohol_frequency = ["마시지 않음", "500ML 미만", "500ML~1L", "1L 이상"]
        self.rb_alcohol_frequency = wx.RadioBox(self, label="", pos=(20, 180), choices=self.alcohol_frequency, style=wx.RA_SPECIFY_ROWS)
        
        self.txt3=wx.StaticText(self, label = '당신은 채식주의자(비건)입니까?', pos=(20,300))
        self.vigun = ["채식주의자가 아님", "플렉시테리언(상황에 따라 육식 허용)", "세미(살코기를 먹지 않음)", "페스코(살코기와 조류를 먹지 않음)","락토(살코기, 조류, 해산물을 먹지 않음)","락토오보(우유, 유제품만 먹음)","비건(어떠한 동물성 식품도 먹지 않음)"]
        self.rb_vigun = wx.RadioBox(self, label="", pos=(20, 320), choices=self.vigun, style=wx.RA_SPECIFY_ROWS)
        
        next_button = wx.Button(self, label="다음", pos=(120, 500))
        next_button.Bind(wx.EVT_BUTTON, self.on_next)
    
    def on_paint(self, event):
        # 페인트 이벤트 처리기
        dc = wx.PaintDC(self)
        img = self.background_image.ConvertToImage()
        img = img.Scale(self.GetSize().GetWidth(), self.GetSize().GetHeight(), wx.IMAGE_QUALITY_HIGH)
        scaled_bitmap = wx.Bitmap(img)
        dc.DrawBitmap(scaled_bitmap, 0, 0, True)
        
        
    def on_next(self, event):
        food_frequency = self.rb_food_frequency.GetStringSelection()
        alcohol_frequency = self.rb_alcohol_frequency.GetStringSelection()
        vigun = self.rb_vigun.GetStringSelection()
        
        alcohol_mapping = {
        "마시지 않음": 0,
        "500ML 미만": 250,   # 평균적으로 500ml 미만은 250ml로 간주
        "500ML~1L": 750,     # 평균적으로 500ml와 1L 사이는 750ml로 간주
        "1L 이상": 1500      # 1L 이상은 평균적으로 1500ml로 간주
        }
        alcohol_volume_ml = alcohol_mapping.get(alcohol_frequency, 0)
        
        # 부모 프레임의 user_data 딕셔너리에 값 저장
        self.GetParent().user_data['식사 횟수'] = food_frequency if food_frequency else "미정"
        self.GetParent().user_data['음주 빈도'] = alcohol_volume_ml
        self.GetParent().user_data['채식주의 여부'] = vigun if vigun else "미정"
        self.GetParent().switch_to_panel4()
        
#다이어트 목표:체중 감량, 근육 증가, 건강 유지        
class ResultPanel4(wx.Panel):
    def __init__(self, parent):
        super(ResultPanel4, self).__init__(parent)
        self.background_image = wx.Bitmap("C:/Users/thjeo/OneDrive/바탕 화면/졸프작품/background.jpg", wx.BITMAP_TYPE_JPEG)  # InputPanel용 배경 이미지
        self.Bind(wx.EVT_PAINT, self.on_paint)
        
        self.txt1=wx.StaticText(self, label = '당신이 다이어트를 하는 주 목적은 무엇입니까?', pos=(20,20))
        self.exercise_achievement = ["건강 유지", "근육 증가", "체중 감량"]
        self.rb_exercise_achievement = wx.RadioBox(self, label="", pos=(20, 40), choices=self.exercise_achievement, style=wx.RA_SPECIFY_ROWS)
        
        next_button = wx.Button(self, label="다음", pos=(120, 120))
        next_button.Bind(wx.EVT_BUTTON, self.on_next)
        
    def on_paint(self, event):
        # 페인트 이벤트 처리기
        dc = wx.PaintDC(self)
        img = self.background_image.ConvertToImage()
        img = img.Scale(self.GetSize().GetWidth(), self.GetSize().GetHeight(), wx.IMAGE_QUALITY_HIGH)
        scaled_bitmap = wx.Bitmap(img)
        dc.DrawBitmap(scaled_bitmap, 0, 0, True)
        
    def on_next(self, event):
        exercise_achievement = self.rb_exercise_achievement.GetStringSelection()
        self.GetParent().user_data['다이어트 목적'] = exercise_achievement if exercise_achievement else "미정"
        
        self.GetParent().switch_to_panel5()

#평소 습관:물 섭취량, 스트레스 수준, 흡연 여부
class ResultPanel5(wx.Panel):
    def __init__(self, parent):
        super(ResultPanel5, self).__init__(parent)
        self.background_image = wx.Bitmap("C:/Users/thjeo/OneDrive/바탕 화면/졸프작품/background.jpg", wx.BITMAP_TYPE_JPEG)  # InputPanel용 배경 이미지
        self.Bind(wx.EVT_PAINT, self.on_paint)
        
        self.txt1=wx.StaticText(self, label = '당신의 하루 평균 물 섭취량은 어느 정도입니까?', pos=(20,20))
        self.water_total = ["1L 이하", "1~2L", "2~3L","3L 이상"]
        self.rb_water_total = wx.RadioBox(self, label="", pos=(20, 40), choices=self.water_total, style=wx.RA_SPECIFY_ROWS)
        
        self.txt2=wx.StaticText(self, label = '당신은 평소에 어느 정도 스트레스를 받습니까?', pos=(20,160))
        self.stress_total = ["스트레스를 거의 받지 않음", "약간 스트레스를 받음", "자주 스트레스를 받음","항상 스트레스를 받음"]
        self.rb_stress_total = wx.RadioBox(self, label="", pos=(20, 180), choices=self.stress_total, style=wx.RA_SPECIFY_ROWS)
        self.txt2_sub=wx.StaticText(self, label = '이 항목은 매우 주관적입니다. 지난 일주일동안 스트레스를 얼마나 받았는지 되돌아보세요.', pos=(20,290))
        
        self.txt3=wx.StaticText(self, label = '당신은 담배 한 갑(20개피)를 얼마만에 다 소진합니까?', pos=(20,320))
        self.smoke_total = ["비흡연자", "일주일 이상", "5~6일","2~4일","1일 이내"]
        self.rb_smoke_total = wx.RadioBox(self, label="", pos=(20, 340), choices=self.smoke_total, style=wx.RA_SPECIFY_ROWS)
        
        next_button = wx.Button(self, label="다음", pos=(120, 420))
        next_button.Bind(wx.EVT_BUTTON, self.on_next)
        
    def on_paint(self, event):
        # 페인트 이벤트 처리기
        dc = wx.PaintDC(self)
        img = self.background_image.ConvertToImage()
        img = img.Scale(self.GetSize().GetWidth(), self.GetSize().GetHeight(), wx.IMAGE_QUALITY_HIGH)
        scaled_bitmap = wx.Bitmap(img)
        dc.DrawBitmap(scaled_bitmap, 0, 0, True)
        
    def on_next(self, event):
        water_total = self.rb_water_total.GetStringSelection()
        stress_total = self.rb_stress_total.GetStringSelection()
        smoke_total = self.rb_smoke_total.GetStringSelection()
        
        self.GetParent().user_data['물 섭취량'] = water_total if water_total else "미정"
        self.GetParent().user_data['스트레스 여부'] = stress_total if stress_total else "미정"
        self.GetParent().user_data['흡연'] = smoke_total if smoke_total else "미정"
        self.GetParent().switch_to_panel6()
            
#알레르기 여부
class ResultPanel6(wx.Panel):
    def __init__(self, parent):
        super(ResultPanel6, self).__init__(parent)
        self.background_image = wx.Bitmap("C:/Users/thjeo/OneDrive/바탕 화면/졸프작품/background.jpg", wx.BITMAP_TYPE_JPEG)  # InputPanel용 배경 이미지
        self.Bind(wx.EVT_PAINT, self.on_paint)
        
        wx.StaticText(self, label="아래 알레르기가 있다면 선택하세요.", pos=(20, 20))

        # 체크박스 목록
        self.cb_peanut = wx.CheckBox(self, label="땅콩", pos=(20, 50))
        self.cb_milk = wx.CheckBox(self, label="우유", pos=(70, 50))
        self.cb_shellfish = wx.CheckBox(self, label="조개류", pos=(120, 50))
        self.cb_egg = wx.CheckBox(self, label="계란", pos=(170, 50))
        self.cb_wheat = wx.CheckBox(self, label="밀", pos=(220, 50))
        self.cb_pinenut = wx.CheckBox(self, label="잣", pos=(20, 70))
        self.cb_walnut = wx.CheckBox(self, label="호두", pos=(70, 70))
        self.cb_crab = wx.CheckBox(self, label="게", pos=(120, 70))
        self.cb_shirmp = wx.CheckBox(self, label="새우", pos=(170, 70))
        self.cb_squid = wx.CheckBox(self, label="오징어", pos=(220, 70))
        self.cb_mackerel = wx.CheckBox(self, label="고등어", pos=(20, 90))
        self.cb_peach = wx.CheckBox(self, label="복숭아", pos=(70, 90))
        self.cb_tomato = wx.CheckBox(self, label="토마토", pos=(120, 90))
        self.cb_chicken = wx.CheckBox(self, label="닭고기", pos=(170, 90))
        self.cb_pig = wx.CheckBox(self, label="돼지고기", pos=(220, 90))
        self.cb_cow = wx.CheckBox(self, label="쇠고기", pos=(20, 110))
        self.cb_buckwheat = wx.CheckBox(self, label="메밀", pos=(70, 110))
        self.cb_soybeans = wx.CheckBox(self, label="대두", pos=(120, 110))
        self.cb_sulfurousacids = wx.CheckBox(self, label="아황산류", pos=(170, 110))
        
        next_button = wx.Button(self, label="다음", pos=(200, 210))
        next_button.Bind(wx.EVT_BUTTON, self.on_next)
        
    def on_paint(self, event):
        # 페인트 이벤트 처리기
        dc = wx.PaintDC(self)
        img = self.background_image.ConvertToImage()
        img = img.Scale(self.GetSize().GetWidth(), self.GetSize().GetHeight(), wx.IMAGE_QUALITY_HIGH)
        scaled_bitmap = wx.Bitmap(img)
        dc.DrawBitmap(scaled_bitmap, 0, 0, True)

    def on_next(self, event):
        """다음 페이지로 이동"""
        # 체크된 알레르기 정보를 수집
        allergies = []
        if self.cb_peanut.GetValue():
            allergies.append("땅콩")
        if self.cb_milk.GetValue():
            allergies.append("우유")
        if self.cb_shellfish.GetValue():
            allergies.append("조개류")
        if self.cb_egg.GetValue():
            allergies.append("계란")
        if self.cb_wheat.GetValue():
            allergies.append("밀")
        if self.cb_pinenut.GetValue():
            allergies.append("잣")
        if self.cb_walnut.GetValue():
            allergies.append("호두")
        if self.cb_crab.GetValue():
            allergies.append("게")
        if self.cb_shirmp.GetValue():
            allergies.append("새우")
        if self.cb_squid.GetValue():
            allergies.append("오징어")
        if self.cb_mackerel.GetValue():
            allergies.append("고등어")
        if self.cb_peach.GetValue():
            allergies.append("복숭아")
        if self.cb_tomato.GetValue():
            allergies.append("토마토")
        if self.cb_chicken.GetValue():
            allergies.append("닭고기")
        if self.cb_pig.GetValue():
            allergies.append("돼지고기")
        if self.cb_cow.GetValue():
            allergies.append("쇠고기")
        if self.cb_buckwheat.GetValue():
            allergies.append("메밀")
        if self.cb_soybeans.GetValue():
            allergies.append("대두")
        if self.cb_sulfurousacids.GetValue():
            allergies.append("아황산류")
        
        # 부모 프레임의 user_data에 알레르기 정보 저장
        self.GetParent().user_data['알레르기'] = ", ".join(allergies) if allergies else "없음"
        self.GetParent().switch_to_resultcomfirm()

#확인 패널
class ResultConfirm(wx.Panel):
    def __init__(self, parent):
        super(ResultConfirm, self).__init__(parent)
        self.background_image = wx.Bitmap("C:/Users/thjeo/OneDrive/바탕 화면/졸프작품/background.jpg", wx.BITMAP_TYPE_JPEG)  # InputPanel용 배경 이미지
        self.Bind(wx.EVT_PAINT, self.on_paint)
        
        # 확인용 텍스트 레이블
        wx.StaticText(self, label="입력된 정보를 확인하세요.", pos=(20, 20))

        # 입력된 정보를 표시할 멀티라인 텍스트 박스
        self.details_text = wx.TextCtrl(self, pos=(20, 50), size=(300, 120), style=wx.TE_MULTILINE | wx.TE_READONLY)

        # '수정' 버튼 (예: 성별 수정)
        self.modify_gender_button = wx.Button(self, label="성별 수정", pos=(20, 200))
        self.modify_gender_button.Bind(wx.EVT_BUTTON, self.on_modify_gender)

        # '수정' 버튼 (예: 신체 정보 수정)
        self.modify_body_button = wx.Button(self, label="신체 정보 수정", pos=(120, 200))
        self.modify_body_button.Bind(wx.EVT_BUTTON, self.on_modify_body)
        
        # '제출' 버튼
        submit_button = wx.Button(self, label="제출", pos=(220, 200))
        submit_button.Bind(wx.EVT_BUTTON, self.on_submit)

    def update_confirmation(self, user_data):
        """입력된 정보를 업데이트"""
        # 입력된 데이터를 문자열로 요약
        details = (
            f"성별: {user_data.get('성별', '미정')}\n"
            f"체중: {user_data.get('체중', '미정')} kg\n"
            f"신장: {user_data.get('신장', '미정')} cm\n"
            f"운동 횟수: {user_data.get('운동 횟수', '미정')}\n"
            f"운동 강도: {user_data.get('운동 강도', '미정')}\n"
            f"식사 횟수: {user_data.get('식사 횟수', '미정')}\n"
            f"음주 빈도: {user_data.get('음주 빈도', '미정')}\n"
            f"채식주의 여부: {user_data.get('채식주의 여부', '미정')}\n"
            f"물 섭취량: {user_data.get('물 섭취량', '미정')}\n"
            f"스트레스 여부: {user_data.get('스트레스 여부', '미정')}\n"
            f"흡연: {user_data.get('흡연', '미정')}\n"
            f"다이어트 목적: {user_data.get('다이어트 목적', '미정')}\n"
            f"알레르기: {user_data.get('알레르기', '없음')}\n"
        )
        # 멀티라인 텍스트 박스에 표시할 내용 설정
        self.details_text.SetValue(details)

    def on_modify_gender(self, event):
        """성별 수정 페이지로 이동"""
        # 수정할 페이지로 전환하는 메서드 호출
        self.GetParent().switch_to_panel1()  # panel1: 성별 수정 페이지
        
    def on_modify_body(self, event):
        """신체 정보 수정 페이지로 이동"""
        # 수정할 페이지로 전환하는 메서드 호출
        self.GetParent().switch_to_panel2()  # panel2: 신체 정보 수정 페이지

    def on_submit(self, event):
        """제출 후 완료 메시지 표시"""
        wx.MessageBox("정보가 제출되었습니다.", "제출 완료", wx.OK | wx.ICON_INFORMATION)
        self.GetParent().switch_to_extendedpanel()
        
    def on_paint(self, event):
        # 페인트 이벤트 처리기
        dc = wx.PaintDC(self)
        img = self.background_image.ConvertToImage()
        img = img.Scale(self.GetSize().GetWidth(), self.GetSize().GetHeight(), wx.IMAGE_QUALITY_HIGH)
        scaled_bitmap = wx.Bitmap(img)
        dc.DrawBitmap(scaled_bitmap, 0, 0, True)
#권장칼로리계산 패널
class Extendedpanel(wx.Panel):
    def __init__(self, parent):
        super(Extendedpanel, self).__init__(parent)
        self.background_image = wx.Bitmap("C:/Users/thjeo/OneDrive/바탕 화면/졸프작품/background.jpg", wx.BITMAP_TYPE_JPEG)  # InputPanel용 배경 이미지
        self.Bind(wx.EVT_PAINT, self.on_paint)
        
        self.parent = parent  # 부모 클래스 참조

        # predicted_calories를 클래스 속성으로 초기화
        self.predicted_calories = None

        # UI 초기화
        self.init_extended_ui()
        self.next_button = wx.Button(self, label="다음", pos=(40, 270))
        self.next_button.Bind(wx.EVT_BUTTON, self.on_next)
        self.next_button.Hide()
        
    def init_extended_ui(self):
        # 권장 칼로리를 계산할 버튼 추가
        predict_button = wx.Button(self, label="권장 칼로리 계산", pos=(20, 300))
        predict_button.Bind(wx.EVT_BUTTON, self.on_predict)

        # 권장 칼로리 결과를 표시할 텍스트 필드 추가
        self.result_text = wx.StaticText(self, label="", pos=(20, 350))

        # 식사별 칼로리 분배를 표시할 텍스트 필드 추가
        self.meal_distribution_text = wx.TextCtrl(self, pos=(20, 380), size=(300, 100), style=wx.TE_MULTILINE | wx.TE_READONLY)

    def collect_user_data(self):
        # 부모 클래스(MainFrame)로부터 user_data를 가져와 details에 저장
        self.details = self.parent.user_data

    def on_predict(self, event):
        
        # 사용자 데이터를 수집
        self.collect_user_data()
        data_store.user_data = self.details

        # 머신러닝 파일에서 권장 칼로리를 예측하는 함수를 호출
        try:
            from training_model import predict_calories 
            self.predicted_calories = predict_calories(self.details) * 1000
            self.GetParent().user_data['칼로리'] = self.predicted_calories
            
            if self.predicted_calories < 1400:
                self.predicted_calories = 1400

            calories_morning = self.predicted_calories * 0.3
            calories_noon = self.predicted_calories * 0.4
            calories_dinner = self.predicted_calories * 0.3

            meal_distribution = {
                "아침": calories_morning,
                "점심": calories_noon,
                "저녁": calories_dinner
            }

            distribution_details = (
                f"아침 칼로리: {meal_distribution['아침']:.2f} kcal\n"
                f"점심 칼로리: {meal_distribution['점심']:.2f} kcal\n"
                f"저녁 칼로리: {meal_distribution['저녁']:.2f} kcal\n"
            )
            self.meal_distribution_text.SetValue(distribution_details)
            self.meal_distribution = meal_distribution

            self.result_text.SetLabel(f"권장 칼로리: {self.predicted_calories:.2f} kcal")
            self.next_button.Show()
        except ImportError as e:
            wx.MessageBox(f"예측 모듈을 불러올 수 없습니다: {str(e)}", "오류", wx.OK | wx.ICON_ERROR)
        except Exception as e:
            wx.MessageBox(f"예측 중 오류가 발생했습니다: {str(e)}", "오류", wx.OK | wx.ICON_ERROR)
            
    def on_paint(self, event):
        dc = wx.PaintDC(self)
        img = self.background_image.ConvertToImage()
        img = img.Scale(self.GetSize().GetWidth(), self.GetSize().GetHeight(), wx.IMAGE_QUALITY_HIGH)
        scaled_bitmap = wx.Bitmap(img)
        dc.DrawBitmap(scaled_bitmap, 0, 0, True)

    def get_predicted_calories(self):
        return self.predicted_calories
    
    def on_next(self, event):
        self.GetParent().switch_to_mealrecommandpanel()
#식단 추천
class MealRecommendationPanel(wx.Panel):
    def __init__(self, parent):
        super(MealRecommendationPanel, self).__init__(parent)
        self.background_image = wx.Bitmap("C:/Users/thjeo/OneDrive/바탕 화면/졸프작품/background.jpg", wx.BITMAP_TYPE_JPEG)  # InputPanel용 배경 이미지
        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.init_ui()
        
        
    def init_ui(self):
        # 텍스트 레이블 추가
        wx.StaticText(self, label="오늘의 추천 식단", pos=(20, 20))
        
        # 아침, 점심, 저녁 레이블 추가
        wx.StaticText(self, label="아침", pos=(20, 50))
        wx.StaticText(self, label="점심", pos=(20, 160))
        wx.StaticText(self, label="저녁", pos=(20, 270))

        # 아침, 점심, 저녁 식단을 표시할 텍스트 필드 추가
        self.breakfast_text = wx.TextCtrl(self, pos=(70, 50), size=(200, 80), style=wx.TE_MULTILINE | wx.TE_READONLY)
        self.lunch_text = wx.TextCtrl(self, pos=(70, 160), size=(200, 80), style=wx.TE_MULTILINE | wx.TE_READONLY)
        self.dinner_text = wx.TextCtrl(self, pos=(70, 270), size=(200, 80), style=wx.TE_MULTILINE | wx.TE_READONLY)

        # 식단 추천 가져오기 버튼 추가
        recommend_button = wx.Button(self, label="식단 추천 가져오기", pos=(20, 370))
        recommend_button.Bind(wx.EVT_BUTTON, self.on_get_recommendation)

        back_button = wx.Button(self, label="다음", pos=(200, 370))
        back_button.Bind(wx.EVT_BUTTON, self.on_next)

    def on_get_recommendation(self, event):
        # 추천 메뉴 가져오기
        user_data = self.GetParent().user_data

        from predict_diner import get_recommended_meals

        recommended_meals = get_recommended_meals(user_data)  # predict_dinner.py에서 추천된 식단 목록 가져오기

        # 추천된 메뉴를 각 텍스트 필드에 표시 (아침, 점심, 저녁 각각 3개씩)
        breakfast_meals = recommended_meals[:3]
        lunch_meals = recommended_meals[3:6]
        dinner_meals = recommended_meals[6:9]

        breakfast_details = "\n".join([f"{meal[0]}: {meal[1]['calories']} kcal" for meal in breakfast_meals])
        lunch_details = "\n".join([f"{meal[0]}: {meal[1]['calories']} kcal" for meal in lunch_meals])
        dinner_details = "\n".join([f"{meal[0]}: {meal[1]['calories']} kcal" for meal in dinner_meals])

        self.breakfast_text.SetValue(breakfast_details)
        self.lunch_text.SetValue(lunch_details)
        self.dinner_text.SetValue(dinner_details)
        
    def on_paint(self, event):
        dc = wx.PaintDC(self)
        img = self.background_image.ConvertToImage()
        img = img.Scale(self.GetSize().GetWidth(), self.GetSize().GetHeight(), wx.IMAGE_QUALITY_HIGH)
        scaled_bitmap = wx.Bitmap(img)
        dc.DrawBitmap(scaled_bitmap, 0, 0, True)

    def on_next(self, event):
        self.GetParent().switch_to_exercisepanel()
        
#운동 추천
class ExerciseRecommendationPanel(wx.Panel):
    def __init__(self, parent):
        super(ExerciseRecommendationPanel, self).__init__(parent)
        self.parent = parent
        self.user_data = data_store.user_data

        # exercise_db를 외부에서 임포트하여 사용
        self.exercise_db = exercise_db

        self.init_ui()

    def init_ui(self):
        # '운동 추천 받기' 버튼 추가
        recommend_button = wx.Button(self, label="운동 추천 받기", pos=(20, 30))
        recommend_button.Bind(wx.EVT_BUTTON, self.on_get_recommendation)

        back_button = wx.Button(self,label="처음 화면으로",pos=(20,80))
        back_button.Bind(wx.EVT_BUTTON, self.go_back)

        
        # 추천된 운동을 표시할 텍스트 필드 추가
        self.recommendation_texts = []

        # 응원 메시지
        self.cheer_messages = [
            "당신은 할 수 있어요!",
            "오늘도 좋은 하루 보내세요!",
            "작은 노력들이 큰 변화를 만듭니다!",
            "당신은 이미 멋진 일을 하고 있어요!",
            "조금만 더 힘내세요, 성공이 눈앞에 있어요!",
            "포기하지 말고 계속 나아가세요!",
            "당신의 건강은 당신의 미래입니다!",
            "훌륭해요! 계속 이렇게 하세요!"
        ]

        # 랜덤으로 응원 메시지 선택
        random_message = random.choice(self.cheer_messages)

        # 응원 메시지 표시 (위치 조정)
        self.cheer_text = wx.StaticText(self, label=random_message, pos=(20, 10))
        font = wx.Font(14, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        self.cheer_text.SetFont(font)

        self.next_button = wx.Button(self, label="마무리", pos=(120, 400))
        self.next_button.Bind(wx.EVT_BUTTON, self.on_finish)
        self.next_button.Hide()
    def go_back(self, event):
        self.GetParent().switch_to_firstpanel()

    def on_finish(self, event):
        wx.MessageBox("모든 과정이 완료되었습니다. 건강하게 지내세요!", "축하합니다", wx.OK | wx.ICON_INFORMATION)

    def on_get_recommendation(self, event):
        # 운동 추천 기능 실행
        from purpose_exercise import recommend_exercises
        exercise_count = self.user_data.get("운동 횟수", 3)
        
        if exercise_count is None:
            wx.MessageBox("운동 횟수가 설정되지 않았습니다. 먼저 운동 횟수를 입력해주세요.", "오류", wx.OK | wx.ICON_ERROR)
            return

        recommended_exercises = recommend_exercises(self.user_data, self.exercise_db)

        # 기존 추천 텍스트가 있으면 모두 삭제
        for text in self.recommendation_texts:
            text.Destroy()
        self.recommendation_texts = []

        # 운동 횟수에 따라 텍스트 박스 생성
        for i in range(exercise_count):
            exercise_label = f"운동 {i + 1}: {recommended_exercises[i]}"
            recommendation_text = wx.StaticText(self, label=exercise_label, pos=(20, 100 + i * 30))
            self.recommendation_texts.append(recommendation_text)

        # 패널을 업데이트하여 새로 추가된 텍스트를 화면에 표시
        self.Layout()

        # 운동 추천이 완료되면 '다음' 버튼 표시
        self.next_button.Show()
        self.Layout()


class ArticlePanel(wx.Panel):
    def __init__(self, parent):
        super(ArticlePanel, self).__init__(parent)

        # 전체 레이아웃 설정
        main_sizer = wx.BoxSizer(wx.VERTICAL)

        # 스크롤 가능한 패널 생성
        self.scroll_panel = wx.ScrolledWindow(self, style=wx.VSCROLL)
        self.scroll_panel.SetScrollRate(5, 5)

        # 스크롤 패널의 레이아웃 설정
        self.vbox = wx.BoxSizer(wx.VERTICAL)
        self.scroll_panel.SetSizer(self.vbox)

        # 전체 레이아웃에 스크롤 패널 추가
        main_sizer.Add(self.scroll_panel, 1, wx.EXPAND | wx.ALL, 5)
        self.SetSizer(main_sizer)

        self.articles = []
        self.current_index = 0

        
        self.timer = wx.Timer(self)#기사 추가하는 부분
        self.Bind(wx.EVT_TIMER, self.update_article, self.timer)

        self.crawl_thread = Thread(target=self.load_articles)#크롤링 수행
        self.crawl_thread.start()

    def load_articles(self):
        articles = get_articles() #크롤링 함수

        wx.CallAfter(self.on_articles_loaded, articles) #크롤링이 완료되면 기사 패널 업데이트

    def on_articles_loaded(self, articles):
        
        self.articles = articles
        self.timer.Start(100)  #크롤링된 기사 데이터를 업데이트하고 타이머 시작,0.1초마다 기사 업데이트

    def update_article(self, event):
        if self.current_index >= len(self.articles):#기사 리스트가 모두 추가되면 타이머 종료
            self.timer.Stop()
            return

        title, link = self.articles[self.current_index]#현재 기사 가져오기

        link_ctrl = wx.StaticText(self.scroll_panel, label=title, style=wx.ALIGN_LEFT)#링크 스타일로 기사 제목 표시
        link_ctrl.SetForegroundColour("blue")  
        font = link_ctrl.GetFont()
        font.SetUnderlined(True)
        link_ctrl.SetFont(font)

        link_ctrl.Bind(wx.EVT_LEFT_DOWN, lambda event, url=link: self.open_link(url))#클릭 이벤트 바인딩

        
        self.vbox.Add(link_ctrl, 0, wx.ALL, 5)#스크롤 패널의 레이아웃에 기사 추가
        self.scroll_panel.Layout()  #레이아웃 갱신

        
        self.current_index += 1#다음 기사를 위한 인덱스 증가

    def open_link(self, url):
        webbrowser.open(url)  #브라우저에서 링크 열기