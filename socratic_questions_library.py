"""
蘇格拉底式問題庫
收集高質量的決策型/邊界型問題範例

🚨 核心修正 2: Data Trap 的核心資產
這些問題用於收集人類的高價值決策數據
"""

from typing import Dict, List, Any

# ========================================
# 問題庫 - 按場景分類
# ========================================

QUESTION_LIBRARY: Dict[str, List[Dict[str, Any]]] = {
    
    # 付款/交易場景 (Payment/Transaction)
    "payment": [
        {
            "text": "如果付款 API 在扣款後超時(30秒無響應),你要如何確認付款是否成功?",
            "category": "error_handling",
            "options": ["A. 立即重試付款請求", "B. 調用查詢付款狀態 API", "C. 標記為待確認,人工處理"],
            "risk_analysis": {"0": "⚠️ 重複扣款風險", "1": "✅ 標準做法", "2": "⚠️ 用戶體驗差"},
            "trap": "測試用戶是否理解冪等性和分布式事務"
        },
        {
            "text": "用戶付款成功但訂單建立失敗,你要如何處理?",
            "category": "recovery",
            "options": ["A. 自動退款給用戶", "B. 重試建立訂單 (最多3次)", "C. 保留付款記錄,允許用戶重新下單"],
            "risk_analysis": {"0": "⚠️ 損失交易機會", "1": "✅ 自動恢復", "2": "⚠️ 客服成本高"},
            "trap": "測試用戶對補償事務的理解"
        },
        {
            "text": "如果用戶在付款過程中按下 '上一頁'，系統會發生什麼？",
            "category": "state_management",
            "options": ["A. 重複建立訂單", "B. 鎖定訂單，提示 '付款中'", "C. 無反應"],
            "risk_analysis": {"0": "⚠️ 髒數據風險", "1": "✅ 狀態機保護", "2": "⚠️ 用戶困惑"},
            "trap": "測試前端狀態鎖定意識"
        }
    ],

    # 庫存/並發場景 (Inventory/Concurrency)
    "inventory": [
        {
            "text": "兩個用戶同時購買最後一件商品,你要如何處理?",
            "category": "concurrency",
            "options": ["A. 先到先得 (DB Lock)", "B. 兩者都成功,超賣後補貨", "C. 使用 Redis 原子操作"],
            "risk_analysis": {"0": "✅ 安全但慢", "1": "⚠️ 商業風險", "2": "✅ 高性能推薦"},
            "trap": "測試並發控制能力"
        },
        {
            "text": "閃購活動 (Flash Sale) 流量瞬間暴增 100倍，數據庫撐不住怎麼辦？",
            "category": "performance",
            "options": ["A. 升級數據庫規格", "B. 引入 Redis 預扣庫存 + 消息隊列", "C. 限流 (Rate Limit)"],
            "risk_analysis": {"0": "⚠️ 成本極高且無效", "1": "✅ 標準架構", "2": "✅ 保護系統但犧牲體驗"},
            "trap": "測試高並發架構設計"
        }
    ],

    # 認證/安全場景 (Auth/Security)
    "authentication": [
        {
            "text": "用戶連續登入失敗 5 次,你要如何處理?",
            "category": "security",
            "options": ["A. 鎖定帳號 30 分鐘", "B. 要求圖形驗證碼", "C. 不處理"],
            "risk_analysis": {"0": "✅ 標準防禦", "1": "✅ 平衡體驗", "2": "⚠️ 暴力破解風險"},
            "trap": "測試暴力破解防禦意識"
        },
        {
            "text": "JWT Token 被盜用了，服務端能強制讓它失效嗎？",
            "category": "security",
            "options": ["A. 不能，JWT 是無狀態的", "B. 可以，使用 Redis 黑名單機制", "C. 可以，刪除用戶"],
            "risk_analysis": {"0": "⚠️ 安全漏洞", "1": "✅ 標準解決方案", "2": "⚠️ 過度反應"},
            "trap": "測試 JWT 機制理解"
        },
        {
            "text": "如果資料庫被 SQL Injection 注入，所有用戶密碼洩漏，後果是什麼？",
            "category": "security",
            "options": ["A. 密碼是明文，全部完蛋", "B. 密碼有加鹽 Hash，暫時安全但需重置", "C. 只有管理員受影響"],
            "risk_analysis": {"0": "💀 災難性後果 (未加密)", "1": "✅ 縱深防禦生效", "2": "⚠️ 錯誤認知"},
            "trap": "測試密碼存儲安全意識"
        }
    ],

    # 數據一致性 (Data Consistency)
    "data_consistency": [
        {
            "text": "主資料庫寫入成功但快取更新失敗,如何保證一致性?",
            "category": "consistency",
            "options": ["A. 回滾資料庫", "B. 設定快取過期時間 (TTL)", "C. 無限重試"],
            "risk_analysis": {"0": "⚠️ 影響性能", "1": "✅ 最終一致性", "2": "⚠️ 可能死鎖"},
            "trap": "測試 CAP 定理與最終一致性"
        },
        {
            "text": "微服務 A 調用 微服務 B 失敗，如何保證數據不丟失？",
            "category": "reliability",
            "options": ["A. 記錄 Log", "B. 使用消息隊列 (Kafka/RabbitMQ) 重試", "C. 放棄操作"],
            "risk_analysis": {"0": "⚠️ 難以自動恢復", "1": "✅ 可靠性設計", "2": "⚠️ 數據丟失"},
            "trap": "測試分布式系統可靠性"
        }
    ],

    # API 集成 (API Integration)
    "api_integration": [
        {
            "text": "第三方 API 響應時間超過 5 秒,你要如何處理?",
            "category": "reliability",
            "options": ["A. 等待直到超時", "B. Circuit Breaker (熔斷機制)", "C. 返回錯誤"],
            "risk_analysis": {"0": "⚠️ 雪崩效應風險", "1": "✅ 保護系統", "2": "⚠️ 體驗差"},
            "trap": "測試服務治理能力"
        },
        {
            "text": "如何防止惡意用戶重複調用你的 API (Replay Attack)？",
            "category": "security",
            "options": ["A. 檢查 User-Agent", "B. 使用 Nonce + Timestamp 簽名", "C. 限制 IP"],
            "risk_analysis": {"0": "⚠️ 易被偽造", "1": "✅ 標準防禦", "2": "⚠️ 誤殺無辜"},
            "trap": "測試 API 安全設計"
        }
    ],

    # 隱私保護 (Privacy)
    "privacy": [
        {
            "text": "日誌 (Log) 中包含用戶的信用卡號，這可以嗎？",
            "category": "compliance",
            "options": ["A. 可以，方便除錯", "B. 不行，必須脫敏 (Masking)", "C. 只有內部人員能看就行"],
            "risk_analysis": {"0": "💀 嚴重違規 (PCI-DSS)", "1": "✅ 合規做法", "2": "⚠️ 內部威脅風險"},
            "trap": "測試隱私合規意識"
        },
        {
            "text": "歐盟用戶要求刪除所有數據 (GDPR)，但備份裡還有，怎麼辦？",
            "category": "compliance",
            "options": ["A. 不用管備份", "B. 標記為已刪除，恢復時過濾", "C. 銷毀所有備份"],
            "risk_analysis": {"0": "⚠️ 法律風險", "1": "✅ 可行方案", "2": "⚠️ 不切實際"},
            "trap": "測試 GDPR 合規處理"
        }
    ],

    # 聊天/通訊場景 (Chat/Messaging)
    "chat": [
        {
            "text": "如果用戶離線時收到100條訊息，重新上線後如何同步？",
            "category": "performance",
            "options": ["A. 一次性推送所有訊息", "B. 分批推送 (Pagination)", "C. 只顯示最後一條"],
            "risk_analysis": {"0": "⚠️ 卡頓/流量爆炸", "1": "✅ 標準做法", "2": "⚠️ 信息丟失"},
            "trap": "測試即時通訊同步機制"
        },
        {
            "text": "訊息發送後，對方未讀，發送方刪除了訊息，對方還能看到嗎？",
            "category": "consistency",
            "options": ["A. 能看到 (雙向刪除需特殊處理)", "B. 不能看到 (物理刪除)", "C. 看運氣"],
            "risk_analysis": {"0": "✅ 隱私保護挑戰", "1": "⚠️ 數據找回困難", "2": "⚠️ 不確定性"},
            "trap": "測試消息撤回/刪除邏輯"
        }
    ],

    # 預約/排程場景 (Booking)
    "booking": [
        {
            "text": "兩個用戶同時預約同一時段，系統如何避免衝突？",
            "category": "concurrency",
            "options": ["A. 先到先得 (Database Constraint)", "B. 候補機制", "C. 人工協調"],
            "risk_analysis": {"0": "✅ 強一致性", "1": "⚠️ 用戶體驗", "2": "⚠️ 運營成本"},
            "trap": "測試資源爭用處理"
        }
    ],

    # 待辦/任務場景 (Todo)
    "todo": [
        {
            "text": "刪除父任務時，子任務應該如何處理？",
            "category": "data_integrity",
            "options": ["A. 級聯刪除 (Cascade Delete)", "B. 子任務變為獨立任務 (Orphan)", "C. 禁止刪除"],
            "risk_analysis": {"0": "✅ 數據清潔", "1": "⚠️ 數據碎片", "2": "⚠️ 僵化"},
            "trap": "測試數據關聯完整性"
        }
    ],

    # 前端安全 (Frontend Security)
    "frontend": [
        {
            "text": "用戶在評論區輸入了 `<script>alert(1)</script>`，會發生什麼？",
            "category": "security",
            "options": ["A. 彈出視窗 (XSS 攻擊成功)", "B. 被轉義顯示為純文本", "C.瀏覽器崩潰"],
            "risk_analysis": {"0": "💀 嚴重漏洞 (XSS)", "1": "✅ 安全編碼", "2": "⚠️ 錯誤認知"},
            "trap": "測試 XSS 防禦意識"
        },
        {
            "text": "API Token 應該存在哪裡最安全？",
            "category": "security",
            "options": ["A. LocalStorage", "B. HttpOnly Cookie", "C. JS 變量"],
            "risk_analysis": {"0": "⚠️ 易受 XSS 攻擊", "1": "✅ 防止 XSS 竊取", "2": "⚠️ page refresh 後丟失"},
            "trap": "測試前端存儲安全"
        }
    ]
}


