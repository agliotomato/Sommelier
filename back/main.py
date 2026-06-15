from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(
    title="Sommelier Wine API",
    description="Backend service for recommending fine wines and food pairings",
    version="1.0.0"
)

# CORS configuration for integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models for request/response validation
class RecommendationRequest(BaseModel):
    mode: str  # "preferences" or "food"
    wine_type: Optional[str] = None  # "Red", "White", "Sparkling", "Rosé", "Dessert"
    sweetness: Optional[int] = 3  # 1 to 5
    acidity: Optional[int] = 3  # 1 to 5
    tannin: Optional[int] = 3  # 1 to 5
    body: Optional[int] = 3  # 1 to 5
    price_range: Optional[str] = None  # "under2", "2to5", "5to10", "over10"
    food: Optional[str] = None  # "meat", "seafood", "cheese", "dessert", "spicy_korean"

class WineResponse(BaseModel):
    name: str
    type: str
    grape: str
    country: str
    region: str
    sweetness: int
    acidity: int
    tannin: int
    body: int
    price_range: str
    price_desc: str
    description: str
    sommelier_tip: str
    pairings: List[str]
    score: float

# In-memory Wine Database
WINE_DATABASE = [
    {
        "name": "Château Margaux",
        "type": "Red",
        "grape": "Cabernet Sauvignon, Merlot",
        "country": "France",
        "region": "Bordeaux",
        "sweetness": 1,
        "acidity": 4,
        "tannin": 5,
        "body": 5,
        "price_range": "over10",
        "price_desc": "10만원 이상 (Fine Wine)",
        "description": "보르도의 여왕이라 불리는 최고급 레드 와인으로 우아하고 복합적인 블랙베리 향과 정교한 오크, 타닌의 구조감이 전설적인 조화를 이룹니다.",
        "sommelier_tip": "마시기 1~2시간 전에 디캔팅을 권장하며, 서빙 온도는 16~18°C가 가장 적합합니다.",
        "pairings": ["meat", "cheese"]
    },
    {
        "name": "Yellow Tail Shiraz",
        "type": "Red",
        "grape": "Shiraz",
        "country": "Australia",
        "region": "South Eastern Australia",
        "sweetness": 2,
        "acidity": 2,
        "tannin": 3,
        "body": 3,
        "price_range": "under2",
        "price_desc": "2만원 이하 (가성비)",
        "description": "과실 향이 톡톡 튀고 달콤한 바닐라 향과 잘 익은 자두 풍미가 매력적이며 목넘김이 매우 부드러운 입문용 데일리 레드 와인입니다.",
        "sommelier_tip": "오픈 후 즉시 시원하게 마시기 좋으며(15~16°C), 캐주얼한 파티나 모임에 어울립니다.",
        "pairings": ["meat", "spicy_korean"]
    },
    {
        "name": "Cloudy Bay Sauvignon Blanc",
        "type": "White",
        "grape": "Sauvignon Blanc",
        "country": "New Zealand",
        "region": "Marlborough",
        "sweetness": 1,
        "acidity": 5,
        "tannin": 1,
        "body": 2,
        "price_range": "2to5",
        "price_desc": "2만원 ~ 5만원 (실속형)",
        "description": "싱그러운 허브, 갓 벤 풀향과 레몬, 자몽, 아스파라거스 아로마가 가득 피어올라 입안에 활력과 청량함을 선사하는 뉴질랜드 대표 화이트 와인입니다.",
        "sommelier_tip": "반드시 차갑게 칠링(8~10°C)하여 마셔야 특유의 톡 쏘는 아로마와 산미를 온전히 즐길 수 있습니다.",
        "pairings": ["seafood", "cheese"]
    },
    {
        "name": "Moscato d'Asti (Vigarosa)",
        "type": "Dessert",
        "grape": "Moscato",
        "country": "Italy",
        "region": "Piemonte",
        "sweetness": 5,
        "acidity": 2,
        "tannin": 1,
        "body": 2,
        "price_range": "under2",
        "price_desc": "2만원 이하 (가성비)",
        "description": "달콤한 꿀 향과 청포도, 아카시아 꽃 향기가 가득하며, 조밀하고 미세한 스파클링이 기분 좋게 혀를 자극하는 달콤한 디저트 와인입니다.",
        "sommelier_tip": "식후 디저트 타임에 6~8°C로 아주 차갑게 보관하여 과일이나 케이크와 곁들여 마시면 최상의 조합입니다.",
        "pairings": ["dessert", "cheese"]
    },
    {
        "name": "Moët & Chandon Impérial",
        "type": "Sparkling",
        "grape": "Pinot Noir, Pinot Meunier, Chardonnay",
        "country": "France",
        "region": "Champagne",
        "sweetness": 1,
        "acidity": 4,
        "tannin": 1,
        "body": 3,
        "price_range": "5to10",
        "price_desc": "5만원 ~ 10만원 (프리미엄)",
        "description": "세계에서 가장 유명한 샴페인 중 하나로, 배, 복숭아의 신선한 청량함에 갓 구운 브리오슈 빵과 고소한 견과류 풍미가 조화롭게 녹아 있습니다.",
        "sommelier_tip": "기념일이나 축하 파티 웰컴 드링크로 최적이며, 8~10°C에서 조밀한 탄산감을 즐겨보세요.",
        "pairings": ["seafood", "cheese"]
    },
    {
        "name": "Whispering Angel Rosé",
        "type": "Rosé",
        "grape": "Grenache, Cinsault, Rolle",
        "country": "France",
        "region": "Provence",
        "sweetness": 1,
        "acidity": 3,
        "tannin": 2,
        "body": 2,
        "price_range": "2to5",
        "price_desc": "2만원 ~ 5만원 (실속형)",
        "description": "은은한 연분홍빛 수채화 같은 비주얼에 붉은 베리와 산뜻한 자몽 향, 은은한 스파이스와 깔끔한 미네랄 피니시가 매혹적인 럭셔리 프로방스 로제입니다.",
        "sommelier_tip": "더운 여름철 야외나 가벼운 샐러드 브런치 파티에서 10~12°C 온도로 세련되게 즐기기 좋습니다.",
        "pairings": ["seafood", "cheese", "dessert"]
    },
    {
        "name": "San Pedro 1865 Cabernet Sauvignon",
        "type": "Red",
        "grape": "Cabernet Sauvignon",
        "country": "Chile",
        "region": "Maipo Valley",
        "sweetness": 1,
        "acidity": 3,
        "tannin": 4,
        "body": 4,
        "price_range": "2to5",
        "price_desc": "2만원 ~ 5만원 (실속형)",
        "description": "한국인에게 오랫동안 사랑받은 레드 와인으로 진한 삼나무, 바닐라의 오크 터치와 잘 익은 블랙커런트, 다크 초콜릿 향이 강렬하게 다가옵니다.",
        "sommelier_tip": "마시기 30분 전에 오픈해 두었다가(16~18°C) 기름진 구이류 고기 요리와 마시면 타닌의 부드러움이 살아납니다.",
        "pairings": ["meat"]
    },
    {
        "name": "Kendall-Jackson Vintner's Reserve Chardonnay",
        "type": "White",
        "grape": "Chardonnay",
        "country": "USA",
        "region": "California",
        "sweetness": 2,
        "acidity": 3,
        "tannin": 1,
        "body": 4,
        "price_range": "2to5",
        "price_desc": "2만원 ~ 5만원 (실속형)",
        "description": "파인애플, 망고 등 풍부한 열대 과일 아로마에 오크 숙성에서 기인한 버터, 구운 바닐라 향이 부드럽고 묵직하게 감싸는 풀바디 화이트 와인입니다.",
        "sommelier_tip": "일반 화이트보다 조금 덜 차가운 온도(10~12°C)에서 테이스팅해야 버터리한 오크 텍스처를 극대화해 느낄 수 있습니다.",
        "pairings": ["seafood", "cheese"]
    },
    {
        "name": "Dom Pérignon Vintage",
        "type": "Sparkling",
        "grape": "Chardonnay, Pinot Noir",
        "country": "France",
        "region": "Champagne",
        "sweetness": 1,
        "acidity": 4,
        "tannin": 1,
        "body": 4,
        "price_range": "over10",
        "price_desc": "10만원 이상 (Fine Wine)",
        "description": "최고의 빈티지 샴페인의 대명사로 오랜 효모 숙성에서 우러나오는 구운 견과류, 토스트 향, 그리고 날카로우면서도 정교한 미네랄리티의 절정을 보여줍니다.",
        "sommelier_tip": "오픈 직후부터 온도 상승에 따라 변화하는 다양한 복합 아로마를 향이 모아지는 샴페인 글라스(10~12°C)에서 천천히 음미해 보세요.",
        "pairings": ["seafood", "cheese"]
    },
    {
        "name": "Tignanello Super Tuscan",
        "type": "Red",
        "grape": "Sangiovese, Cabernet Sauvignon",
        "country": "Italy",
        "region": "Toscana",
        "sweetness": 1,
        "acidity": 4,
        "tannin": 4,
        "body": 5,
        "price_range": "over10",
        "price_desc": "10만원 이상 (Fine Wine)",
        "description": "이탈리아 와인의 역사를 새로 쓴 명품 토스카나 와인으로 체리, 라즈베리의 과일향과 허브, 가죽, 감초, 부드러운 오크 터치의 레이어가 고도의 우아함을 선사합니다.",
        "sommelier_tip": "적어도 1~2시간 이상 디캔팅이 필수적이며 넓은 볼의 보르도 잔(16~18°C)에 서빙해 이국적인 스파이스 향을 즐기세요.",
        "pairings": ["meat", "cheese"]
    },
    {
        "name": "Villa M Rosé",
        "type": "Dessert",
        "grape": "Brachetto",
        "country": "Italy",
        "region": "Piemonte",
        "sweetness": 5,
        "acidity": 3,
        "tannin": 1,
        "body": 1,
        "price_range": "2to5",
        "price_desc": "2만원 ~ 5만원 (실속형)",
        "description": "달콤한 생딸기, 라즈베리 향과 장미꽃 잎의 로맨틱한 풍미가 돋보이며 약발포성을 띤 향긋하고 매력적인 핑크빛 세미-스윗 로제 디저트 와인입니다.",
        "sommelier_tip": "연인과의 기념일이나 파티에 6~8°C로 아주 차갑게 보관하여 가벼운 과일 디저트나 초콜릿과 곁들이면 로맨틱한 분위기를 완성해 줍니다.",
        "pairings": ["dessert"]
    },
    {
        "name": "Bogle Old Vine Zinfandel",
        "type": "Red",
        "grape": "Zinfandel",
        "country": "USA",
        "region": "California Lodi",
        "sweetness": 2,
        "acidity": 3,
        "tannin": 3,
        "body": 4,
        "price_range": "2to5",
        "price_desc": "2만원 ~ 5만원 (실속형)",
        "description": "수령이 오래된 포도나무(Old Vine)에서 자란 포도로 만들어 강렬한 블랙베리 잼 풍미와 후추, 정향 같은 스파이시함이 독특하게 퍼지는 풀바디 와인입니다.",
        "sommelier_tip": "진하고 매콤달콤한 소스의 한식 육류 요리(제육볶음, 갈비 등)나 바비큐 요리에 매치할 때 놀라운 케미를 발휘합니다.",
        "pairings": ["meat", "spicy_korean"]
    },
    {
        "name": "Louis Jadot Chablis",
        "type": "White",
        "grape": "Chardonnay",
        "country": "France",
        "region": "Bourgogne Chablis",
        "sweetness": 1,
        "acidity": 4,
        "tannin": 1,
        "body": 3,
        "price_range": "5to10",
        "price_desc": "5만원 ~ 10만원 (프리미엄)",
        "description": "부르고뉴 샤블리 지역의 미네랄이 풍부한 석회질 토양 덕분에 레몬, 라임의 아삭한 과실 풍미와 함께 짭조름한 조개껍질 향의 미네랄 뉘앙스가 돋보입니다.",
        "sommelier_tip": "익히지 않은 생굴, 신선한 모듬 회, 스시 등 해산물 요리와 9~11°C 온도로 매칭하면 비린 맛을 잡아주며 훌륭히 어우러집니다.",
        "pairings": ["seafood"]
    },
    {
        "name": "Gancia Moscato Rosé",
        "type": "Sparkling",
        "grape": "Moscato, Brachetto",
        "country": "Italy",
        "region": "Piemonte",
        "sweetness": 4,
        "acidity": 3,
        "tannin": 1,
        "body": 2,
        "price_range": "under2",
        "price_desc": "2만원 이하 (가성비)",
        "description": "신선한 복숭아, 베리류의 다채로운 아로마와 입안 가득 감도는 핑크빛 기포가 주는 가벼운 청량함이 홈파티를 한층 화사하게 만들어 주는 세미-스윗 스파클링입니다.",
        "sommelier_tip": "6~8°C 정도로 차갑게 칠링하여 식전주로 즐기거나, 각종 모듬 치즈, 과일 타르트와 즐겁게 매칭하세요.",
        "pairings": ["dessert", "cheese"]
    },
    {
        "name": "Substance Cabernet Sauvignon",
        "type": "Red",
        "grape": "Cabernet Sauvignon",
        "country": "USA",
        "region": "Washington State",
        "sweetness": 1,
        "acidity": 3,
        "tannin": 4,
        "body": 4,
        "price_range": "2to5",
        "price_desc": "2만원 ~ 5만원 (실속형)",
        "description": "강렬한 검은 과실 향, 연필심, 담뱃잎의 매혹적인 아로마와 강인하고 견고한 타닌 구조감이 프렌치 오크 터치와 어우러진 현대적인 미국 카베르네 소비뇽입니다.",
        "sommelier_tip": "기름진 두툼한 티본 스테이크나 수제 소고기 패티 버거와 16~18°C 온도에서 기막힌 맛의 시너지를 보여줍니다.",
        "pairings": ["meat"]
    }
]

