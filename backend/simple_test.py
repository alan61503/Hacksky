#!/usr/bin/env python3
"""
Simple test script that works when run from the backend directory.
"""

import asyncio
import sys
import os

def test_imports():
    """Test if all modules can be imported correctly."""
    print("🔍 Testing imports...")
    
    try:
        from config import settings, AGENT_INTERVAL, DEBUG, API_HOST, API_PORT
        print("✅ Config module imported successfully")
        print(f"   - AGENT_INTERVAL: {AGENT_INTERVAL}")
        print(f"   - DEBUG: {DEBUG}")
        print(f"   - API_HOST: {API_HOST}")
        print(f"   - API_PORT: {API_PORT}")
    except Exception as e:
        print(f"❌ Config import failed: {e}")
        return False
    
    try:
        from feed.fake_feed import generate_fake_post
        print("✅ Fake feed module imported successfully")
    except Exception as e:
        print(f"❌ Fake feed import failed: {e}")
        return False
    
    try:
        from detection.pipeline import analyze_post
        print("✅ Detection pipeline imported successfully")
    except Exception as e:
        print(f"❌ Detection pipeline import failed: {e}")
        return False
    
    try:
        from logs.logger import log_detection, log_system_event, get_logs
        print("✅ Logger module imported successfully")
    except Exception as e:
        print(f"❌ Logger import failed: {e}")
        return False
    
    try:
        from agent import AutonomousAgent
        print("✅ Agent module imported successfully")
    except Exception as e:
        print(f"❌ Agent import failed: {e}")
        return False
    
    return True

def test_fake_feed():
    """Test fake feed generation."""
    print("\n📝 Testing fake feed generation...")
    
    try:
        from feed.fake_feed import generate_fake_post
        
        # Generate a few test posts
        for i in range(3):
            post = generate_fake_post()
            print(f"   ✅ Generated post #{post['id']}: {post['content'][:60]}...")
        
        return True
    except Exception as e:
        print(f"   ❌ Fake feed test failed: {e}")
        return False

def test_detection_pipeline():
    """Test detection pipeline."""
    print("\n🔍 Testing detection pipeline...")
    
    try:
        from feed.fake_feed import generate_fake_post
        from detection.pipeline import analyze_post
        
        # Generate and analyze a post
        post = generate_fake_post()
        result = analyze_post(post)
        
        print(f"   ✅ Analyzed post #{result['post_id']}")
        print(f"   ✅ Trust score: {result['trust_score']}%")
        print(f"   ✅ Reason: {result['reason'][:80]}...")
        
        return True
    except Exception as e:
        print(f"   ❌ Detection pipeline test failed: {e}")
        return False

def test_logging():
    """Test logging system."""
    print("\n📋 Testing logging system...")
    
    try:
        from logs.logger import log_detection, log_system_event, get_logs
        from feed.fake_feed import generate_fake_post
        from detection.pipeline import analyze_post
        
        # Test system event logging
        log_system_event("TEST", "🧪 Testing logging system")
        print("   ✅ System event logged")
        
        # Test detection logging
        post = generate_fake_post()
        result = analyze_post(post)
        log_detection(result)
        print("   ✅ Detection result logged")
        
        # Test log retrieval
        logs = get_logs(limit=5)
        print(f"   ✅ Retrieved {len(logs)} recent logs")
        
        return True
    except Exception as e:
        print(f"   ❌ Logging test failed: {e}")
        return False

async def test_agent():
    """Test autonomous agent."""
    print("\n🤖 Testing autonomous agent...")
    
    try:
        from agent import AutonomousAgent
        
        # Create agent instance
        agent = AutonomousAgent()
        print("   ✅ Agent created successfully")
        
        # Test agent start (briefly)
        print("   🔄 Starting agent for 3 seconds...")
        agent_task = asyncio.create_task(agent.start())
        
        # Let it run for 3 seconds
        await asyncio.sleep(3)
        
        # Stop the agent
        await agent.stop()
        agent_task.cancel()
        
        try:
            await agent_task
        except asyncio.CancelledError:
            pass
        
        print(f"   ✅ Agent processed {agent.posts_processed} posts")
        print(f"   ✅ Agent uptime: {agent.get_uptime():.2f} seconds")
        
        return True
    except Exception as e:
        print(f"   ❌ Agent test failed: {e}")
        return False

def test_fastapi_import():
    """Test FastAPI import and basic setup."""
    print("\n🚀 Testing FastAPI setup...")
    
    try:
        from main import app
        print("   ✅ FastAPI app imported successfully")
        
        # Test basic app properties
        print(f"   ✅ App title: {app.title}")
        print(f"   ✅ App version: {app.version}")
        
        return True
    except Exception as e:
        print(f"   ❌ FastAPI test failed: {e}")
        return False

async def main():
    """Run all tests."""
    print("🧪 Starting Backend AI Engine Tests (Simple Version)")
    print("=" * 50)
    
    tests = [
        ("Import Test", test_imports),
        ("Fake Feed Test", test_fake_feed),
        ("Detection Pipeline Test", test_detection_pipeline),
        ("Logging Test", test_logging),
        ("FastAPI Test", test_fastapi_import),
        ("Agent Test", test_agent),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if asyncio.iscoroutinefunction(test_func):
                result = await test_func()
            else:
                result = test_func()
            
            if result:
                passed += 1
            else:
                print(f"   ❌ {test_name} failed")
                
        except Exception as e:
            print(f"   ❌ {test_name} crashed: {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Backend is ready to run.")
        print("\n🚀 To start the FastAPI server, run:")
        print("   python main.py")
        print("\n🌐 Then visit: http://localhost:8000")
        return True
    else:
        print("❌ Some tests failed. Please fix the issues above.")
        return False

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1) 