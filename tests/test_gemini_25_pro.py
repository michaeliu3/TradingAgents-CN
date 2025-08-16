#!/usr/bin/env python3
"""
测试指定的Gemini模型
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# --- FIX 1: Correctly define the project root directory ---
# This now points to the main 'TradingAgents-CN' folder, not the 'tests' sub-folder.
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# 加载环境变量
load_dotenv()

# --- FIX 2: Make the model name a variable for easy testing ---
MODEL_TO_TEST = "gemini-2.5-flash"  # Start with a known stable model to verify your setup

def test_gemini_basic(model_name):
    """测试Gemini基础功能"""
    try:
        print(f"🧪 测试 {model_name} 基础功能")
        print("=" * 60)
        
        from langchain_google_genai import ChatGoogleGenerativeAI
        
        google_api_key = os.getenv('GOOGLE_API_KEY')
        if not google_api_key:
            print("❌ Google API密钥未配置")
            return False
        
        print(f"✅ Google API密钥已配置: {google_api_key[:20]}...")
        
        print(f"🚀 创建 {model_name} 实例...")
        llm = ChatGoogleGenerativeAI(
            model=model_name,
            temperature=0.1,
            max_tokens=1500,
            google_api_key=google_api_key
        )
        print(f"✅ {model_name} 实例创建成功")
        
        print("📊 测试中文股票分析...")
        response = llm.invoke("请用中文分析苹果公司(AAPL)的投资价值。")
        
        if response and response.content and len(response.content) > 100:
            print("✅ 中文股票分析成功")
            print(f"   响应预览: {response.content[:150]}...")
            return True
        else:
            print("❌ 中文股票分析失败: 响应过短或无内容")
            return False
            
    except Exception as e:
        print(f"❌ {model_name} 基础测试失败: {e}")
        return False

def test_gemini_tradingagents(model_name):
    """测试Gemini在TradingAgents中的使用"""
    try:
        print(f"\n🧪 测试 {model_name} 在TradingAgents中的使用")
        print("=" * 60)
        
        from tradingagents.graph.trading_graph import TradingAgentsGraph
        from tradingagents.default_config import DEFAULT_CONFIG
        
        config = DEFAULT_CONFIG.copy()
        config["llm_provider"] = "google"
        config["deep_think_llm"] = model_name
        config["quick_think_llm"] = model_name
        config["online_tools"] = True
        
        print("✅ 配置创建成功")
        print(f"   模型: {model_name}")
        
        print("🚀 初始化TradingAgents图...")
        graph = TradingAgentsGraph(["market"], config=config, debug=False)
        print("✅ TradingAgents图初始化成功")
        
        print("📊 开始股票分析...")
        state, decision = graph.propagate("AAPL", "2025-08-06")
        
        if state and decision and decision.get("action"):
            print("✅ Gemini驱动的股票分析成功！")
            print(f"   最终决策: {decision.get('action')}, 置信度: {decision.get('confidence')}")
            return True
        else:
            print("❌ 分析完成但结果无效或为空")
            return False
            
    except Exception as e:
        print(f"❌ TradingAgents测试失败: {e}")
        import traceback
        print(traceback.format_exc())
        return False

def main():
    """主测试函数"""
    print(f"🧪 {MODEL_TO_TEST} 完整测试")
    print("=" * 70)
    
    google_api_key = os.getenv('GOOGLE_API_KEY')
    if not google_api_key:
        print("❌ Google API密钥未配置. 请检查.env文件.")
        return
    
    results = {}
    
    print("第1步: 基础功能测试")
    print("-" * 30)
    results['基础功能'] = test_gemini_basic(MODEL_TO_TEST)
    
    print("\n第2步: TradingAgents集成测试")
    print("-" * 30)
    # Only run integration test if basic test passed
    if results['基础功能']:
        results['TradingAgents集成'] = test_gemini_tradingagents(MODEL_TO_TEST)
    else:
        results['TradingAgents集成'] = False
        print("⏭️  跳过集成测试，因为基础功能测试失败。")

    print(f"\n📊 {MODEL_TO_TEST} 测试结果总结:")
    print("=" * 50)
    
    successful_tests = 0
    for test_name, success in results.items():
        status = "✅ 通过" if success else "❌ 失败"
        print(f"  {test_name}: {status}")
        if success:
            successful_tests += 1
    
    print(f"\n🎯 总体结果: {successful_tests}/{len(results)} 测试通过")
    
    if successful_tests == len(results):
        print(f"🎉 模型 {MODEL_TO_TEST} 完全可用！")
    else:
        print(f"❌ 模型 {MODEL_TO_TEST} 未通过所有测试。")
        print("💡 请检查错误日志。如果基础功能失败，很可能是模型名称无效或API密钥权限不足。")

if __name__ == "__main__":
    main()