# ========================================
# 問題生成輔助函數
# ========================================

def get_questions_by_category(category: str) -> List[Dict[str, Any]]:
    """
    根據類別獲取問題
    
    Args:
        category: 問題類別 (payment, inventory, authentication, etc.)
        
    Returns:
        問題列表
    """
    return QUESTION_LIBRARY.get(category, [])


def get_random_questions(count: int = 5) -> List[Dict[str, Any]]:
    """
    隨機獲取指定數量的問題
    
    Args:
        count: 問題數量
        
    Returns:
        問題列表
    """
    import random
    
    all_questions = []
    for questions in QUESTION_LIBRARY.values():
        all_questions.extend(questions)
    
    return random.sample(all_questions, min(count, len(all_questions)))


def get_questions_for_module(module_name: str, module_description: str) -> List[Dict[str, Any]]:
    """
    根據模組名稱和描述智能選擇問題
    
    Args:
        module_name: 模組名稱
        module_description: 模組描述
        
    Returns:
        相關問題列表
    """
    text = (module_name + " " + module_description).lower()
    
    selected_questions = []
    
    # 根據關鍵詞匹配問題類別
    if any(kw in text for kw in ['付款', '支付', 'payment', '交易']):
        selected_questions.extend(get_questions_by_category('payment'))
    
    if any(kw in text for kw in ['庫存', 'inventory', '商品', '購物']):
        selected_questions.extend(get_questions_by_category('inventory'))
    
    if any(kw in text for kw in ['登入', '認證', 'auth', '用戶', 'user']):
        selected_questions.extend(get_questions_by_category('authentication'))
    
    if any(kw in text for kw in ['數據', 'data', '快取', 'cache']):
        selected_questions.extend(get_questions_by_category('data_consistency'))
    
    if any(kw in text for kw in ['api', '接口', '第三方', 'integration']):
        selected_questions.extend(get_questions_by_category('api_integration'))
    
    # 如果沒有匹配,返回隨機問題
    if not selected_questions:
        selected_questions = get_random_questions(5)
    
    return selected_questions[:5]  # 最多返回 5 個問題


