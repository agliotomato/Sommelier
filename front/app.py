import streamlit as st
import requests
import os

# 1. Page Configuration
st.set_page_config(
    page_title="Sommelier - Wine & Pairing Recommender",
    page_icon="🍷",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. Minimal CSS (rely on Streamlit default theme)


# 3. Environment Config for API Backend
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

# 4. App Title & Premium Banner
st.title("🍷 SOMMELIER")
st.caption("당신만을 위한 맞춤형 와인 & 안주 마리아주 추천 | 2021204064 서현택")
st.divider()

# 5. Core Layout Structure (Sidebar Inputs & Main Panel Recommendations)
col1, col2 = st.columns([1, 2.2])

with col1:
    st.markdown("<h3 style='margin-top:0;'>🍷 추천 조건 설정</h3>", unsafe_allow_html=True)
    
    # Mode Toggle
    rec_mode = st.radio(
        "추천 방식을 선택하세요",
        options=["취향 맞춤 추천", "푸드 페어링 추천"],
        index=0,
        label_visibility="collapsed"
    )
    
    st.markdown("<div style='margin-bottom: 15px;'></div>", unsafe_allow_html=True)
    
    # 5.1 Wine Preference Mode Inputs
    if rec_mode == "취향 맞춤 추천":
        st.info("당신의 맛 취향과 가격대를 조합해 최적의 와인을 소싱합니다.")
        
        # Wine Type filter
        wine_type = st.selectbox(
            "선호하는 와인 타입",
            options=["All", "Red", "White", "Sparkling", "Rosé", "Dessert"],
            format_func=lambda x: {
                "All": "모든 종류",
                "Red": "레드 와인 (Red)",
                "White": "화이트 와인 (White)",
                "Sparkling": "스파클링 와인 (Sparkling)",
                "Rosé": "로제 와인 (Rosé)",
                "Dessert": "디저트 와인 (Dessert)"
            }[x]
        )
        
        st.markdown("<p style='margin-bottom: 5px; font-weight: bold;'>맛 프로필 세부 조정 (1: 낮음 ~ 5: 높음)</p>", unsafe_allow_html=True)
        
        sweetness = st.slider("🍭 당도 (Sweetness)", 1, 5, 3)
        acidity = st.slider("🍋 산도 (Acidity)", 1, 5, 3)
        tannin = st.slider("🪵 타닌 (Tannin - 떫은맛)", 1, 5, 3)
        body = st.slider("⚖️ 바디감 (Body - 묵직함)", 1, 5, 3)
        
        price_range = st.selectbox(
            "선호하는 가격대",
            options=["All", "under2", "2to5", "5to10", "over10"],
            format_func=lambda x: {
                "All": "모든 가격대",
                "under2": "2만원 이하 (가성비)",
                "2to5": "2만원 ~ 5만원 (실속형)",
                "5to10": "5만원 ~ 10만원 (프리미엄)",
                "over10": "10만원 이상 (Fine Wine)"
            }[x]
        )
        
        # Payload Construction
        api_payload = {
            "mode": "preferences",
            "wine_type": wine_type,
            "sweetness": sweetness,
            "acidity": acidity,
            "tannin": tannin,
            "body": body,
            "price_range": price_range
        }

    # 5.2 Food Pairing Mode Inputs
    else:
        st.info("오늘 먹을 음식을 알려주시면, 마리아주가 가장 훌륭한 와인을 찾아드립니다.")
        
        food_selection = st.selectbox(
            "오늘의 안주/요리 메뉴",
            options=["meat", "seafood", "cheese", "dessert", "spicy_korean"],
            format_func=lambda x: {
                "meat": "🥩 소고기 스테이크 / 갈비 / 육류 요리",
                "seafood": "🐟 생선회 / 굴 / 조개 및 해산물 요리",
                "cheese": "🧀 모듬 치즈 / 하몽 / 샤르큐트리 플래터",
                "dessert": "🍰 케이크 / 마카롱 / 달콤한 디저트 & 과일",
                "spicy_korean": "🌶️ 삼겹살 / 매콤한 제육볶음 / 양념 한식 요리"
            }[x]
        )
        
        price_range = st.selectbox(
            "선호하는 가격대",
            options=["All", "under2", "2to5", "5to10", "over10"],
            format_func=lambda x: {
                "All": "모든 가격대",
                "under2": "2만원 이하 (가성비)",
                "2to5": "2만원 ~ 5만원 (실속형)",
                "5to10": "5만원 ~ 10만원 (프리미엄)",
                "over10": "10만원 이상 (Fine Wine)"
            }[x]
        )
        
        # Payload Construction
        api_payload = {
            "mode": "food",
            "food": food_selection,
            "price_range": price_range
        }
        
    st.markdown("<div style='margin-bottom: 20px;'></div>", unsafe_allow_html=True)
    trigger_rec = st.button("🍷 소믈리에 추천 받기")

# 6. Main Panel Layout (Display Results)
with col2:
    st.markdown("<h3 style='margin-top:0;'>✨ 오늘의 소믈리에 추천 와인</h3>", unsafe_allow_html=True)
    
    if trigger_rec:
        with st.spinner("소믈리에가 최고의 와인을 셀러에서 고르고 있습니다..."):
            try:
                # HTTP Request to FastAPI backend
                api_endpoint = f"{BACKEND_URL}/recommend"
                response = requests.post(api_endpoint, json=api_payload, timeout=8)
                
                if response.status_code == 200:
                    wines = response.json()
                    
                    if not wines:
                        st.warning("조건에 부합하는 와인을 찾지 못했습니다. 설정 범위를 조정하여 다시 시도해 주세요.")
                    else:
                        for idx, wine in enumerate(wines):
                            rank_emoji = ["🥇", "🥈", "🥉"][idx] if idx < 3 else "🍷"

                            with st.container(border=True):
                                # Header: name + type + score
                                st.markdown(f"### {rank_emoji} {wine['name']} `{wine['type']}` — 매칭도 **{wine['score']}%**")
                                st.caption(f"🍇 품종: {wine['grape']}  |  📍 생산지: {wine['country']} ({wine['region']})  |  💵 {wine['price_desc']}")

                                # Description
                                st.markdown(wine["description"])

                                # Taste profile with progress bars
                                st.markdown("**맛 프로필**")
                                m1, m2 = st.columns(2)
                                with m1:
                                    st.caption(f"🍭 당도: {wine['sweetness']}/5")
                                    st.progress(wine["sweetness"] / 5.0)
                                    st.caption(f"🍋 산도: {wine['acidity']}/5")
                                    st.progress(wine["acidity"] / 5.0)
                                with m2:
                                    st.caption(f"🪵 타닌: {wine['tannin']}/5")
                                    st.progress(wine["tannin"] / 5.0)
                                    st.caption(f"⚖️ 바디: {wine['body']}/5")
                                    st.progress(wine["body"] / 5.0)

                                # Food pairings
                                food_icons = {
                                    "meat": "🥩 육류",
                                    "seafood": "🐟 해산물",
                                    "cheese": "🧀 치즈/하몽",
                                    "dessert": "🍰 디저트",
                                    "spicy_korean": "🌶️ 매콤한 한식"
                                }
                                pairing_tags = "  |  ".join([food_icons.get(p, p) for p in wine["pairings"]])
                                st.markdown(f"**추천 페어링:** {pairing_tags}")

                                # Sommelier tip
                                st.info(f"💡 **소믈리에 팁:** {wine['sommelier_tip']}")
                else:
                    st.error(f"백엔드 통신 오류가 발생했습니다. (상태 코드: {response.status_code})")
            except requests.exceptions.ConnectionError:
                st.error("백엔드 서버에 연결할 수 없습니다. FastAPI 컨테이너가 정상 구동 중인지, 포트 설정이 맞는지 확인해 주세요.")
            except Exception as e:
                st.error(f"오류가 발생했습니다: {str(e)}")
    else:
        # Initial guide state before clicking recommend
        st.markdown(
            """
            <div style="background: rgba(255,255,255,0.05); padding: 40px; border-radius: 12px; text-align: center; border: 1px dashed rgba(212,175,55,0.25);">
                <span style="font-size: 3rem;">🍷</span>
                <h4 style="margin-top: 15px; color: #D4AF37; font-family: 'Playfair Display', serif;">당신의 취향을 탐험할 시간입니다</h4>
                <p style="color: #A9A9A9; font-size: 14px; max-width: 450px; margin: 10px auto;">
                    좌측 설정 패널에서 취향 점수 혹은 오늘 저녁에 곁들일 음식 메뉴를 설정하고 
                    <strong>'소믈리에 추천 받기'</strong> 버튼을 클릭하여 궁극의 마리아주 와인을 매칭해 보세요.
                </p>
            </div>
            """, 
            unsafe_allow_html=True
        )

# 7. Premium Footer with metadata
st.divider()
st.caption("Sommelier Recommendation App • Streamlit & FastAPI & Docker • OSS Final Project • 2021204064 서현택")
