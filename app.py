import streamlit as st
import random
from collections import defaultdict

# 한국어 끝말잇기 단어 데이터베이스
class KoreanWordDatabase:
    def __init__(self):
        # 단어 데이터베이스 확장 (단어: [품사, 뜻, 대체어])
        self.words = {
            "사과": ["명사", "과일의 일종 또는 잘못을 뉘우침", ["애플", "과일"]],
            "과일": ["명사", "나무에서 열리는 먹을 수 있는 열매", ["과실", "열매"]],
            "열매": ["명사", "식물의 씨를 싸고 있는 부분", ["과실", "과일"]],
            "매화": ["명사", "봄에 꽃을 피우는 나무", ["매화나무", "매화꽃"]],
            "화가": ["명사", "그림을 그리는 사람", ["그림쟁이", "예술가"]],
            "가수": ["명사", "노래를 부르는 사람", ["싱어", "가창자"]],
            "수박": ["명사", "여름에 먹는 큰 과일", ["참외", "과일"]],
            "박사": ["명사", "최고의 학위를 가진 사람", ["학자", "전문가"]],
            "사자": ["명사", "동물의 일종", ["라이언", "맹수"]],
            "자동차": ["명사", "도로를 달리는 탈것", ["차", "오토모빌"]],
            "차표": ["명사", "차를 탈 때 필요한 표", ["티켓", "승차권"]],
            "표범": ["명사", "동물의 일종", ["레오파드", "맹수"]],
            "범인": ["명사", "범죄를 저지른 사람", ["죄인", "범죄자"]],
            "인간": ["명사", "사람", ["인류", "사람"]],
            "간호사": ["명사", "병원에서 일하는 사람", ["간호사", "의료인"]],
            "사랑": ["명사", "남을 아끼고 귀여워하는 마음", ["애정", "연애"]],
            "랑이": ["명사", "호랑이의 준말", ["호랑이", "맹수"]],
            "이발소": ["명사", "머리를 깎는 곳", ["미용실", "이발관"]],
            "소방차": ["명사", "불을 끄는 차", ["소방차", "구급차"]],
            "차이": ["명사", "다른 점", ["차별점", "다름"]],
            "이음": ["명사", "잇는 것", ["연결", "접속"]],
            "음악": ["명사", "소리를 예술로 표현한 것", ["뮤직", "곡"]],
            "악기": ["명사", "음악을 연주하는 도구", ["악기", "연주도구"]],
            "기차": ["명사", "철도로 달리는 탈것", ["열차", "철도"]],
            "차고": ["명사", "차를 보관하는 곳", ["주차장", "차량보관소"]],
            "고양이": ["명사", "집에서 기르는 동물", ["냥이", "고냥이"]],
            "이불": ["명사", "잘 때 덮는 것", ["담요", "침구"]],
            "불고기": ["명사", "한국 전통 음식", ["구이", "고기요리"]],
            "기린": ["명사", "목이 긴 동물", ["지라프", "동물"]],
            "린스": ["명사", "머리 감을 때 쓰는 것", ["컨디셔너", "헤어린스"]],
            "스키": ["명사", "겨울 스포츠", ["스키", "설상스포츠"]],
            "키위": ["명사", "과일의 일종", ["과일", "키위"]],
            "위성": ["명사", "지구를 도는 천체", ["인공위성", "위성"]],
            "성격": ["명사", "사람의 성질", ["성품", "기질"]],
            "격투": ["명사", "싸우는 것", ["투쟁", "싸움"]],
            "투수": ["명사", "야구에서 공을 던지는 사람", ["피처", "야구선수"]],
            "수영": ["명사", "물에서 하는 운동", ["수영", "헤엄"]],
            "영화": ["명사", "영상으로 만든 이야기", ["무비", "영상물"]],
            "화분": ["명사", "식물을 키우는 그릇", ["화분", "화초"]],
            "분수": ["명사", "물이 뿜어져 나오는 장치", ["분수", "물분수"]],
            "수학": ["명사", "숫자를 다루는 학문", ["수학", "산수"]],
            "학생": ["명사", "학교에 다니는 사람", ["학생", "제자"]],
            "생선": ["명사", "물고기", ["어류", "물고기"]],
            "선물": ["명사", "남에게 주는 것", ["프레젠트", "증정품"]],
            "물고기": ["명사", "물에 사는 동물", ["어류", "생선"]],
            "기적": ["명사", "놀라운 일", ["이적", "불가사의"]],
            "적군": ["명사", "적의 군대", ["적병", "적"]],
            "군인": ["명사", "군대에 속한 사람", ["병사", "군대"]],
            "인형": ["명사", "사람 모양의 장난감", ["도리", "인형"]],
            "형제": ["명사", "형과 동생", ["형제", "형제자매"]],
            "제비": ["명사", "새의 일종", ["제비", "철새"]],
            "비행기": ["명사", "하늘을 나는 탈것", ["에어플레인", "항공기"]],
            "기억": ["명사", "과거의 일을 생각함", ["메모리", "추억"]],
            "억양": ["명사", "말의 높낮이", ["억양", "어조"]],
            "양말": ["명사", "발에 신는 것", ["양말", "스타킹"]],
            "말차": ["명사", "차의 일종", ["말차", "녹차"]],
            "차량": ["명사", "차", ["자동차", "탈것"]],
            "량이": ["명사", "양의 준말", ["양", "동물"]],
            "이유": ["명사", "까닭", ["원인", "동기"]],
            "유리": ["명사", "투명한 재료", ["글라스", "유리"]],
            "리본": ["명사", "장식용 끈", ["리본", "끈"]],
            "본드": ["명사", "붙이는 물질", ["접착제", "풀"]],
            "드럼": ["명사", "악기의 일종", ["드럼", "타악기"]],
            "럼버": ["명사", "나무를 다루는 사람", ["목수", "나무장인"]],
            "버스": ["명사", "여러 사람이 타는 차", ["버스", "공중교통"]],
            "스튜": ["명사", "요리의 일종", ["스튜", "찌개"]],
            "튜브": ["명사", "관 모양의 것", ["튜브", "관"]],
            "브라": ["명사", "속옷의 일종", ["브래지어", "속옷"]],
            "라면": ["명사", "인스턴트 음식", ["라면", "인스턴트"]],
            "면도": ["명사", "털을 깎는 행위", ["면도", "제모"]],
            "도서": ["명사", "책", ["책", "서적"]],
            "서류": ["명사", "문서", ["문서", "서류"]],
            "류리": ["명사", "유리의 다른 표현", ["유리", "글라스"]],
            "이사": ["명사", "집을 옮기는 것", ["이사", "이주"]],
            "사탕": ["명사", "달콤한 음식", ["캔디", "과자"]],
            "탕수": ["명사", "중국 요리의 일종", ["탕수육", "중식"]],
            "수건": ["명사", "몸을 닦는 것", ["타월", "행주"]],
            "건강": ["명사", "몸이 건강한 상태", ["헬스", "건강"]],
            "강아지": ["명사", "개의 새끼", ["강아지", "멍멍이"]],
            "지우개": ["명사", "연필 자국을 지우는 것", ["지우개", "eraser"]],
            "개미": ["명사", "곤충의 일종", ["개미", "곤충"]],
            "미술": ["명사", "그림을 그리는 예술", ["아트", "회화"]],
            "술병": ["명사", "술을 담는 그릇", ["병", "술병"]],
            "병원": ["명사", "병을 치료하는 곳", ["병원", "의원"]],
            "원숭이": ["명사", "동물의 일종", ["원숭이", "몽키"]],
            "이탄": ["명사", "석탄의 일종", ["이탄", "석탄"]],
            "탄산": ["명사", "음료에 들어가는 것", ["탄산", "가스"]],
            "산소": ["명사", "우리가 숨쉬는 기체", ["산소", "oxygen"]],
            "소나무": ["명사", "나무의 일종", ["소나무", "솔"]],
            "무지개": ["명사", "하늘의 색깔띠", ["무지개", "레인보우"]],
            "개나리": ["명사", "꽃의 일종", ["개나리", "꽃"]],
            "리본": ["명사", "장식용 끈", ["리본", "끈"]],
            "본인": ["명사", "자기 자신", ["자신", "본인"]],
            "인사": ["명사", "서로 만나서 하는 예절", ["인사", "예의"]],
            "사다리": ["명사", "오르내리는 도구", ["사닥다리", "계단"]],
            "다리": ["명사", "몸의 일부 또는 건물의 구조물", ["leg", "교량"]],
            "리모컨": ["명사", "원격 조종기", ["리모콘", "조종기"]],
            "컨디션": ["명사", "상태나 조건", ["컨디션", "상태"]],
            "션샤인": ["명사", "햇빛", ["선샤인", "햇빛"]],
            "인공": ["명사", "사람이 만든 것", ["인공", "인조"]],
            "공원": ["명사", "공공 휴식 공간", ["공원", "park"]],
            "원피스": ["명사", "여성 의상의 일종", ["원피스", "드레스"]],
            "스토리": ["명사", "이야기", ["스토리", "이야기"]],
            "리더": ["명사", "지도자", ["리더", "지도자"]],
            "더하기": ["명사", "덧셈", ["더하기", "합산"]],
            "기회": ["명사", "찬스", ["기회", "찬스"]],
            "회의": ["명사", "모임", ["회의", "미팅"]],
            "의사": ["명사", "병원에서 일하는 사람", ["의사", "닥터"]],
            "사진": ["명사", "찰영한 그림", ["사진", "photo"]],
            "진리": ["명사", "참된道理", ["진리", "真理"]],
            "이론": ["명사", "학문적 주장", ["이론", "theory"]],
            "논리": ["명사", "사고의 법칙", ["논리", "로직"]],
            "이상": ["명사", "보통과 다른 상태", ["이상", "비정상"]],
            "상자": ["명사", "물건을 담는 것", ["상자", "박스"]],
            "자석": ["명사", "철을 끄는 물질", ["자석", "마그넷"]],
            "석양": ["명사", "지는 해", ["석양", "일몰"]],
            "양식": ["명사", "서양식 음식", ["양식", "서양식"]],
            "식사": ["명사", "밥 먹는 것", ["식사", "밥"]],
            "사랑": ["명사", "애정", ["사랑", "love"]],
            # "유도" 단어 추가
            "유도": ["명사", "어떤 방향으로 이끎", ["인도", "지도"]],
            "도구": ["명사", "연장", ["도구", "연장"]],
            "구름": ["명사", "하늘의 수증기", ["구름", "cloud"]],
            "음식": ["명사", "먹는 것", ["음식", "food"]],
            "식물": ["명사", "풀과 나무", ["식물", "plant"]],
            "물질": ["명사", "물체를 이루는 것", ["물질", "substance"]],
            "질문": ["명사", "묻는 것", ["질문", "question"]],
            "문제": ["명사", "풀어야 할 것", ["문제", "question"]],
            "제목": ["명사", "글의 이름", ["제목", "title"]],
            "목표": ["명사", "달성하려는 것", ["목표", "goal"]],
            "표정": ["명사", "얼굴 모양", ["표정", "expression"]],
            "정원": ["명사", "마당", ["정원", "garden"]],
            "원인": ["명사", "원흉", ["원인", "cause"]],
            "인과": ["명사", "원인과 결과", ["인과", "causality"]],
            "과자": ["명사", "간식", ["과자", "snack"]],
            "자전거": ["명사", "두 바퀴 탈것", ["자전거", "bicycle"]],
            "거미": ["명사", "절지동물", ["거미", "spider"]],
            "미래": ["명사", "앞으로의 시간", ["미래", "future"]],
            "래킷": ["명사", "라켓의 다른 표현", ["라켓", "racket"]],
            "트리": ["명사", "나무", ["트리", "tree"]],
        }
        
        # 끝말을 시작으로 하는 단어 목록
        self.word_start = defaultdict(list)
        for word in self.words.keys():
            start_char = word[0]
            self.word_start[start_char].append(word)
    
    def is_valid_word(self, word):
        """단어가 사전에 있는지 확인"""
        return word in self.words
    
    def get_word_info(self, word):
        """단어 정보 반환"""
        if word in self.words:
            return self.words[word]
        return None
    
    def get_next_words(self, last_char):
        """마지막 글자로 시작하는 단어 목록 반환"""
        return self.word_start.get(last_char, [])
    
    def get_random_word(self, last_char=None):
        """랜덤 단어 반환"""
        if last_char:
            words = self.get_next_words(last_char)
            return random.choice(words) if words else None
        else:
            return random.choice(list(self.words.keys()))