# ========================================
# 問題質量評估
# ========================================

def evaluate_question_quality(question: Dict[str, Any]) -> Dict[str, Any]:
    """
    評估問題質量
    
    Args:
        question: 問題字典
        
    Returns:
        評估結果
    """
    score = 0
    feedback = []
    
    # 檢查必要字段
    required_fields = ['text', 'category', 'options', 'risk_analysis']
    for field in required_fields:
        if field in question:
            score += 25
        else:
            feedback.append(f"缺少必要字段: {field}")
    
    # 檢查選項數量
    if 'options' in question and len(question['options']) >= 3:
        feedback.append("✅ 選項數量充足")
    else:
        feedback.append("⚠️ 選項數量不足 (建議 3-4 個)")
        score -= 10
    
    # 檢查風險分析
    if 'risk_analysis' in question:
        if all(key in question['risk_analysis'] for key in ['0', '1', '2']):
            feedback.append("✅ 風險分析完整")
        else:
            feedback.append("⚠️ 風險分析不完整")
            score -= 10
    
    return {
        "score": max(0, score),
        "feedback": feedback,
        "quality": "優秀" if score >= 90 else "良好" if score >= 70 else "需改進"
    }


if __name__ == "__main__":
    # 測試問題庫
    print("=" * 70)
    print("🧪 蘇格拉底式問題庫測試")
    print("=" * 70)
    print()
    
    # 測試各類別問題數量
    print("📊 問題庫統計:")
    total = 0
    for category, questions in QUESTION_LIBRARY.items():
        count = len(questions)
        total += count
        print(f"  - {category:20s}: {count} 個問題")
    print(f"\n  總計: {total} 個問題")
    print()
    
    # 測試智能選擇
    print("🎯 智能問題選擇測試:")
    test_modules = [
        ("付款系統", "處理用戶付款和訂單"),
        ("庫存管理", "管理商品庫存"),
        ("用戶認證", "處理用戶登入和權限")
    ]
    
    for name, desc in test_modules:
        questions = get_questions_for_module(name, desc)
        print(f"\n  模組: {name}")
        print(f"  匹配到 {len(questions)} 個問題:")
        for q in questions[:2]:  # 只顯示前2個
            print(f"    - {q['text'][:50]}...")
    
    print()
    print("✅ 問題庫測試完成!")
