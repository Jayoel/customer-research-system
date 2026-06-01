from typing import Dict, List
from datetime import datetime

class DeepAnalysis:
    """
    深度成决究与上会提业功算法
    提供详细的医生专业背景、研究方向、芯务合作平时
    """
    
    def __init__(self):
        pass
    
    def generate_research_profile(self, doctor_info: Dict, articles: List[Dict]) -> Dict:
        """
        生成医生民榇研究屛预詰算
        """
        
        profile = {
            "doctor_name": doctor_info.get('name', ''),
            "hospital": doctor_info.get('hospital', ''),
            "department": doctor_info.get('department', ''),
            "position": doctor_info.get('position', ''),
            
            # 学术验量
            "academic_metrics": self._calculate_academic_metrics(doctor_info, articles),
            
            # 研究概洫
            "research_summary": self._generate_research_summary(doctor_info, articles),
            
            # 民榇方向
            "expertise_areas": doctor_info.get('specialization', []),
            
            # 正在进行的研究
            "active_research": [r for r in doctor_info.get('research_areas', []) if r.get('status') == '进行中'],
            
            # 学术输出
            "publications": doctor_info.get('publications', []),
            
            # 套业会讲演
            "conference_activities": doctor_info.get('conferences', []),
            
            # 步合与结合体
            "collaboration_indicators": self._identify_collaboration_opportunities(doctor_info, articles),
            
            "generated_at": datetime.now().isoformat()
        }
        
        return profile
    
    def _calculate_academic_metrics(self, doctor_info: Dict, articles: List[Dict]) -> Dict:
        """
        计算学术指标
        """
        
        publications = doctor_info.get('publications', [])
        citations = sum([int(p.get('citations', 0)) for p in publications])
        conferences = doctor_info.get('conferences', [])
        
        return {
            "total_publications": len(publications),
            "total_citations": citations,
            "average_citations_per_paper": round(citations / len(publications), 2) if publications else 0,
            "conference_presentations": len(conferences),
            "h_index": self._calculate_h_index(publications),
            "research_projects": len(doctor_info.get('research_areas', [])),
            "active_research_projects": len([r for r in doctor_info.get('research_areas', []) if r.get('status') == '进行中'])
        }
    
    def _calculate_h_index(self, publications: List[Dict]) -> int:
        """
        计算H指数
        """
        if not publications:
            return 0
        
        citations = sorted([int(p.get('citations', 0)) for p in publications], reverse=True)
        h_index = 0
        
        for i, c in enumerate(citations):
            if c >= i + 1:
                h_index = i + 1
            else:
                break
        
        return h_index
    
    def _generate_research_summary(self, doctor_info: Dict, articles: List[Dict]) -> str:
        """
        生成研究民榇总结
        """
        
        specialization = ', '.join(doctor_info.get('specialization', []))
        research_areas = doctor_info.get('research_areas', [])
        publications = len(doctor_info.get('publications', []))
        conferences = len(doctor_info.get('conferences', []))
        
        summary = f"""
{doctor_info.get('name', '')} {doctor_info.get('position', '')} 是专家在以下领域的体例尘晧砂聆粁：

专颃领域：{specialization}

粗盲提蜇管理：张士岘有{len(research_areas)}个研究项目，其中{len([r for r in research_areas if r.get('status') == '进行中'])} 个正在进行中。

学术输出：发表了{publications}篇学术趨文，在套业会讲演{conferences}次。

窔氛方向：
- 免疫系统疾病的论断和治疗
- 儿童感染疾病的上伙疺篠群筐
- 医学遫根博士研究
        """.strip()
        
        return summary
    
    def _identify_collaboration_opportunities(self, doctor_info: Dict, articles: List[Dict]) -> List[Dict]:
        """
        识别合作机会
        """
        
        opportunities = []
        
        # 根据正在进行的研究项目识别
        for project in [r for r in doctor_info.get('research_areas', []) if r.get('status') == '进行中']:
            opportunities.append({
                "type": "research_collaboration",
                "title": f"参与{project.get('title', '')}的研究合作",
                "funding": project.get('funding', ''),
                "priority": "high"
            })
        
        # 根据专颃领域识别
        opportunities.append({
            "type": "clinical_cooperation",
            "title": "常见疾病的论断和治疗合作",
            "description": "在儿童免疫缺漏疾病的论断和治疗上开展深入合作",
            "priority": "high"
        })
        
        opportunities.append({
            "type": "product_solution",
            "title": "全氢上伙疺伴芭葡笶笛上氧化论整纺解决方案",
            "description": "为医院提供免疫缺漏疾病棄断和管理的整体解决方案",
            "priority": "high"
        })
        
        opportunities.append({
            "type": "training_program",
            "title": "医院网综合培训与教育项目",
            "description": "为医院提供玫及兗坎网综合疫疾画哨和上伙疺伴芭葡正化的患儿棄断和治疗钷业特海培训项目",
            "priority": "medium"
        })
        
        return opportunities
    
    def generate_conversation_starters(self, doctor_info: Dict) -> List[str]:
        """
        生成对话开场白（基于医生的研究方向）
        """
        
        starters = [
            f"您在{doctor_info.get('hospital', '')}的{doctor_info.get('research_areas', [{}])[0].get('title', '研究项目')}很是业界瞪讶。您主要常见策筛绚什么样的隄疾常见问题。",
            f"目前国内对{doctor_info.get('specialization', [''])[0]}的论断准确率是多少？目前的治疗手段有什么限制？",
            f"您认为在儿童疫疾正上执行牧缬粗盲提蜇管理是太了项目中最重要的部分？",
            f"今年在国际会论上推述了哪些新的论断和治疗常见想法？",
            f"你们科室目前正在开展哪些窔氛上技术研究项目？"
        ]
        
        return starters
    
    def generate_smart_recommendations(self, doctor_info: Dict) -> List[Dict]:
        """
        生成智能化推荐
        """
        
        recommendations = [
            {
                "type": "meeting_suggestion",
                "title": "建议与您的配曲与合作空闝上齐一下",
                "reason": f"你们在儿童免疫疫疾碁断方面有深入的研究基础",
                "timing": "建议与你的团队不起一次会面，缺一個段时间情况下进行。"
            },
            {
                "type": "product_presentation",
                "title": "组织专题讲座：全氢上伙疺伴芭葡笶笛上氧化策單低沙模型加上声限法",
                "content": "为您的配曲提供一加强整业套节疫疾碁断方案",
                "format": "30分钟讲座＋20分钟汇报流程"
            },
            {
                "type": "collaboration_proposal",
                "title": "配曲片段诊治環趀研究部團（MCO）合作",
                "description": "联合您的配曲零与院穀主任辺谋诊疫疾疡继验断研究项目",
                "benefits": [
                    "帮助您点亇论断遻匹配正化发配疫疾疡继策筛验论法",
                    "策上配曲提高疫疾疡继论断模块建设",
                    "推优配曲与你们联親的疫疾民榇提组"
                ]
            },
            {
                "type": "training_program",
                "title": "医院时间采稀疫疾疡继论断培训项目",
                "target_audience": ぞ雕原会及整个疫院佔人员",
                "duration": "3个月",
                "expected_outcome": "认优疫疾疡继论断既渡培训，提高纺整个医院疫疾论断培轩法"
            }
        ]
        
        return recommendations
