import streamlit as st
import random
import requests
from collections import defaultdict

# 한국어 단어 검색을 위한 클래스
class KoreanWordChecker:
    def __init__(self):
        # 기본 단어 목록 (백업용)
        self.basic_words = {
            "사과", "과일", "열매", "매화", "화가", "가수", "수박", "박사", "사자", 
            "자동차", "차표", "표범", "범인", "인간", "간호사", "사랑", "랑이", 
            "이발소", "소방차", "차이", "이음", "음악", "악기", "기차", "차고",
            "고양이", "이불", "불고기", "기린", "린스", "스키", "키위", "위성",
            "성격", "격투", "투수", "수영", "영화", "화분", "분수", "수학",
            "학생", "생선", "선물", "물고기", "기적", "적군", "군인", "인형",
            "형제", "제비", "비행기", "기억", "억양", "양말", "말차", "차량",
            "량이", "이유", "유리", "리본", "본드", "드럼", "럼버", "버스",
            "스튜", "튜브", "브라", "라면", "면도", "도서", "서류", "류리",
            "이사", "사탕", "탕수", "수건", "건강", "강아지", "지우개", "개미",
            "미술", "술병", "병원", "원숭이", "이탄", "탄산", "산소", "소나무",
            "무지개", "개나리", "리본", "본인", "인사", "사다리", "다리", "리모컨",
            "컨디션", "션샤인", "인공", "공원", "원피스", "스토리", "리더", "더하기",
            "기회", "회의", "의사", "사진", "진리", "이론", "논리", "이상", "상자",
            "자석", "석양", "양식", "식사", "도구", "구름", "음식", "식물", "물질",
            "질문", "문제", "제목", "목표", "표정", "정원", "원인", "인과", "과자",
            "자전거", "거미", "미래", "래킷", "트리", "유도", "도시", "시계", "계단",
            "단어", "어린이", "이마", "마음", "음료", "료리", "이력", "력기", "기대",
            "대화", "화장", "장미", "미소", "소설", "설계", "계획", "화재", "재산",
            "산책", "책상", "상상", "상품", "품질", "질량", "량산", "산업", "업무",
            "무료", "료칸", "간식", "식욕", "욕구", "구조", "조각", "각도", "도망",
            "망원", "원격", "격리", "이동", "동물", "물건", "건강", "강력", "력사",
            "사건", "건물", "물병", "병아리", "이익", "익스", "스파이", "이상", "상처",
            "처리", "이유", "유머", "머리", "리본", "본능", "능력", "력행", "행복",
            "복사", "사랑", "랑해", "해변", "변화", "화면", "면접", "접수", "수업",
            "업적", "적용", "용기", "기름", "름바", "바다", "다리", "리포트", "트랙",
            "랙킹", "킹콩", "콩나물", "물질", "질문", "문제", "제작", "작품", "품격",
            "격려", "려행", "행운", "운동", "동전", "전화", "화분", "분석", "석유",
            "유전", "전기", "기술", "술집", "집중", "중요", "요리", "이론", "논문",
            "문서", "서비스", "스타", "타임", "임무", "무적", "적군", "군대", "대학",
            "학문", "문학", "학생", "생활", "활동", "동아리", "이벤트", "트럼프", "프로"
        }
        
        # 끝말을 시작으로 하는 단어 목록
        self.word_start = defaultdict(list)
        for word in self.basic_words:
            start_char = word[0]
            self.word_start[start_char].append(word)
    
    def is_valid_word(self, word):
        """단어가 유효한지 확인 (간단한 검증)"""
        if not word or len(word) < 2:
            return False
        
        # 한글 여부 확인 (기본적인 검증)
        if not all('가' <= char <= '힣' for char in word):
            return False
            
        # 기본 단어 목록에 있는지 확인
        return word in self.basic_words
    
    def get_word_info(self, word):
        """단어 정보 반환 (간단한 버전)"""
        if word in self.basic_words:
            # 간단한 뜻 정보 (실제로는 API를 사용하는 것이 좋음)
            meanings = {
                "사과": "과일의 일종 또는 잘못을 뉘우침",
                "과일": "나무에서 열리는 먹을 수 있는 열매",
                "유도": "어떤 방향으로 이끎",
                "도시": "많은 사람이 사는 지역",
                # ... 다른 단어들도 추가 가능
            }
            meaning = meanings.get(word, "일반적인 명사")
            return ["명사", meaning, [word]]
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
            return random.choice(list(self.basic_words))

