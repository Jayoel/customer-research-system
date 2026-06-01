import os
import requests
from typing import Dict, Optional

class DeepSeekService:
    """
    DeepSeek API服务 - 使用DeepSeek深度推理模型
    """
    
    def __init__(self):
        api_key = os.getenv('DEEPSEEK_API_KEY')
        if api_key and api_key != 'sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx':
            self.api_key = api_key
            self.use_api = True
        else:
            self.use_api = False
        
        self.base_url = os.getenv('DEEPSEEK_API_URL', 'https://api.deepseek.com/v1')
        self.model = os.getenv('DEEPSEEK_MODEL', 'deepseek-chat')
    
    def generate_visit_plan(self, customer_profile: Dict) -> Dict:
        """
        使用DeepSeek生成拜访方案
        """
        
        prompt = f"""
你是一位资深的B2B销售顾问和医疗行业专家。基于以下客户信息，
生成一份专业的拜访方案和讨论话题。

=== 客户信息 ===
客户姓名: {customer_profile.get('name', 'N/A')}
客户单位: {customer_profile.get('company', 'N/A')}
职位/角色: {customer_profile.get('position', '管理者')}
公司行业: {customer_profile.get('industry', '医疗健康')}
公司规模: {customer_profile.get('company_size', '1000-2000人')}
最近动态: {customer_profile.get('recent_news', '暂旦')}
专长领域: {', '.join(customer_profile.get('specialization', []))}
研究项目: {', '.join(customer_profile.get('research_areas', []))}

=== 请生成以下内容 ===

1. 【客户现状分析】(3-5点核心发现)
   分析客户企业的战略方向、业务痛点、发展机会

2. 【拜访目标】(2-3个具体、可衡量的目标)
   例如：了解医院在某领域的需求、建立关键决策人关系等

3. 【核心讨论话题】(5个具体话题)
   基于行业趋势和企业现状的话题，能引发共鸣

4. 【提问框架】(使用MEDDIC销售方法论)
   - 指标 (Metrics): 
   - 经济影响 (Economic Impact):
   - 决策流程 (Decision Process):
   - 决策标准 (Decision Criteria):
   - 确定人选 (Identify the Individual):
   - 竞争态势 (Competition):

5. 【拜访步骤】(从开场到收尾)
   Step 1: 开场破冰 (1分钟)
   Step 2: 建立信任 (5分钟)
   Step 3: 需求探查 (15分钟)
   Step 4: 价值呈现 (10分钟)
   Step 5: 行动计划 (5分钟)

6. 【风险识别与应对】
   可能的异议和应对话术

7. 【后续跟进计划】
   会后24小时、1周、1个月的跟进建议

请以专业、具体、可直接使用的方式回答，避免空泛的建议。
"""
        
        if self.use_api:
            try:
                return self._call_deepseek_api(prompt)
            except Exception as e:
                print(f"DeepSeek API 错误: {e}")
                return self._generate_demo_plan(customer_profile)
        else:
            return self._generate_demo_plan(customer_profile)
    
    def _call_deepseek_api(self, prompt: str) -> Dict:
        """
        调用DeepSeek API
        """
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        
        payload = {
            'model': self.model,
            'messages': [
                {
                    'role': 'system',
                    'content': '你是一位资深的B2B销售顾问和医疗行业专家'
                },
                {
                    'role': 'user',
                    'content': prompt
                }
            ],
            'temperature': 0.7,
            'max_tokens': 2000,
            'top_p': 0.95
        }
        
        response = requests.post(
            f'{self.base_url}/chat/completions',
            headers=headers,
            json=payload,
            timeout=60
        )
        
        if response.status_code == 200:
            data = response.json()
            return {
                'status': 'success',
                'plan': data['choices'][0]['message']['content']
            }
        else:
            raise Exception(f'DeepSeek API error: {response.status_code} - {response.text}')
    
    def _generate_demo_plan(self, customer_profile: Dict) -> Dict:
        """
        生成演示版披訪方案（当API不可用时）
        """
        name = customer_profile.get('name', '客户')
        company = customer_profile.get('company', '企业')
        
        demo_plan = f"""
## 【客户现状分析】

1. **战略升级阶段**
   {company}正处于医疗技术数字化转型的关键期，致力于提升论断能力和患者体验

2. **业务痛点**
   - 传统论断流程效率有待提高
   - 数据管理和分析能力不足
   - 医疗资源配置和协调需要优化

3. **市场机遇**
   - 儿童医疗领域政策支持力度大
   - 社会对高质量医疗服务需求增长
   - 医疗AI和信息化解决方案市场前景广阔

4. **竞争态势**
   与国内其他一流儿童医院相比，需要在技术创新和患者体验上继续领先

5. **关键需求**
   寻求能够帮助提升医疗服务质量、降低成本、改善患者满意度的解决方案

---

## 【拜访目标】

✓ **主目标**：了解{company}在医疗数字化和效率提升方面的具体需求

✓ **副目标1**：与{name}建立信任关系，了解其职能范围和决策权

✓ **副目标2**：获得与其他关键决策人接触的机会

---

## 【核心讨论话题】

**话题1：儿童医疗领域的数字化趋势**
- 分享行业内数字化转型成功案例
- 讨论如何通过技术提升论断效率

**话题2：医疗资源优化配置**
- 医院科室间的协调与资源共享
- 患者分流和合理配置的创新方案

**话题3：患者体验提升**
- 挂号、就诊、结算全流程体验优化
- 患者满意度提升的关键指标

**话题4：医疗数据安全与合规**
- 敏感数据的保护要求
- 满足医疗行业监管的解决方案

**话题5：投资回报率（ROI）**
- 医疗信息化项目的成本预算
- 预期的效益和效率提升

---

## 【MEDDIC提问框架】

**M - 指标 (Metrics)**
"请问贵院目前如何衡量医疗服务质量？关键KPI有哪些？"

**E - 经济影响 (Economic Impact)**
"您觉得通过流程优化，每年能节省多少成本或增加多少收益？"

**D - 决策流程 (Decision Process)**
"贵院在采购新系统或服务时，通常需要多长时间完成决策？哪些部门参与？"

**D - 决策标准 (Decision Criteria)**
"在选择合作伙伴时，贵院最看重哪些因素？"

**I - 确定人选 (Identify the Individual)**
"除了您，还有其他哪些关键人员参与此类决策？"

**C - 竞争态势 (Competition)**
"目前贵院是否已与其他厂商接触过类似方案？"

---

## 【拜访步骤】

### Step 1: 开场破冰 (1分钟)
"您好{name}，非常感谢您百忙之中抽出时间。我一直很关注{company}在儿童医疗领域的创新工作，贵院最近的X项目给我留下了深刻印象。"

### Step 2: 建立信任与背景介绍 (5分钟)
- 简要介绍自己和公司
- 分享行业内的一个成功案例
- 获得对方的反馈和共鸣点

### Step 3: 需求探查 (15分钟)
- 用MEDDIC框架提出5-6个关键问题
- 认真倾听，记录关键信息
- 追问和深化，找到真正的痛点

### Step 4: 价值呈现 (10分钟)
- 针对对方提到的痛点，介绍我们的解决方案
- 分享客户案例，展示具体效果
- 阐述合作的潜在收益

### Step 5: 行动计划与约下一步 (5分钟)
- 总结讨论内容和达成共识
- 明确下一步行动（如安排演示、拜访相关部门等）
- 确认后续跟进时间

---

## 【风险识别与应对】

**可能的异议1：「我们已经有供应商了」**
→ 应对：「我理解。不过我想分享一个案例，另一家医院通过与我们合作，在原有基础上又提升了30%的效率...")

**可能的异议2：「成本太高」**
→ 应对：「我完全理解成本考量。让我们先进行ROI分析，看看在多久能收回成本...")

**可能的异议3：「需要向领导汇报」**
→ 应对：「完全同意。我建议我们一起准备一份详细的提案，这样您汇报时更有说服力...")

---

## 【后续跟进计划】

**会后24小时**
- 发送感谢邮件 + 会议要点总结
- 针对对方提出的问题提供详细回答

**会后1周**
- 分享相关行业报告和成功案例
- 邀请参加产品演示或行业峰会

**会后1个月**
- 确认下一步合作意向
- 如无进展，询问决策时间表
"""
        
        return {
            "status": "success",
            "plan": demo_plan
        }