# 게임 상태 관리
class WordRelayGame:
    def __init__(self):
        self.db = KoreanWordDatabase()
        self.reset_game()
    
    def reset_game(self):
        self.used_words = set()
        self.current_word = None
        self.game_over = False
        self.winner = None
        self.history = []
        self.waiting_for_ai = False
    
    def start_game(self):
        self.reset_game()
        self.current_word = self.db.get_random_word()
        self.used_words.add(self.current_word)
        self.history.append(("AI", self.current_word))
        return self.current_word
    
    def is_valid_next_word(self, word, last_char):
        """다음 단어가 유효한지 확인"""
        if not word or len(word) < 2:
            return False, "2글자 이상의 단어를 입력해주세요."
        
        if word in self.used_words:
            return False, "이미 사용된 단어입니다."
        
        if not self.db.is_valid_word(word):
            return False, "사전에 없는 단어입니다."
        
        if word[0] != last_char:
            return False, f"'{last_char}'(으)로 시작하는 단어를 입력해주세요."
        
        return True, "유효한 단어입니다."
    
    def player_turn(self, word):
        """플레이어의 차례 처리"""
        if self.game_over:
            return False, "게임이 이미 종료되었습니다."
        
        last_char = self.current_word[-1]
        is_valid, message = self.is_valid_next_word(word, last_char)
        
        if not is_valid:
            self.game_over = True
            self.winner = "AI"
            return False, message
        
        # 유효한 단어인 경우
        self.current_word = word
        self.used_words.add(word)
        self.history.append(("플레이어", word))
        
        # 'ㅇ' 받침 체크
        if word[-1] == 'ㅇ':
            self.game_over = True
            self.winner = "AI"
            return True, f"'{word}'! 'ㅇ' 받침으로 끝나는 단어는 사용할 수 없습니다. AI 승리!"
        
        # AI 차례 준비
        self.waiting_for_ai = True
        return True, f"'{word}' - 좋은 단어입니다! AI가 생각 중..."
    
    def ai_turn(self):
        """AI의 차례 처리"""
        if self.game_over or not self.waiting_for_ai:
            return None, "AI 차례가 아닙니다."
        
        last_char = self.current_word[-1]
        possible_words = self.db.get_next_words(last_char)
        
        # 사용하지 않은 단어만 필터링
        available_words = [word for word in possible_words if word not in self.used_words]
        
        if not available_words:
            self.game_over = True
            self.winner = "플레이어"
            self.waiting_for_ai = False
            return None, "AI가 다음 단어를 찾지 못했습니다. 플레이어 승리!"
        
        # 랜덤으로 단어 선택
        ai_word = random.choice(available_words)
        self.current_word = ai_word
        self.used_words.add(ai_word)
        self.history.append(("AI", ai_word))
        self.waiting_for_ai = False
        
        # AI가 'ㅇ'으로 끝나는 단어를 썼는지 확인
        if ai_word[-1] == 'ㅇ':
            self.game_over = True
            self.winner = "플레이어"
            return ai_word, f"'{ai_word}'! 'ㅇ' 받침으로 끝나는 단어는 사용할 수 없습니다. 플레이어 승리!"
        
        return ai_word, f"AI: '{ai_word}'"