# 게임 상태 관리
class WordRelayGame:
    def __init__(self):
        self.db = KoreanWordChecker()
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
            return False, "사전에 없는 단어입니다. 일반적인 한국어 단어를 사용해주세요."
        
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
        return True, f"✅ '{word}' - 좋은 단어입니다! AI가 생각 중..."
    
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
            return None, "🤖 AI가 다음 단어를 찾지 못했습니다. 🎉 플레이어 승리!"
        
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
            return ai_word, f"'{ai_word}'! 'ㅇ' 받침으로 끝나는 단어는 사용할 수 없습니다. 🎉 플레이어 승리!"
        
        return ai_word, f"🤖 AI: '{ai_word}'"

# Streamlit 앱
def main():
    st.set_page_config(
        page_title="AI와 끝말잇기",
        page_icon="🇰🇷",
        layout="centered"
    )
    
    st.title("🎮 AI와 실시간 끝말잇기!")
    st.markdown("### 🤖 인공지능과 재미있는 한국어 끝말잇기 대결!")
    
    # 게임 상태 초기화
    if 'game' not in st.session_state:
        st.session_state.game = WordRelayGame()
        st.session_state.game_started = False
        st.session_state.input_key = 0  # 입력 필드 초기화를 위한 키
    
    game = st.session_state.game
    
    # 사이드바
    with st.sidebar:
        st.header("ℹ️ 게임 정보")
        st.markdown("""
        ### 📝 게임 규칙:
        1. **마지막 글자**로 시작하는 단어를 말하세요
        2. **이미 사용한 단어**는 사용 불가
        3. **2글자 이상**의 단어만 가능
        4. **'ㅇ' 받침**으로 끝나면 안됨
        5. **일반적인 한국어 단어**를 사용하세요
        """)
        
        st.info("💡 **팁**: 사과 → 과일 → 일기 → 기차 ...")
        
        if st.button("🔄 새 게임 시작", type="primary", use_container_width=True):
            st.session_state.game_started = True
            st.session_state.input_key += 1  # 입력 필드 초기화
            starting_word = game.start_game()
            st.success(f"🎯 게임 시작! AI: **'{starting_word}'**")
            st.rerun()
    
    # 메인 게임 영역
    if not st.session_state.game_started:
        st.info("👈 **왼쪽에서 '새 게임 시작' 버튼을 눌러주세요!**")
        st.image("https://via.placeholder.com/400x200/4CAF50/FFFFFF?text=끝말잇기+게임", use_column_width=True)
        return
    
    # 현재 게임 상태
    st.subheader("📊 게임 현황")
    
    col1, col2, col3 = st.columns([2, 1, 2])
    
    with col1:
        if game.current_word:
            current_char = game.current_word[-1]
            st.metric("현재 단어", game.current_word)
            st.metric("다음 단어 시작 글자", f"'{current_char}'")
    
    with col2:
        st.metric("사용된 단어", len(game.used_words))
    
    with col3:
        if game.game_over:
            st.error("게임 종료")
            st.balloons()
        elif game.waiting_for_ai:
            st.warning("AI 차례")
        else:
            st.success("당신 차례")
    
    if game.game_over:
        st.success(f"## 🏆 승리자: {game.winner} 🏆")
        if st.button("다시 시작하기", type="primary"):
            st.session_state.game_started = False
            st.rerun()
    
    # 단어 입력
    if not game.game_over and not game.waiting_for_ai:
        st.subheader("💬 당신의 차례")
        
        with st.form("word_form", clear_on_submit=True):
            user_input = st.text_input(
                "다음 단어를 입력하세요:",
                placeholder=f"'{game.current_word[-1]}'로 시작하는 단어...",
                key=f"input_{st.session_state.input_key}"
            )
            
            submitted = st.form_submit_button("🚀 단어 제출", use_container_width=True)
            
            if submitted:
                if user_input.strip():
                    success, message = game.player_turn(user_input.strip())
                    if success:
                        st.success(message)
                        # AI 차례 자동 실행
                        if game.waiting_for_ai and not game.game_over:
                            with st.spinner("AI가 단어를 생각하는 중..."):
                                ai_word, ai_message = game.ai_turn()
                                if ai_word:
                                    st.info(ai_message)
                                else:
                                    st.error(ai_message)
                    else:
                        st.error(message)
                else:
                    st.warning("단어를 입력해주세요.")
    
    # 사용된 단어 목록
    with st.expander("📋 사용된 단어 목록"):
        if game.used_words:
            cols = st.columns(3)
            words_list = list(game.used_words)
            for i, word in enumerate(words_list):
                cols[i % 3].write(f"- {word}")
        else:
            st.write("아직 사용된 단어가 없습니다.")
    
    # 게임 히스토리
    with st.expander("📜 게임 기록"):
        if game.history:
            for i, (player, word) in enumerate(game.history[-10:]):
                if player == "AI":
                    st.write(f"{i+1}. 🤖 **{player}**: {word}")
                else:
                    st.write(f"{i+1}. 👤 **{player}**: {word}")
        else:
            st.write("게임 기록이 없습니다.")

if __name__ == "__main__":
    main()
