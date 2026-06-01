from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from datetime import datetime
import os
from config import Config, DevelopmentConfig
from services.qichacha_service import QiChachaService
from services.news_service import NewsService
from services.ai_service import AIService
from services.web_scraper import WebScraper
from services.deep_analysis import DeepAnalysis

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
CORS(app)

# 初始化服务
qichacha_service = QiChachaService()
news_service = NewsService()
ai_service = AIService()
web_scraper = WebScraper()
deep_analysis = DeepAnalysis()

@app.route('/')
def index():
    """主页"""
    return render_template('index.html')

@app.route('/api/health')
def health():
    """健康检查"""
    return jsonify({"status": "ok", "message": "Service is running"})

@app.route('/api/generate-plan', methods=['POST'])
def generate_plan():
    """
    生成深度调研报告
    POST 数据:
    {
        "name": "王艺",
        "company": "上海儿童医院"
    }
    """
    try:
        data = request.get_json()
        name = data.get('name', '').strip()
        company = data.get('company', '').strip()
        
        if not name or not company:
            return jsonify({
                "status": "error",
                "message": "姓名和单位不能为空"
            }), 400
        
        print(f"\n[查询信息] 姓名: {name}, 单位: {company}")
        
        # 1. 收集企业信息
        print("[步骤1] 收集企业信息...")
        company_info = qichacha_service.search_company(company)
        
        # 2. 获取企业新闻
        print("[步骤2] 获取企业新闻...")
        company_news = news_service.search_news(company, limit=3)
        
        # 3. 获取个人相关新闻
        print("[步骤3] 获取个人相关新闻...")
        person_news = news_service.search_person_news(name, company)
        
        # 4. 爬取医院官网医生信息
        print("[步骤4] 爬取医院官网医生信息...")
        doctor_info = web_scraper.scrape_hospital_doctor_info(company, name)
        
        # 5. 爬取微信公众号文章
        print("[步骤5] 爬取微信公众号相关文章...")
        wechat_articles = web_scraper.scrape_wechat_official_account(company, name)
        
        # 6. 深度分析生成研究资料
        print("[步骤6] 生成深度研究资料...")
        research_profile = deep_analysis.generate_research_profile(doctor_info, wechat_articles)
        
        # 7. 提取研究关键词
        print("[步骤7] 提取研究关键词...")
        research_keywords = web_scraper.extract_research_keywords(wechat_articles)
        
        # 8. 提取研究方向
        print("[步骤8] 提取研究方向...")
        research_directions = web_scraper.extract_research_directions(doctor_info, wechat_articles)
        
        # 9. 生成对话开场
        print("[步骤9] 生成对话开场...")
        conversation_starters = deep_analysis.generate_conversation_starters(doctor_info)
        
        # 10. 生成智能推荐
        print("[步骤10] 生成智能推荐...")
        smart_recommendations = deep_analysis.generate_smart_recommendations(doctor_info)
        
        # 11. 生成AI拜访方案
        print("[步骤11] 生成AI拜访方案...")
        visit_plan = ai_service.generate_visit_plan({
            "name": name,
            "company": company,
            "position": doctor_info.get('position', ''),
            "industry": company_info.get('data', {}).get('industry', '医疗健康'),
            "company_size": company_info.get('data', {}).get('employee_count', ''),
            "recent_news": [item['title'] for item in company_news[:3]],
            "specialization": doctor_info.get('specialization', []),
            "research_areas": [r.get('title', '') for r in doctor_info.get('research_areas', [])],
        })
        
        print("[完成] 深度调研报告已生成")
        
        return jsonify({
            "status": "success",
            "data": {
                "customer_info": {
                    "name": name,
                    "company": company,
                    "position": doctor_info.get('position', ''),
                    "department": doctor_info.get('department', ''),
                    "company_info": {
                        "industry": company_info.get('data', {}).get('industry', 'N/A'),
                        "size": company_info.get('data', {}).get('employee_count', 'N/A'),
                        "registered_capital": company_info.get('data', {}).get('registered_capital', 'N/A'),
                        "established_at": company_info.get('data', {}).get('established_at', 'N/A'),
                        "address": company_info.get('data', {}).get('address', 'N/A'),
                        "business_scope": company_info.get('data', {}).get('business_scope', 'N/A')
                    }
                },
                "doctor_profile": doctor_info,
                "research_profile": research_profile,
                "company_news": company_news,
                "person_news": person_news,
                "wechat_articles": wechat_articles,
                "research_keywords": research_keywords,
                "research_directions": research_directions,
                "conversation_starters": conversation_starters,
                "smart_recommendations": smart_recommendations,
                "visit_plan": visit_plan['plan'],
                "generated_at": datetime.now().isoformat()
            }
        })
    
    except Exception as e:
        print(f"错误: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({
            "status": "error",
            "message": f"生成方案失败: {str(e)}"
        }), 500

@app.route('/api/export-report', methods=['POST'])
def export_report():
    """
    导出完整调研报告为Markdown
    """
    try:
        data = request.get_json()
        name = data.get('name', '')
        company = data.get('company', '')
        report_data = data.get('report', {})
        
        # 生成Markdown内容
        markdown_content = f"""# 客户深度调研报告

**客户姓名**: {name}  
**所属机构**: {company}  
**岗位**: {report_data.get('position', 'N/A')}  
**科室**: {report_data.get('department', 'N/A')}  
**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

## 📊 研究者学术档案

### 基本信息
- **姓名**: {name}
- **职位**: {report_data.get('position', 'N/A')}
- **科室**: {report_data.get('department', 'N/A')}
- **医院**: {company}

### 专长领域
{self._format_list(report_data.get('specialization', []))}

### 学术指标
- 发表论文数: {report_data.get('publications_count', 0)}
- 总引用数: {report_data.get('total_citations', 0)}
- H-指数: {report_data.get('h_index', 0)}
- 会议演讲: {report_data.get('conference_presentations', 0)}

---

## 🔬 研究方向

### 活跃研究项目
{self._format_research_areas(report_data.get('active_research', []))}

---

## 📰 研究洞察

### 微信公众号文章摘要
{self._format_articles(report_data.get('wechat_articles', []))}

---

## 🎯 拜访方案

{report_data.get('visit_plan', '')}

---

## 💡 智能推荐

{self._format_recommendations(report_data.get('smart_recommendations', []))}

---

*此报告由客户调研系统自动生成*
"""
        
        return jsonify({
            "status": "success",
            "content": markdown_content,
            "filename": f"调研报告_{name}_{company}_{datetime.now().strftime('%Y%m%d%H%M%S')}.md"
        })
    
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=app.config['DEBUG']
    )