# Streamlit 앱
def main():
    st.set_page_config(
        page_title="AI와 끝말잇기",
        page_icon="🇰🇷",
        layout="centered"
    )
    
    st.title("🤖 AI와 끝말잇기 대결!")
    st.markdown("인공지능과 한국어 끝말잇기 게임을 즐겨보세요!")
    
    # 게임 상태 초기화 (간소화된 방식)
    if 'game' not in st.session_state:
        st.session_state.game = WordRelayGame()
    
    if 'game_started' not in st.session_state:
        st.session_state.game_started = False
    
    if 'last_input' not in st.session_state:
        st.session_state.last_input = ""
    
    game = st.session_state.game
    
    # 사이드바
    with st.sidebar:
        st.header("🎮 게임 정보")
        st.markdown("""
        ### 📝 게임 규칙:
        1. 앞 사람이 말한 단어의 **마지막 글자**로 시작하는 단어를 말합니다
        2. 이미 사용한 단어는 **다시 사용할 수 없습니다**
        3. **2글자 이상**의 단어만 사용 가능합니다
        4. **'ㅇ' 받침**으로 끝나는 단어는 사용할 수 없습니다
        5. 단어를 이을 수 없는 사람이 지게 됩니다
        """)
        
        if st.button("🔄 새 게임 시작", type="primary", use_container_width=True):
            st.session_state.game_started = True
            starting_word = game.start_game()
            st.session_state.last_input = ""
            st.success(f"🎯 게임 시작! AI: **'{starting_word}'**")
    
    # 메인 게임 영역
    if not st.session_state.game_started:
        st.info("👈 왼쪽 사이드바에서 **'새 게임 시작'** 버튼을 눌러 게임을 시작하세요!")
        return
    
    # 현재 게임 상태 표시
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 현재 상태")
        if game.current_word:
            current_char = game.current_word[-1]
            st.markdown(f"**현재 단어:** `{game.current_word}`")
            st.markdown(f"**다음 단어는 `{current_char}`(으)로 시작해야 합니다**")
            
            if game.waiting_for_ai:
                st.info("🤔 AI가 다음 단어를 생각하는 중...")
        
        if game.game_over:
            st.balloons()
            st.success(f"## 🎉 게임 종료! 승리자: {game.winner} 🎉")
    
    with col2:
        st.subheader("📋 사용된 단어")
        if game.used_words:
            recent_words = list(game.used_words)[-8:]
            for word in recent_words:
                st.write(f"- {word}")
        else:
            st.write("아직 사용된 단어가 없습니다.")
    
    # 단어 입력 영역
    if not game.game_over:
        st.subheader("💬 당신의 차례")
        
        # 사용자 입력 (키를 고정해서 재사용 문제 방지)
        user_input = st.text_input(
            "다음 단어를 입력하세요:",
            value=st.session_state.last_input,
            key="word_input",
            placeholder=f"'{game.current_word[-1]}'로 시작하는 단어를 입력하세요",
            label_visibility="collapsed"
        )
        
        col1, col2 = st.columns([1, 4])
        with col1:
            submit_clicked = st.button("🚀 단어 제출", type="primary", use_container_width=True)
        
        with col2:
            if st.button("🗑️ 입력 초기화", use_container_width=True):
                st.session_state.last_input = ""
                st.rerun()
        
        if submit_clicked and user_input.strip():
            success, message = game.player_turn(user_input.strip())
            if success:
                st.success(message)
                # AI 차례 자동 실행
                if game.waiting_for_ai and not game.game_over:
                    ai_word, ai_message = game.ai_turn()
                    if ai_word:
                        st.info(ai_message)
                    else:
                        st.error(ai_message)
                # 입력 필드 초기화
                st.session_state.last_input = ""
            else:
                st.error(message)
                st.session_state.last_input = ""  # 오류 시에도 입력 필드 초기화
        elif submit_clicked and not user_input.strip():
            st.warning("단어를 입력해주세요.")
    
    # 단어 정보 표시
    if game.current_word and not game.waiting_for_ai:
        st.subheader("📚 단어 정보")
        word_info = game.db.get_word_info(game.current_word)
        if word_info:
            pos, meaning, alternatives = word_info
            st.markdown(f"**📖 단어:** {game.current_word}")
            st.markdown(f"**🏷️ 품사:** {pos}")
            st.markdown(f"**💡 뜻:** {meaning}")
            st.markdown(f"**🔄 대체어:** {', '.join(alternatives)}")
    
    # 게임 히스토리
    st.subheader("📜 게임 히스토리")
    if game.history:
        for i, (player, word) in enumerate(game.history[-8:]):
            if player == "AI":
                st.write(f"{i+1}. 🤖 {player}: **{word}**")
            else:
                st.write(f"{i+1}. 👤 {player}: **{word}**")
    else:
        st.write("게임 기록이 없습니다.")

if __name__ == "__main__":
    main()
