import sys
from server import mcp

if __name__ == "__main__":
    print("🚀 Starting BlueMouse Brain in Standalone Mode (SSE/HTTP over Port 8001)...")
    print("👉 Connect your browser to: http://localhost:8001/sse")
    try:
        # Force SSE transport for Web UI
        # Note: We use 'sse' transport which uses FastAPI/Uvicorn under the hood
        mcp.run(transport="sse", port=8001)
    except Exception as e:
        print(f"❌ Server Error: {e}")
        input("Press Enter to exit...")