@app.post("/recommend", response_model=List[WineResponse])
def get_wine_recommendation(request: RecommendationRequest):
    scored_wines = []
    
    for wine in WINE_DATABASE:
        score = 0.0
        
        # Mode 1: Recommendation by Taste Preferences
        if request.mode == "preferences":
            # 1. Type filter (Large penalty if it doesn't match and type is specified)
            if request.wine_type and request.wine_type != "All":
                if wine["type"].lower() != request.wine_type.lower():
                    continue # Filter out unmatched types completely
            
            # 2. Taste Profile Matching (Distance calculation)
            # Maximum distance per attribute is 4 (5 - 1). Sum of 4 attributes max distance = 16.
            # Convert to a similarity score out of 100 points
            dist = 0.0
            dist += abs(wine["sweetness"] - (request.sweetness or 3))
            dist += abs(wine["acidity"] - (request.acidity or 3))
            dist += abs(wine["tannin"] - (request.tannin or 3))
            dist += abs(wine["body"] - (request.body or 3))
            
            # Normalize distance to 0 - 80 points (closer tastes get higher scores)
            taste_score = 80.0 * (1.0 - (dist / 16.0))
            score += taste_score
            
            # 3. Price Range Matching (20 points max)
            if request.price_range and request.price_range != "All":
                if wine["price_range"] == request.price_range:
                    score += 20.0
                else:
                    # Partial score for adjacent price tiers could be added, but here we just penalize mismatch
                    score += 0.0
            else:
                score += 20.0 # No price filter means auto full price score
                
        # Mode 2: Recommendation by Food Pairing
        elif request.mode == "food":
            # Food selection is required for food mode
            if not request.food:
                raise HTTPException(status_code=400, detail="Food parameter is required in 'food' mode")
                
            # If the wine is explicitly paired with selected food, start with base score
            if request.food in wine["pairings"]:
                score += 70.0
                
                # Classify food match combinations (Classic sommelier wisdom matching)
                # Meat pairs best with Red
                if request.food == "meat" and wine["type"] == "Red":
                    score += 30.0
                # Seafood pairs best with White or Sparkling
                elif request.food == "seafood" and wine["type"] in ["White", "Sparkling"]:
                    score += 30.0
                # Cheese pairs well with almost anything, but especially high acidity White/Red or Sparkling
                elif request.food == "cheese" and wine["type"] in ["Red", "White", "Sparkling"]:
                    score += 30.0
                # Dessert pairs best with Dessert type wines
                elif request.food == "dessert" and wine["type"] == "Dessert":
                    score += 30.0
                # Spicy Korean food pairs best with fruity/mild reds (e.g. Shiraz, Zinfandel) or refreshing whites
                elif request.food == "spicy_korean":
                    if wine["name"] in ["Yellow Tail Shiraz", "Bogle Old Vine Zinfandel"]:
                        score += 30.0
                    elif wine["type"] in ["Red", "White"]:
                        score += 15.0
            else:
                # If food doesn't match the wine's direct pairings, give a very low default score
                score += 20.0
                
            # Filter price range if selected in food mode as well
            if request.price_range and request.price_range != "All":
                if wine["price_range"] != request.price_range:
                    score -= 30.0 # Demote mismatched price range
                    
        else:
            raise HTTPException(status_code=400, detail="Invalid mode. Must be 'preferences' or 'food'")
            
        # Format and append wine details with their calculated score
        scored_wines.append({
            **wine,
            "score": round(max(0.0, score), 1)
        })
        
    # Sort wines descending by compatibility score
    scored_wines.sort(key=lambda x: x["score"], reverse=True)
    
    # Return top 3 recommendations
    return [WineResponse(**w) for w in scored_wines[:3]]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
